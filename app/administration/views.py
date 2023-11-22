import flask
import logging
from datetime import datetime
from flask_login import current_user, login_required, login_user
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from sqlalchemy import or_
from . import administration
from .. import db
from ..models import (Permission, User, Role, Raffle, Book, Ticket, Author, 
        AuthorBook, Category, CategoryBook, Notification, Task)


#------------------------------------------------------------------------------
#                               USER MANAGEMENT
#------------------------------------------------------------------------------
@administration.route('/users', methods = ["GET"])
@jwt_required()
def get_users():
    """Gets list of all users"""
    try:
        # Log the user ID for the request
        logging.info(f"User requested details for multiple users")

        # Checking if the current user has permission to view user details
        if current_user.can(Permission.VISIT):
            logging.warning(f"Unauthorized attempt to view multiple user details")
            return flask.jsonify({"error": "Unauthorized"}), 403

        # Fetch user details from the database
        users = User.query.all()
        users = [user.getDetails() for user in users]

        if users:
            # Log successful user details retrieval
            logging.info(f"Multiple User details retrieved successfully by user")

            # Return user details as JSON
            return flask.jsonify({"users": users}), 200
    
        else:
            # Log unsuccessful user details retrieval
            logging.warning(f"User details found in the database")

            return flask.jsonify({"error": "Users not found"}), 404

    except Exception as e:
        # Log any errors that occur during fetching of multiple user details 
        logging.error(f"Error fetching multiple user details: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching multiple user details"}) , 500


@administration.route('/users/<int:user_id>', methods = ["GET"])
def get_user(user_id):
    """Gets details of a specific user"""
    try:
        # Log the user ID for the request
        logging.info(f"User requested details for user with ID {user_id}")

        # Checking if the current user has permission to view user details
        if current_user.can(Permission.VISIT):
            logging.warning(f"Unauthorized attempt to view user details for user with ID {user_id}")
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

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error occured while fetching user details: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching requested user details"}) , 500


@administration.route('/users/<int:user_id>', methods = ["PUT"])
def update_user(user_id):
    """Updates details of a user"""
    try:
        # Retrieve the specific user from the database
        user = User.query.get(user_id)

        if not user:
            # Log that the user with the specified user_id was not found
            logging.warning(f"User with userId {user_id} not found")

            # Return a not found response
            return jsonify({"error": "User not found"}), 404

        # Extract data from the request JSON
        data = flask.request.json

        # Confirm all values are present
        #################TO BE IMPLEMENTED#############
        
        # Update user details with the extracted data
        #################TO BE IMPLEMENTED#############

        # Log the successful update of the user details
        logging.info(f"Successfully updated details for user with ID {user_id}")

        # Return a success response
        return jsonify({"message": "User details updated successfully"}), 200

    except Exception as e:
        # Log any errors that occur during update of user details 
        logging.error(f"Error updating details of user {user_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while updating user details"}) , 500


@administration.route('/users/<int:user_id>', methods = ["DELETE"])
def delete_user(user_id):
    """Deletes a user"""
    try:
        # Retrieve the specific user from the database
        user = User.query.get(user_id)

        if not user:
            # Log that the user with the specified user_id was not found
            logging.warning(f"User with userId {user_id} not found")

            # Return a not found response
            return jsonify({"error": "User not found"}), 404

        # Remove user
        user.remove()

        # Log the successful deletion of user record
        logging.info(f"Successfully deleted details for user with ID {user_id}")

        # Return a success response
        return jsonify({"message": "User details deleted successfully"}), 200

    except Exception as e:
        # Log any errors that occur during deletion of user record 
        logging.error(f"Error deleting details for user {user_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while deleting user details"}) , 500


@administration.route('/users/<int:user_id>/upload-image', methods = ["POST"])
def upload_user_image(user_id):
    """Uploads user image"""
    try:
        user = User.query.get(user_id)

        if not user:
            # Log that the user with the specified user_id was not found
            logging.warning(f"User with userId {user_id} not found")

            # Return a not found response
            return jsonify({"error": "User not found"}), 404

        # Check if the request contains a file
        if 'file' not in flask.request.files:
            return jsonify({"error": "No file provided"}), 400

        file = flask.request.files['file']

        if not user.updateProfileImage(file, 
                flask.current_app.config["USER_IMAGES_UPLOAD_PATH"]):
            # Log the invalid file was provided
            logging.warning("Invalid file provided for image upload")

            # Return an error response for the invalid file
            return jsonify({"error": "Invalid file type. Allowed types: png, jpg, jpeg, gif"}), 400

        # Log the successful image upload
        logging.info(f"Image uploaded successfully for user with userId {user_id}")
            
        # Return a success response
        return jsonify({"message": "Image uploaded successfully"}), 200

    except Exception as e:
        # Log any errors that occur during image upload 
        logging.error(f"Error uploading user image: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while uploading user image"}) , 500


@administration.route('/users/<int:user_id>/tickets', methods = ["GET"])
def get_user_tickets(user_id):
    """Retrieves tickets purchased by a user"""
    try:
        # Retrieve the specific user from the database
        user = User.query.get(user_id)

        if not user:
            # Log that the user with the specified user_id was not found
            logging.warning(f"User with userId {user_id} not found")

            # Return a not found response
            return jsonify({"error": "User not found"}), 404

        # Get tickets of the user
        tickets = [{ticket.ticketId: ticket.getDetails()} 
                for ticket in user.tickets]

        # Return the tickets as a JSON response
        return jsonify({"user_tickets": tickets}), 200


    except Exception as e:
        # Log any errors that occur during extraction of user tickets
        logging.error(f"Error extracting tickets for user {user_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving user tickets"}) , 500


@administration.route('/users/<int:user_id>/tasks', methods = ["GET"])
def get_user_tasks(user_id):
    """Retrieves tasks belonging to the user"""
    try:
        # Retrieve the specific user from the database
        user = User.query.get(user_id)

        if not user:
            # Log that the user with the specified user_id was not found
            logging.warning(f"User with userId {user_id} not found")

            # Return a not found response
            return jsonify({"error": "User not found"}), 404

        # Get tasks of the user
        tasks = [{task.taskId: task.getDetails()} 
                for task in user.tasks]

        # Return the tasks as a JSON response
        return jsonify({"user_tasks": tasks}), 200


    except Exception as e:
        # Log any errors that occur during extraction of tasks
        logging.error(f"Error extracting tasks for user {user_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving user tasks"}) , 500


@administration.route('/users/<int:user_id>/notifications', methods = ["GET"])
def get_user_notifications(user_id):
    """Retrieves notifications associated to the user"""
    try:
        # Retrieve the specific user from the database
        user = User.query.get(user_id)

        if not user:
            # Log that the user with the specified user_id was not found
            logging.warning(f"User with userId {user_id} not found")

            # Return a not found response
            return jsonify({"error": "User not found"}), 404

        # Get notifications of the user
        notifications = [{notification.notificationId: notification.getDetails()} 
                for notification in user.notifications]

        # Return the notifications as a JSON response
        return jsonify({"user_notifications": notifications}), 200


    except Exception as e:
        # Log any errors that occur during extraction of notifications
        logging.error(f"Error extracting notifications for user {user_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving user notifications"}) , 500


#------------------------------------------------------------------------------
#                               RAFFLE MANAGEMENT
#------------------------------------------------------------------------------
@administration.route('/raffles', methods = ["GET"])
def get_raffles():
    """Gets list of all raffles"""
    try:
        # Fetch all raffles from the database
        raffles = Raffle.query.all()

        # Log the successful retrieval of raffles
        logging.info("Raffles fetched successfully")

        # Retrieve details in jsonfiable format
        raffles = [{raffle.raffleId: raffle.getDetails()} for raffle in raffles]

        # Return the raffles as a JSON response
        return jsonify({"raffles": raffles}), 200
    
    except Exception as e:
        # Log any errors that occur during fetching of raffles 
        logging.error(f"Error fetching raffles: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching raffles"}) , 500


@administration.route('/raffles/<int:raffle_id>', methods = ["GET"])
def get_raffle(raffle_id):
    """Gets details of a specific raffle"""
    try:
        # Get Raffle details from the database
        raffle = Raffle.query.get(raffle_id)
        if raffle:
            logging.info(f"Details fetched successfully for raffle with raffleId {raffle_id}")
            return jsonify(raffle.getDetails()), 200

        else:
            # Log that the raffle with the specified raffle_id was not found
            logging.warning(f"Raffle with raffleId {raffle_id} not found")

            return jsonify({"error": "Raffle not found"}), 404

    except Exception as e:
        # Log any errors that occur during fetcing of raffle details
        logging.error(f"Error fetching raffle details: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching raffle details"}) , 500


@administration.route('/raffles', methods = ["POST"])
def create_raffle():
    """Opens a new raffle"""
    try:
        # Get raffle details from the request JSON
        data = flask.request.json

        # Check if required fields are present in the request
        required_fields = ['participantLimit', 'bookId', 'price']
        if not all (field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new raffle instance with the provided details
        raffle = Raffle.open(data)
        if raffle:
            # Log the successful creation of a new raffle
            logging.info(f"Successfully created a new raffle with ID: {raffle.raffleId}")

            # Return a success message
            return jsonify({"message": "Raffle created successfully"}), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error creating the raffle: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while creating the raffle"}) , 500


@administration.route('/raffles/<int:raffle_id>', methods = ["PUT"])
def update_raffle(raffle_id):
    """Updates details of a raffle"""
    try:
        # Retrieve the specific raffle from the database
        raffle = Raffle.query.get(raffle_id)

        if not raffle:
            # Log that the raffle with the specified raffle_id was not found
            logging.warning(f"Raffle with raffleId {raffle_id} not found")

            # Return a not found response
            return jsonify({"error": "Raffle not found"}), 404

        # Extract data from the request JSON
        data = flask.request.json

        # Confirm all values are present
        #################TO BE IMPLEMENTED#############
        
        # Update raffle details with the extracted data
        #################TO BE IMPLEMENTED#############

        # Log the successful update of the raffle details
        logging.info(f"Successfully updated details for raffle with ID {raffle_id}")

        # Return a success response
        return jsonify({"message": "Raffle details updated successfully"}), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error updating details for raffle {raffle_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while updating raffle details"}) , 500


@administration.route('/raffles/<int:raffle_id>/close', methods = ["POST"])
def close_raffle(raffle_id):
    """Closes a raffle"""
    try:
        # Retrieve the specific raffle from the database
        raffle = Raffle.query.get(raffle_id)

        if not raffle:
            # Log that the raffle with the specified raffle_id was not found
            logging.warning(f"Raffle with raffleId {raffle_id} not found")

            # Return a not found response
            return jsonify({"error": "Raffle not found"}), 404

        # Check if the raffle is already closed
        if not raffle.isOngoing():
            logging.warning(f"Attempted to close an already closed raffle with raffleId {raffle_id}")

            # Return a conflict response
            return jsonify({"error": "Raffle is already closed"})

        # Perform actual closing of the raffle
        raffle.close()

        # Return a success message
        return jsonify({"message": "Raffle closed successfully"})

    except Exception as e:
        # Log any errors that occur during closing of the raffle 
        logging.error(f"Error closing the raffle: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while closing the raffle"}) , 500


@administration.route('/raffles/<int:raffle_id>/activate', methods = ["POST"])
def activate_raffle(raffle_id):
    """Activates a raffle"""
    try:
        # Retrieve the specic raffle from the database
        raffle = Raffle.query.get(raffle_id)

        if not raffle:
            # Log that the raffle with the specified raffle_id was not found
            logging.warning(f"Raffle with raffleId {raffle_id} not found")

            # Return a not found response
            return jsonify({"error": "Raffle not found"}), 404

        # Activate the raffle
        if 400 in raffle.activate():
            # Log that the raffle is already closed
            logging.warning(f"Attempted to activate an already closed raffle with raffleId {raffle_id}")

            # Return a conflict response
            return jsonify({"error": "Raffle is already closed"})

        # Log the successful activation of the raffle
        logging.info(f"Successfully activated raffle with raffleId {raffle_id}")

        # Return a success message
        return jsonify({"message": "Raffle activated successfully"}), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error activating raffle {raffle_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while activating the raffle"}) , 500


@administration.route('/raffles/<int:raffle_id>/deactivate}', methods = ["POST"])
def deactivate_raffle(raffle_id):
    """Deactivates a raffle"""
    try:
        # Retrieve the specic raffle from the database
        raffle = Raffle.query.get(raffle_id)

        if not raffle:
            # Log that the raffle with the specified raffle_id was not found
            logging.warning(f"Raffle with raffleId {raffle_id} not found")

            # Return a not found response
            return jsonify({"error": "Raffle not found"}), 404

        # Activate the raffle
        if 400 in raffle.activate():
            # Log that the raffle is already closed
            logging.warning(f"Attempted to activate an already closed raffle with raffleId {raffle_id}")

            # Return a conflict response
            return jsonify({"error": "Raffle is already closed"})

        # Log the successful de-activation of the raffle
        logging.info(f"Successfully de-activated raffle with raffleId {raffle_id}")

        # Return a success message
        return jsonify({"message": "Raffle de-activated successfully"}), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error ...: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while ..."}) , 500


@administration.route('/raffles/<int:raffle_id>/tickets', methods = ["GET"])
def get_raffle_tickets(raffle_id):
    """Gets tickets belonging to a raffle"""
    try:
        # Retrieve the specific raffle from the database
        raffle = Raffle.query.get(raffle_id)

        if not raffle:
            # Log that the raffle with the specified raffle_id was not found
            logging.warning(f"Raffle with raffleId {raffle_id} not found")

            # Return a not found response
            return jsonify({"error": "Raffle not found"}), 404

        # Get tickets of the raffle
        tickets = [{ticket.ticketId: ticket.getDetails()} 
                for ticket in raffle.tickets]

        # Return the tickets as a JSON response
        return jsonify({"raffle_tickets": tickets}), 200

    except Exception as e:
        # Log any errors that occur during extraction of raffle tickets
        logging.error(f"Error extracting tickets for raffle {raffle_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving raffle tickets"}) , 500


@administration.route('/raffles/<int:raffle_id>/purchase', methods = ["POST"])
def purchase_ticket(raffle_id):
    """Purchases raffle tickets for a book"""
    try:
        pass
    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error ...: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while ..."}) , 500


#------------------------------------------------------------------------------
#                               AUTHOR MANAGEMENT
#------------------------------------------------------------------------------
@administration.route('/authors', methods = ["GET"])
def get_authors():
    """Get list of all authors"""
    try:
        # Fetch all authors from the database
        authors = Author.query.all()

        # Log the successful retrieval of authors
        logging.info("Authors fetched successfully")

        # Retrieve details in jsonfiable format
        authors = [{author.authorId: author.getDetails()} for author in authors]

        # Return the authors as a JSON response
        return jsonify({"authors": authors}), 200

    except Exception as e:
        # Log any errors that occur during fetching authors
        logging.error(f"Error fetching authors: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching authors"}) , 500


@administration.route('/authors/<int:author_id>', methods = ["GET"])
def get_author(author_id):
    """Get details of a specific author"""
    try:
        author = Author.query.get(author_id)
        if author:
            logging.info(f"Details fetched successfully for author with authorId {author_id}")
            return jsonify(author.getDetails()), 200

        else:
            # Log that the author with the specified author_id was not found
            logging.warning(f"Author with authorId {author_id} not found")

            return jsonify({"error": "Author not found"}), 404
        
    except Exception as e:
        # Log any errors that occur during author details retrieval
        logging.error(f"Error fetching author details: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching author details"}) , 500


@administration.route('/authors/<int:author_id>/books', methods = ["GET"])
def get_author_books(author_id):
    """Get books of a particular author"""
    try:
        # Retrieve the specific author from the database
        author = Author.query.get(author_id)

        if not author:
            # Log that the author with the specified author_id was not found
            logging.warning(f"Author with authorId {author_id} not found")

            # Return a not found response
            return jsonify({"error": "Author not found"}), 404

        # Get books of the author
        books = [{book.bookId: book.getDetails()} 
                for book in author.books]

        # Return the books as a JSON response
        return jsonify({"author_books": books}), 200


    except Exception as e:
        # Log any errors that occur during deletion of author record 
        logging.error(f"Error extracting books for author {author_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving author books"}) , 500


@administration.route('/authors', methods = ["POST"])
def add_author():
    """Add a new author"""
    try:
        # Get author details from the request JSON
        data = flask.request.json

        # Check if required fields are present in the request
        required_fields = ["firstName", "middleName", "lastName", "emailAddress", 
                "nationality", "summary", "phoneNumber", "gender"]
        if not all (field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new author instance with the provided details
        author = Author.add(data)
        if author:
            # Log the successful creation of a new author
            logging.info(f"Successfully added a new author with ID: {author.authorId}")

            # Return a success message
            return jsonify({"message": "Author added successfully"}), 200

    except Exception as e:
        # Log any errors that occur during adding of the author 
        logging.error(f"Error creating the author: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while creating the author"}) , 500


@administration.route('/authors/<int:author_id>', methods = ["PUT"])
def update_author(author_id):
    """Update details of an author"""
    try:
        # Retrieve the specific author from the database
        author = Author.query.get(author_id)

        if not author:
            # Log that the author with the specified author_id was not found
            logging.warning(f"Author with authorId {author_id} not found")

            # Return a not found response
            return jsonify({"error": "Author not found"}), 404

        # Extract data from the request JSON
        data = flask.request.json

        # Confirm all values are present
        #################TO BE IMPLEMENTED#############
        
        # Update author details with the extracted data
        #################TO BE IMPLEMENTED#############

        # Log the successful update of the author details
        logging.info(f"Successfully updated details for author with ID {author_id}")

        # Return a success response
        return jsonify({"message": "Author details updated successfully"}), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error updating details for author {author_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while updating author details"}) , 500


@administration.route('/authors/{author_id}', methods = ["DELETE"])
def delete_author(author_id):
    """Delete an author"""
    try:
        # Retrieve the specific author from the database
        author = Author.query.get(author_id)

        if not author:
            # Log that the author with the specified author_id was not found
            logging.warning(f"Author with authorId {author_id} not found")

            # Return a not found response
            return jsonify({"error": "Author not found"}), 404

        # Remove author
        author.remove()

        # Log the successful deletion of author record
        logging.info(f"Successfully deleted details for author with ID {author_id}")

        # Return a success response
        return jsonify({"message": "Author details deleted successfully"}), 200

    except Exception as e:
        # Log any errors that occur during deletion of author record 
        logging.error(f"Error deleting details for author {author_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while deleting author details"}) , 500


#------------------------------------------------------------------------------
#                               BOOK MANAGEMENT
#------------------------------------------------------------------------------
@administration.route('/books', methods = ["GET"])
def get_books():
    """Gets list of all books"""
    try:
        # Fetch all books from the database
        books = Book.query.all()

        # Log the successful retrieval of books
        logging.info("Books fetched successfully")

        # Retrieve details in jsonfiable format
        books = [{book.bookId: book.getDetails()} for book in books]

        # Return the books as a JSON response
        return jsonify({"books": books}), 200

    except Exception as e:
        # Log any errors that occur during fetching of books 
        logging.error(f"Error fetching books: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching books"}) , 500


@administration.route('/books/<int:book_id>', methods = ["GET"])
def get_book(book_id):
    """Gets details of a specific book"""
    try:
        book = Book.query.get(book_id)
        if book:
            logging.info(f"Details fetched successfully for book with bookId {book_id}")
            return jsonify(book.getDetails()), 200

        else:
            # Log that the book with the specified book_id was not found
            logging.warning(f"Book with bookId {book_id} not found")

            return jsonify({"error": "Book not found"}), 404

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error fetching book details: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching book details"}) , 500


@administration.route('/books/search', methods = ["GET"])
def search_books():
    """Gets books fitting query string"""
    try:
        # Get the search query from the request parameters
        search_query = flask.request.args.get('1', '')

        # Perform a case-insensitive search on the title, publisher and summary 
        # columns
        books = Book.query.filter(or_(
            Book.title.ilike(f"%{search_query}%"),
            Book.publisher.ilike(f"%{search_query}%"),
            Book.summary.ilike(f"%{search_query}%")
            )).all()

        # Log the successful book search
        logging.info(f"Books searched successfully with query: {search_query}")

        # Get jsonifiable book details
        books_list = [book.getDetails() for book in books]

        # Return the search results as a JSON response
        return jsonify({"books": books_list}), 200

    except Exception as e:
        # Log any errors that occur during book search
        logging.error(f"Error searching books: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while searching books"}) , 500


@administration.route('/books/<int:book_id>/categories', methods = ["GET"])
def get_book_categories(book_id):
    """Get categories of a particular book"""
    try:
        # Retrieve the specific book from the database
        book = Book.query.get(book_id)

        if not book:
            # Log that the book with the specified book_id was not found
            logging.warning(f"Book with bookId {book_id} not found")

            # Return a not found response
            return jsonify({"error": "Book not found"}), 404

        # Get categorys of the book
        categories = [{category.categoryId: category.getDetails()} 
                for category in book.categories]

        # Return the categories as a JSON response
        return jsonify({"book_categories": categories}), 200


    except Exception as e:
        # Log any errors that occur during retrieval of book categories
        logging.error(f"Error retrieving categories for book {book_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving categories"}) , 500


@administration.route('/books/<int:book_id>/authors', methods = ["GET"])
def get_book_authors(book_id):
    """Get authors of a particular book"""
    try:
        # Retrieve the specific book from the database
        book = Book.query.get(book_id)

        if not book:
            # Log that the book with the specified book_id was not found
            logging.warning(f"Book with bookId {book_id} not found")

            # Return a not found response
            return jsonify({"error": "Book not found"}), 404

        # Get authors of the book
        authors = [{author.authorId: author.getDetails()} 
                for author in book.authors]

        # Return the authors as a JSON response
        return jsonify({"book_authors": authors}), 200


    except Exception as e:
        # Log any errors that occur during deletion of book record 
        logging.error(f"Error retrieving authors for book {book_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving authors"}) , 500


@administration.route('/books/<int:book_id>/upload-image', methods = ["POST"])
def upload_book_image(book_id):
    """Uploads book cover image"""
    try:
        book = Book.query.get(book_id)

        if not book:
            # Log that the book with the specified book_id was not found
            logging.warning(f"Book with bookId {book_id} not found")

            # Return a not found response
            return jsonify({"error": "Book not found"}), 404

        # Check if the request contains a file
        if 'file' not in flask.request.files:
            return jsonify({"error": "No file provided"}), 400

        file = flask.request.files['file']

        if not book.uploadImage(file, 
                flask.current_app.config["BOOK_IMAGES_UPLOAD_PATH"]):
            # Log the invalid file was provided
            logging.warning("Invalid file provided for image upload")

            # Return an error response for the invalid file
            return jsonify({"error": "Invalid file type. Allowed types: png, jpg, jpeg, gif"}), 400

        # Log the successful image upload
        logging.info(f"Image uploaded successfully for book with bookId {book_id}")
            
        # Return a success response
        return jsonify({"message": "Image uploaded successfully"}), 200

    except Exception as e:
        # Log any errors that occur during image upload 
        logging.error(f"Error uploading book image: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while uploading book image"}) , 500


@administration.route('/books/<int:book_id>/upload-images', methods = ["POST"])
def upload_book_images(book_id):
    """Uploads book images"""
    try:
        pass
    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error ...: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while ..."}) , 500


@administration.route('/books', methods = ["POST"])
def add_book():
    """Adds a book"""
    try:
        # Get book details from the request JSON
        data = flask.request.json

        # Check if required fields are present in the request
        required_fields = ["title", "summary", "publisher", "yearPublished", 
                "edition"]
        if not all (field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new book instance with the provided details
        book = Book.add(data)
        if book:
            # Log the successful creation of a new book
            logging.info(f"Successfully added a new book with ID: {book.bookId}")

            # Return a success message
            return jsonify({"message": "Book added successfully"}), 200

    except Exception as e:
        # Log any errors that occur during adding of the book 
        logging.error(f"Error creating the book: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while creating the book"}) , 500


@administration.route('/books/<int:book_id>', methods = ["PUT"])
def update_book(book_id):
    """Updates details of a book"""
    try:
        # Retrieve the specific book from the database
        book = Book.query.get(book_id)

        if not book:
            # Log that the book with the specified book_id was not found
            logging.warning(f"Book with bookId {book_id} not found")

            # Return a not found response
            return jsonify({"error": "Book not found"}), 404

        # Extract data from the request JSON
        data = flask.request.json

        # Confirm all values are present
        #################TO BE IMPLEMENTED#############
        
        # Update book details with the extracted data
        #################TO BE IMPLEMENTED#############

        # Log the successful update of the book details
        logging.info(f"Successfully updated details for book with ID {book_id}")

        # Return a success response
        return jsonify({"message": "Book details updated successfully"}), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error updating details for book {book_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while updating book details"}) , 500


@administration.route('/books/<int:book_id>', methods = ["DELETE"])
def delete_book(book_id):
    """Deletes a book"""
    try:
        # Retrieve the specific book from the database
        book = Book.query.get(book_id)

        if not book:
            # Log that the book with the specified book_id was not found
            logging.warning(f"Book with bookId {book_id} not found")

            # Return a not found response
            return jsonify({"error": "Book not found"}), 404

        # Remove book
        book.remove()

        # Log the successful deletion of book record
        logging.info(f"Successfully deleted details for book with ID {book_id}")

        # Return a success response
        return jsonify({"message": "Book details deleted successfully"}), 200

    except Exception as e:
        # Log any errors that occur during deletion of book record 
        logging.error(f"Error deleting details for book {book_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while deleting book details"}) , 500


#------------------------------------------------------------------------------
#                               TICKET MANAGEMENT
#------------------------------------------------------------------------------
@administration.route('/tickets/<int:ticket_id>', methods = ["GET"])
def get_ticket(ticket_id):
    """Get details of a specific ticket"""
    try:
        # Retrieve the specific ticket from the database
        ticket = Ticket.query.get(ticket_id)

        if not ticket:
            # Log that the ticket with the specified ticket_id was not found
            logging.warning(f"Ticket with ticketId {ticket_id} not found")

            # Return a not found response
            return jsonify({"error": "Ticket not found"}), 404

        # Log the successful retrieval of ticket details
        logging.info(f"Successfully retrieved details for ticket with ticketId {ticket_id}")

        return jsonify(ticket.getDetails()), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error retrieving details for ticket {ticket_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving ticket details"}) , 500


@administration.route('/tickets/<int:ticket_id>/cancel', methods = ["POST"])
def cancel_ticket(ticket_id):
    """Cancels a ticket"""
    try:
        pass
    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error ...: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while ..."}) , 500


@administration.route('/tickets/<int:ticket_id>/validate', methods = ["GET"])
def validate_ticket(ticket_id):
    """Checks if a ticket is valid"""
    try:
        # Retrieve the specific ticket from the database
        ticket = Ticket.query.get(ticket_id)

        if not ticket:
            # Log that the ticket with the specified ticket_id was not found
            logging.warning(f"Ticket with ticketId {ticket_id} not found")

            # Return a not found response
            return jsonify({"error": "Ticket not found"}), 404

        # Check if the ticket is cancelled
        if ticket.isCancelled:
            # Log that the ticket is cancelled
            logging.warning(f"Attempted to validate a cancelled ticket with ticketId {ticket_id}")

            # Return a conflicting response
            return jsonify({"error": "Ticket is cancelled and cannot be validated"}), 409
        
        # Check if the ticket is valid
        if ticket.isValid():
            # Log that the ticket is a valid ticket
            logging.info(f"Ticket with ticketId {ticket_id} is a valid ticket")

            # Return a success response indicating the ticket is valid
            return jsonify({"message": "Ticket is valid"}), 200

        # Log that the ticket is not valid
        logging.warning(f"Ticket with ticketId {ticket_id} is not valid")

        # Return error response
        return jsonify({"error": "Ticket is invalid"}), 400

    except Exception as e:
        # Log any errors that occur during the validation of the ticket
        logging.error(f"Error validating ticket {ticket_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while validating the ticket"}) , 500


#------------------------------------------------------------------------------
#                               ROLE MANAGEMENT
#------------------------------------------------------------------------------
@administration.route('/roles', methods = ["GET"])
def get_roles():
    """Get list of all roles"""
    try:
        # Fetch all roles from the database
        roles = Role.query.all()

        # Log the successful retrieval of roles
        logging.info("Roles fetched successfully")

        # Retrieve details in jsonfiable format
        roles = [{role.roleId: role.getDetails()} for role in roles]

        # Return the roles as a JSON response
        return jsonify({"roles": roles}), 200

    except Exception as e:
        # Log any errors that occur during fetching roles
        logging.error(f"Error fetching roles: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching roles"}) , 500


@administration.route('/roles/<int:role_id>', methods = ["GET"])
def get_role(role_id):
    """Gets details of a specific role"""
    try:
        role = Role.query.get(role_id)
        if role:
            logging.info(f"Details fetched successfully for role with roleId {role_id}")
            return jsonify(role.getDetails()), 200

        else:
            # Log that the role with the specified role_id was not found
            logging.warning(f"Role with roleId {role_id} not found")

            return jsonify({"error": "Role not found"}), 404
        
    except Exception as e:
        # Log any errors that occur during role details retrieval
        logging.error(f"Error fetching role details: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching role details"}) , 500


@administration.route('/roles', methods = ["POST"])
def add_role():
    """Creates a new role"""
    try:
        # Get role details from the request JSON
        data = flask.request.json

        # Check if required fields are present in the request
        required_fields = ["title", "description"]

        if not all (field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new role instance with the provided details
        role = Role.add(data)
        if role:
            # Log the successful creation of a new role
            logging.info(f"Successfully added a new role with ID: {role.roleId}")

            # Return a success message
            return jsonify({"message": "Role added successfully"}), 200

    except Exception as e:
        # Log any errors that occur during adding of the role 
        logging.error(f"Error creating the role: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while creating the role"}) , 500


@administration.route('/roles/<int:role_id>', methods = ["PUT"])
def update_role(role_id):
    """Updates details of a role"""
    try:
        # Retrieve the specific role from the database
        role = Role.query.get(role_id)

        if not role:
            # Log that the role with the specified role_id was not found
            logging.warning(f"Role with roleId {role_id} not found")

            # Return a not found response
            return jsonify({"error": "Role not found"}), 404

        # Extract data from the request JSON
        data = flask.request.json

        # Confirm all values are present
        #################TO BE IMPLEMENTED#############
        
        # Update role details with the extracted data
        #################TO BE IMPLEMENTED#############

        # Log the successful update of the role details
        logging.info(f"Successfully updated details for role with ID {role_id}")

        # Return a success response
        return jsonify({"message": "Role details updated successfully"}), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error updating details for role {role_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while updating role details"}) , 500


@administration.route('/roles/<int:role_id>', methods = ["DELETE"])
def delete_role(role_id): 
    """Deletes a role"""
    try:
        # Retrieve the specific role from the database
        role = Role.query.get(role_id)

        if not role:
            # Log that the role with the specified role_id was not found
            logging.warning(f"Role with roleId {role_id} not found")

            # Return a not found response
            return jsonify({"error": "Role not found"}), 404

        # Remove role
        role.remove()

        # Log the successful deletion of role record
        logging.info(f"Successfully deleted details for role with ID {role_id}")

        # Return a success response
        return jsonify({"message": "Role details deleted successfully"}), 200

    except Exception as e:
        # Log any errors that occur during deletion of role record 
        logging.error(f"Error deleting details for role {role_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while deleting role details"}) , 500


@administration.route('/roles/<int:role_id>/users', methods = ["GET"])
@login_required
def get_role_users(role_id):
    """Gets list of all users with the given role"""
    try:
        # Log the user ID for the request
        logging.info(f"User with ID {current_user.userId} requested details for multiple users with role Id {role_id}")

        # Checking if the current user has permission to view user details
        if current_user.can(Permission.VISIT):
            logging.warning(f"Unauthorized attempt by user with ID {current_user.userId} to view multiple user details")
            return flask.jsonify({"error": "Unauthorized"}), 403

        # Fetch Role details from the database
        role = Role.query.get(role_id)
        users = [user.getDetails() for user in role.users]

        if users:
            # Log successful user details retrieval
            logging.info(f"Multiple User details with role Id {role_id} retrieved successfully by user with ID {current_user.userId}")

            # Return user details as JSON
            return flask.jsonify({"users": users}), 200
    
        else:
            # Log unsuccessful user details retrieval
            logging.warning(f"User details found in the database")

            return flask.jsonify({"error": "Users not found"}), 404

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error fetching multiple user details: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching multiple user details"}) , 500



#------------------------------------------------------------------------------
#                            NOTIFICATION MANAGEMENT
#------------------------------------------------------------------------------
@administration.route('/notifications/<int:notification_id>', methods = ["GET"])
def get_notification():
    """Gets details of a particular notification"""
    try:
        # Fetch all notifications from the database
        notifications = Notification.query.all()

        # Log the successful retrieval of notifications
        logging.info("Notifications fetched successfully")

        # Retrieve details in jsonfiable format
        notifications = [{notification.notificationId: notification.getDetails()} 
                for notification in notifications]

        # Return the notifications as a JSON response
        return jsonify({"notifications": notifications}), 200

    except Exception as e:
        # Log any errors that occur during fetching of notifications 
        logging.error(f"Error fetching notifications: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching notifications"}) , 500


#------------------------------------------------------------------------------
#                            CATEGORY MANAGEMENT
#------------------------------------------------------------------------------
@administration.route('/categories', methods = ["GET"])
def get_categories():
    """Get list of all categories"""
    try:
        # Fetch all categories from the database
        categories = Category.query.all()

        # Log the successful retrieval of categories
        logging.info("Categories fetched successfully")

        # Retrieve details in jsonfiable format
        categories = [{category.categoryId: category.getDetails()} for category in categories]

        # Return the categories as a JSON response
        return jsonify({"categories": categories}), 200

    except Exception as e:
        # Log any errors that occur during fetching categories
        logging.error(f"Error fetching categories: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching categories"}) , 500


@administration.route('/categories/<int:category_id>', methods = ["GET"])
def get_category(category_id):
    """Gets details of a specific category"""
    try:
        category = Category.query.get(category_id)
        if category:
            logging.info(f"Details fetched successfully for category with categoryId {category_id}")
            return jsonify(category.getDetails()), 200

        else:
            # Log that the category with the specified category_id was not found
            logging.warning(f"Category with categoryId {category_id} not found")

            return jsonify({"error": "Category not found"}), 404
        
    except Exception as e:
        # Log any errors that occur during category details retrieval
        logging.error(f"Error fetching category details: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while fetching category details"}) , 500


@administration.route('/categories', methods = ["POST"])
def add_category():
    """Creates a new category"""
    try:
        # Get category details from the request JSON
        data = flask.request.json

        # Check if required fields are present in the request
        required_fields = ["name", "description"]

        if not all (field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new category instance with the provided details
        category = Category.create(data)
        if category:
            # Log the successful creation of a new category
            logging.info(f"Successfully added a new category with ID: {category.categoryId}")

            # Return a success message
            return jsonify({"message": "Category added successfully"}), 200

    except Exception as e:
        # Log any errors that occur during adding of the category 
        logging.error(f"Error creating the category: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while creating the category"}) , 500


@administration.route('/categories/<int:category_id>', methods = ["PUT"])
def update_category(category_id):
    """Updates details of a category"""
    try:
        # Retrieve the specific category from the database
        category = Category.query.get(category_id)

        if not category:
            # Log that the category with the specified category_id was not found
            logging.warning(f"Category with categoryId {category_id} not found")

            # Return a not found response
            return jsonify({"error": "Category not found"}), 404

        # Extract data from the request JSON
        data = flask.request.json

        # Confirm all values are present
        #################TO BE IMPLEMENTED#############
        
        # Update category details with the extracted data
        #################TO BE IMPLEMENTED#############

        # Log the successful update of the category details
        logging.info(f"Successfully updated details for category with ID {category_id}")

        # Return a success response
        return jsonify({"message": "Category details updated successfully"}), 200

    except Exception as e:
        # Log any errors that occur during 
        logging.error(f"Error updating details for category {category_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while updating category details"}) , 500


@administration.route('/categories/<int:category_id>', methods = ["DELETE"])
def delete_category(category_id): 
    """Deletes a category"""
    try:
        # Retrieve the specific category from the database
        category = Category.query.get(category_id)

        if not category:
            # Log that the category with the specified category_id was not found
            logging.warning(f"Category with categoryId {category_id} not found")

            # Return a not found response
            return jsonify({"error": "Category not found"}), 404

        # Remove category
        category.remove()

        # Log the successful deletion of category record
        logging.info(f"Successfully deleted details for category with ID {category_id}")

        # Return a success response
        return jsonify({"message": "Category details deleted successfully"}), 200

    except Exception as e:
        # Log any errors that occur during deletion of category record 
        logging.error(f"Error deleting details for category {category_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while deleting category details"}) , 500


@administration.route('/categories/<int:category_id>/books', methods = ["GET"])
def get_category_books(category_id):
    """Get books of a particular category"""
    try:
        # Retrieve the specific category from the database
        category = Category.query.get(category_id)

        if not category:
            # Log that the category with the specified category_id was not found
            logging.warning(f"Category with categoryId {category_id} not found")

            # Return a not found response
            return jsonify({"error": "Category not found"}), 404

        # Get books of the category
        books = [{book.bookId: book.getDetails()} 
                for book in category.books]

        # Return the books as a JSON response
        return jsonify({"category_books": books}), 200


    except Exception as e:
        # Log any errors that occur during retrieval of category books
        logging.error(f"Error retrieving books for category {category_id}: {str(e)}")

        # Return an error response
        return jsonify({"error": "An error occurred while retrieving books"}) , 500
