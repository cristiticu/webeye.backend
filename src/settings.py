from dotenv import load_dotenv
import os

load_dotenv('.env')

ENVIRONMENT = os.environ.get('ENVIRONMENT')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME')

AUTH_REFRESH_RETENTION_DAYS = int(
    os.environ.get('AUTH_REFRESH_RETENTION_DAYS', 1))

DYNAMODB_URL_OVERRIDE = os.environ.get('DYNAMODB_URL_OVERRIDE')
TABLE_PREFIX = os.environ.get(
    'TABLE_PREFIX') or "production" if ENVIRONMENT == "production" else "stage"
USER_ACCOUNTS_TABLE_NAME = "webeye.user-accounts"
USER_ACCOUNTS_EMAIL_GSI = "email-gsi"
MONITORED_WEBPAGES_TABLE_NAME = "webeye.monitored-webpages"
SCHEDULED_TASKS_TABLE_NAME = "webeye.scheduled-tasks"
SCHEDULED_TASKS_SCHEDULE_GSI = "schedule-gsi"
MONITORING_EVENTS_TABLE_NAME = "webeye.monitoring-events"

SECRET_KEY = "b386aaadd83435c99d40d96234972bf3330506473c6a41d081565a6cc39d1b7c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 if ENVIRONMENT == 'production' else 60 * 24
