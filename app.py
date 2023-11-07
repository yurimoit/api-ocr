from flask import Flask, jsonify
import pymssql
import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__)

DEBUG = os.getenv('DEBUG', default=False)
SERVER = os.getenv('BD_SERVER')
DATABASE = os.getenv('BD_NAME')
USER = os.getenv('BD_USER')
PASS = os.getenv('BD_PASS')
BD_PORT = os.getenv('BD_PORT')
PORT = os.getenv('PORT')

dadosBanco = {
    'server': SERVER,
    'database': DATABASE,
    'user': USER,
    'password': PASS,
    'port': int(BD_PORT),
}

def desserelizadorResponse(cursor, dados):
    return [dict(zip([column[0] for column in cursor.description], row)) for row in dados]

@app.route("/")
def get_dados():
    try:
        conexao = pymssql.connect(**dadosBanco)
        cursor = conexao.cursor(as_dict=True)  # Use as_dict=True to return results as dictionaries
        cursor.execute('select * from usuarios')
        dados = cursor.fetchall()
        conexao.close()
        resultado = desserelizadorResponse(cursor, dados)

        return jsonify({'Dados': resultado})

    except Exception as e:
        return jsonify({'Error': str(e)})

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
