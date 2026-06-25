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
def test_addtocart(Seller_auth_client,session):
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
    response2 = Seller_auth_client.get(f"/product/{productid}")
    response3=Seller_auth_client.post(f"/cart/addtocart/{productid}")

    try:
        assert response2.status_code==200

        assert response2.json()["ProductName"]=="Face Wash"
        assert response3.status_code == 201
        assert response3.json()["message"]=="Successfully added to cart"
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()

def test_cartmycart(Seller_auth_client,session):
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
    response2 = Seller_auth_client.get(f"/product/{productid}")
    response3=Seller_auth_client.post(f"/cart/addtocart/{productid}")
    response4=Seller_auth_client.get(f"/cart/mycart")

    try:
        assert response2.status_code==200
        assert response4.status_code == 200

        assert response2.json()["ProductName"]=="Face Wash"
        assert response4.json()[0]["ProductName"] == "Face Wash"
        assert response3.status_code == 201
        assert response3.json()["message"]=="Successfully added to cart"
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_updatecart(Seller_auth_client,session):
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
    response2 = Seller_auth_client.get(f"/product/{productid}")
    response3=Seller_auth_client.post(f"/cart/addtocart/{productid}")
    response4=Seller_auth_client.patch(f"/cart/updatequantity/{productid}",json={"Quantity":4})

    try:
        assert response2.status_code==200
        assert response4.status_code == 200
        assert response4.json()["message"]=="quantity updated succesfully "

        assert response2.json()["ProductName"]=="Face Wash"
        assert response3.status_code == 201
        assert response3.json()["message"]=="Successfully added to cart"
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_updatecartfail(Seller_auth_client,session):
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
        "Inventory":2
    }
    response1 = Seller_auth_client.post(f"/product/update_inventory/{productid}",json=to_write)
    response2 = Seller_auth_client.get(f"/product/{productid}")
    response3=Seller_auth_client.post(f"/cart/addtocart/{productid}")
    response4=Seller_auth_client.patch(f"/cart/updatequantity/{productid}",json={"Quantity":4})

    try:
        assert response2.status_code==200
        assert response4.status_code == 400
        assert response4.json()["detail"]=="Not enough inventory"

        assert response2.json()["ProductName"]=="Face Wash"
        assert response3.status_code == 201
        assert response3.json()["message"]=="Successfully added to cart"
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_cartdelete(Seller_auth_client,session):
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
    response2 = Seller_auth_client.get(f"/product/{productid}")
    response3=Seller_auth_client.post(f"/cart/addtocart/{productid}")

    response4=Seller_auth_client.delete(f"/cart/deleteitem/{productid}")

    try:
        assert response2.status_code==200
        assert response4.status_code == 200
        assert response4.json()["message"] == "Item deleted From cart"

        assert response2.json()["ProductName"]=="Face Wash"

        assert response3.status_code == 201
        assert response3.json()["message"]=="Successfully added to cart"
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()