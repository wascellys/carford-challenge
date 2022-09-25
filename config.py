import os
from datetime import timedelta

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
db = os.environ.get('DB_NAME')
gen = string.ascii_letters + string.digits + string.ascii_uppercase
secret_key = ''.join(random.choice(gen) for i in range(12))


class Config(object):
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = secret_key
