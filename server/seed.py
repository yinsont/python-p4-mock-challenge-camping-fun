from random import choice as rc

from app import app
from models import db, Activity, Signup, Camper

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Activity.query.delete()
        Signup.query.delete()
        Camper.query.delete()

        print("Done seeding!")
