import os
from dotenv import load_dotenv

load_dotenv('.env')

ENVIRONMENT = os.environ.get('ENVIRONMENT')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB_NAME')
POSTGRES_ADDRESS = os.environ.get('POSTGRES_ADDRESS')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')

DYNAMODB_URL_OVERRIDE = os.environ.get('DYNAMODB_URL_OVERRIDE')
TABLE_PREFIX = os.environ.get(
    'TABLE_PREFIX') or "production" if ENVIRONMENT == "production" else "stage"
USER_ACCOUNTS_TABLE_NAME = "webeye.user-accounts"
USER_ACCOUNTS_EMAIL_GSI = "email-gsi"
MONITORED_WEBPAGES_TABLE_NAME = "webeye.monitored-webpages"
SCHEDULED_TASKS_TABLE_NAME = "webeye.scheduled-tasks"

SECRET_KEY = "b386aaadd83435c99d40d96234972bf3330506473c6a41d081565a6cc39d1b7c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
