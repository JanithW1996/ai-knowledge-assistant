"""HTTP API for the governed AI Knowledge Assistant."""

from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.answer_service import answer_question
from src.runtime_security import validate_runtime_security


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
    """Validated demonstration request."""

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


validate_runtime_security()

app = FastAPI(
    title="AI Knowledge Assistant API",
    version="1.1.0",
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


@app.post(
    "/v1/answers",
    response_model=AnswerResponse,
)
def create_answer(
    request: AnswerRequest,
) -> AnswerResponse:
    """Return an authorised and grounded answer."""
    result = answer_question(
        request.question,
        request.role,
    )

    return AnswerResponse(**result)