import csv
import os

FILE = "data/users.csv"


def create_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "username",
                "password",
                "email",
                "phone",
                "country",
                "birthdate"
            ])


def register_user(username, password, email, phone, country, birthdate):
    create_file()

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            username,
            password,
            email,
            phone,
            country,
            birthdate
        ])
