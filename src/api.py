"""HTTP API for the governed AI Knowledge Assistant."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.answer_service import answer_question


UserRole = Literal[
    "employee",
    "manager",
    "hr_adviser",
    "it_support_officer",
]


class AnswerRequest(BaseModel):
    """Validated demonstration request."""

    question: str = Field(min_length=3, max_length=500)
    role: UserRole = "employee"


class AnswerResponse(BaseModel):
    """Stable response contract for approved clients."""

    answer: str
    citations: list[str]
    grounded: bool
    mode: str


app = FastAPI(
    title="AI Knowledge Assistant API",
    version="1.0.0",
    description=(
        "Governed question answering over synthetic, fictional data."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    """Confirm that the API process is running."""
    return {
        "status": "healthy",
        "data_policy": "synthetic-fictional-only",
    }


@app.post("/v1/answers", response_model=AnswerResponse)
def create_answer(request: AnswerRequest) -> AnswerResponse:
    """Return an authorised and grounded demonstration answer."""
    result = answer_question(request.question, request.role)
    return AnswerResponse(**result)