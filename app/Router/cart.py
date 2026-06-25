import shutil
import uuid
import random
import os
from fastapi.responses import HTMLResponse

from fastapi import APIRouter, HTTPException, status, Depends, Form, UploadFile, File,status,Request
from fastapi.params import Form


from sqlalchemy import or_,and_

from sqlalchemy.orm import Session, outerjoin
from typing import List

from sqlalchemy.sql.functions import current_user

from .. import schemas, Oauth2, model, database,utility
router=APIRouter(
    prefix="/cart",
    tags=["cart"]
)
@router.post("/addtocart/{id}",status_code=status.HTTP_201_CREATED)
def add_to_cart(id,db:Session=Depends(database.get_db),current_user:model.User=Depends(Oauth2.current_user)):
    get_product = db.query(model.Product).filter(model.Product.productId == id).first()
    if get_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    product_complete_db = db.query(model.Product, model.PriceandInventory).join(model.PriceandInventory,
                                                                                model.Product.productId == model.PriceandInventory.productid).filter(
        model.Product.productId == id).first()
    if product_complete_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product Does not exits")
    if product_complete_db[1].Inventory <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product Out of stock")
    seller_detail = db.query(model.Product, model.SellerProfile).join(model.SellerProfile,model.Product.sellerid == model.SellerProfile.currentsellerid).filter(model.Product.productId == id).first()
    if seller_detail is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Seller details not found")
    if db.query(model.Cart).filter(model.Cart.UserId == current_user.id).filter(model.Cart.productid == product_complete_db[0].productId).first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already in cart")

    cart=model.Cart(
        productid=product_complete_db[0].productId,
        Price=product_complete_db[1].Price,
        ProductName=product_complete_db[0].ProductName,
        img1=product_complete_db[0].img1,
        UserId=current_user.id,
        

    )
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return {
        "message":"Successfully added to cart"
    }
@router.patch("/updatequantity/{productid}")
def update_cart(productid,user_response:schemas.updateqty,current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(database.get_db)):
    product_complete_db = db.query(model.Product, model.PriceandInventory).join(model.PriceandInventory,
                                                                                model.Product.productId == model.PriceandInventory.productid).filter(
        model.Product.productId == productid).first()
    if product_complete_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Not Found")
    db_query1 = db.query(model.Cart).filter(model.Cart.productid == productid).filter(model.Cart.UserId==current_user.id).first()
    if user_response.Quantity > product_complete_db[1].Inventory:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough inventory")
    if db_query1 is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item dont exits")
    if db_query1.UserId != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="This cart dont belongs to you")
    db_query=db.query(model.Cart).filter(model.Cart.productid==productid).filter(model.Cart.UserId==current_user.id).update({"Quantity":user_response.Quantity},synchronize_session=False)

    db.commit()
    db.refresh(db_query1)
    return {"message":"quantity updated succesfully "}
@router.get("/mycart",response_model=List[schemas.mycart])
def mycart(current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(database.get_db)):
    query=db.query(model.Cart).filter(model.Cart.UserId==current_user.id).all()
    return query

@router.delete("/deleteitem/{productid}")
def deleteitem(productid:int,current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(database.get_db)):
    query=db.query(model.Cart).filter(model.Cart.productid==productid).filter(model.Cart.UserId==current_user.id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Cant Find item in cart")
    query.delete()
    db.commit()

    return {"message":"Item deleted From cart"}



