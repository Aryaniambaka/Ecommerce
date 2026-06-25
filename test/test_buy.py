import pytest
import time
from jose import jwt
from app import config
from sqlalchemy import desc

from test.db import session
from app import schemas,Oauth2,model,utility,model
from app import schemas
from freezegun import freeze_time
from datetime import datetime, timedelta
import os
from pathlib import Path
def test_checkout(S_auth_client,Seller_auth_client,session):# A seller user can still buy add to cart and do all things a buyer can
    to_write1 = {
        "name": "aryan",
        "address": "O-609,OXY HOMEZ",
        "pincode": "201005"
    }
    response0 = S_auth_client.post("/user/add_profile", json=to_write1)
    assert response0.json()["message"] == "profile creation is success"
    assert response0.status_code == 201
    to_write = {

        "GSTNo": "07AAAAA1111A2Z1",
        "CompanyName": "Test Corp",
        "OwnerName": "Owner",
        "Address": "Addr",
        "Pincode": "123456"
    }
    Seller_auth_client.post("/seller/add_details", json=to_write)
    path=Path(__file__).parent / "asset"
    files={
        "img1":("product1.png",(path / "img.png").read_bytes(),"image/png"),
        "img2": ("product1S.png", (path / "img.png").read_bytes(), "image/png"),
        "video1": ("product1.png", (path / "test.mp4").read_bytes(), "video/mp4"),
    }
    data={
        "ProductName": "Face Wash",
        "ProductDescription": "This Face Wash has rice starch",

    }
    response = Seller_auth_client.post("/product/create", data=data, files=files)
    assert response.status_code==201
    productid=response.json()["productId"]
    product = session.query(model.Product).filter(
        model.Product.productId == productid
    ).first()
    to_write={
        "Price":100,
        "Inventory":100
    }
    response1 = Seller_auth_client.post(f"/product/update_inventory/{productid}",json=to_write)
    response2 = S_auth_client.get(f"/product/{productid}")
    response3=S_auth_client.post(f"/cart/addtocart/{productid}")
    response4=S_auth_client.post("/buy/checkout")

    try:
        assert response2.status_code==200
        assert response4.status_code==200
        assert response4.json()["message"] == "Order Completed Successfully"


        assert response2.json()["ProductName"]=="Face Wash"
        assert response3.status_code == 201
        assert response3.json()["message"]=="Successfully added to cart"

    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_myorder(S_auth_client,Seller_auth_client,session):# A seller user can still buy add to cart and do all things a buyer can
    to_write1 = {
        "name": "aryan",
        "address": "O-609,OXY HOMEZ",
        "pincode": "201005"
    }
    response0 = S_auth_client.post("/user/add_profile", json=to_write1)
    assert response0.json()["message"] == "profile creation is success"
    assert response0.status_code == 201
    to_write = {

        "GSTNo": "07AAAAA1111A2Z1",
        "CompanyName": "Test Corp",
        "OwnerName": "Owner",
        "Address": "Addr",
        "Pincode": "123456"
    }
    Seller_auth_client.post("/seller/add_details", json=to_write)
    path=Path(__file__).parent / "asset"
    files={
        "img1":("product1.png",(path / "img.png").read_bytes(),"image/png"),
        "img2": ("product1S.png", (path / "img.png").read_bytes(), "image/png"),
        "video1": ("product1.png", (path / "test.mp4").read_bytes(), "video/mp4"),
    }
    data={
        "ProductName": "Face Wash",
        "ProductDescription": "This Face Wash has rice starch",

    }
    response = Seller_auth_client.post("/product/create", data=data, files=files)
    assert response.status_code==201
    productid=response.json()["productId"]
    product = session.query(model.Product).filter(
        model.Product.productId == productid
    ).first()
    to_write={
        "Price":100,
        "Inventory":100
    }
    response1 = Seller_auth_client.post(f"/product/update_inventory/{productid}",json=to_write)
    response2 = S_auth_client.get(f"/product/{productid}")
    response3=S_auth_client.post(f"/cart/addtocart/{productid}")
    response4=S_auth_client.post("/buy/checkout")
    response5=S_auth_client.get("/buy/my_order")

    try:
        assert response2.status_code==200
        assert response4.status_code==200
        assert response4.json()["message"] == "Order Completed Successfully"
        assert response5.status_code==200

        assert response5.json()[0]["ProductName"] == "Face Wash"


        assert response2.json()["ProductName"]=="Face Wash"
        assert response3.status_code == 201
        assert response3.json()["message"]=="Successfully added to cart"

    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()