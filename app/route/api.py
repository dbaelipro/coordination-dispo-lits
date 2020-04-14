import os
from flask import Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger

from config import BASE_SERVER_PATH
from resource.user import SignupApi, LoginApi, UserAPI, UserListAPI

api_blueprint = Blueprint('api', __name__)

api = swagger.docs(Api(api_blueprint), apiVersion='0.1',
                   basePath=BASE_SERVER_PATH,
                   resourcePath='/',
                   produces=["application/json", "text/html"],
                   api_spec_url='/docs',
                   description='Coordinations lits api')

api.add_resource(SignupApi, '/auth/signup')
api.add_resource(LoginApi, '/auth/login')

api.add_resource(UserListAPI, '/users')
api.add_resource(UserAPI, '/users/<int:id>')
