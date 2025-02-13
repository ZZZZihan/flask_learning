from flask import Blueprint
from .auth import api as auth_api
from .achievements import api as achievements_api

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

api_v1.register_blueprint(auth_api, url_prefix='/auth')
api_v1.register_blueprint(achievements_api) 