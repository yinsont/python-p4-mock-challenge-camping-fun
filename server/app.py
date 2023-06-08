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
        campers = [camper.to_dict(only = ('id', 'name', 'age')) for camper in Camper.query.all()]

        return campers, 200
    
    def post(self):
        try:
            new_camper = Camper(
                name = request.json['name'],
                age = request.json['age']
            )
            db.session.add(new_camper)
            db.session.commit()
            return new_camper.to_dict(only=('id', 'name', 'age')), 201
        except:
            return {'error': '400: Validation error'}, 400
        
api.add_resource(Campers, '/campers')


class CampersByID(Resource):
    def get(self, id):
        try:
            camper = Camper.query.filter_by(id = id).first().to_dict(only = ('id', 'name', 'age', 'activities'))
            return camper, 200
        except:
            return {'error': '404: Camper not found'}, 404
api.add_resource(CampersByID, '/campers/<int:id>')

class Activities(Resource):
    def get(self):
        activities = [activity.to_dict(only = ('id', 'name', 'difficulty')) for activity in Activity.query.all()]
        return activities, 200
api.add_resource(Activities, '/activities')

class ActivityByID(Resource):
    def delete(self, id):
        try:
            activity = Activity.query.filter_by(id = id).first()
            db.session.delete(activity)
            db.session.commit()
            return {},204
        except:
            return {'error': '404: Activity not found'}, 404
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

            return new_signup.to_dict(), 200
        except:
            return {"error":"jhjhjh"},400
    
api.add_resource(Signups, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
