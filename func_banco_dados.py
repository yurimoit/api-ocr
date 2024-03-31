from flask import request, jsonify
import psycopg2
import os
import json
from dotenv import load_dotenv
import copy
from datetime import datetime
from dateutil.relativedelta import relativedelta


load_dotenv()


HOST = os.environ.get('host')
DATA_BASE = os.environ.get('database')
USER = os.environ.get('user')
PASSWORD = os.environ.get('password')


def formataData(data: str):
    """Formata data"""

    data_list = (data).split('-')

    data_list_mes = data_list[1][0] == '0' if '' + \
        data_list[1][1] else data_list[1]

    data_formatada = datetime(int(data_list[0]), int(
        data_list_mes), int(data_list[2]))
    data_atual = data if data_formatada else datetime.now(
    )

    return data_atual


def inserir_exame_no_banco_dados():
    """INSERIR INFORMAÇÃO NO BANCO DE DADOS"""

    id_usuario = int(request.usuario[0])
    dados = request.get_json('resposta')
    dados_exame = dados['resposta']

    cursor = None
    conn = None

    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DATA_BASE,
            user=USER,
            password=PASSWORD
        )

        json_dados = json.dumps(dados_exame['lista_dados'])

        data_atual = formataData(dados_exame['data_exame'])

        cursor = conn.cursor()

        cursor.execute("INSERT INTO files (nome_exame, url_exame, lista_dados, observacao, data_exame, id_usuario) VALUES (%s, %s,%s,%s,%s,%s)",
                       (dados_exame['nome_exame'], dados_exame['url_exame'], json_dados, dados_exame['observacao'], data_atual, id_usuario))
        conn.commit()

        print("Inserção bem-sucedida no banco de dados.")
        return jsonify({'mensagem': "Inserção bem-sucedida no banco de dados."}), 201

    except Exception as e:
        print(f"Erro inserir dados no banco: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def atualiza_exame_no_banco_dados(id):
    """ATUALIZA EXAME"""

    dados = request.get_json('resposta')
    dados_exame_atualiza = dados['resposta']
    print("Dados atualizacao: ", dados_exame_atualiza['nome_exame'])

    cursor = None
    conn = None

    data_atual = formataData(dados_exame_atualiza['data_exame'])

    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DATA_BASE,
            user=USER,
            password=PASSWORD
        )

        id_exame = int(id)

        json_dados_atualizacao = json.dumps(
            dados_exame_atualiza['lista_dados'])

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE files 
            SET nome_exame = %s, lista_dados = %s, observacao = %s,data_exame =%s
            WHERE id = %s
            RETURNING *;
        """, (dados_exame_atualiza['nome_exame'],
              json_dados_atualizacao, dados_exame_atualiza['observacao'], data_atual, id_exame))

        conn.commit()

        atualizacao = cursor.fetchone()

        if not atualizacao:
            return jsonify({'error': 'Erro no servidor ao tentar atualiza cadastro usuario'}), 500

        return jsonify({"mensagem": "Atualização realizada com sucesso."}), 201

    except Exception as e:
        print(f"Erro atualiza exame banco de dados: {e}")
        return jsonify({'mensagem': "Erro no servidor na atualizacao"}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def deletar_exame_banco_dados(id):
    """DELETAR EXAME DO BANCO DE DADOS"""

    id_exame = int(id)

    cursor = None
    conn = None

    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DATA_BASE,
            user=USER,
            password=PASSWORD
        )

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM files WHERE id=%s", (id_exame,))
        exame = cursor.fetchone()

        if not exame:
            return jsonify({'mensagem': 'Exame não encontrado.'}), 404

        cursor.execute("DELETE FROM files WHERE id=%s", (id_exame,))
        conn.commit()

        return jsonify({"mensagem": "Exame deletado com sucesso.", "id_deletado": id_exame}), 200

    except (Exception, psycopg2.Error) as error:
        print("Erro ao deletar exame do banco de dados:", error)
        return jsonify({'error': 'Erro ao deletar o exame do banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_exames():
    """BUSCAR COBRANÇAS NO BANCO DE DADOS"""

    cursor = None
    conn = None

    try:
        id_usuario = int(request.usuario[0])
        busca = request.args.get('busca')

        print("Buscar: ", busca)

        query = "SELECT * FROM files WHERE id_usuario = %s"

        params = [id_usuario]

        if busca:
            query += " AND (nome_exame ILIKE %s OR id::text ILIKE %s OR data_exame::text ILIKE %s)"
            params.extend([f"%{busca}%", f"%{busca}%", f"%{busca}%"])

        conn = psycopg2.connect(
            host=HOST,
            database=DATA_BASE,
            user=USER,
            password=PASSWORD
        )

        cursor = conn.cursor()

        cursor.execute(query, params)
        exames = cursor.fetchall()
        print(exames)

        conn.commit()

        if not exames:
            return jsonify({"mensagem": "Nenhum resultado encontrado."}), 404

        print("Exames: ", exames)

        lista_objeto = []
        lista_revertida = exames[::-1]
        for obj in lista_revertida:
            lista_objeto.append({
                "id": obj[0],
                "nome_exame": obj[1],
                "url_exame": obj[2],
                "lista_dados": obj[3],
                'observacao': obj[4],
                'data_exame': obj[5],
                'id_usuario': obj[6]
            })

        print("OBjeto:--------------------------------------------------------------------",
              lista_objeto, sep='\n')

        print('\n')
        print("Lista---------------------------------------------------- ",
              lista_revertida)
        return jsonify(lista_objeto), 200

    except (Exception, psycopg2.Error) as error:
        print("Erro ao consultar o banco de dados:", error)
        return jsonify({'error': 'Erro ao consultar o banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_banco():
    """FAZER UM GET DOS DADOS NO BANCO"""

    cursor = None
    conn = None

    try:
        # Substitua as informações de conexão conforme necessário
        conn = psycopg2.connect(
            host=HOST,
            database=DATA_BASE,
            user=USER,
            password=PASSWORD
        )

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM files")
        rows = cursor.fetchall()

        result_list = []
        for row in rows:
            result_dict = {
                'id': row[0],
                'nome_exame': row[1],
                'url_exame': row[2],
                'lista_dados': row[3],
                'observacao': row[4],
                'data_exame': row[5],
                'id_usuario': row[6]
            }
            result_list.append(result_dict)

        result_list.reverse()

        for item in result_list:
            print("id_r: ", item)

        return jsonify(result_list), 200

    except (Exception, psycopg2.Error) as error:
        print("Erro ao consultar o banco de dados:", error)
        return jsonify({'error': 'Erro ao consultar o banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
