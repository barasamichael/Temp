import flask
from app import create_app, db
from tests import BaseTestCase
from app.models import User


class AuthenticationTestCase(BaseTestCase):
    def test_login_user_success(self):
        # Add a user to the database
        data = {
                "firstName": "John",
                "lastName": "Doe",
                "middleName": "James",
                "emailAddress": "john.doe@example.com",
                "phoneNumber": "0700000000",
                "password": "password123",
                "nationality": "Kenya",
                "gender": "Male"
                }

        response = self.client.post("/api/registration/register", json = data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"User registered successfully", response.data)

        # Check if the user details were inserted in the database
        user = User.query.filter_by(emailAddress = "john.doe@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.firstName, "John")

        login_data = {
                "emailAddress": "john.doe@example.com",
                "password": "password123"
                }

        response = self.client.post("/api/authentication/login", json = login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login successful", response.data)


    def test_login_user_missing_values(self):
        # Missing "emailAddress" in the data
        login_data = {
                "password": "hashed_password"
                }

        response = self.client.post("/api/authentication/login", json = login_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)


    def test_login_user_invalid_credentials(self):
        # Add a user to the database
        data = {
                "firstName": "John",
                "lastName": "Doe",
                "middleName": "James",
                "emailAddress": "john.doe@example.com",
                "phoneNumber": "0700000000",
                "password": "password123",
                "nationality": "Kenya",
                "gender": "Male"
                }

        response = self.client.post("/api/registration/register", json = data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"User registered successfully", response.data)

        # Check if the user details were inserted in the database
        user = User.query.filter_by(emailAddress = "john.doe@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.firstName, "John")

        login_data = {
                "emailAddress": "john.doe@example.com",
                "password": "password345"
                }

        response = self.client.post("/api/authentication/login", json = login_data)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Invalid credentials", response.data)


    def test_login_user_not_found(self):
        login_data = {
                "emailAddress": "kamau.james@example.com",
                "password": "password123"
                }

        response = self.client.post("/api/authentication/login", json = login_data)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"User not found", response.data)
