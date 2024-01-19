from io import BytesIO
import pytest
from requests import post
from flask_testing import TestCase

from main import app

def image_path():
    return "tests/test_images/"

class FaceRecognitionTests(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_positive_files(self):
        try:
            with open(image_path() + "AB_1.jpg", "rb") as f:
                image1 = f.read()
        except FileNotFoundError:
            pytest.fail("File tests/test_images/AB_1.jpg not found")

        try:
            with open(image_path() + "AB_2.jpg", "rb") as f:
                image2 = f.read()
        except FileNotFoundError:
            pytest.fail("File tests/test_images/AB_2.jpg not found")

        positive_files = {
            "image1": (BytesIO(image1), "AB_1.jpg"),
            "image2": (BytesIO(image2), "AB_2.jpg")
        }

        response = self.client.post("/face-recognition", content_type="multipart/form-data", data=positive_files)
        assert response.status_code == 200
        assert response.json["result"] == "True"


    def test_negative_files(self):
        try:
            with open(image_path() + "AB_1.jpg", "rb") as f:
                image1 = f.read()
        except FileNotFoundError:
            pytest.fail("File tests/test_images/AB_1.jpg not found")

        try:
            with open(image_path() + "AM_1.jpg", "rb") as f:
                image2 = f.read()
        except FileNotFoundError:
            pytest.fail("File tests/test_images/AM_1.jpg not found")

        negative_files = {
            "image1": (BytesIO(image1), "AB_1.jpg"),
            "image2": (BytesIO(image2), "AM_1.jpg")
        }

        response = self.client.post("/face-recognition", content_type="multipart/form-data", data=negative_files)
        assert response.status_code == 200
        assert response.json["result"] == "False"