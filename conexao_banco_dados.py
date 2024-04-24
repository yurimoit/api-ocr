from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()


def connectar_banco():
    """CONNECTA COM BANCO DE DADOS"""

    conn = psycopg2.connect(
        host=os.getenv('host'),
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password')
    )

    return conn
