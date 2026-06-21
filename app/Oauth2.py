
from wsgiref import headers
from jose import jwt,JWTError

from fastapi.security import OAuth2PasswordBearer


from app import config,schemas,model
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from . import database
from fastapi import Depends,status,HTTPException,Request
#oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login/verification")
SECRET_KEY=config.settings.SECRET_KEY_1
ALGORITHM=config.settings.ALGORITHM_1
ACCESS_TOKEN_EXPIRE=config.settings.ACCESS_TOKEN_EXPIRE_1
def create_access_token(data:dict):
    to_encode=data.copy()
    expire= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
def verify_access_token(token:str,setofexception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)#dictionary
        id=payload.get("id")
        email=payload.get("email")
        if id is None or email is None:
            raise setofexception
        token_data = schemas.Tokenpayload(id=id, email=email)#using just to verify schema(also if error raises it is in try block)pydantic model
    except JWTError:
        raise setofexception
    return token_data
def current_user(request:Request,db:Session=Depends(database.get_db)):
    setofexeception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Validation failed",headers={"WWW-Authenticate":"Bearer"})
    token=request.cookies.get("access_token")
    if token is None:
        raise setofexeception
    fromtokentouser=verify_access_token(token,setofexeception)
    user=db.query(model.User).filter(model.User.id==fromtokentouser.id,model.User.email==fromtokentouser.email).first()
    if user is None:
        raise setofexeception
    return user




