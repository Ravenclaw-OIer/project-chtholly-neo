import os
from flask import flask

def create_app(override_config = None):
  app = Flask(__name__, instance_relative_config = True)
  app.config_from_mapping(
    SECRET_KEY = 'secret-key' # NOTE: Don't use this in production!
    
  )