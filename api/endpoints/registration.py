from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from db import Sessionlocal
from services.password import Hashing
from services.auth import Token
from model.users import User
from schemas.registration import Registration,Login


router = APIRouter()
Hash   = Hashing()
token  = Token()

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
        encrypt_password = Hash.get_password_hash(payload.password)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        new_user = User(
            user_role = 2,
            username=payload.username,
            email=payload.email,
            contact=payload.contact,
            dob=payload.dob,
            password=encrypt_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"msg": "User registered successfully", "user_id": new_user.user_id}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")
    

@router.post('/login')
def login(payload:Login, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not Hashing.verify_password(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password"
            )
        access_token = Token.generate_access_token({"sub": user.email, "user_id": user.user_id })
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "email": user.email,
            "user_id":user.user_id
            }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Login Failed: {str(e)}")

