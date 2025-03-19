from pydantic import BaseModel


class Registration(BaseModel):
    username:str
    email:str
    contact:str
    dob:str
    password:str