import logging
import random
import flask
from flask import url_for
from datetime import datetime
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db, login_manager
from utilities.file_saver import save_image, is_allowed_file
from utilities.securities import get_gravatar_hash

# Configure logging
logging.basicConfig(filename = 'app.log', level = logging.INFO)


class Permission:
    VISIT = 1
    MEMBER = 2
    ADMIN = 8


class Code:
    SUCCESS = 200
    NOT_FOUND = 404
    FORBIDDEN = 403
    FAILURE = 400


class Status:
    def __init__(self, code, message, info = None, **kwargs):
        self.code = code
        self.message = message
        self.info = info


    def __repr__(self):
        return f"<Status(code = {self.code}, message = {self.message}, info = {self.info})>"

@login_manager.user_loader
def load_user(user_id):
    """
    Queries the database for a record of currently logged in user
    Returns User object containing info about logged in user
    """
    return User.query.get(int(user_id))


class Anonymous_User(flask_login.AnonymousUserMixin):
    def can(self, permission):
        return False


    def is_administrator(self):
        return False


login_manager.anonymous_user = Anonymous_User


class User(flask_login.UserMixin, db.Model):
    """Represents a user in the system"""
    __tablename__ = 'users'

    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    gender = db.Column(db.String(10), default='FEMALE')
    imageUrl = db.Column(db.String(255))
    emailAddress = db.Column(db.String(128), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=False)
    nationality = db.Column(db.String(60), default='Kenya')
    passwordHash = db.Column(db.String(255), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    isSuspended = db.Column(db.Boolean, default=False)
    isConfirmed = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(255))
    tokenExpiration = db.Column(db.DateTime)
    accountBalance = db.Column(db.Float, default=0, nullable=False,
            server_default="0")
    lastMessageReadTime = db.Column(db.DateTime, default=datetime.utcnow)
    lastSeen = db.Column(db.DateTime, default=datetime.utcnow)
    avatarHash = db.Column(db.String(32))
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow,
            onupdate=datetime.utcnow)

    roleId = db.Column(db.Integer, db.ForeignKey('roles.roleId'))

    tasks = db.relationship('Task', backref = 'owner', lazy = 'dynamic')
    notifications = db.relationship('Notification', backref = 'owner',
            lazy = 'dynamic')
    tickets = db.relationship('Ticket', backref = 'owner', lazy = 'dynamic')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # Assign default role to user
        if self.roleId is None:
            if self.emailAddress==flask.current_app.config["ADMINISTRATOR_EMAIL"]:
                role = Role.query.filter_by(name = "Administrator").first()

            else:
                role = Role.query.filter_by(default = True).first()

            # initialize roleId
            self.roleId = role.roleId

        # Generate avatar hash
        if self.emailAddress is not None and self.avatarHash is None:
            self.avatarHash = get_gravatar_hash(self.emailAddress)


    def __repr__(self):
        """Retrieves a string representation of the User object"""
        return f"<User(userId={self.userId}, firstName={self.firstName}, lastName={self.lastName})>"


    def get_id(self):
        """
        Inherited UserMixin class method used to retrieve user id by flask_login
        """
        return self.userId


    @staticmethod
    def register(details = {}):
        """Registers a new user"""
        # Create a new user
        user = User(
                firstName = details.get('firstName'),
                middleName= details.get('middleName'),
                lastName = details.get('lastName'),
                gender = details.get('gender'),
                password = details.get('password'),
                phoneNumber = details.get('phoneNumber'),
                nationality = details.get('nationality'),
                emailAddress = details.get('emailAddress')
                )

        # Add the new user to the database
        db.session.add(user)
        db.session.commit()

        return user


    def confirm(self):
        serializer = Serializer(flask.current_app.config["SECRET_KEY"])

        try:
            data = serializer.loads(token.encode("utf-8"))

        except Exception as e:
            logging.error(f"An error occured while loading the token: {str(e)}")
            return False

        if data.get("confirm" != self.userId):
            return False

        self.confirmed = True
        db.session.add(self)
        return True


    def login(self, password):
        """"Authenticates user login"""
        if self.verifyPassword(password):
            flask_login.login_user(self)
            return Status(Code.SUCCESS, "Login successful")

        return Status(Code.FAILURE, "Passwords do not match")


    def logout(self):
        """Handles user logout"""
        flask_login.logout_user()
        return Status(Code.SUCCESS, "Logout successful")


    def updateDetails(self, details):
        """Updates user details"""

        db.session.add(self)

        return self


    def getToken(self, expiration):
        """Returns token and generates if not available"""
        pass


    def revokeToken(self):
        """Revoke's user token"""
        self.token


    def checkToken(self, token):
        """Check the validility of a token"""
        pass


    def purchaseTicket(self):
        """Initiailizes ticket for a raffle"""
        pass


    def cancelTicket(self):
        """Cancels a purchased ticket"""
        pass


    def getPurchasedTicket(self):
        """Retrieves purchased tickets"""
        pass


    def getDetails(self):
        """Retrieve user details"""
        return {
                "userId": self.userId,
                "firstName": self.firstName,
                "middleName": self.middleName,
                "lastName": self.lastName,
                "gender": self.gender,
                "emailAddress": self.emailAddress,
                "phoneNumber": self.phoneNumber,
                "nationality": self.nationality,
                "dateCreated": self.dateCreated,
                "lastUpdated": self.lastUpdated,
                "isSuspended": self.isSuspended,
                "isActive": self.isActive,
                "isConfirmed": self.isConfirmed,
                "rafflesWon": len(self.getWonRaffles()),
                "pastRaffles": len(self.getPastRaffles()),
                "activeRaffles": len(self.getPendingRaffles()),
                "notifications": self.notifications.count(),
                "tasks": self.tasks.count(),
                "accountBalance": self.accountBalance,
                "avatarUrl": self.getGravatar(255),
                "uploadProfileImageUrl": url_for(
                    "administration.upload_user_image",
                    user_id = self.userId, _external = True),
                "tasksUrl": url_for("administration.get_user_tasks",
                    user_id = self.userId, _external = True),
                "notificationsUrl":url_for("administration.get_user_notifications",
                    user_id = self.userId, _external = True),
                "ticketsUrl": url_for("administration.get_user_tickets",
                    user_id = self.userId, _external = True),
                "imageUrl": url_for("static", filename = "images/profiles/" + 
                    self.imageUrl, _external = True) if self.imageUrl else self.getGravatar(255),
                "deleteUserUrl": url_for("administration.delete_user",
                    user_id = self.userId, _external = True),
                "updateUserUrl": url_for("administration.update_user",
                    user_id = self.userId, _external = True),
                "url": url_for("administration.get_user",
                    user_id = self.userId, _external = True),
                }


    def getWonRaffles(self):
        """Retrieve raffles won by the user"""
        return [ticket.getRaffle for ticket in self.tickets 
                if ticket.isWinningTicket]


    def getPastRaffles(self):
        """Retrieve completed raffles participated by the user"""
        return [ticket.getRaffle for ticket in self.tickets 
                if not ticket.getRaffle.isOngoing()]


    def getPendingRaffles(self):
        """Retrieve ongoing raffles for the user"""
        return [ticket.getRaffle for ticket in self.tickets 
                if ticket.getRaffle.isOngoing()]


    def addNotification(self, name, data):
        """Add a notification for the user"""
        self.notifications.filter_by(name = name).delete()

        details = {"name": name, "userId": self.userId}
        notification = Notification.add(details)
        notification.payloadJSON = json.dumps(data)

        db.session.add(notification)
        return notification


    def launchTask(self, name, description):
        """Initiate a background task"""
        pass


    def getTasksInProgress(self):
        """Retrieve tasks in progress"""
        pass


    def getTaskInProgress(self, name):
        """Retrieve details of a specific task in progress"""
        pass


    @property
    def password(self):
        """Establishes password not publicly accessible"""
        raise AttributeError('password is not a readable attribute')


    @password.setter
    def password(self, password):
        """Hashes password"""
        self.passwordHash = generate_password_hash(password)


    def verifyPassword(self, password):
        """Verifies a user's password"""
        return check_password_hash(self.passwordHash, password)


    @staticmethod
    def resetPassword(token, new_password):
        """Resets the user's password"""
        serializer = Serializer(flask.current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token.encode("utf-8"))
        except Exception as e:
            logging.error(f"An error occurred while validating the token: { str(e) }")
            return False

        user = User.query.get(data.get('reset'))
        if user is None:
            logging.error("Password reset attempted for unknown user")
            return False

        user.password = new_password
        db.session.add(user)

        logging.info(f"Password reset successful for user with ID: {user.userId}")
        return True


    def generate_confirmation_token(self):
        serializer = Serializer(flask.current_app.config["SECRET_KEY"], 'confirm')
        return serializer.dumps(self.userId)


    @staticmethod
    def verify_reset_credential_token(token):
        try:
            user_id = jwt.decode(token, flask.current_app.config["SECRET_KEY"],
                    algorithms = ["HS256"])['reset_credential']
        except Exception as e:
            logging.error(f"An error occured while verifying reset credential token: {str(e)}")
            return

        # Return retrieved user
        return User.query.get(user_id)


    def ping(self):
        self.lastSeen = datetime.utcnow()
        db.session.add(self)


    def resetEmailAddress(self, token, email_address):
        """Resets the user's email address"""

        serializer = Serializer(flask.current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token.encode("utf-8"))
        except Exception as e:
            logging.error(f"An error occurred while validating the token: { str(e) }")
            return False
        new_email = data.get("new_email")
        if new_email is None:
            logging.error(f"New email was not provided by user with ID {self.userId}")
            return False

        self.emailAddress = new_email
        self.avatarHash = self.gravatar_hash()


    def resetPhoneNumber(self, token, phone_number):
        """Resets the user's phone number"""
        serializer = Serializer(flask.current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token.encode("utf-8"))
        except Exception as e:
            logging.error(f"An error occurred while validating the token: { str(e) }")
            return False


    def can(self, permission):
        """Checks whether a user has a specific permission"""
        pass


    def isAdministrator(self):
        """Checks if the user has administrator privileges"""
        pass


    def deactivate(self):
        """Deactivates a user's account"""
        pass


    def activate(self):
        """Activates a user's account"""
        pass


    def suspend(self):
        """Suspends a user's account"""
        pass


    def updateProfileImage(self, image, folder):
        """Updates the user's profile image"""
        if not is_allowed_file(image):
            return "Invalid Image", 400

        # Save image on file system
        image_url = save_image(image, folder)

        # Save filename in database
        self.imageUrl = image.filename
        db.session.commit()

        return self


    def getGravatar(self, size = 100, default = 'identicon', rating = 'g'):
        """Generates a Gravatar URL for the user"""
        url = 'https://secure.gravatar.com/avatar'

        # Generate avatar hash if it does not exist
        if not self.avatarHash:
            self.avatarHash = get_gravatar_hash(self.emailAddress)

        # Retrieve it for usage
        hash = self.avatarHash
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(url = url,
                hash = hash, size = size, default = default, rating = rating)



class Role(db.Model):
    """Represents a role in the system"""
    __tablename__ = 'roles'

    roleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(32), nullable=False)
    description = db.Column(db.Text)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer, default=0)

    users = db.relationship('User', backref = 'role_users', lazy = 'dynamic')


    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0


    @staticmethod
    def add(details = {}):
        """Creates a new role"""
        role = Role(
                title = details.get("title"),
                description = details.get("description")
                )

        db.session.add(role)
        db.session.commit()

        return role


    def updateDetails(self, details = {}):
        """Updated role details"""
        self.title = details.get("title")
        self.description = details.get("description")

        db.session.add(self)
        return self


    @staticmethod
    def insert_roles():
        """Static method to insert predefined roles"""
        roles = {
                'Guest' : [Permission.VISIT],
                'Member' : [Permission.VISIT, Permission.MEMBER],
                'Administrator' : [Permission.VISIT, Permission.MEMBER,
                    Permission.ADMIN]
                }

        default_role = 'Guest'

        for r in roles:
            role = Role.query.filter_by(title = r).first()
            if role is None:
                role = Role(title = r)

            role.resetPermissions()
            for perm in roles[r]:
                role.addPermission(perm)

            role.default = (role.title == default_role)
            db.session.add(role)
        db.session.commit()


    def addPermission(self, permission):
        """Adds a permission to the role"""
        if not self.hasPermission(permission):
            self.permissions += permission


    def removePermission(self, permission):
        """Remove a permission from the role"""
        if self.hasPermission(permission):
            self.permissions -= permission


    def resetPermissions(self):
        """Resets all permissions for the role"""
        self.permissions = 0


    def hasPermission(self, permission):
        """Checks if the role has a specific permission"""
        return self.permissions & permission == permission


    def getDetails(self):
        """Retrieves role details"""
        details = {
                "roleId": self.roleId,
                "title": self.title,
                "description": self.description,
                "permissions": self.permissions,
                "isDefault": self.default,
                "usersCount": self.users.count(),
                "deleteRoleUrl": url_for("administration.delete_role",
                    role_id = self.roleId, _external = True),
                "updateRoleUrl": url_for("administration.update_role",
                    role_id = self.roleId, _external = True),
                "usersUrl": url_for("administration.get_role_users",
                    role_id = self.roleId, _external = True),
                "url": url_for("administration.get_role",
                    role_id = self.roleId, _external = True),
                }
        return details


    def __repr__(self):
        """Retrieves a string representation of the Role object"""
        return f"<Role(roleId={self.roleId}, title={self.title})>"



class Book(db.Model):
    """Represents a book in the system"""
    __tablename__ = 'books'

    __searchable__ = ['title', 'publisher', 'yearPublished', 'summary', 'edition']

    bookId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    summary = db.Column(db.Text)
    publisher = db.Column(db.String(255), nullable=False)
    yearPublished = db.Column(db.Integer, nullable=False)
    edition = db.Column(db.Integer, nullable=False, server_default="1")
    imageUrl = db.Column(db.String(255))
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow,
            onupdate=datetime.utcnow)
    isSuspended = db.Column(db.Boolean, default = False)
    isActive = db.Column(db.Boolean, default = True)

    raffles = db.relationship('Raffle', backref = 'book', lazy = 'dynamic')
    
    @property
    def authors(self):
        """Retrieves all authors of the book"""
        authors = Author.query.join(AuthorBook, AuthorBook.authorId == Author.authorId)\
                .join(Book, Book.bookId == self.bookId).all()
        return authors


    @property
    def categories(self):
        """Retrieves all categories this book falls under"""
        categories = Category.query.join(CategoryBook, CategoryBook.categoryId == Category.categoryId)\
                .join(Book, Book.bookId == self.bookId).all()
        return categories


    def __repr__(self):
        """Retrieves a string representation of the Book object"""
        return f"<Book(bookId={self.bookId}, title={self.title})>"

    @staticmethod
    def add(details = {}):
        """Adds a new book"""
        book = Book(
                title = details.get("title"),
                summary = details.get("summary"),
                publisher = details.get("publisher"),
                yearPublished = details.get("yearPublished"),
                edition = details.get("edition")
                )

        db.session.add(book)
        db.session.commit()

        return book


    def remove(self):
        """Removes a book"""
        pass


    def updateDetails(self, details = {}):
        """Updates book details"""
        self.title = details.get("title")
        self.summary = details.get("summary")
        self.publisher = details.get("publisher")
        self.yearPublished = details.get("yearPublished")
        self.edition = details.get("edition")

        db.session.add(self)

        return self


    def uploadImage(self, image, folder):
        """Uploads primary book image"""
        if not is_allowed_file(image):
            return "Invalid Image", 400

        # Change filename to match book ID
        filename = secure_filename(image.filename)
        image.filename = str(self.bookId) + "." + \
                filename.rsplit('.', 1)[1].lower()  

        # Save image on file system
        image_url = save_image(image, folder)

        # Save filename in database
        self.imageUrl = image.filename
        db.session.commit()

        return self


    def uploadImages(self, images, folder):
        """Uploads multiple book images"""
        for image in images:
            if not is_allowed_file(image):
                return "Invalid Image", 400

            # Save image on file system
            image_url = save_image(image, folder)
        return


    def deactivate(self):
        """Deactivates a book"""
        if self.isActive:
            self.isActive = False

        return self


    def activate(self):
        """Activates a book"""
        # Unsuspend the book
        if self.isSuspended:
            self.isSuspended = False

        # Activate the book
        if not self.isActive:
            self.isActive = True

        return self


    def suspend(self):
        """Suspends a book"""
        if not self.isSuspended:
            self.deactivate()
            self.isSuspended = True

        return self 


    def isRaffled(self):
        """Checks if a book is already raffled"""
        return self.raffles.count() > 0


    def isActive(self):
        """Checks if a book is active"""
        return self.isActive and not self.isSuspended


    def getDetails(self):
        """Retrieves book details"""
        return {
                "bookId": self.bookId,
                "title": self.title,
                "summary": self.summary,
                "publisher": self.publisher,
                "yearPublished": self.yearPublished,
                "edition": self.edition,
                "imageUrl": url_for("static", filename = "images/books/" + 
                    (self.imageUrl or "book.jpg"), 
                    _external = True),
                "dateCreated": self.dateCreated,
                "lastUpdated": self.lastUpdated,
                "isSuspended": self.isSuspended,
                "isActive": self.isActive(),
                "isRaffled": self.isRaffled(),
                "authorsCount": len(self.authors),
                "categoriesCount": len(self.categories),
                "uploadMultipleImagesUrl": url_for(
                    "administration.upload_book_images", 
                    book_id = self.bookId, _external = True),
                "uploadCoverImageUrl": url_for("administration.upload_book_image",
                    book_id = self.bookId, _external = True),
                "deleteBookUrl": url_for("administration.delete_book",
                    book_id = self.bookId, _external = True),
                "updateBookUrl": url_for("administration.update_book",
                    book_id = self.bookId, _external = True),
                "url": url_for("administration.get_book", book_id = self.bookId,
                    _external = True),
                "authorsUrl": url_for("administration.get_book_authors",
                    book_id = self.bookId, _external = True),
                "categoriesUrl": url_for("administration.get_book_categories", 
                    book_id = self.bookId, _external = True),
                }


class Author(db.Model):
    """Represents an author in the system"""
    __tablename__ = 'authors'

    authorId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50), nullable=False)
    middleName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))
    gender = db.Column(db.String(10), default='FEMALE')
    emailAddress = db.Column(db.String(128))
    phoneNumber = db.Column(db.String(20))
    imageUrl = db.Column(db.String(255))
    nationality = db.Column(db.String(60), default='Kenya')
    summary = db.Column(db.Text)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, 
            onupdate=datetime.utcnow)


    def __repr__(self):
        """Retrieves a string representation of the Author object"""
        return f"<Author(authorId={self.authorId}, firstName={self.firstName}, lastName={self.lastName})>"


    @property
    def books(self):
        """Retrieves all books by the author"""
        books = Book.query.join(AuthorBook, AuthorBook.bookId == Book.bookId)\
                .join(Author, Author.authorId == self.authorId).all()
        return books
    

    @staticmethod
    def add(details = {}):
        """Adds a new author"""
        author = Author(
                firstName = details.get("firstName"),
                middleName = details.get("middleName"),
                lastName = details.get("lastName"),
                emailAddress = details.get("emailAddress"),
                nationality = details.get("nationality"),
                summary = details.get("summary"),
                phoneNumber = details.get("phoneNumber"),
                gender = details.get("gender")
                )

        db.session.add(author)
        db.session.commit()

        return author


    def remove(self):
        """Removes an author"""
        pass


    def uploadImage(self, image, folder):
        """Uploads an author's image"""
        if not is_allowed_file(image):
            return "Invalid Image", 400

        # Save image on file system
        image_url = save_image(image, folder)

        # Save filename in database
        self.imageUrl = image.filename
        db.session.commit()

        return self


    def updateDetails(self, details):
        """Updates author details"""
        pass


    def getDetails(self):
        """Retrieve author details"""
        return {
                "authorId": self.authorId,
                "firstName": self.firstName,
                "middleName": self.middleName,
                "lastName": self.lastName,
                "gender": self.gender,
                "emailAddress": self.emailAddress,
                "phoneNumber": self.phoneNumber,
                "imageUrl": self.imageUrl,
                "nationality": self.nationality,
                "dateCreated": self.dateCreated,
                "lastUpdated": self.lastUpdated,
                "summary": self.summary,
                "booksCount": len(self.books),
                "booksUrl": url_for("administration.get_author_books", 
                    author_id = self.authorId, _external = True),
                "deleteAuthorUrl": url_for("administration.delete_author",
                    author_id = self.authorId, _external = True),
                "updateAuthorUrl": url_for("administration.update_author",
                    author_id = self.authorId, _external = True),
                "url": url_for("administration.get_author", 
                    author_id = self.authorId, _external = True),
                }


class Raffle(db.Model):
    """Represents a raffle in the system"""
    __tablename__ = 'raffles'

    raffleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    participantLimit = db.Column(db.Integer, nullable=False)
    startTime = db.Column(db.DateTime, default=datetime.utcnow)
    endTime = db.Column(db.DateTime)
    bookId = db.Column(db.Integer, db.ForeignKey('books.bookId'))
    isClosed = db.Column(db.Boolean, default=False)
    isActive = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, default=0, nullable=False, server_default="1")

    tickets = db.relationship('Ticket', backref = 'raffle', lazy = 'dynamic')


    def __repr__(self):
        """Retrieves a string representation of the Raffle object"""
        return f"<Raffle(raffleId={self.raffleId}, participantLimit={self.participantLimit})>"

    @property
    def getBook(self):
        """Returns instance of associated book"""
        return Book.query.get(self.bookId)


    @staticmethod
    def open(details = {}):
        """Creates a new raffle"""
        # Note: Raffle is inactive by default
        raffle = Raffle(
                participantLimit = details.get('participantLimit'),
                bookId = details.get('bookId'),
                price = details.get('price')
                )

        db.session.add(raffle)
        db.session.commit()

        return raffle


    def update(self, details):
        """Updates raffle details"""
        pass


    def close(self):
        """Closes a raffle"""
        # Draw raffle for winner
        self.getWinner()

        # Deactivate the raffle
        self.deactivate()

        # Close the raffle
        self.isClosed = True
        self.endTime = datetime.utcnow()

        db.session.add(self)
        db.sessioncommit()


    def getWinner(self):
        """Retrieves the winner of a raffle"""
        winner = Use
        return winner


    def activate(self):
        """Activates a raffle"""
        if self.isClosed:
            return "Cannot activate a closed raffle", 400

        if not self.isActive:
            self.isActive = True

        db.session.add(self)
        db.session.commit()
        return self


    def deactivate(self):
        """Deactivates a raffle"""
        if self.isClosed:
            return "Cannot deactivate a closed raffle", 400

        if self.isActive:
            self.Active = False

        db.session.add(self)
        db.session.commit()
        return self


    def isOngoing(self):
        """Checks if a raffle is ongoing"""
        return not self.isClosed and self.isActive


    def getDetails(self):
        """Retrieves raffle details"""
        return {
                "raffleId": self.raffleId,
                "participantLimit": self.participantLimit,
                "startTime": self.startTime,
                "endTime": self.endTime,
                "price": self.price,
                "bookId": self.bookId,
                "dateCreated": self.dateCreated,
                "lastUpdated": self.lastUpdated,
                "isClosed": self.isClosed,
                "isOngoing": self.isOngoing(),
                "ticketsPurchased": self.tickets.count(),
                "updateRaffleurl": url_for("administration.update_raffle",
                    raffle_id = self.raffleId, _external = True),
                "purchaseTicketUrl": url_for("administration.purchase_ticket",
                    raffle_id = self.raffleId, _external = True),
                "ticketsUrl": url_for("administration.get_raffle_tickets",
                    raffle_id = self.raffleId, _external = True),
                "closeRaffleUrl": url_for("administration.close_raffle",
                    raffle_id = self.raffleId, _external = True),
                "deactivateRaffleUrl": url_for("administration.deactivate_raffle",
                    raffle_id = self.raffleId, _external = True),
                "activateRaffleUrl": url_for("administration.activate_raffle",
                    raffle_id = self.raffleId, _external = True),
                "url": url_for("administration.get_raffle",
                    raffle_id = self.raffleId, _external = True),
                "bookDetails": self.getBook.getDetails()
                }



class Ticket(db.Model):
    """Represents a ticket in the system"""
    __tablename__ = 'tickets'

    ticketId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    raffleId = db.Column(db.Integer, db.ForeignKey('raffles.raffleId'))
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    isWinningTicket = db.Column(db.Boolean, default=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    uniqueNumber = db.Column(db.String, nullable=False)
    isCancelled = db.Column(db.Boolean, default=False)


    def __repr__(self):
        """Retrieves a string representation of the Ticket object"""
        return f"<Ticket(ticketId={self.ticketId}, raffleId={self.raffleId}, uniqueNumber={self.uniqueNumber})>"

    @property
    def getRaffle(self):
        """Returns an instance of the associated raffle"""
        return Raffle.query.get(self.raffleId)


    @staticmethod
    def create(details = {}):
        """Creates a new ticket"""
        ticket = Ticket(
                raffleId = details.get("raffleId"),
                userId = details.get("userId"),
                uniqueNumber = random.randrange(20231411, 20300000)
                )

        db.session.add(ticket)
        db.session.commit()

        return ticket


    def cancel(self):
        """Cancels a ticket"""
        pass


    def getDetails(self):
        """Retrieves ticket details"""
        return {
                "selfId": self.ticketId,
                "raffleId": self.raffleId,
                "isWinningTicket": self.hasWon(),
                "dateCreated": self.dateCreated,
                "lastUpdated": self.lastUpdated,
                "uniqueNumber": self.uniqueNumber,
                "isCancelled": self.isCancelled,
                "userId": self.userId,
                "validateTicketUrl": url_for("administration.validate_ticket",
                    ticket_id = self.ticketId, _external = True),
                "cancelTicketUrl": url_for("administration.cancel_ticket",
                    ticket_id = self.ticketId, _external = True),
                "url": url_for("administration.get_ticket",
                    ticket_id = self.ticketId, _external = True),
                }


    def isValid(self):
        """Checks if the ticket is valid"""
        pass


    def hasWon(self):
        """Checks if a ticket has won"""
        return ticket.isWinningTicket


    def declareWon(self):
        """Declares a ticket as won"""
        pass



class Notification(db.Model):
    """Represents a notification in the system"""
    __tablename__ = 'notifications'

    notificationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    payloadJSON = db.Column(db.Text)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(db.DateTime, default=datetime.utcnow,
            onupdate=datetime.utcnow)


    def __repr__(self):
        """Retrieves a string representation of the Notification object"""
        return f"<Notification(notificationId={self.notificationId}, content={self.content})>"


    @staticmethod
    def create(details = {}):
        """Creates a new notification"""
        notification = Notification(
                name = details.get('name'),
                userId = details.get('userId')
                )

        db.session.add(notification)
        db.session.commit()

        return notification


    def getDetails(self):
        """Retrieves notification details"""
        return {
                "notificationId": self.notificationId,
                "name": self.name,
                "payloadJSON": self.payloadJSON,
                "dateCreated": self.dateCreated,
                "lastUpdated": self.lastUpdated,
                "userId": self.userId,
                "userUrl": url_for("administration.get_user", 
                    user_id = self.userId, _external = True),
                "url": url_for("administration.get_notification", 
                    notification_id = self.notificationId, _external = True)
                }


    def getContent(self):
        """Retrieves notification content"""
        return self.content


    def getData(self):
        """Retrieves notification data"""
        return self.payloadJSON


    def updateDetails(self, details = {}):
        """Updates notification details"""
        self.content = details.get("content")
        self.payloadJSON = details.get("payloadJSON")

        db.session.add()
        db.session.commit()

        return self


class Task(db.Model):
    """Represents a task in the system"""
    __tablename__ = 'tasks'

    taskId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'))
    isComplete = db.Column(db.Boolean, default=False)


    def __repr__(self):
        """Retrieves a string representation of the Task object"""
        return f"<Task(taskId={self.taskId}, name={self.name})>"

    @staticmethod
    def create(details = {}):
        """Creates a new task"""
        pass


    def getRQJob(self):
        """Retrieves the RQ job associated with the task"""
        pass


    def getProgress(self):
        """Retrieves the progress of the task"""
        pass


    def getDetails(self):
        """Retrieves details of the task"""
        pass


class Category(db.Model):
    __tablename__ = 'categories'

    categoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)


    def __repr__(self):
        """Retrieves a string representation of the Category object"""
        return f"<Category(categoryId={self.categoryId}, name={self.name})>"
   

    @property
    def books(self):
        """Retrieves all books belonging to this category"""
        books = Book.query.join(CategoryBook, CategoryBook.bookId == Book.bookId)\
                .join(Category, Category.categoryId == self.categoryId).all()
        return books


    @staticmethod
    def create(details = {}):
        """Creates a new category"""
        category = Category(
                name = details.get("name"),
                description = details.get("description")
                )

        db.session.add(category)
        db.session.commit()

        return category


    def remove(self):
        """Removes an existing category"""
        pass


    def updateDetails(self, details = {}):
        """Updates details of the category"""
        self.name = details.get("name")
        self.category = details.get("category")

        db.session.add(self)
        db.session.commit()

        return self


    def getDetails(self):
        """Retrieve details of the Category"""
        return {
                "categoryId": self.categoryId,
                "name": self.name,
                "description": self.description,
                "booksCount": len(self.books),
                "deleteCategoryUrl": url_for("administration.delete_category",
                    category_id = self.categoryId, _external = True),
                "updateCategoryUrl": url_for("administration.update_category",
                    category_id = self.categoryId, _external = True),
                "url": url_for("administration.get_category", 
                    category_id = self.categoryId, _external = True),
                "booksUrl": url_for("administration.get_category_books", 
                    category_id = self.categoryId, _external = True),
                }


# Association Tables
class AuthorBook(db.Model):
    """Represents a relationship between a category and a book in the system"""
    __table_name_ = 'author_book',

    authorBookId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    authorId = db.Column(db.Integer, db.ForeignKey('authors.authorId'))
    bookId = db.Column(db.Integer, db.ForeignKey('books.bookId'))


    def __repr__(self):
        return f"<AuthorBook(authorBookId={self.authorBookId})>"


class CategoryBook(db.Model):
    """Represents a relationship between a category and a book in the system"""
    __tablename__ = 'category_book'

    categoryBookId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.categoryId'))
    bookId = db.Column(db.Integer, db.ForeignKey('books.bookId'))


    def __repr__(self):
        return f"<CategoryBook(categoryBookId={self.categoryBookId})>"
