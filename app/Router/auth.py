from fastapi import APIRouter,Depends,HTTPException,status,Response

from ..database import get_db
from app import model,utility,Oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import JWTtokenandTYPE

router=APIRouter(
    prefix="/login/verification",
    tags=["auth"]
)
@router.post("/")
def login(response:Response,loginform:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    querytogetemaildb=db.query(model.User).filter(model.User.email==loginform.username).first()
    if not querytogetemaildb:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="PLEASE CREATE AN ACCOUNT")
    if not utility.verify_hashed_password(loginform.password,querytogetemaildb.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    access_token_datatosend=Oauth2.create_access_token(data={"id":querytogetemaildb.id,"email":querytogetemaildb.email})
    response.set_cookie(key="access_token",value=f"{access_token_datatosend}",httponly=True)

    return {"Login Success"}


