#!/usr/bin/env python3

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}")

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Activity, Camper, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        campers = [camper.to_dict() for camper in Camper.query.all()]

        return make_response(campers, 200)
    
    def post(self):
        data = request.json()
        new_camper = Camper(
            name = data['name'],
            age = data['age']
        )
        db.session.add(new_camper)
        db.session.commit()
        return make_response(new_camper.to_dict(), 201)
    
Api.add_resource(Campers, '/campers')

class CamperByID(Resource):
    def get(self, id):
        camper = Camper.query.filter_by(id = id).first().to_dict()

        if not camper: return make_response({"error": "404: Camper not found"}, 404)
        return make_response(camper, 200)
    
Api.add_resource(CamperByID, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        activities = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(activities, 200)
    
Api.add_resource(Activities, '/activities')

class ActivityByID(Resource):
    def delete(self, id):
        activity = Activity.query.filter_by(id = id).first().to_dict()

        if activity == None: return make_response({"error":"404: Activiity not found"}, 404)
        db.session.delete(activity)
        db.session.commit()

        return make_response(activity, 202)
        pass

class Signups(Resource):
    def post(self):
        data = request.json()
        new_signup = Signup(
            time = data['time'],
            camper_id = data['camper_id'],
            activity_id = data['activity_id']
        )

        db.session.add(new_signup)
        db.session.commit()

        return make_response(new_signup.to_dict(), 202)
    
Api.add_resource(ActivityByID, '/activities/<int:id>')
if __name__ == '__main__':
    app.run(port=5555, debug=True)
