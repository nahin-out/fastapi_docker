from pydantic import BaseModel

class UserProfileBase(BaseModel):
    name: str | None
    age: int | None
    secret_name: str