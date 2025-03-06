from psycopg2 import pool
import os
from dotenv import load_dotenv

# Cargar claves desde .env (Opcional)
load_dotenv()

class DatabaseConnectionFactory:
    _connection_pool = None

    @classmethod
    def initialize(cls, minconn: int = 1, maxconn: int = 5):
        if cls._connection_pool is None:
            cls._connection_pool = pool.SimpleConnectionPool(
                minconn, maxconn,
                database=os.getenv("db_name", "prueba_db"),
                user=os.getenv("db_user", "prueba_user"),
                password=os.getenv("db_password", "prueba_pass"),
                host=os.getenv("db_host", "localhost"),
                port=os.getenv("db_port", "5432")
            )

    @classmethod
    def get_connection(cls):
        if cls._connection_pool is None:
            raise Exception("Connection pool is not initialized")
        return cls._connection_pool.getconn()

    @classmethod
    def release_connection(cls, connection):
        cls._connection_pool.putconn(connection)

    @classmethod
    def close_pool(cls):
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            cls._connection_pool = None