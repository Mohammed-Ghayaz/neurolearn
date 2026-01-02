from datetime import timezone, datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from ..models.mistake_event_model import MistakeEvent
from ..dependencies.auth_dependency import require_student
from ..models.user_model import User
from ..models.course_model import Course
from ..models.topic_model import Topic
from ..models.subtopic_model import Subtopic
from ..models.lesson_model import Lesson
from ..models.lesson_session_model import LessonSession
from ..db.database import get_db
from ..schema.mistake_schema import MistakeEventRequest
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

router = APIRouter(dependencies=[Depends(require_student)])

@router.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).filter_by(is_active=True).order_by(Course.order_index).all()

    return {
        "courses": [{
            "course_id": str(course.course_id),
            "title": course.title,
            "description": course.description
        } for course in courses]
    }

@router.get("/courses/{course_id}/topics")
def get_course_topics(course_id: UUID, db: Session = Depends(get_db)):
    course = db.query(Course).filter_by(course_id=course_id, is_active=True).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    topics = db.query(Topic).filter_by(course_id=course_id, is_active=True).order_by(Topic.order_index).all()

    return {
        "topics": [{
            "topic_id": str(topic.topic_id),
            "title": topic.title
        } for topic in topics]
    }

@router.get("/topics/{topic_id}/subtopics")
def get_topic_subtopics(topic_id: UUID, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter_by(topic_id=topic_id, is_active=True).first()
    
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    subtopics = db.query(Subtopic).filter_by(topic_id=topic_id, is_active=True).order_by(Subtopic.order_index).all()

    return {
        "subtopics": [{
            "subtopic_id": str(subtopic.subtopic_id),
            "title": subtopic.title
        } for subtopic in subtopics]
    }

@router.get("/subtopics/{subtopic_id}/lessons")
def get_subtopic_lessons(subtopic_id: UUID, db: Session = Depends(get_db)):
    subtopic = db.query(Subtopic).filter_by(subtopic_id=subtopic_id, is_active=True).first()
    
    if not subtopic:
        raise HTTPException(status_code=404, detail="Subtopic not found")

    lessons = db.query(Lesson).filter_by(subtopic_id=subtopic_id, is_active=True).order_by(Lesson.order_index).all()

    return {
        "lessons": [{
            "lesson_id": str(lesson.lesson_id),
            "title": lesson.title,
            "content": lesson.content,
            "difficulty": lesson.difficulty,
            "estimated_time": lesson.estimated_time_minutes
        } for lesson in lessons]
    }

@router.get("/lessons/{lesson_id}")
def get_lesson_content(lesson_id: UUID, db: Session = Depends(get_db), dyslexic_mode: Optional[bool] = False):
    lesson = db.query(Lesson).filter_by(lesson_id=lesson_id, is_active=True).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    return {
        "content": lesson.content
    }

@router.post("/lessons/{lesson_id}/start")
def create_lesson_session(lesson_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(require_student)):
    lesson = db.query(Lesson).filter_by(lesson_id=lesson_id, is_active=True).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    existing_lesson_session = db.query(LessonSession).filter_by(
        lesson_id=lesson_id, 
        user_id=current_user.user_id,
        ended_at=None
        ).first()

    if existing_lesson_session:
        return JSONResponse(status_code=200, content={"session_id": existing_lesson_session.session_id})

    new_session = LessonSession(lesson_id=lesson_id, user_id=current_user.user_id, completed=False, progress_percent=0)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return JSONResponse(status_code=201, content={
        "session_id": new_session.session_id
    })

@router.post("/mistakes")
def record_mistake(mistake_event: MistakeEventRequest, db: Session = Depends(get_db), current_user: User = Depends(require_student)):
    session = db.query(LessonSession).filter_by(session_id = mistake_event.session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")


    if session.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if session.ended_at is not None:
        raise HTTPException(status_code=400, detail="Session already ended")

    lesson = db.query(Lesson).filter_by(lesson_id = session.lesson_id, is_active=True).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Associated lesson not found")

    existing_mistake_event = db.query(MistakeEvent).filter_by(session_id=mistake_event.session_id, mistake_type=mistake_event.mistake_type, context=mistake_event.context, user_id=current_user.user_id).order_by(MistakeEvent.created_at.desc()).first()

    if existing_mistake_event:
        time_difference = datetime.now(timezone.utc) - existing_mistake_event.created_at
        time_diff_in_sec = time_difference.total_seconds()

        if time_diff_in_sec < 2:
            raise HTTPException(status_code=409, detail="Conflicting resource")

    new_mistake_event = MistakeEvent(
        session_id=mistake_event.session_id, 
        lesson_id=session.lesson_id,
        subtopic_id=lesson.subtopic_id,
        user_id=current_user.user_id,
        mistake_type=mistake_event.mistake_type,
        context=mistake_event.context
        )

    db.add(new_mistake_event)
    db.commit()
    db.refresh(new_mistake_event)

    return JSONResponse(status_code=201, content={"status": "mistake recorded"})

