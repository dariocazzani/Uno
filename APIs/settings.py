import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Twitter settings
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') 
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# Reddit settings
USER_AGENT = os.environ.get('USER_AGENT')

# gmail settings
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
LOGIN_USER = os.environ.get('LOGIN_USER')
LOGIN_PASSWORD = os.environ.get('LOGIN_PASSWORD')
UNO_ADDRESS = os.environ.get('UNO_ADDRESS')
