from flask import jsonify, Blueprint
from flask_restful import request
from flask_jwt_extended import jwt_required, create_refresh_token, create_access_token
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from core.models import Owner, Car, owners_serializer, owner_serializer, cars_serializer, car_serializer, User, \
    users_serializer, user_serializer

db = SQLAlchemy()

bp_owners = Blueprint('owner', __name__, url_prefix='/v1')
bp_cars = Blueprint('cars', __name__, url_prefix='/v1')
auth = Blueprint("auth", __name__)
bp_users = Blueprint('users', __name__, url_prefix='/v1')


@bp_owners.route('/owners', methods=['GET'])
@jwt_required()
def get_owners():
    try:
        owners = Owner.query.all()
        if owners:
            result = owners_serializer.dump(owners)
            return jsonify({'message': 'successfully fetched', 'data': result})

        return jsonify({'message': 'nothing found', 'data': {}})
    except (Exception,):
        return jsonify({'message': "unable to list"}), 500


@bp_owners.route('/owners/<int:id>', methods=['GET'])
@jwt_required()
def get_owner_by_id(id: int):
    try:
        owner = Owner.query.get(id)
        if owner:
            result = owner_serializer.dump(owner)
            return jsonify({'message': 'successfully fetched', 'data': result}), 200

        return jsonify({'message': "Owner don't exist", 'data': {}}), 404
    except (Exception,):
        return jsonify({'message': "unable to list"}), 500


@bp_owners.route('/owners', methods=['POST'])
@jwt_required()
def post_owner():
    try:
        name = request.json.get("name")
        owner = Owner.query.filter_by(name=name).first()
        if owner:
            return jsonify({'message': 'Owner already exists'})

        owner = Owner(name=name)

        print(owner)

        db.session.add(owner)
        db.session.commit()
        result = owner_serializer.dump(owner)
        return jsonify({'message': 'successfully registered', 'data': result}), 201

    except (Exception,):
        return jsonify({'message': 'unable to create'}), 500


@bp_owners.route('/owners/<int:id>', methods=['PUT'])
@jwt_required()
def update_owner(id: int):
    name = request.json['name']
    owner = Owner.query.get(id)

    if owner:
        try:
            owner.name = name
            db.session.commit()
            result = owner_serializer.dump(owner)
            return jsonify({'message': 'successfully updated', 'data': result}), 201
        except:
            return jsonify({'message': 'unable to update'}), 500

    return jsonify({'message': "owner don't exist", 'data': {}}), 404


@bp_owners.route('/owners/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_owner(id: int):
    owner = Owner.query.get(id)

    if owner:
        try:
            db.session.delete(owner)
            db.session.commit()
            return jsonify({'message': 'successfully deleted'}), 200
        except (Exception,):
            return jsonify({'message': 'unable to update'}), 500

    return jsonify({'message': "owner don't exist", 'data': {}}), 404


@bp_cars.route('/cars', methods=['GET'])
@jwt_required()
def get_cars():
    try:
        cars = Car.query.all()
        if cars:
            result = cars_serializer.dump(cars)
            return jsonify({'message': 'successfully fetched', 'data': result})

        return jsonify({'message': 'nothing found', 'data': {}})
    except (Exception,):
        return jsonify({'message': "unable to list"}), 500


@bp_cars.route('/cars/<int:id>', methods=['GET'])
@jwt_required()
def get_car_by_id(id):
    try:
        car = Car.query.get(id)
        if car:
            result = car_serializer.dump(car)
            return jsonify({'message': 'successfully fetched', 'data': result}), 200

        return jsonify({'message': "Car don't exist", 'data': {}}), 404
    except (Exception,):
        return jsonify({'message': "unable to list"}), 500


@bp_cars.route('/cars', methods=['POST'])
@jwt_required()
def post_car():
    try:
        args = request.json
        qtd_cars_owner = Car.query.filter(Car.owner_id == args['owner_id']).count()

        if qtd_cars_owner >= 3:
            return jsonify({'message': 'amount exceeded'}), 200

        car = Car(**args)
        db.session.add(car)
        db.session.commit()
        result = car_serializer.dump(car)

        return jsonify({'message': 'successfully registered', 'data': result}), 201
    except (Exception,):
        return jsonify({'message': 'unable to create'}), 500


@bp_cars.route('/cars/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_car(id: int):
    try:
        car = Car.query.get(id)
        if not car:
            return jsonify({'message': "user don't exist", 'data': {}}), 404

        if car:
            db.session.delete(car)
            db.session.commit()
            return jsonify({'message': 'successfully deleted'}), 200
    except (Exception,):
        return jsonify({'message': 'unable to delete', 'data': {}}), 500


@bp_cars.route('/cars/<int:id>', methods=['PUT'])
@jwt_required()
def update_car(id: int):
    try:
        args = request.json
        car = Car.query.get(id)

        if not car:
            return jsonify({'message': "Car don't exist", 'data': {}}), 404

        if car:
            car.name = args['name']
            car.color = args['color']
            car.model = args['model']
            car.owner_id = args['owner_id']
            db.session.commit()
            result = car_serializer.dump(car)
            return jsonify({'message': 'successfully updated', 'data': result}), 201
    except (Exception,):
        return jsonify({'message': 'unable to update'}), 500


@auth.post('/register')
def register():
    try:
        username = request.json['username']
        name = request.json['name']
        password = request.json['password']
        email = request.json['email']

        pwd_hash = generate_password_hash(password)

        user = User(username=username, password=pwd_hash, email=email, name=name)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'register successfull'}), 201
    except (Exception,):
        return jsonify({'message': 'register error'}), 500


@auth.post('/login')
def login():
    try:
        username = request.json.get("username")
        password = request.json.get("password")

        user = User.query.filter_by(username=username).first()

        if not check_password_hash(user.password, password):
            return jsonify({"error": "credentials error."}), 400

        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        return jsonify({"refresh": refresh,
                        "access_token": access,
                        "name": user.name,
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                        }), 200
    except (Exception,):
        return jsonify({'message': 'login error'}), 500


@bp_users.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        if users:
            result = users_serializer.dump(users)
            return jsonify({'message': 'successfully fetched', 'data': result})

        return jsonify({'message': 'nothing found', 'data': {}})
    except (Exception,):
        return jsonify({'message': "unable to list"}), 500


@bp_users.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user_by_id(id):
    try:
        user = User.query.get(id)
        if user:
            result = user_serializer.dump(user)
            return jsonify({'message': 'successfully fetched', 'data': result}), 200

        return jsonify({'message': "Car don't exist", 'data': {}}), 404
    except (Exception,):
        return jsonify({'message': "unable to list"}), 500


@bp_users.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id: int):
    try:
        args = request.json
        user = User.query.get(id)

        if not user:
            return jsonify({'message': "User don't exist", 'data': {}}), 404

        if user:
            user.name = args['name']
            user.password = generate_password_hash(args['password'])
            user.username = args['username']
            user.email = args['email']
            db.session.commit()
            result = user_serializer.dump(user)
            return jsonify({'message': 'successfully updated', 'data': result}), 201
    except (Exception,):
        return jsonify({'message': 'unable to update'}), 500
