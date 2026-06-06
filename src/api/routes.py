from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Blueprint('api', __name__)


@api.route('/signup', methods=['POST'])
def signup():
    body = request.json
    email = body.get("email", None)
    password = body.get("password", None)

    if email is None or password is None:
        return jsonify({"msg": "Se requiere email y contraseña"}), 400

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"msg": "El usuario ya existe"}), 400

    new_user = User(email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario creado con exito"}), 201


@api.route('/token', methods=['POST'])
def create_token():
    body = request.json
    email = body.get("email", None)
    password = body.get("password", None)

    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg": "Email o contraseña incorrectos"}), 401

    access_token = create_access_token(identity=user.email)
    return jsonify(access_token=access_token), 200


@api.route('/private', methods=['GET'])
@jwt_required()
def private_route():
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user}), 200
