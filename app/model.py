from alembic.autogenerate.compare import server_defaults
from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.engine import default
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    id = Column(Integer, primary_key=True,nullable=False )
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    role=Column(String,nullable=False)

class Product(Base):
    __tablename__="product"
    productId=Column(Integer,primary_key=True,nullable=False)
    sellerid=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    ProductName=Column(String,nullable=False)
    ProductDescription=Column(String,nullable=False)
    img1=Column(String,nullable=False)
    img2=Column(String,nullable=True)
    video1=Column(String,nullable=True)

    seller_detail=relationship("User")
class UserProfile(Base):
    __tablename__="userprofile"
    currentuserid=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    name=Column(String,nullable=False)
    address=Column(String,nullable=False)
    pincode=Column(String,nullable=False)

    current_detail=relationship("User")

class SellerProfile(Base):
    __tablename__="sellerprofile"
    currentsellerid=Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)

    id = Column(Integer, primary_key=True, nullable=False)
    GSTNo=Column(String,nullable=False)
    CompanyName=Column(String,nullable=False)
    OwnerName=Column(String,nullable=False)
    Address=Column(String,nullable=False)
    Pincode=Column(String,nullable=False)

    current_detail=relationship("User")
class PriceandInventory(Base):
    __tablename__="warehouse"
    id=Column(Integer,primary_key=True,nullable=False)
    productid=Column(Integer, ForeignKey("product.productId", ondelete="CASCADE"), nullable=False,unique=True)
    currentsellerid = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    Price = Column(Integer,nullable=False)
    Inventory=Column(Integer,nullable=False)
    current_detail = relationship("User")
    product_detail = relationship("Product")
class Cart(Base):
    __tablename__="myCart"
    id = Column(Integer, primary_key=True, nullable=False)
    productid = Column(Integer, ForeignKey("product.productId", ondelete="CASCADE"), nullable=False)
    Quantity=Column(Integer, nullable=False,default=1)
    Price = Column(Integer, nullable=False)
    ProductName = Column(String, nullable=False)
    img1 = Column(String, nullable=False)
    UserId=Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    current_detail = relationship("User")
    product_detail = relationship("Product")
class Buy(Base):
    __tablename__="Buy"
    OrderId=Column(String, nullable=False)
    id= Column(Integer,primary_key=True,nullable=False)
    productid = Column(Integer, ForeignKey("product.productId", ondelete="CASCADE"), nullable=False)
    Quantity = Column(Integer, nullable=False)
    ProductName = Column(String, nullable=False)
    UserId = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    OrderedAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    current_detail = relationship("User", foreign_keys=[UserId])
    product_detail = relationship("Product", foreign_keys=[productid])
class Forgot_password(Base):
    __tablename__="passwordreset"
    id=Column(Integer,primary_key=True,nullable=False)
    useremail=Column(String,ForeignKey("user.email",ondelete="CASCADE"),nullable=False)
    otp=Column(String,nullable=False)
    time=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    userdetail=relationship("User")