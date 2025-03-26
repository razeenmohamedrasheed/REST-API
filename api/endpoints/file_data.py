from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.responses import FileResponse
from model.users import Tasks
from db import Sessionlocal
from services.auth import Token
import pandas as pd

router = APIRouter(tags=["file"])

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/files')
def list_all_taks(current_user: dict = Depends(Token.verify_token), db: Session = Depends(get_db)):
    user_id = current_user.get("role_id")
    if user_id!=1:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only admin can view all tasks."
        )
    tasks = db.query(Tasks).all()

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tasks found"
        )

    task_list = [
        {
            "Task ID": task.task_id,
            "User ID": task.user_id,
            "Task Name": task.taskname,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
        for task in tasks
    ]

    df = pd.DataFrame(task_list)
    file_name = "task_report.xlsx"
    file_path = f"./{file_name}"

    df.to_excel(file_path, index=False, engine='openpyxl')


    return FileResponse(
        path=file_path,
        filename=file_name,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    