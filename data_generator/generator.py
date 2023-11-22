import random
from faker import Faker
from datetime import datetime, timedelta
from app.models import db, User, Role, Book, Author, Raffle, Ticket, Notification, Task, Category, AuthorBook, CategoryBook

fake = Faker()

class DataGenerator:
    @classmethod
    def generate_users(cls, num_users=10):
        """Generate user records with random data."""
        for i in range(num_users):
            user_data = {
                    "firstName": fake.first_name(),
                    "middleName": fake.first_name(),
                    "lastName": fake.last_name(),
                    "gender": fake.random_element(elements=("male", "female")),
                    "emailAddress": fake.email(),
                    "phoneNumber": fake.phone_number(),
                    "nationality": fake.country(),
                    "password": fake.password(),
                    }

            User.register(details=user_data)
            print(f"User #{i} added successfully...")


    @classmethod
    def generate_books(cls, num_books=10):
        """Generate book records with random data."""
        for _ in range(num_books):
            book_data = {
                    "title": fake.catch_phrase(),
                    "summary": fake.paragraph(),
                    "publisher": fake.company(),
                    "yearPublished": fake.year(),
                    "edition": fake.random_int(min=1, max=5),
                    }

            Book.add(details=book_data)
            print(f"Book #{i} added successfully...")


    @classmethod
    def generate_authors(cls, num_authors=10):
        """Generate author records with random data."""
        for _ in range(num_authors):
            author_data = {
                    "firstName": fake.first_name(),
                    "middleName": fake.first_name(),
                    "lastName": fake.last_name(),
                    "gender": fake.random_element(elements=("male", "female")),
                    "emailAddress": fake.email(),
                    "phoneNumber": fake.phone_number(),
                    "nationality": fake.country(),
                    "summary": fake.paragraph(),
                    }

            Author.add(details=author_data)
            print(f"Author #{i} added successfully...")


    @classmethod
    def generate_raffles(cls, num_raffles=5):
        """Generate raffle records with random data."""
        books = Book.query.all()

        for _ in range(num_raffles):
            raffle_data = {
                    "participantLimit": fake.random_int(min=10, max=50),
                    "bookId": random.choice(books).bookId,
                    "price": fake.pyfloat(left_digits=3, right_digits=0),
                    }

            Raffle.open(details=raffle_data)
            print(f"Raffle #{i} added successfully...")


    @classmethod
    def generate_tickets(cls, num_tickets=20):
        """Generate ticket records with random data."""
        raffles = Raffle.query.all()
        users = User.query.all()

        for _ in range(num_tickets):
            ticket_data = {
                    "raffleId": random.choice(raffles).raffleId,
                    "userId": random.choice(users).userId,
                    }

            Ticket.create(details=ticket_data)
            print(f"Ticket #{i} added successfully...")


    @classmethod
    def generate_notifications(cls, num_notifications=10):
        """Generate notification records with random data."""
        users = User.query.all()

        for _ in range(num_notifications):
            notification_data = {
                    "name": fake.word(),
                    "userId": random.choice(users).userId,
                    }

            Notification.create(details=notification_data)
            print(f"Notification #{i} added successfully...")


    @classmethod
    def generate_tasks(cls, num_tasks=10):
        """Generate task records with random data."""
        users = User.query.all()

        for _ in range(num_tasks):
            task_data = {
                    "name": fake.word(),
                    "description": fake.paragraph(),
                    "userId": random.choice(users).userId,
                    }

            Task.create(details=task_data)
            print(f"Task #{i} added successfully...")


    @classmethod
    def generate_categories(cls, num_categories=5):
        """Generate category records with random data."""
        for _ in range(num_categories):
            category_data = {
                    "name": fake.word(),
                    "description": fake.paragraph(),
                    }

            Category.create(details=category_data)
            print(f"Category #{i} added successfully...")


# Run the data generation
DataGenerator.generate_users()
DataGenerator.generate_books()
DataGenerator.generate_authors()
DataGenerator.generate_raffles()
DataGenerator.generate_tickets()
DataGenerator.generate_notifications()
DataGenerator.generate_tasks()
DataGenerator.generate_categories()
