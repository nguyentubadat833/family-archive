from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from models import LoginResponse, UserLogin
from services import verify_password
from ..services import get_password_hash
from ..configs import SessionDep
from ..models import UserPublic, UserCreate, UserPersistence

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

user_routers = APIRouter(prefix="/users", tags=["Users"])
auth_routers = APIRouter(prefix="/auth", tags=["Auth"])


@auth_routers.post("/login", response_model=LoginResponse)
def user_login(credentials: UserLogin, session: SessionDep):
    user_query = select(UserPersistence).where(UserPersistence.username == credentials.username)
    user = session.exec(user_query).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise credentials_exception
    return LoginResponse(access_token=user.public_id)


@user_routers.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    hashed = get_password_hash(user.password)
    data = user.model_dump(exclude={"password"})
    db_user = UserPersistence(**data, hashed_password=hashed)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
