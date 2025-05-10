from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from auth.dependencies import refresh_token_data, user_token_data
from auth.model import RefreshTokenData, UserTokenData
from context import ApplicationContext
import settings
from shared.utils import parse_user_agent


router = APIRouter(prefix="/auth", tags=["authentication"])
application_context = ApplicationContext()


@router.post("")
def authenticate(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)], request: Request):
    browser = parse_user_agent(request.headers.get("User-Agent", ""))

    tokens = application_context.authentication.authenticate(
        form_data.username,
        form_data.password,
        settings.AUTH_REFRESH_RETENTION_DAYS,
        browser)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "access_token": tokens["access_token"],
                            "refresh_token": tokens["refresh_token"],
                            "token_type": "bearer"
                        }
                        )


@router.post("/refresh")
def refresh(refresh_token: Annotated[RefreshTokenData, Depends(refresh_token_data)]):
    tokens = application_context.authentication.refresh(
        refresh_token.raw_token,
        refresh_token.user_guid,
        refresh_token.device_guid
    )

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "access_token": tokens["access_token"],
                            "refresh_token": tokens["refresh_token"],
                            "token_type": "bearer"
                        }
                        )


@router.post("/logout")
def logout(refresh_token: Annotated[RefreshTokenData, Depends(refresh_token_data)]):
    application_context.authentication.logout(
        refresh_token.user_guid, refresh_token.device_guid)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="No content")


@router.post("/logout-all")
def logout_all_sessions(token: Annotated[UserTokenData, Depends(user_token_data)]):
    application_context.authentication.logout_all_sessions(token.user_guid)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content="No content")


@router.get("/sessions")
def get_logged_in_sessions(token: Annotated[UserTokenData, Depends(user_token_data)]):
    devices = application_context.authentication.get_logged_in_sessions(
        token.user_guid)

    return devices
