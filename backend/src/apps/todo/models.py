import uuid
from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class NewTaskModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    completed: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "",
                "name": "My Task",
                "completed": True
            }
        }


class UpdateTaskModel(BaseModel):
    name: Optional[str]
    completed: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "New Task Name",
                "completed": True
            }
        }


class ViewTaskModel(BaseModel):
    name: str
    completed: bool
