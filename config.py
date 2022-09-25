import os
from datetime import timedelta

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
db = os.environ.get('DB_NAME')
secret_key = os.environ.get('SECRET_KEY')


class Config(object):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ALGORITHM = "HS256"
    JWT_SECRET_KEY = secret_key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
