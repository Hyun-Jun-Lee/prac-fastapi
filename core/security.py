from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from core.config import settings

# 암호화 관련 설정, bcrypt 알고리즘을 사용
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

def create_assess_token(subject:Union[str,Any], expires_delta:timedelta=None)->str:
    """
    현재시간에서 expires_delta 더한 만큼 토근 유효기간 설정하고 토근 생성 및 반환
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTE)
    
    # 토근에 포함될 내용
    to_encode = {"exp":expire, "sub":str(subject)}
    # 토큰 생성
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password:str, hashed_password:str)->bool:
    """일반 비밀번호와 해쉬 비밀번호를 비교하여 일치 여부 반환"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str)-> str:
    return pwd_context.hash(password)