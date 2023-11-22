import logging
from flask_login import current_user, login_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify, abort
from ..models import db, User
from . import authentication


@authentication.route('/login', methods = ['POST'])
def login_user():
    data = request.json

    # Check if required fields are present in the request
    required_fields = ["emailAddress", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Find the user by email address
    user = User.query.filter_by(emailAddress = data.get("emailAddress")).first()

    if user:
        status = user.login(data.get("password"))
        if status.code == 200:
            # Log successful login
            logging.info(f"User {user.emailAddress} logged in successfully")

            # Generate jwt access token
            access_token = create_access_token(identity = data.get('emailAddress'))

            # Return success response
            return jsonify({
                "message": "Login successful", 
                "access_token": access_token,
                "details": user.getDetails(),
                }), 200

        elif status.code == 400:
            # Log unsuccessful login
            logging.warning(f"Unsuccessful login attempt for user: {user.emailAddress}")
            return jsonify({"error": "Invalid credentials"}), 401
            
        # Log an unknown error occurred
        logging.danger(f"Login failed for user : {user.emailAddress} - reason unknown")
        return jsonify({"error": "An error occurred. Admin attention required"}), 401

    # Log user not found
    logging.warning(f"Login attempt by unregistered user {data.get('emailAddress')}")
    return jsonify({"error": "User not found"}), 401


@authentication.route('/logout', methods = ["POST"])
@jwt_required()
def logout():
    # Log the user ID for the logout request
    #logging.info(f"User with ID {current_user.userId} is logging out")

    # Create temporary placeholder for user ID before being flushed
    #userId = current_user.userId

    emailAddress = get_jwt_identity()
    # Perform the logout operation
    #current_user.logout()

    # Log successful logout
    #logging.info(f"User with ID {userId} has been successfully logged out")

    return jsonify({"message": "Logout successful"}), 200
