import logging
from flask import Blueprint, request, jsonify
from app.models import db, User
from . import registration

@registration.route('/register', methods = ['POST'])
def register_user():
    data = request.json

    # Check if required fields are present in the request
    required_fields = ['firstName', 'lastName', 'emailAddress', 'phoneNumber',
            'password', 'middleName', 'nationality', 'gender']
    if not all (field in data for field in required_fields):
        logging.error("Required fields are missing")
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the email address is already registered
    if User.query.filter_by(emailAddress = data.get('emailAddress')).first():
        logging.error("Email address provided is already registered")
        return jsonify({"error": "Email address is already registered"}), 400

    # Check if the phone number is already registered
    if User.query.filter_by(phoneNumber = data.get('phoneNumber')).first():
        logging.error("Phone number provided is already registered")
        return jsonify({"error": "Phone number is already registered"}), 400

    # Add user to the database
    if User.register(details = data):
        logging.info(f"User with email address {data.get('emailAddress')} registered successfully")
        return jsonify({"message": "User registered successfully"}), 201
