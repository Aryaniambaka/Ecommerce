from pydantic import BaseModel,EmailStr,Field,ConfigDict
from typing import Optional,List
from fastapi import Form
from datetime import datetime
class UserInputLogin(BaseModel):
    email:EmailStr
    password: str
    role:Optional[str] = None
class SuccessLoginReturn(BaseModel):
    id: int
    email:EmailStr
    created_at: datetime
    role:str
    class Config:
        from_attributes = True
class JWTtokenandTYPE(BaseModel):
    access_token:str
    token_type:str
class Tokenpayload(BaseModel):
    id:Optional[int]=None
    email:Optional[EmailStr]=None
class Current_user_detail(BaseModel):
    id:int
    email:str
    role:str

    class Config:
        from_attributes = True
class form_pydantic_product_input(BaseModel):


    ProductName : str = Field(...,max_length=50)
    ProductDescription : str = Field(...,max_length=200)

    @classmethod
    def as_form(
            cls,




            ProductName: str = Form(...,max_length=50),
            ProductDescription: str = Form(...,max_length=200)

    ):
        return cls(




            ProductName= ProductName,
            ProductDescription=ProductDescription
        )

class Product_output(BaseModel):
    productId:int
    sellerid:int
    class Config:
        from_attributes = True
class profile_user_input(BaseModel):
    name:str=Field(...,max_length=100)
    address:str=Field(...,max_length=200)
    pincode:str=Field(...,max_length=6,min_length=6,pattern="^[1-9][0-9]{5}$")
class profile_seller_input(BaseModel):
    GSTNo: str = Field(..., pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{2}[0-9A-Z]{1}$")
    CompanyName:str = Field(...,max_length=50)
    OwnerName:str=Field(...,max_length=50)
    Address:str=Field(...,max_length=500)
    Pincode:str=Field(...,max_length=6,min_length=6,pattern="^[1-9][0-9]{5}$")
class warehouse_input(BaseModel):
    Price:int
    Inventory:int
class warehouse_output(BaseModel):
    Price: int
    Inventory: int
    class Config:
        from_attributes = True
class allproduct_output(BaseModel):
    productId:int
    ProductName:str
    img1:str
    Price:int=Field(...,gt=0)
    class Config:
        from_attributes=True


class ProductDetailResponse(BaseModel):
    productId: int
    sellerid: int
    ProductName: str
    ProductDescription: Optional[str] = None
    img1: str
    img2: Optional[str] = None
    video1: Optional[str] = None
    Price: int
    Inventory: int
    CompanyName: str

    class Config:
        from_attributes = True
class updateqty(BaseModel):
    Quantity:int
class mycart(BaseModel):
    id:int
    ProductName:str
    UserId:int
    productid:int
    Quantity:int
    Price:int
    img1:str
    class Config:
        from_attributes = True
class my_order(BaseModel):
    productid:int
    Quantity:int
    ProductName:str
    UserId:int
    OrderedAt:datetime
    class Config:
        from_attributes=True
class forgotpassword(BaseModel):
    email:EmailStr
class verifyotp(BaseModel):
    email:EmailStr
    otp:str
    newpassword:str
class updateprofile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name : Optional[str] = None
    address : Optional[str] = None
    pincode : Optional[str] = None
class updateproduct(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ProductName : Optional[str] = None
    ProductDescription : Optional[str] = None
class updateinventory(BaseModel):
    model_config = ConfigDict(extra="forbid")
    Inventory: Optional[int]=None
    Price: Optional[int]=None

class sellerprofileupdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    GSTNo: str|None = Field(None, pattern=r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{2}[0-9A-Z]{1}$")
    CompanyName: str|None = Field(None, max_length=50)
    OwnerName: str|None = Field(None, max_length=50)
    Address: str|None = Field(None, max_length=500)
    Pincode: str|None = Field(None, max_length=6, min_length=6, pattern="^[1-9][0-9]{5}$")
class myproduct(BaseModel):
    productId:int
    ProductName:str
    ProductDescription:str
    Price:int=0
    Inventory:int=0
    class Config:
        from_attributes = True


class OrderReceivedSchema(BaseModel):
    ProductName: str
    Quantity: int
    Address: str
    Pincode: str

    class Config:
        from_attributes = True