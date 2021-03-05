from flask import Flask
from flask_restful import Api


def create_app():
    """
    Create app object and register views
    .views contains endpoints
    .api contains api calls used
    """
    app = Flask(__name__)
    app.config.from_object('config')
    from .views import views
    # from .api import loginAction, userAction
    # api = Api(app)
    # api.add_resource(loginAction, '/api/login')
    # api.add_resource(userAction, '/api/user')

    app.register_blueprint(views)
    return app
