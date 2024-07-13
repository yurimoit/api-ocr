"""Module providing a function printing python version."""
from __future__ import annotations


import copy
import json
from flask import request, jsonify
from listas.lista_exame_hemograma import lista_dados
from listas.controlado_dados_lista import get_dados_info, funcao_or_dados, ordena_novo_json, valor_max_min_med
from conexao_banco_dados import connectar_banco
from controlador_dado import analisa_dados_range_referencia


def inserir_exame_no_banco_dados():
    """INSERIR INFORMAÇÃO NO BANCO DE DADOS"""

    id_usuario = int(request.usuario[0])
    dados = request.get_json('resposta')

    if dados is None:
        return jsonify({'mensagem': 'Dados não fornecidos'}), 400

    dados_exame = dados['resposta']
    id_paciente = dados_exame['id_paciente']
    nome_paciente = dados_exame['nome_paciente']
    data_nascimento = dados_exame['data_nascimento']
    sexo = dados_exame['sexo']
    cursor = None
    conn = None

    try:

        json_dados = []
        json_dados = json.dumps(dados_exame['lista_dados'])
        dados_exame['observacao'] = analisa_dados_range_referencia(
            dados_exame['lista_dados'])
        data_atual = dados_exame['data_exame']

        conn = connectar_banco()

        with conn.cursor() as cursor:
            if id_paciente:
                cursor.execute("INSERT INTO files (nome_exame, url_exame, lista_dados, observacao, data_exame, id_usuario,id_paciente) VALUES (%s, %s,%s,%s,%s,%s,%s)",
                               (dados_exame['nome_exame'], dados_exame['url_exame'], json_dados, dados_exame['observacao'], data_atual, id_usuario,  id_paciente))
            else:
                cursor.execute("INSERT INTO files (nome_exame, url_exame, lista_dados, observacao, data_exame, id_usuario) VALUES (%s, %s,%s,%s,%s,%s)",
                               (dados_exame['nome_exame'], dados_exame['url_exame'], json_dados, dados_exame['observacao'], data_atual, id_usuario))

            conn.commit()

        dados = get_banco_exames_exclusiva(id_paciente)
        novos_dados = ordena_novo_json(dados[0])
        data_1=novos_dados["data_1"]
        data_2=novos_dados["data_2"]
        data_3=novos_dados["data_3"]
        data_primeiro_registro=novos_dados["data_primeiro_registro"]
        data_ultimo_registro=novos_dados["data_ultimo_registro"]

        print("Novos dados: ", novos_dados)

        novos_json_dados = json.dumps(novos_dados["dados_estatistico"])

        if dados[1] > 1090:
            with conn.cursor() as cursor:
                if id_paciente:
                    cursor.execute(
                        """UPDATE relatorios
                        SET lista_dados=%s,  data_1=%s, data_2=%s, data_3=%s, data_primeiro_registro=%s, data_ultimo_registro=%s
                        WHERE id_usuario=%s and id_paciente=%s
                        RETURNING *;""",
                        (novos_json_dados, data_1, data_2, data_3, data_primeiro_registro, data_ultimo_registro, id_usuario, id_paciente))
                    conn.commit()
                else:
                    cursor.execute(
                        """UPDATE relatorios
                        SET lista_dados=%s, data_1=%s, data_2=%s, data_3=%s, data_primeiro_registro=%s, data_ultimo_registro=%s
                        WHERE id_usuario=%s
                        RETURNING *;""",
                        (novos_json_dados, data_1, data_2, data_3, data_primeiro_registro, data_ultimo_registro, id_usuario))
                    conn.commit()

            return jsonify({'mensagem': "Inserção bem-sucedida no banco de dados."}), 201

        with conn.cursor() as cursor:
            if id_paciente:
                cursor.execute(
                    """INSERT INTO relatorios
                    (nome_paciente, data_nascimento, sexo, data_1, data_2, data_3, data_primeiro_registro, data_ultimo_registro,
                     lista_dados, id_usuario, id_paciente)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (nome_paciente, data_nascimento, sexo,
                    data_1, data_2, data_3, data_primeiro_registro,
                    data_ultimo_registro, novos_json_dados, id_usuario, id_paciente))
                conn.commit()
            else:
                cursor.execute(
                    """INSERT INTO relatorios
                    (nome_paciente, data_nascimento, sexo, data_1, data_2, data_3, data_primeiro_registro, data_ultimo_registro, lista_dados, id_usuario)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (nome_paciente, data_nascimento, sexo,
                     data_1, data_2, data_3, data_primeiro_registro,
                    data_ultimo_registro, novos_json_dados, id_usuario))
                conn.commit()

        return jsonify({'mensagem': "Inserção bem-sucedida no banco de dados."}), 201

    except Exception as e:
        print(f"Erro inserir dados no banco: {str(e)}")
        return jsonify({'mensagem': "Erro no servidor"}), 500

    finally:
        if conn:
            conn.close()


def atualiza_exame_no_banco_dados(id):
    """ATUALIZA EXAME"""

    dados = request.get_json('resposta')
    dados_exame_atualiza = dados['resposta']
    id_usuario = int(request.usuario[0])
    # print("Dados atualizacao: ", dados_exame_atualiza['nome_exame'])

    cursor = None
    conn = None

    data_atual = dados_exame_atualiza['data_exame']

    try:
        conn = connectar_banco()

        id_exame = int(id)

        json_dados_atualizacao = json.dumps(
            dados_exame_atualiza['lista_dados'])

        dados_exame_atualiza['observacao'] = analisa_dados_range_referencia(
            dados_exame_atualiza['lista_dados'])

        # print("Observacao", dados_exame['observacao'])

        with conn.cursor() as cursor:

            cursor.execute("""
                UPDATE files
                SET nome_exame = %s, lista_dados = %s, observacao = %s,data_exame =%s
                WHERE id = %s and id_usuario=%s
                RETURNING *;
            """, (dados_exame_atualiza['nome_exame'],
                  json_dados_atualizacao, dados_exame_atualiza['observacao'], data_atual, id_exame, id_usuario))

            conn.commit()

            atualizacao = cursor.fetchone()
            lista_gerada = list(atualizacao)
            id_paciente = lista_gerada[-1]

            if not atualizacao:
                return jsonify({'error': 'Erro no servidor ao tentar atualiza cadastro usuario'}), 500

        dados = get_banco_exames_exclusiva(id_paciente)
        novos_dados = ordena_novo_json(dados[0])
        data_1=novos_dados["data_1"]
        data_2=novos_dados["data_2"]
        data_3=novos_dados["data_3"]
        data_primeiro_registro=novos_dados["data_primeiro_registro"]
        data_ultimo_registro=novos_dados["data_ultimo_registro"]

        novos_json_dados = json.dumps(novos_dados["dados_estatistico"])

        with conn.cursor() as cursor:
            if id_paciente:
                cursor.execute(
                        """UPDATE relatorios
                        SET lista_dados=%s,  data_1=%s, data_2=%s, data_3=%s, data_primeiro_registro=%s, data_ultimo_registro=%s
                        WHERE id_usuario=%s and id_paciente=%s
                        RETURNING *;""",
                        (novos_json_dados, data_1, data_2, data_3, data_primeiro_registro, data_ultimo_registro, id_usuario, id_paciente))
                conn.commit()
            else:
                cursor.execute(
                        """UPDATE relatorios
                        SET lista_dados=%s, data_1=%s, data_2=%s, data_3=%s, data_primeiro_registro=%s, data_ultimo_registro=%s
                        WHERE id_usuario=%s
                        RETURNING *;""",
                        (novos_json_dados, data_1, data_2, data_3, data_primeiro_registro, data_ultimo_registro, id_usuario))
                conn.commit()

        return jsonify({"mensagem": "Atualização realizada com sucesso."}), 201

    except Exception as e:
        print(f"Erro atualiza exame banco de dados: {e}")
        return jsonify({'mensagem': "Erro no servidor na atualizacao"}), 500

    finally:
        if conn:
            conn.close()


def deletar_exame_banco_dados(id):
    """DELETAR EXAME DO BANCO DE DADOS"""

    id_exame = int(id)
    id_usuario = int(request.usuario[0])

    cursor = None
    conn = None

    try:

        conn = connectar_banco()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM files WHERE id=%s", (id_exame,))
        exame = cursor.fetchone()

        if not exame:
            return jsonify({'mensagem': 'Exame não encontrado.'}), 404

        cursor.execute(
            "DELETE FROM files WHERE id=%s and id_usuario=%s", (id_exame, id_usuario))
        conn.commit()

        return jsonify({"mensagem": "Exame deletado com sucesso.", "id_deletado": id_exame}), 200

    except Exception:
        # print("Erro ao deletar exame do banco de dados:", e)
        return jsonify({'mensagem': 'Erro ao deletar o exame do banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def buscar_exames():
    """BUSCAR EXAMES NO BANCO DE DADOS FILTRO"""

    id_usuario = int(request.usuario[0])
    busca = request.args.get('busca')
    id_paciente = request.args.get('id')

    if id_paciente == 'null':
        id_paciente = None

    cursor = None
    conn = None

    try:
        # print("Buscar: ", busca, id_paciente)

        if id_paciente is not None:
            query = "SELECT * FROM files WHERE id_paciente = %s and id_usuario=%s"
            params = [id_paciente, id_usuario]
        else:
            query = "SELECT * FROM files WHERE id_usuario = %s"
            params = [id_usuario]

        if busca:
            query += " AND (nome_exame ILIKE %s OR id::text ILIKE %s OR data_exame::text ILIKE %s)"
            params.extend([f"%{busca}%", f"%{busca}%", f"%{busca}%"])

        conn = connectar_banco()
        cursor = conn.cursor()

        cursor.execute(query, params)
        exames = cursor.fetchall()

        conn.commit()

        if not exames:
            return jsonify({"mensagem": "Nenhum resultado encontrado."}), 404

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

        return jsonify(lista_objeto), 200

    except Exception:
        # print("Erro ao consultar o banco de dados:", e)
        return jsonify({'error': 'Erro ao consultar o banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_banco():
    """FAZER UM GET DOS DADOS NO BANCO PARA LISTA EXAMES"""

    id_usuario = int(request.usuario[0])
    id_paciente = request.args.get('id')

    if id_paciente == 'null':
        id_paciente = None

    cursor = None
    conn = None

    try:
        # Substitua as informações de conexão conforme necessário
        conn = connectar_banco()
        cursor = conn.cursor()

        if id_paciente is not None:
            cursor.execute(
                "SELECT * FROM files where id_paciente=%s and id_usuario=%s", (id_paciente, id_usuario))
        else:
            cursor.execute(
                "SELECT * FROM files where id_usuario=%s", (id_usuario,))

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

        # for item in result_list:
        #     print("id_r: ", item)

        return jsonify(result_list), 200

    except Exception:
        # print("Erro ao consultar o banco de dados:", e)
        return jsonify({'error': 'Erro ao consultar o banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_banco_exames():
    """FAZER UM GET DOS EXAMES DE DADOS NO BANCO PARA OS GRAFICOS"""

    id_usuario = int(request.usuario[0])
    id_paciente = request.args.get('id')
    if id_paciente == 'null':
        id_paciente = None

    cursor = None
    conn = None

    try:
        # Substitua as informações de conexão conforme necessário
        conn = connectar_banco()
        cursor = conn.cursor()

        if id_paciente is not None:
            cursor.execute(
                "SELECT * FROM files where id_paciente=%s and id_usuario=%s", (id_paciente, id_usuario))
        else:
            cursor.execute(
                "SELECT * FROM files where id_usuario=%s", (id_usuario,))

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

        lista_dados_novos = copy.deepcopy(lista_dados)

        get_dados_info(lista_dados_novos, result_list, funcao_or_dados)

        return jsonify(lista_dados_novos), 200

    except Exception as e:
        print("Erro ao consultar o banco de dados:", e)
        return jsonify({'error': 'Erro ao consultar o banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_dados_relatorio():
    """FAZER UM GET PARA O GRAFICO DAS ESTATÍSTICA"""

    id_usuario = int(request.usuario[0])
    id_paciente = request.args.get('id')
    if id_paciente == 'null':
        id_paciente = None

    conn = None

    try:
        conn = connectar_banco()
        with conn.cursor() as cursor:
            if id_paciente:
                cursor.execute(
                    "select * from relatorios where id_usuario=%s and id_paciente=%s", (id_usuario, id_paciente))
            else:
                cursor.execute(
                    "select * from relatorios where id_usuario=%s", (id_usuario,))

            row = cursor.fetchone()

            return jsonify(row), 200

    except Exception as e:
        print("Erro ao consultar o banco de dados:", e)
        return jsonify({'error': 'Erro ao consultar o banco de dados'}), 500
    finally:
        if conn:
            conn.close()


def get_banco_exames_exclusiva(id=None):
    """FAZER UM GET DOS EXAMES DE DADOS NO BANCO PARA OS GRAFICOS"""

    id_usuario = int(request.usuario[0])
    id_paciente = id

    if id_paciente:
        id_paciente = int(id_paciente)

    cursor = None
    conn = None

    try:
        # Substitua as informações de conexão conforme necessário
        conn = connectar_banco()
        cursor = conn.cursor()

        if id_paciente:
            cursor.execute(
                "SELECT * FROM files where id_paciente=%s and id_usuario=%s", (id_paciente, id_usuario))
        else:
            cursor.execute(
                "SELECT * FROM files where id_usuario=%s", (id_usuario,))

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

        lista_dados_novos = copy.deepcopy(lista_dados)

        get_dados_info(lista_dados_novos, result_list, funcao_or_dados)
        valor_max_min_med(lista_dados_novos)

        return [lista_dados_novos, len(rows)]

    except Exception as e:
        print("Erro ao consultar o banco de dados:", e)
        return jsonify({'error': 'Erro ao consultar o banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
