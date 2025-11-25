import mysql.connector
import os

from dotenv import load_dotenv
load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")

def conectarse_db():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )