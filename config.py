DEBUG=True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

THREADS_PER_PAGE = 2


CSRF_ENABLED = True
CSRF_SESSION_KEY = ""

SECRET_KEY = ""


API = { "api_key": os.environ["APIKEY"] }
