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
        assert response1.json()["ProductName"]=="Face wash"
    finally:
        os.remove(product.img1)
        os.remove(product.img2)
        os.remove(product.video1)
        session.close()