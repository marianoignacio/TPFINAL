import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sql_path = os.path.join(BASE_DIR, "init_db.sql")

with open(sql_path, "r") as f:
    sql = f.read()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,

)


cursor = conn.cursor()
for query in sql.split(";"):
    if query.strip():
        print(query)
        cursor.execute(query)
        conn.commit()
        print("Query ejecutada correctamente")

cursor.close()
conn.close()