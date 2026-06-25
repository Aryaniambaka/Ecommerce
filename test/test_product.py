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
def test_createproduct(Seller_auth_client,session):

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
    try:
        assert product
        assert os.path.exists(product.img1)
        assert os.path.exists(product.img2)
        assert os.path.exists(product.video1)
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()


def test_myproduct(Seller_auth_client,session):
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
    response1 = Seller_auth_client.get("/seller/myproduct")
    try:
        assert response1.status_code==200
        assert response1.json()[0]["ProductName"]=="Face Wash"#flattened list
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_addinventory(Seller_auth_client,session):

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

    try:
        assert response1.status_code==200
        assert response1.json()["Price"]==100#flattened list
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_allproduct(Seller_auth_client,session):
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
    response2 = Seller_auth_client.get("/product/allproduct")

    try:
        assert response2.status_code==200
        assert response2.json()[0]["ProductName"]=="Face Wash"#flattened list
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_updateinventory(Seller_auth_client,session):
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

    try:
        assert response1.status_code==200
        assert response1.json()["Price"]==100
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_viewproduct(Seller_auth_client,session):
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

    try:
        assert response2.status_code==200

        assert response2.json()["ProductName"]=="Face Wash"
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_viewproductfail(Seller_auth_client,session):

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

    try:
        assert response2.status_code==400

        assert response2.json()["detail"]=="Seller details not found"#flattened list
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_updateinventorypass(Seller_auth_client,session):
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
    response2 = Seller_auth_client.patch(f"/product/updateinventory/{productid}", json=to_write)
    try:
        assert response2.status_code==200
        assert response2.json()["message"]=="inventory updated"
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()


def test_updatenoimg(Seller_auth_client,session):

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
    response1=(Seller_auth_client.patch(f"/product/updateproduct/{productid}",json=data))
    response1.status_code==200

    response1.json()["message"]=="successfully updated"
    try:
        assert product
        assert os.path.exists(product.img1)
        assert os.path.exists(product.img2)
        assert os.path.exists(product.video1)
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
def test_deleteproduct(Seller_auth_client,session):

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

    try:
        assert product
        assert os.path.exists(product.img1)
        assert os.path.exists(product.img2)
        assert os.path.exists(product.video1)
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
    response1 = (Seller_auth_client.delete(f"/product/myproduct/{productid}"))
    response1.status_code == 200

    response1.json()["message"] == "succesfully deleted"
    session.close()

def test_updateimg(Seller_auth_client,session):

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
    upload={}
    response1=(Seller_auth_client.patch(f"/product/updateimg/{productid}",files=upload))
    response1.status_code==200

    response1.json()["message"]=="Media updated successfully"
    try:
        assert product
        assert os.path.exists(product.img1)
        assert os.path.exists(product.img2)
        assert os.path.exists(product.video1)
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()
    