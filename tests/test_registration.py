import flask
from app import create_app, db
from tests import BaseTestCase
from app.models import User


class RegistrationTestCase(BaseTestCase):
    def test_register_user_success(self):
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


    def test_register_user_missing_fields(self):
        # Missing 'firstName' in the data
        data = {
                "lastName": "Doe",
                "middleName": "James",
                "emailAddress": "john.doe@example.com",
                "phoneNumber": "0700000000",
                "password": "password123",
                "nationality": "Kenya",
                "gender": "Male"
                }

        response = self.client.post('/api/registration/register', json = data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)


    def test_register_user_email_already_registered(self):
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

        # Register john.doe@example.com
        response = self.client.post('/api/registration/register', json = data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"User registered successfully", response.data)

        # Check if the user details were inserted in the database
        user = User.query.filter_by(emailAddress = "john.doe@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.firstName, "John")

        # Re-register john.doe@example.com
        response = self.client.post('/api/registration/register', json = data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Email address is already registered", response.data)
    
    
    def test_register_user_phone_number_registered(self):
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

        # Register john.doe@example.com
        response = self.client.post('/api/registration/register', json = data)
        self.assertEqual(response.status_code, 201)
        self.assertIn(b"User registered successfully", response.data)

        # Check if the user details were inserted in the database
        user = User.query.filter_by(emailAddress = "john.doe@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.firstName, "John")

        data = {
                "firstName": "Mary",
                "lastName": "Jane",
                "middleName": "Kloe",
                "emailAddress": "mary.jane@example.com",
                "phoneNumber": "0700000000",
                "password": "password123",
                "nationality": "Kenya",
                "gender": "Male"
                }
        # Re-register john.doe@example.com
        response = self.client.post('/api/registration/register', json = data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Phone number is already registered", response.data)
