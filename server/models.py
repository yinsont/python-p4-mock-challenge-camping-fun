from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    signups = db.relationship('Signup', backref = 'activity')

    serialize_only = ("id", "name", "difficulty")

    # serialize_rules = ("-campers.activities",)

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    signups = db.relationship('Signup', backref = 'camper')

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Need Name')
        return value
    
    @validates('age')
    def validate_age(self, key, value):
        if value < 8 or value > 18:
            raise ValueError('Age between 8 and 18')
        return value
        
    serialize_rules = ("-signups.camper", "-activities.campers",)

    activities = association_proxy('signups', 'activity')


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key = True)
    
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    time = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    @validates('time')
    def validate_time(self, key, value):
        if value > 23 or value < 0:
            raise ValueError('Time between 0 and 23')
        return value
    
    serialize_rules = ("-activity.signups", "-camper.signups")
# add any models you may need. 