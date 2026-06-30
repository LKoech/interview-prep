from fastapi import APIRouter, Depends

from app.dependencies import get_feedback_service, get_question_repo
from app.models.feedback import AnswerFeedback, AnswerSubmission
from app.repositories.question_repo import QuestionRepository
from app.services.feedback_service import FeedbackService

router = APIRouter()


@router.post("/evaluate", response_model=AnswerFeedback)
async def evaluate_answer(
    body: AnswerSubmission,
    feedback_service: FeedbackService = Depends(get_feedback_service),
    question_repo: QuestionRepository = Depends(get_question_repo),
) -> AnswerFeedback:
    question = await question_repo.get_question(body.question_id)
    question_text = question.text if question else "General interview question"

    feedback = feedback_service.evaluate(question_text, body.answer_text)
    feedback.question_id = body.question_id
    return feedback
