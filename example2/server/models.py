from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4

def generate_uuid():
    return str(uuid4())

class CommandEnum(str, Enum):
    execute = "execute"
    config = "config"

class StatusEnum(str, Enum):
    done = "done"
    pending = "pending"

class RATModel(BaseModel):
    id: str = Field(default_factory=generate_uuid, alias='_id')
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True

class Command(RATModel):   
    command_type: CommandEnum
    argument: str = ""
    status: StatusEnum = "pending"

class Result(RATModel):
    command_id: Optional[str]
    command_type: CommandEnum
    argument: str = ""
    result: str = ""