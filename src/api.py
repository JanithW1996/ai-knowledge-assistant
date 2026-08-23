"""HTTP API for the governed AI Knowledge Assistant."""

from pathlib import Path
from typing import Literal

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.answer_service import answer_question
from src.entra_identity import (
    IdentityError,
    VerifiedIdentity,
    parse_entra_identity,
)
from src.runtime_security import (
    get_identity_mode,
    validate_runtime_security,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIRECTORY = PROJECT_ROOT / "src" / "static"

UserRole = Literal[
    "employee",
    "manager",
    "senior_executive",
    "hr_adviser",
    "it_support_officer",
    "finance_officer",
]


class AnswerRequest(BaseModel):
    """Validated answer request."""

    question: str = Field(
        min_length=3,
        max_length=500,
    )
    role: UserRole = "employee"


class AnswerResponse(BaseModel):
    """Stable response contract for approved clients."""

    answer: str
    citations: list[str]
    grounded: bool
    mode: str


class SessionResponse(BaseModel):
    """Identity information required by the interface."""

    identity_mode: str
    role: str | None
    display_name: str
    allow_demo_role_selection: bool


def require_entra_identity(
    encoded_principal: str | None,
) -> VerifiedIdentity:
    """Return a trusted identity or reject the request."""
    try:
        return parse_entra_identity(
            encoded_principal
        )
    except IdentityError as error:
        raise HTTPException(
            status_code=401,
            detail=(
                "Verified Microsoft Entra identity "
                "with one assigned application role "
                "is required."
            ),
        ) from error


def resolve_request_role(
    requested_role: str,
    encoded_principal: str | None,
) -> str:
    """Use demo roles locally and trusted roles in Entra mode."""
    if get_identity_mode() == "demo":
        return requested_role

    identity = require_entra_identity(
        encoded_principal
    )

    return identity.role


validate_runtime_security()

app = FastAPI(
    title="AI Knowledge Assistant API",
    version="1.2.0",
    description=(
        "Governed question answering over synthetic, "
        "fictional data."
    ),
)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIRECTORY),
    name="static",
)


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    """Serve the non-technical presentation interface."""
    return FileResponse(
        STATIC_DIRECTORY / "index.html"
    )


@app.get("/health")
def health() -> dict[str, str]:
    """Confirm that the API process is running."""
    return {
        "status": "healthy",
        "data_policy": "synthetic-fictional-only",
    }


@app.get(
    "/v1/session",
    response_model=SessionResponse,
)
def get_session(
    client_principal: str | None = Header(
        default=None,
        alias="X-MS-CLIENT-PRINCIPAL",
    ),
) -> SessionResponse:
    """Return the trusted session used by the interface."""
    identity_mode = get_identity_mode()

    if identity_mode == "demo":
        return SessionResponse(
            identity_mode="demo",
            role=None,
            display_name="Demo user",
            allow_demo_role_selection=True,
        )

    identity = require_entra_identity(
        client_principal
    )

    return SessionResponse(
        identity_mode="entra",
        role=identity.role,
        display_name=identity.display_name,
        allow_demo_role_selection=False,
    )


@app.post(
    "/v1/answers",
    response_model=AnswerResponse,
)
def create_answer(
    request: AnswerRequest,
    client_principal: str | None = Header(
        default=None,
        alias="X-MS-CLIENT-PRINCIPAL",
    ),
) -> AnswerResponse:
    """Return an authorized and grounded answer."""
    trusted_role = resolve_request_role(
        request.role,
        client_principal,
    )

    result = answer_question(
        request.question,
        trusted_role,
    )

    return AnswerResponse(**result)