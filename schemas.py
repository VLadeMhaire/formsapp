from typing import List, Optional
from pydantic import BaseModel


class QuestionIn(BaseModel):
    label: str
    field_type: str = "text"  # text | textarea | radio | checkbox
    options: Optional[str] = ""  # "Red,Green,Blue"
    required: bool = False


class FormCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    questions: List[QuestionIn]
