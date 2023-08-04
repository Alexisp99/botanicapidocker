from dotenv import load_dotenv
import pymysql
import os
from urllib.parse import urlparse

def connect():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    # Parse the database URL
    url_components = urlparse(database_url)
    db_host = url_components.hostname
    db_user = url_components.username
    db_password = url_components.password
    db_name = url_components.path[1:]  

    # Configurer la connexion à la base de données MySQL
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn