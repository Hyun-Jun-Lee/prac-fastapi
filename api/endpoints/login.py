from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud, models, schema
from api import deps
from core import security
from core.config import settings
from core.security import get_password_hash

router = APIRouter()


@router.post("/login/access-token", response_model=schema.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive User")

    access_token_expires = timedelta(minutes=settings.TOKEN_EXPIRE_MINUTE)
    return {
        "access_token": security.create_assess_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
