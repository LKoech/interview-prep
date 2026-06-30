"""WebSocket endpoint for real-time mock interview sessions.

The client connects, receives questions one at a time,
sends answers back, and gets instant feedback.
"""

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.repositories.question_repo import QuestionRepository
from app.repositories.session_repo import SessionRepository
from app.services.feedback_service import FeedbackService

router = APIRouter()


@router.websocket("/ws/interview/{session_id}")
async def interview_websocket(websocket: WebSocket, session_id: str):
    await websocket.accept()
    redis = websocket.app.state.redis

    session_repo = SessionRepository(redis)
    question_repo = QuestionRepository(redis)
    feedback_service = FeedbackService()

    session = await session_repo.get_session(session_id)
    if session is None:
        await websocket.send_json({"error": "Session not found"})
        await websocket.close()
        return

    questions = await question_repo.get_by_session(session_id)
    if not questions:
        await websocket.send_json({"error": "No questions generated. Generate questions first."})
        await websocket.close()
        return

    await websocket.send_json({
        "type": "interview_start",
        "company": session.company,
        "role": session.role,
        "total_questions": len(questions),
    })

    try:
        for i, question in enumerate(questions):
            await websocket.send_json({
                "type": "question",
                "number": i + 1,
                "total": len(questions),
                "question_id": question.id,
                "question_type": question.type,
                "text": question.text,
            })

            # Wait for answer
            raw = await websocket.receive_text()
            data = json.loads(raw)
            answer_text = data.get("answer", "")

            feedback = feedback_service.evaluate(question.text, answer_text)
            feedback.question_id = question.id

            await websocket.send_json({
                "type": "feedback",
                "question_number": i + 1,
                **feedback.model_dump(),
            })

        await websocket.send_json({
            "type": "interview_complete",
            "message": "Mock interview complete. Review your feedback above.",
        })

    except WebSocketDisconnect:
        pass
