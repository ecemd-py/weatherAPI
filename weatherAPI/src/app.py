from flask import Flask


def create_app():
    app = Flask(__name__)

    # blueprint for auth routes in app (all routes are under auth)
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

if __name__ == '__main__':
    create_app()