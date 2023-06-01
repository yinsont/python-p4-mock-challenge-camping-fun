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

api = Api(app)

@app.route('/')
def home():
    return ''

class Campers(Resource):
    def get(self):
        campers = [camper.to_dict() for camper in Camper.query.all()]
        return make_response(campers, 200)
    def post(self):
        try:
            new_camper = Camper(
                name = request.json['name'],
                age = request.json['age']
            )
            db.session.add(new_camper)
            db.session.commit()
            return make_response(new_camper.to_dict(), 201)
        except:
            return {"error": "404: Validation error"}, 400
api.add_resource(Campers, '/campers')

class CamperByID(Resource):
    def get(self, id):
        try:
            camper = Camper.query.filter_by(id = id).first()
            return make_response(camper.to_dict(), 200)
        except:
            return {"error": "404: Camper not found"}, 404
api.add_resource(CamperByID, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        activities = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(activities, 200)
api.add_resource(Activities, '/activities')

class ActivityByID(Resource):
    def delete(self, id):
        try:
            activity = Activity.query.filter_by(id = id).first()
            db.session.delete(activity)
            db.session.commit()
            return {}, 204
        except:
            return {"error":"404: Activity not found"}, 404
api.add_resource(ActivityByID, '/activities/<int:id>')

class Signups(Resource):
    def post(self):
        try:
            new_signup = Signup(
                time = request.json['time'],
                camper_id = request.json['camper_id'],
                activity_id = request.json['activity_id']
            )
            db.session.add(new_signup)
            db.session.commit()
            return make_response(new_signup.activity_id.to_dict(), 202)
        except:
            return {"error": "400: Validation error"}, 400
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
