# Help me create the schema for a todo which contains
# id, title ,description and status ( completed or not )

from pydantic import BaseModel
from typing import Optional 

class TodoCreateSchema(BaseModel):
    title: str
    description: str = None
    status: Optional[str] = "pending"


