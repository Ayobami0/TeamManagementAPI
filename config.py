import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
HOSTNAME = os.environ.get("MYSQL_HOST")
DB_NAME = os.environ.get("MYSQL_NAME")
PORT = os.environ.get("MYSQL_PORT")
# SSL_CERT = os.environ.get("MYSQL_SSL_CERT")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30),
)
