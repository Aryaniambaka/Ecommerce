

from fastapi import APIRouter,status,Depends,BackgroundTasks,HTTPException
import secrets
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from .. import schemas ,utility ,model,Oauth2,config
from .. database import get_db
from datetime import datetime, timezone
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy import desc
from datetime import  timedelta





router=APIRouter(
    prefix="/user",
    tags=["user"]
)
@router.post("/login/create",status_code=status.HTTP_201_CREATED,response_model=schemas.SuccessLoginReturn)
def create_user(user:schemas.UserInputLogin,db:Session=Depends(get_db)):
    hashed_password=user.password
    user.password=utility.hashing_password(hashed_password)
    get_dictionary_from_json=model.User(**{**user.model_dump(),"role":"user","created_at":datetime.now(timezone.utc)})
    db.add(get_dictionary_from_json)
    db.commit()
    db.refresh(get_dictionary_from_json)
    return get_dictionary_from_json
@router.post("/add_profile",status_code=status.HTTP_201_CREATED)
def add_user_profile(user:schemas.profile_user_input,current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(get_db)):
    profile=model.UserProfile(
        currentuserid=current_user.id,
        name=user.name,
        address=user.address,
        pincode=user.pincode


    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return {"message":"profile creation is success"}
@router.post("/forgotpassword")
def forgotpassword(user_response:schemas.forgotpassword,Background_task:BackgroundTasks,db:Session=Depends(get_db)):
    Otp=str(secrets.randbelow(1000000)).zfill(6)
    to_add=model.Forgot_password(
        time=datetime.now(timezone.utc),
        otp=Otp,
        useremail=user_response.email

    )
    html_layout = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <h2>Password Reset OTP</h2>

        <p>Your OTP is:</p>

        <div style="
            font-size:32px;
            font-weight:bold;
            letter-spacing:8px;
            color:#2563eb;
        ">
            {Otp}
        </div>

        <p>This OTP expires in 10 minutes.</p>
    </body>
    </html>
    """
    message = MessageSchema(
        subject="Forgot password",
        recipients=[user_response.email],
        body=html_layout,
        subtype=MessageType.html
    )
    fm = FastMail(config.conf)
    Background_task.add_task(fm.send_message, message)
    db.add(to_add)
    db.commit()
    db.refresh(to_add)
    return {"message":"Otp Sent"}
@router.patch("/verifyotp")
def verifyotp(user_response:schemas.verifyotp,db:Session=Depends(get_db)):

    query=db.query(model.User,model.Forgot_password).join(model.Forgot_password,model.User.email==model.Forgot_password.useremail).filter(model.User.email==user_response.email).order_by(desc(model.Forgot_password.id)).first()

    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Does not exits")

    if query[1].otp==user_response.otp and (datetime.now(timezone.utc)-query[1].time).total_seconds()<=600:
        db.query(model.User).filter(model.User.email==user_response.email).update({"password":utility.hashing_password(user_response.newpassword)},synchronize_session=False)
        db.delete(query[1])

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    cutoff=datetime.now(timezone.utc)-timedelta(minutes=10)
    db.query(model.Forgot_password).filter(cutoff>model.Forgot_password.time).delete()
    db.commit()
    return {"message":"password reset successfully"}
@router.delete("/delete/{id}")
def deleteuser(id,db:Session=Depends(get_db),current_user:model.User=Depends(Oauth2.current_user)):
    query = db.query(model.User).filter(model.User.id == id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cant find profile")
    if current_user.id==int(id):

        query.delete()
        db.commit()
        return {"message":"Deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you cant delete other account")

@router.patch("/updateprofile/me")
def updateprofile(user_response:schemas.updateprofile,current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(get_db)):
    query=db.query(model.UserProfile).filter(model.UserProfile.currentuserid==current_user.id)
    if query.first() is None:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you cant access this")
    to_update=user_response.dict(exclude_unset=True)
    query.update(to_update)
    db.commit()
    return {"message": "Profile updated successfully"}
