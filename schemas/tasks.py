from pydantic import BaseModel

class Task(BaseModel):
    username:str
    user_id:str
    taskname:str