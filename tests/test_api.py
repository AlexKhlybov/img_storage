import os

from fastapi import status
from fastapi.testclient import TestClient
from test_base import drop_db, override_get_db

from main import app

client = TestClient(app)
db = override_get_db()


def test_upload_file():
    test_upload_file = 'test_file.jpeg'
    response = client.put(
        "/frame/", files={"up_file": ("filename", open(f'tests/{test_upload_file}', "rb"), "image/jpeg")}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'Files uploaded successfully!'}

def test_upload_no_file():
    response = client.put("/frame/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_list():
    response = client.get('/frame/')
    assert response.status_code == status.HTTP_200_OK

def test_positive_delete_img():
    img_id = 1
    response = client.delete(f'/frame/{img_id}')
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json() == {'detail': 'Files delete successfully!'}

def test_negative_delete_img():
    img_id = 100
    response = client.delete(f'/frame/{img_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
