from fastapi.testclient import TestClient #acts like browser
from fastapi import status

from app.database import Base,get_db

from app import schemas,Oauth2
import pytest

