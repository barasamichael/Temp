import logging
import flask
from flask_login import current_user, login_required
from . import profiles
from ..models import Permission, User

logging.basicConfig(filename = "app.log", level = logging.INFO)


@profiles.route('/user/<int:user_id>', methods = ['GET'])
@login_required
def get_user_details(user_id):
    # Log the user ID for the request
    logging.info(f"User with ID {current_user.userId} requested details for user with ID {user_id}")

    # Checking if the current user has permission to view user details
    if current_user.can(Permission.VISIT):
        logging.warning(f"Unauthorized attempt by user with ID {current_user.userId} to view user details for user with ID {user_id}")
        return flask.jsonify({"error": "Unauthorized"}), 403

    # Fetch user details from the database
    user = User.query.get(user_id)

    if user:
        # Log successful user details retrieval
        logging.info(f"User details retrived successfully for user with ID {user_id}")

        # Return user details as JSON
        return flask.jsonify(user.getDetails()), 200
    
    else:
        # Log unsuccessful user details retrieval
        logging.warning(f"User details not found for user with ID {user_id}")

        return flask.jsonify({"error": "User not found"}), 404


