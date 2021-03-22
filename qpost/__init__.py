from flask import Flask
from .views import views


def create_app():
    """
    Create Flask object and register views
    .views contains endpoints
    .api contains api calls used
    """
    app = Flask(__name__)
    app.config.from_object('config')
    app.register_blueprint(views)
    return app
