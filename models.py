import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Integer, Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Form(Base):
    __tablename__ = "forms"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship(
        "Question", back_populates="form",
        cascade="all, delete-orphan", order_by="Question.position"
    )
    responses = relationship(
        "Response", back_populates="form", cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    form_id = Column(UUID(as_uuid=False), ForeignKey("forms.id"), nullable=False)
    label = Column(String, nullable=False)
    # "text" | "textarea" | "radio" | "checkbox"
    field_type = Column(String, default="text")
    options = Column(Text, default="")  # comma-separated, used for radio/checkbox
    required = Column(Boolean, default=False)
    position = Column(Integer, default=0)

    form = relationship("Form", back_populates="questions")


class Response(Base):
    __tablename__ = "responses"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    form_id = Column(UUID(as_uuid=False), ForeignKey("forms.id"), nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    form = relationship("Form", back_populates="responses")
    answers = relationship(
        "Answer", back_populates="response", cascade="all, delete-orphan"
    )


class Answer(Base):
    __tablename__ = "answers"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    response_id = Column(UUID(as_uuid=False), ForeignKey("responses.id"), nullable=False)
    question_id = Column(UUID(as_uuid=False), ForeignKey("questions.id"), nullable=False)
    value = Column(Text, default="")

    response = relationship("Response", back_populates="answers")
