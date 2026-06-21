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

from .. import schemas, Oauth2, model, database


router = APIRouter(
    prefix="/product",
    tags=["product"]
)

UPLOAD_DIR = "static/upload"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/create", response_model=schemas.Product_output,
    status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: schemas.form_pydantic_product_input = Depends(schemas.form_pydantic_product_input.as_form),
    img1: UploadFile = File(...),
    img2: UploadFile = File(...),
    video1: UploadFile = File(...),
    current_user: model.User = Depends(Oauth2.current_user),
    db: Session = Depends(database.get_db),

):
    if current_user.role != "seller":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only seller can list a product ")
    if (db.query(model.Product).filter(model.Product.ProductName == product_data.ProductName).first() is not None) or (
            db.query(model.Product).filter(
                    model.Product.ProductDescription == product_data.ProductDescription).first() is not None):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="this product name or description is already used please change and try again ")

    if current_user.role == "seller":
        image1_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex}_{img1.filename}"
        with open(image1_path, "wb") as buffer:
            shutil.copyfileobj(img1.file, buffer)

        image2_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex}_{img2.filename}"
        with open(image2_path, "wb") as buffer:
            shutil.copyfileobj(img2.file, buffer)

        video1_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex}_{video1.filename}"
        with open(video1_path, "wb") as buffer:
            shutil.copyfileobj(video1.file, buffer)

        new_product = model.Product(
            sellerid=current_user.id,
            ProductName=product_data.ProductName,
            ProductDescription=product_data.ProductDescription,
            img1=image1_path,
            img2=image2_path,
            video1=video1_path
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return {
            "productId": new_product.productId,
            "sellerid": current_user.id
        }

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cant create this")
@router.post("/update_inventory/{product_id}",response_model=schemas.warehouse_output)
def update_inventory(product_id:int,user_response:schemas.warehouse_input,current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(database.get_db)):
    get_product=db.query(model.Product).filter(model.Product.productId == product_id).first()
    check=db.query(model.PriceandInventory).filter(model.PriceandInventory.productid==product_id).first()
    if get_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product dont exists")
    if check is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inventory already added")

    if get_product.seller_detail.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cant access it")
    else:
        inventory = model.PriceandInventory(
            productid=product_id,
            currentsellerid=current_user.id,
            Price=user_response.Price,
            Inventory=user_response.Inventory
        )
        db.add(inventory)
        db.commit()
        db.refresh(inventory)
    return {
        "Price":user_response.Price,
        "Inventory":user_response.Inventory
    }
@router.get("/allproduct",response_model=List[schemas.allproduct_output])
def all_product(request:Request,db:Session=Depends(database.get_db)):
    get_active_product=db.query(model.Product,model.PriceandInventory).join(model.PriceandInventory,model.Product.productId==model.PriceandInventory.productid).filter(and_(model.PriceandInventory.Price != None,model.PriceandInventory.Inventory != None,model.PriceandInventory.Inventory > 0)).all()
    flattened_data = []
    base_url=str(request.base_url)
    for product,warehouse in get_active_product:
        full_url=f"{base_url}{product.img1}"
        item_dict={
            "productId":product.productId,
            "ProductName":product.ProductName,
            "img1":full_url,
            "Price":warehouse.Price,
        }
        flattened_data.append(item_dict)



    return flattened_data
@router.get("/{id}",response_model=schemas.ProductDetailResponse)
def view_product(request:Request,id,db:Session=Depends(database.get_db)):
    get_product=db.query(model.Product).filter(model.Product.productId==id).first()
    if get_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product Not Found")
    product_complete_db=db.query(model.Product,model.PriceandInventory).join(model.PriceandInventory,model.Product.productId==model.PriceandInventory.productid).filter(model.Product.productId == id).first()
    if product_complete_db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product Does not exits")
    if product_complete_db[1].Inventory <= 0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product Out of stock")
    seller_detail=db.query(model.Product,model.SellerProfile).join(model.SellerProfile,model.Product.sellerid==model.SellerProfile.currentsellerid).filter(model.Product.productId==id).first()
    if seller_detail is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Seller details not found")

    base_url = str(request.base_url)
    return {
        "productId": product_complete_db[0].productId,
        "sellerid": product_complete_db[0].sellerid,
        "ProductName": product_complete_db[0].ProductName,
        "ProductDescription": product_complete_db[0].ProductDescription,
        "img1": f"{base_url}{product_complete_db[0].img1}",
        "img2": f"{base_url}{product_complete_db[0].img2}",
        "video1": f"{base_url}{product_complete_db[0].video1}",
        "Price": product_complete_db[1].Price,
        "Inventory": product_complete_db[1].Inventory,
        "CompanyName": seller_detail[1].CompanyName
    }
@router.post("/addtocart/{id}")
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
        productid=product_complete_db[0].productid,
        Price=product_complete_db[1].Price,
        ProductName=product_complete_db[0].productName,
        img1=product_complete_db[0].img1,
        UserId=current_user.id

    )
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return {
        "message":"Successfully added to cart"
    }

@router.delete("/myproduct/{id}")
def deleteproduct(id,db:Session=Depends(database.get_db),current_user:model.User=Depends(Oauth2.current_user)):
    query = db.query(model.Product).filter(model.Product.productId==id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exits")
    if query.first().sellerid != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cant access it")
    filename1=query.first().img1
    filename2=query.first().img2
    filename3=query.first().video1
    query.delete()
    db.commit()
    for file in [filename1, filename2, filename3]:
        if file and os.path.exists(file):
            os.remove(file)
    return{"message":"succesfully deleted"}
@router.patch("/updateproduct/{productid}")
def updateProduct(productid:int,userresponse:schemas.updateproduct,db:Session=Depends(database.get_db),current_user:model.User=Depends(Oauth2.current_user)):
    query=db.query(model.Product).filter(model.Product.sellerid==current_user.id).filter(model.Product.productId==productid)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product does not exits")
    if query.first().sellerid != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cant access it")
    to_update=userresponse.dict(exclude_unset=True)
    query.update(to_update)
    db.commit()
    return {"message":"successfully updated"}

@router.patch("/updateimg/{id}")
async def updateimg(
        id:int,
        img1:UploadFile|None=File(None),
        img2:UploadFile|None=File(None),
        video1:UploadFile|None=File(None),
        current_user:model.User=Depends(Oauth2.current_user),
        db:Session=Depends(database.get_db)

):
    query=db.query(model.Product).filter(model.Product.productId==id).first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product dont exits")
    if query.sellerid !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cant access it")
    if img1:
        if query.img1 and os.path.exists(query.img1):
            os.remove(query.img1)
        image1_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex}_{img1.filename}"
        with open(image1_path, "wb") as buffer:
            shutil.copyfileobj(img1.file, buffer)

        query.img1 = image1_path
    if img2:
        if query.img2 and os.path.exists(query.img2):
            os.remove(query.img2)
        image2_path=f"{UPLOAD_DIR}/{uuid.uuid4().hex}_{img2.filename}"
        with open(image2_path,"wb") as buffer:
            shutil.copyfileobj(img2.file,buffer)
        query.img2=image2_path

    if video1:
        if query.video1 and os.path.exists(query.video1):
            os.remove(query.video1)

        video1_path = f"{UPLOAD_DIR}/{uuid.uuid4().hex}_{video1.filename}"

        with open(video1_path, "wb") as buffer:
            shutil.copyfileobj(video1.file, buffer)

        query.video1 = video1_path

    db.commit()

    return {"message": "Media updated successfully"}










@router.patch("/updateinventory/{id}")
def updateInventory(id:int,user_response:schemas.updateinventory,db:Session=Depends(database.get_db),current_seller:model.User=Depends(Oauth2.current_user)):
    query= db.query(model.PriceandInventory).filter(model.PriceandInventory.productid==id)
    if query.first() is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product dont exits")
    if query.first().currentsellerid != current_seller.id:
        raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You cant access it")
    to_update=user_response.dict(exclude_unset=True)
    query.update(to_update)
    db.commit()
    db.refresh(query.first())
    return {"message":"inventory updated"}



