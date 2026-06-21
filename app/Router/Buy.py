import shutil
import secrets
import uuid
import random
import os
from fastapi.responses import HTMLResponse
from fastapi_mail import FastMail, MessageSchema, MessageType

from fastapi import APIRouter, HTTPException, status, Depends, Form, UploadFile, File,status,Request,BackgroundTasks
from fastapi.params import Form


from sqlalchemy import or_,and_
from datetime import datetime, timezone

from sqlalchemy.orm import Session, outerjoin
from typing import List

from sqlalchemy.sql.functions import current_user

from .. import schemas, Oauth2, model, database,config
router=APIRouter(
    prefix="/buy",
    tags=["buy"]
)
@router.post("/checkout")
async def checkout(Background_task:BackgroundTasks,current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(database.get_db)):
    query=db.query(model.Cart).filter(model.Cart.UserId==current_user.id).all()
    profilecompleted=db.query(model.UserProfile).filter(model.UserProfile.currentuserid==current_user.id).first()
    if profilecompleted is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Complete Your Profile To Order")

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No cart Exits")
    my_order = ""

    for objects in query:
        orderid=f"ORD-{secrets.token_hex(4).upper()}"

        to_add=model.Buy(
            OrderId=orderid,
            productid=objects.productid,
            Quantity=objects.Quantity,
            ProductName=objects.ProductName,
            UserId=current_user.id,
            OrderedAt=datetime.now(timezone.utc)






        )
        x=db.query(model.PriceandInventory).filter(model.PriceandInventory.productid==objects.productid).first()
        qty=x.Inventory  # type: ignore[union-attr]
        db.query(model.PriceandInventory).filter(model.PriceandInventory.productid == objects.productid).update({"Inventory":qty-objects.Quantity},synchronize_session=False)


        db.add(to_add)
        my_order+=f"""
        <hr>
        <p><b>Order ID:</b> {orderid}</p>
        <p><b>Product ID:</b> {objects.productid}</p>
        <p><b>Product Name:</b> {objects.ProductName}</p>
        <p><b>Quantity:</b> {objects.Quantity}</p>
        """

    db.query(model.Cart).filter(model.Cart.UserId==current_user.id).delete()
    db.commit()
    html_layout = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; padding: 20px;">
        <h2>Thanks For Ordering</h2>
        <p>Your order has been placed successfully.</p>

        {my_order}
    </div>
    """
    message = MessageSchema(
        subject="YAY! Order placed",
        recipients=[current_user.email],
        body=html_layout,
        subtype=MessageType.html
    )
    fm = FastMail(config.conf)
    Background_task.add_task(fm.send_message, message)


    return {
        "message":"Order Completed Successfully"
    }
@router.get("/my_order",response_model=List[schemas.my_order])
def myorder(db:Session=Depends(database.get_db),current_user:model.User=Depends(Oauth2.current_user)):
    query=db.query(model.Buy).filter(model.Buy.UserId==current_user.id).all()
    return query