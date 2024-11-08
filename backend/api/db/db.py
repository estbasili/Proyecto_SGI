from mysql.connector import (connection)
import os


def get_db_connection():
    try:
        conn = connection.MySQLConnection(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            raise_on_warnings=True
        )
        return conn
    except Exception as ex:
        print(ex)


class DBError(Exception):
    pass

print(os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'))
