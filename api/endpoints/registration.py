from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from db import Sessionlocal
from model.users import User
from schemas.registration import Registration,Login


router = APIRouter()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/registration')
async def registration(payload:Registration, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == payload.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        new_user = User(
            username=payload.username,
            email=payload.email,
            contact=payload.contact,
            dob=payload.dob,
            password=payload.password  
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"msg": "User registered successfully", "user_id": new_user.id}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")
    

@router.post('/login')
def login(payload:Login, db: Session = Depends(get_db)):
    try:
        pass
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Login Failed: {str(e)}")

