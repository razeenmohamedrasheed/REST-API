from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException
from services.auth import Token
from schemas.tasks import Task
from sqlalchemy.orm import Session
from model.users import Tasks
from db import Sessionlocal

router = APIRouter(tags=["Task Data"])

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/tasks')
async def create_new_task(payload:Task, db: Session = Depends(get_db),  current_user: dict = Depends(Token.verify_token)):
    try:
        new_task = Tasks(
             user_id = current_user.get("user_id"),
             taskname = payload.taskname
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return { 
                "msg": "Task Created",
                "created_by": current_user.get("user_id") }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task. Please try again. error:{e}"
        )

@router.get('/tasks')   
async def view_individual_task( db: Session = Depends(get_db),current_user: dict = Depends(Token.verify_token)):
    user_id = current_user.get("user_id")
    tasks = db.query(Tasks).filter(Tasks.user_id == user_id).all()

    if not tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No tasks found for user ID {user_id}"
        )
    
    return {
        "user_id": user_id,
        "total_tasks": len(tasks),
        "tasks": [
            {
                "task_id": item.task_id,            
                "taskname": item.taskname,
                "created_at": item.created_at,
                "updated_at": item.updated_at
            }
            for item in tasks                    
        ]
    }
