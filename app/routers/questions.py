from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_question_service, get_session_repo
from app.models.question import Question, QuestionGenerateRequest
from app.repositories.session_repo import SessionRepository
from app.services.question_service import QuestionService

router = APIRouter()


@router.post("/generate", response_model=list[Question])
async def generate_questions(
    body: QuestionGenerateRequest,
    question_service: QuestionService = Depends(get_question_service),
    session_repo: SessionRepository = Depends(get_session_repo),
) -> list[Question]:
    session = await session_repo.get_session(body.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    questions = await question_service.generate_for_session(
        session_id=body.session_id,
        jd_text=session.jd_text,
        types=body.types,
        count_per_type=body.count_per_type,
    )
    return questions


@router.get("/{session_id}", response_model=list[Question])
async def get_session_questions(
    session_id: str,
    question_service: QuestionService = Depends(get_question_service),
) -> list[Question]:
    return await question_service.get_session_questions(session_id)
