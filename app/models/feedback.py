from pydantic import BaseModel, Field


class AnswerSubmission(BaseModel):
    question_id: str
    session_id: str
    answer_text: str


class FeedbackCriteria(BaseModel):
    score: int = Field(ge=1, le=5)
    comment: str


class AnswerFeedback(BaseModel):
    question_id: str
    has_concrete_example: FeedbackCriteria
    has_metric: FeedbackCriteria
    is_concise: FeedbackCriteria
    answers_the_question: FeedbackCriteria
    uses_star_format: FeedbackCriteria
    overall_score: float
    suggestion: str
