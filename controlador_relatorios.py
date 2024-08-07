# pylint: disable=missing-function-docstring
"""Module providing a function printing python version."""
from __future__ import annotations

import json
import copy
from flask import request, jsonify

from conexao_banco_dados import connectar_banco
from listas.controlado_dados_lista import ordena_novo_json
from listas.controlado_dados_lista import get_dados_info, funcao_or_dados
from listas.controlado_dados_lista import  valor_max_min_med
from listas.lista_exame_hemograma import lista_dados


def inserir_relatorio_no_banco_dados(id_p, nome_paciente, data_nascimento, sexo):
    """ATUALIZA EXAME"""
    
    id_paciente=id_p
    id_usuario = int(request.usuario[0])

    cursor = None
    conn = None


    try:
        conn = connectar_banco()

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
                    """INSERT INTO relatorios
                    (nome_paciente, data_nascimento, sexo, data_1, data_2, data_3, data_primeiro_registro, data_ultimo_registro,
                     lista_dados, id_usuario, id_paciente)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (nome_paciente, data_nascimento, sexo,
                    data_1, data_2, data_3, data_primeiro_registro,
                    data_ultimo_registro, novos_json_dados, id_usuario, id_paciente))
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

                
        return jsonify({"mensagem": "Atualização realizada com sucesso."}), 201
    

    except Exception as e:
        print(f"Erro inserir relatorio no banco de dados: {e}")
        return jsonify({'mensagem': "Erro no servidor na inserção de dados"}), 500
    finally:
        if conn:
            conn.close()

def atualiza_relatorio_no_banco_dados(id_p):
    """ATUALIZA EXAME"""
    
    id_paciente=id_p
    id_usuario = int(request.usuario[0])


    cursor = None
    conn = None


    try:
        conn = connectar_banco()

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

        print("Atualizou relatorio")        
        return jsonify({"mensagem": "Atualização realizada com sucesso."}), 201
    

    except Exception as e:
        print(f"Erro atualiza relatorio no banco de dados: {e}")
        return jsonify({'mensagem': "Erro no servidor na atualização de dados"}), 500

    finally:
        if conn:
            conn.close()


def deletar_relatorio_no_banco_dados(id_paciente):
    """DELETAR EXAME DO BANCO DE DADOS"""

    id_p=id_paciente
    id_usuario = int(request.usuario[0])

    if not id_paciente or id_paciente=="null":
        id_p=int(request.usuario[0])

    cursor = None
    conn = None

    try:

        conn = connectar_banco()

        with conn.cursor() as cursor:
            if id_paciente:
                cursor.execute("SELECT * FROM relatorios WHERE id_paciente=%s and id_usuario=%s", (id_p, id_usuario))
            else:
                cursor.execute("SELECT * FROM relatorios WHERE id_usuario=%s", (id_usuario,))

            dados_relatorio = cursor.fetchone()

            if not dados_relatorio:
               return jsonify({'mensagem': 'Exame não encontrado.'}), 404
            
            lista_gerada = list(dados_relatorio)
            id_relatorio = lista_gerada[0]
            
            cursor.execute(
                "DELETE FROM relatorios WHERE id=%s", (id_relatorio, ))
            
            conn.commit()

        return jsonify({"mensagem": "Relatorio deletado com sucesso.", "id_deletado": id_relatorio}), 200

    except Exception as e:
        print("Erro ao deletar relatorio do banco de dados Paranalisador:", {str(e)})
        return jsonify({'mensagem': 'Erro ao deletar relatorio do exame do banco de dados'}), 500
    finally:
        if conn:
            conn.close()


def get_banco_exames_exclusiva(id_p=None):
    """FAZER UM GET DOS EXAMES DE DADOS NO BANCO PARA OS GRAFICOS"""

    id_usuario = int(request.usuario[0])
    id_paciente = None

    if id_p!="null" and id_p:
       id_paciente = int(id_p)

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