from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette.concurrency import run_in_threadpool

from app.dependencies import CurrentUser, DbSession
from app.models import User
from app.schemas import LoginRequest, RegisterRequest, TokenRead, UserRead
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(payload: RegisterRequest, session: DbSession) -> User:
    existing_user = await session.scalar(
        select(User).where(User.email == payload.email)
    )
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = User(
        email=payload.email,
        password_hash=await run_in_threadpool(hash_password, payload.password),
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from None

    await session.refresh(user)
    return user


@router.post("/login", response_model=TokenRead)
async def login(
    payload: LoginRequest,
    session: DbSession,
    request: Request,
) -> TokenRead:
    user = await session.scalar(select(User).where(User.email == payload.email))
    if user is None or not await run_in_threadpool(
        verify_password,
        payload.password,
        user.password_hash if user is not None else "",
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenRead(
        access_token=create_access_token(
            user.id,
            request.app.state.jwt_secret_key,
            request.app.state.access_token_minutes,
        )
    )


@router.get("/me", response_model=UserRead)
async def read_current_user(user: CurrentUser) -> User:
    return user
