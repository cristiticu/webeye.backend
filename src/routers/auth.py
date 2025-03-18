from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from context import ApplicationContext


router = APIRouter(prefix="/auth", tags=["authentication"])
application_context = ApplicationContext()


@router.post("")
def authenticate(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    token = application_context.authentication.authenticate(
        form_data.username, form_data.password)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"access_token": token, "token_type": "bearer"}
                        )
