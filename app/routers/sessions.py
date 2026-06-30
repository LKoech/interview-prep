from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_event_bus, get_jd_parser, get_session_repo
from app.events.bus import EventBus
from app.models.session import InterviewSession, SessionCreate
from app.repositories.session_repo import SessionRepository
from app.services.jd_parser import JDParser

router = APIRouter()


@router.post("/", response_model=InterviewSession)
async def create_session(
    body: SessionCreate,
    repo: SessionRepository = Depends(get_session_repo),
    parser: JDParser = Depends(get_jd_parser),
    event_bus: EventBus = Depends(get_event_bus),
) -> InterviewSession:
    skills = parser.extract_skills(body.jd_text)
    session = InterviewSession(
        company=body.company,
        role=body.role,
        jd_text=body.jd_text,
        stage=body.stage,
        skills_extracted=skills,
    )
    await repo.save_session(session)
    await event_bus.publish(
        "session_created",
        {"session_id": session.id, "company": session.company},
    )
    return session


@router.get("/", response_model=list[InterviewSession])
async def list_sessions(
    repo: SessionRepository = Depends(get_session_repo),
) -> list[InterviewSession]:
    return await repo.list_sessions()


@router.get("/{session_id}", response_model=InterviewSession)
async def get_session(
    session_id: str,
    repo: SessionRepository = Depends(get_session_repo),
) -> InterviewSession:
    session = await repo.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    repo: SessionRepository = Depends(get_session_repo),
) -> dict:
    deleted = await repo.delete(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"deleted": session_id}
