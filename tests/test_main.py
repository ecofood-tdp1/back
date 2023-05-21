import logging
import pymongo
import pytest

from fastapi.testclient import TestClient

from app.main import app


def test_get_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}