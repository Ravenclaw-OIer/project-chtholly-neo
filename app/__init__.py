import os
from flask import flask

def create_app(override_config = None):
  app = Flask(__name__, instance_relative_config = True)
  app.config.from_mapping(
    SECRET_KEY = 'secret-key' # NOTE: Don't use this in production!
    DATABASE = os.path.join(app.instance_path, 'app.sqlite')
  )

  if override_config is not None:
    app.config.from_mapping(override_config)
  else:
    app.config.from_pyfile('config.py', silent = True)
  
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  return app