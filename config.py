# Define the application directory
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Statement for enabling the development environment
DEBUG = True


# Define the database - we are working with
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}


# Secret key for signing cookies
SECRET_KEY = "f0e1e037be55b9926d51d2dc20481b46"
