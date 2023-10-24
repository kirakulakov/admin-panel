from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.api.depends import get_user_id_from_token, get_auth_service
from src.core.config import settings
from src.schemas.v1.request.auth import RequestSignUp
from src.schemas.v1.response.auth import ResponseToken
from src.schemas.v1.response.base import ResponseEmpty
from src.services.auth_service import AuthService

router = APIRouter()


@router.post('/sign-in', response_model=ResponseToken)
async def sign_in(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: AuthService = Depends(get_auth_service)
):
    user = await auth_service.sign_in(login=form_data.username, password=form_data.password)
    return ResponseToken(
        access_token=user.get_access_token(secrets=settings.secrets)
    )

@router.post('/sign-up', response_model=ResponseEmpty)
async def sign_up(
        request_model: RequestSignUp,
        auth_service: AuthService = Depends(get_auth_service)
):
    await auth_service.sign_up(login=request_model.login, password=request_model.password)
    return ResponseEmpty()
