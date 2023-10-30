from flask import Flask, jsonify
import pyodbc

app=Flask(__name__)

server = 'leitorappocr.database.windows.net'
database = 'leitor-ocr'
username = 'azurer'
password = 'Destroi96&'
port=1433

dadosBanco = (
               'Driver={ODBC Driver 18 for SQL Server};'
               f'Server={server};'
               f'Database={database};'
               f'Uid={username};'
               f'Pwd={password};'
               f'Port={port};'
)   

@app.get("/")
def helloWorld():
    try:
        conexao = pyodbc.connect(dadosBanco)
        cursor = conexao.cursor()
        cursor.execute("select * from usuarios")
        resultado = cursor.fetchall()
        conexao.close()
        
        data_list = [dict(zip([column[0] for column in cursor.description], row)) for row in resultado]

        return jsonify({'resultado': data_list})  
    except pyodbc.Error as e: 
        return jsonify({'erro': str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=3000)