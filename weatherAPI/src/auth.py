from flask import Blueprint, request, json, Response
from Databases.DBOps import DBOps
from Authenticate import Authenticate
from Databases.UserInfoModel import UserInfoModel
from Databases.WeatherInfoModel import WeatherInfoModel

auth = Blueprint('auth', __name__)
dbops = DBOps()
authops = Authenticate()

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.json["username"]
    password = request.json["password"]

    # check if user actually exists
    if dbops.check_user_exist(username) and dbops.check_correct_password(username, password):
        token = authops.create_token(username, password)
        response = Response(
            response=json.dumps({"token": token}),
            status=200,
            mimetype='application/json'
        )
    
    else:
        response = Response(
            response=json.dumps({"Error Message": "Check username and password!"}),
            status=401,
            mimetype='application/json'
        )
    return response

@auth.route('/user', methods=['POST'])
@authops.validate_token
@authops.validate_admin
def create_user():
    user_info = request.json
    try:
        user_info_model = UserInfoModel.parse(user_info).__dict__
    except Exception as e:
        return Response(
            response=json.dumps({"Error Message": e.__str__()}),
            status=400,
            mimetype='application/json'
        )

    db_res = dbops.insert_new_user(user_info_model)

    if db_res:
        response = Response(
            response=json.dumps({"response": "User created!", "user_info": user_info_model}),
            status=201,
            mimetype='application/json'
        )
    else:
        response = Response(
            response=json.dumps({"Error Message": "Problem occured while trying to add a new user! Try again!"}),
            status=409,
            mimetype='application/json'
        )
    return response

@auth.route('/user/<user_id>', methods=['GET'])
@authops.validate_token
@authops.validate_admin
def get_user_info(user_id):
    user_info = dbops.get_userinfo_by_userid(user_id)

    if len(user_info) > 0:
        response = Response(
            response=json.dumps(user_info),
            status=200,
            mimetype='application/json'
        )
    else:
        response = Response(
            response=json.dumps({"Error Message": "User not found!"}),
            status=404,
            mimetype='application/json'
        )

    return response

@auth.route('/user/<user_id>', methods=['PUT', 'POST'])
@authops.validate_token
@authops.validate_admin
def update_user_info(user_id):
    update_info = request.json
    if len(update_info) > 1:
        response = Response(
            response=json.dumps({"Error Message": "Only one field can be changed!"}), 
            status=400,
            mimetype='application/json'
        )
        return response

    user_info = dbops.update_userinfo_by_userid(user_id, update_info)

    if user_info:
        response = Response(
            response=json.dumps({"response": "User updated!"}),
            status=200,
            mimetype='application/json'
        )
    else:
        response = Response(
            response=json.dumps({"Error Message": "Problem occured while trying to update user info! Try again!"}), 
            status=409,
            mimetype='application/json'
        )

    return response

@auth.route('/user/<user_id>', methods=['DELETE'])
@authops.validate_token
@authops.validate_admin
def delete_user_info(user_id):
    db_res = dbops.delete_user(user_id)
    if db_res:
        response = Response(
            response=json.dumps({"response": "User deleted!"}),
            status=200,
            mimetype='application/json'
        )
    else:
        response = Response(
            response=json.dumps({"Error Message": "Problem occured while trying to delete user! Try again!"}), 
            status=409,
            mimetype='application/json'
        )
    return response

@auth.route('/weather', methods=['GET'])
@authops.validate_token
def get_weather_info():
    filter = request.json
    modeled_filter = WeatherInfoModel.parse(filter).__dict__
    weather_info = dbops.get_weather_info(modeled_filter)

    if len(weather_info):
        response = Response(
            response=json.dumps(weather_info),
            status=200,
            mimetype='application/json'
        )
    else:
        response = Response(
            response=json.dumps({"Error Message": "Weather info not found!"}),
            status=404,
            mimetype='application/json'
        )
    return response