import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# Twitter settings
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN') 
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

# Reddit settings
USER_AGENT = os.environ.get('USER_AGENT')