from fastapi import FastAPI, HTTPException, Depends, status
from jose import jwt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
import bcrypt

app = FastAPI()

# JWT Config
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 30

# OauthSetup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )

# Dummy user DB
fake_user_db = {
   "admin": {
       "username": "admin",
       "hashed_password": hash_password("1234")
   }
}

# Create token
def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update( {
        "exp":expire
    })
    token = jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

    return token

# Login API (OAuth2 Form)
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_user_db.get(form_data.username)
    if not user or not verify_password(form_data.password,user["hashed_password"]):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password"
        )
    access_token = create_token({"sub": form_data.username})

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }
    

# Token Verify
def verify_token(token:str = Depends(oauth2_scheme)):
    try:
        payload =jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
            status_code=401,
            detail="Invalid Token"
            )
        return username
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

# Protected ROUTE
@app.get("/protected")
def protected_route(username:str = Depends(verify_token)):
    return {
        "message":f"Hello {username}, you have access to this protected route!",
        "user":username
    }