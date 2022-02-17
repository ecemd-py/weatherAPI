from functools import wraps
import jwt
from flask import Response, request, jsonify, json
from Databases.DBOps import DBOps
from cryptography.hazmat.primitives import serialization

# Create api key with:
# >>> import secrets
# >>> secrets.token_urlsafe(16)

api_key = 'C31sRDgbZNTjb5_WXHpG6A'
dbops = DBOps()

class Authenticate:
    def create_token(self, username, password):
        payload_data = {
            "username": username,
            "pass": password
        }
        token = jwt.encode(
            payload=payload_data,
            key=api_key,
            algorithm="HS256"
        )
        return token
    
    def validate_token(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
        
            token = None

            if 'token' in request.headers:
                token = request.headers['token']
                username = request.headers["username"]
                password = request.headers["password"]
                try:
                    decoded = jwt.decode(
                        token,
                        key=api_key,
                        algorithms="HS256"
                    )
                except:
                    return Response(
                        response=json.dumps({"response": "Token is not valid!"}),
                        status=401,
                        mimetype='application/json'
                    )

                if decoded["username"] == username and decoded["pass"] == password:
                    return f(*args, **kwargs)
                else:
                    return Response(
                        response=json.dumps({"response": "Token is not valid!"}),
                        status=401,
                        mimetype='application/json'
                    )

            if not token:
                return Response(
                        response=json.dumps({"response": "No token has been sent!"}),
                        status=401,
                        mimetype='application/json'
                    )
            
            return f(*args, **kwargs) 
        return decorator

    def validate_admin(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
        
            username = request.headers["username"]
            if dbops.is_Admin(username):
                return f(*args, **kwargs)
            else:
                return Response(
                        response=json.dumps({"response": "Unauthorized Request!"}),
                        status=401,
                        mimetype='application/json'
                    )
            
        return decorator
