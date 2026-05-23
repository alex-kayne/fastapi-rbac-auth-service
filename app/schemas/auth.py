from pydantic import BaseModel, EmailStr, Field, model_validator


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=6)
    repeat_password: str

    @model_validator(mode="after")
    def validate_password(self) -> "RegisterRequest":
        if self.password != self.repeat_password:
            raise ValueError("Password must match")
        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
