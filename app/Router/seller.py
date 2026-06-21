from typing import List

from fastapi import APIRouter,status,Depends,HTTPException
from sqlalchemy.orm import Session


from .. import schemas ,utility ,model,Oauth2
from .. database import get_db



router=APIRouter(
    prefix="/seller",
    tags=["seller"]
)
@router.post("/login/create",status_code=status.HTTP_201_CREATED,response_model=schemas.SuccessLoginReturn)
def create_user(user:schemas.UserInputLogin,db:Session=Depends(get_db)):
    hashed_password=user.password
    user.password=utility.hashing_password(hashed_password)
    complete_details={**user.model_dump(),"role":"seller"}
    get_dictionary_from_json=model.User(**complete_details)
    db.add(get_dictionary_from_json)
    db.commit()
    db.refresh(get_dictionary_from_json)
    return get_dictionary_from_json
@router.post("/add_details",status_code=status.HTTP_201_CREATED)
def add_profile(user_response:schemas.profile_seller_input,current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(get_db)):
    profile=model.SellerProfile(
        currentsellerid=current_user.id,
        GSTNo=user_response.GSTNo,
        CompanyName=user_response.CompanyName,
        OwnerName=user_response.OwnerName,
        Address=user_response.Address,
        Pincode=user_response.Pincode
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return {"message":"profile created succesfully"}

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
@router.patch("/updateprofile/{id}")
def updateprofile(id:int,user_response:schemas.sellerprofileupdate,current_user:model.User=Depends(Oauth2.current_user),db:Session=Depends(get_db)):
    query=db.query(model.SellerProfile).filter(model.SellerProfile.currentsellerid==id)
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="you cannot access it")
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="profile do not exits")
    to_update=user_response.dict(exclude_unset=True)
    query.update(to_update)
    db.commit()
    db.refresh(query.first())
    return {"message":"successfully updated"}
@router.get("/myproduct",response_model=List[schemas.myproduct])
def myproduct(db:Session=Depends(get_db),currentuser:model.User=Depends(Oauth2.current_user)):
    flattedlist=[]
    query=db.query(model.Product,model.PriceandInventory).outerjoin(model.PriceandInventory,model.Product.productId==model.PriceandInventory.productid).filter(model.Product.sellerid==currentuser.id).all()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="YOU DONT HAVE LISTED ANY PRODUCT YET")
    for product,inventory in query:
        flattedlist.append({
            "productId": product.productId,
            "ProductName": product.ProductName,
            "ProductDescription": product.ProductDescription,
            "Price": inventory.Price if inventory else 0,
            "Inventory": inventory.Inventory if inventory else 0
        })
    return flattedlist

@router.get("/orderrecived",response_model=List[schemas.OrderReceivedSchema])
def orderrecived(db:Session=Depends(get_db),current_user:model.User=Depends(Oauth2.current_user)):
    query=db.query(model.Buy,model.Product).join(model.Product,model.Product.ProductName==model.Buy.ProductName).filter(model.Product.sellerid==current_user.id).all()

    flattedlist=[]

    for buy,product in query:
        hi=db.query(model.Buy,model.UserProfile).join(model.UserProfile,model.UserProfile.currentuserid==model.Buy.UserId).filter(model.UserProfile.currentuserid==buy.UserId).first()
        flattedlist.append({
            "ProductName":buy.ProductName,
            "Quantity":buy.Quantity,
            "Address":hi[1].address ,
            "Pincode":hi[1].pincode
        })
    return flattedlist