# Copyright 2018 Biz2Credit Infoservices Pvt Ltd. All Rights Reserved.
#
# Author: Mohit Kumar
# Version: 1.0.0
#
# Loads all configuration from ENV file
import os
from pathlib import Path
try:
    from dotenv import read_dotenv

    # Load the env file from the APP root directory
    env_path = Path('..') / '.env'
    read_dotenv(env_path)
except:
    from dotenv import load_dotenv

    # Load the env file from the APP root directory
    env_path = Path('..') / '.env'
    load_dotenv(env_path)

#Loads all configuration from ENV file
DB_HOST = os.environ.get('DB_HOST', None)
DB_PORT = os.environ.get('DB_PORT', None)
DB_NAME = os.environ.get('DB_NAME', None)
DB_USER = os.environ.get('DB_USER', None)
DB_PASSWORD = os.environ.get('DB_PASSWORD', None)
DB_COLLECTION = os.environ.get('DB_COLLECTION', None)
DB_PROVIDER = os.environ.get('DB_PROVIDER', None)
SESSION_EXPIRY_TIME=os.environ.get('SESSION_EXPIRY_TIME', None)
SUPERUSEREMAIL=os.environ.get('SUPERUSEREMAIL', None)
SUPERUSERPASSWORD=os.environ.get('SUPERUSERPASSWORD', None)
SERVERPORT = os.environ.get('SERVERPORT', None)
REDIS_HOST = os.environ.get('REDIS_HOST', None)
REDIS_PORT = os.environ.get('REDIS_PORT',None)
