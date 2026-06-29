from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str

class LoginResponse(BaseModel):
    token: str

class ValidateResponse(BaseModel):
    valid: bool

MY_JWT_TOKEN = None

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/login", response_model=LoginResponse)
def login(login_request: LoginRequest):
    global MY_JWT_TOKEN

    if (
        login_request.username == "admin"
        and login_request.password == "password"
    ):
        MY_JWT_TOKEN = "sample-jwt-token"
        return {"token": MY_JWT_TOKEN}

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )

@app.post("/validate")
def validate(token: Token):
    return {
        "valid": token.token == MY_JWT_TOKEN
    }