import os
from dotenv import load_dotenv

load_dotenv('.env')

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB_NAME')
POSTGRES_ADDRESS = os.environ.get('POSTGRES_ADDRESS')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
