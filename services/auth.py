from datetime import datetime, timedelta, timezone
from jose import jwt

# 🔥 Secret key and algorithm
SECRET_KEY = "690d8829850945fdab27462d2d83b4df"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token:
    @staticmethod
    def generate_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """Generates a JWT access token with expiration time."""
        
        # ✅ Copy the input data
        to_encode = data.copy()

        # ✅ Set expiration time in UTC
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        print(expire)
        # ✅ Add expiration time to the token payload
        to_encode.update({"exp": expire})

        # ✅ Encode the JWT token
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
