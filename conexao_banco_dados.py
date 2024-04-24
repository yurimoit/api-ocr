from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()


def conectar_banco():
    """Conecta com o banco de dados"""
    conn = psycopg2.connect(
        host=os.getenv('host'),
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        port=os.getenv('portBD')
    )

    return conn
