from fastapi import APIRouter

from ..configs import SessionDep
from ..models import UserPublic, UserCreate, UserPersistence

user_routers = APIRouter(prefix="/users", tags=["Users"])

@user_routers.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    hashed = user.password_plain_text
    data = user.model_dump(exclude={"password_plain_text"})
    db_user = UserPersistence(**data, hashed_password=hashed)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user