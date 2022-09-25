import enum
import datetime
from flask_marshmallow import Schema
from flask_sqlalchemy import SQLAlchemy
from marshmallow_enum import EnumField

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'


class UserSerializer(Schema):
    class Meta:
        model = User
        fields = ('id', 'name',
                  'username', 'email', 'created_on')


user_serializer = UserSerializer()
users_serializer = UserSerializer(many=True)


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Owner {self.name}>'


class OwnerSerializer(Schema):
    class Meta:
        model = Owner
        fields = ('id', 'name', 'created_on')


owner_serializer = OwnerSerializer()
owners_serializer = OwnerSerializer(many=True)


class ModelChoices(enum.Enum):
    Hatch = "Hatch"
    Sedan = "Sedan"
    Convertible = "Convertible"


class ColorChoices(enum.Enum):
    Blue = "Blue"
    Gray = "Gray"
    Yellow = "Yellow"


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model = db.Column(db.Enum(ModelChoices), nullable=False)
    color = db.Column(db.Enum(ColorChoices), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'),
                         nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name, owner_id, model, color):
        self.name = name
        self.owner_id = owner_id
        self.color = color
        self.model = model

    def __repr__(self):
        return f'<Car {self.name}>'


class CarSerializer(Schema):
    model = EnumField(ModelChoices, by_value=True)
    color = EnumField(ColorChoices, by_value=True)

    class Meta:
        model = Car
        fields = ('id', 'model', 'name', 'color', 'owner_id',
                  'available', 'created_on')


car_serializer = CarSerializer()
cars_serializer = CarSerializer(many=True)
