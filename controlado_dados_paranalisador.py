# pylint: disable=missing-function-docstring
"""Module providing a function printing python version."""
from __future__ import annotations
import copy


from flask import request, jsonify

from conexao_banco_dados import connectar_banco
from funcao_formata_data import ordenar_valores_paranalisador_p_data

def determinar_resultado_paranalisado(valor_H, valor_G):
    
    #           H                     G
    if (-0.4<=valor_H<=0.4) and (-1<=valor_G<=-0.6):
       return "P-ID"
    if (-0.4<=valor_H<=0.4) and (0.6<=valor_G<=1):
       return "IN"
    if (0.6<=valor_H<=1) and (-0.4<=valor_G<=0.4):
       return "V"
    if (-1<=valor_H<=-0.6) and (-0.4<=valor_G<=0.4):
       return "F"
    if (0<=valor_H<0.6) and (0<=valor_G<0.6):
       return "QT -> V | QV -> T"
    if (0<=valor_H<0.6) and (-0.6<valor_G<0):
       return "QV -> ID | QID -> V"
    if (-0.6<valor_H<0) and (-0.6<valor_G<0):
       return "ID -> F | QF -> ID"
    if (-0.6<valor_H<0) and (0<=valor_G<0.6):
       return "QF -> T | QT -> F"
   
    return "AG-IN"
   

def inserir_dados_paranalisador(lista, data, id_paciente, id_exame):

    id_usuario = int(request.usuario[0])
    valor_certeza=lista[0]
    valor_incerteza=lista[1]
    grau_certeza=valor_certeza-valor_incerteza
    
    try:
        abs_certeza=round(grau_certeza,2)
        grau_incerteza=(valor_certeza+valor_incerteza)-1
        abs_incerteza=round(grau_incerteza,2)

        resultado=determinar_resultado_paranalisado(grau_certeza, grau_incerteza)

        conn = connectar_banco()

        with conn.cursor() as cursor:
            if id_paciente:
                cursor.execute("""INSERT INTO dados_paranalisador
                               (
                                 valor_certeza, 
                                 valor_incerteza, 
                                 h_certeza, 
                                 g_incerteza, 
                                 resultado, 
                                 data_exame,
                                 id_exame, 
                                 id_usuario, 
                                 id_paciente
                               )
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                               """, (valor_certeza, valor_incerteza, abs_certeza, abs_incerteza, resultado, data, id_exame,  id_usuario , id_paciente ))
                
                conn.commit()
            else:
                 cursor.execute("""INSERT INTO dados_paranalisador
                               (
                                 valor_certeza, 
                                 valor_incerteza, 
                                 h_certeza, 
                                 g_incerteza, 
                                 resultado, 
                                 data_exame,
                                 id_exame,  
                                 id_usuario, 
                               )
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                               """, (valor_certeza, valor_incerteza, abs_certeza, abs_incerteza, resultado, data, id_exame, id_usuario )) 
                 
                 conn.commit()
         

        return jsonify({"mensagem": "Inserido realizada com sucesso."}), 201
    
    except Exception as e:
        print(f"Erro inserir dados no banco Paranalisador: {str(e)}")
        return jsonify({'mensagem': "Erro no servidor"}), 500
    finally:
        if conn:
            conn.close()    


def atualizar_dados_paranalisador(lista, data, id_exame):

    valor_certeza=lista[0]
    valor_incerteza=lista[1]
    grau_certeza=valor_certeza-valor_incerteza
    
    try:
        abs_certeza=round(grau_certeza,2)
        grau_incerteza=(valor_certeza+valor_incerteza)-1
        abs_incerteza=round(grau_incerteza,2)

        resultado=determinar_resultado_paranalisado(grau_certeza, grau_incerteza)

        conn = connectar_banco()

        with conn.cursor() as cursor:
            cursor.execute("""UPDATE dados_paranalisador
                               
                            SET
                                 valor_certeza=%s, 
                                 valor_incerteza=%s, 
                                 h_certeza=%s, 
                                 g_incerteza=%s, 
                                 resultado=%s,
                                 data_exame=%s
                           WHERE
                                 id_exame=%s 
                                 
                               RETURNING *;""", (valor_certeza, valor_incerteza, abs_certeza, abs_incerteza, resultado, data, id_exame ))
                
            conn.commit()

            return jsonify({"mensagem": "Atualização realizada com sucesso."}), 201

    except Exception as e:
        print(f"Erro atualizar dados no banco Paranalisador: {str(e)}")
        return jsonify({'mensagem': "Erro no servidor"}), 500
    finally:
        if conn:
            conn.close()  


def deletar_dados_paranalisador(id):
    """DELETAR EXAME DO BANCO DE DADOS"""

    id_exame = int(id)
    cursor = None
    conn = None

    try:

        conn = connectar_banco()

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dados_paranalisador WHERE id_exame=%s", (id_exame,))
            dados_exame = cursor.fetchone()

            if not dados_exame:
               return jsonify({'mensagem': 'Exame não encontrado.'}), 404
            
            cursor.execute(
                "DELETE FROM dados_paranalisador WHERE id_exame=%s", (id_exame, ))
            
            conn.commit()

        return jsonify({"mensagem": "Dados exame deletado com sucesso.", "id_deletado": id_exame}), 200

    except Exception as e:
        print("Erro ao deletar exame do banco de dados Paranalisador:", {str(e)})
        return jsonify({'mensagem': 'Erro ao deletar o dados do exame do banco de dados'}), 500
    finally:
        if conn:
            conn.close()        


def get_dados_paranalisador():
    
    id_usuario = int(request.usuario[0])
    id_paciente = request.args.get('id_paciente')
    
    if not id_paciente or id_paciente=="null":
        id_paciente=None

    cursor = None
    conn = None

    try:

        conn = connectar_banco()

        with conn.cursor() as cursor:
            if id_paciente:
                cursor.execute("SELECT * FROM dados_paranalisador WHERE id_paciente=%s AND id_usuario=%s", (id_paciente, id_usuario))
            else:
                cursor.execute("SELECT * FROM dados_paranalisador WHERE id_usuario=%s", (id_usuario, ))

            dados_paranalisador = cursor.fetchall()

            if not dados_paranalisador:
               return jsonify({'mensagem': 'Exame não encontrado.'}), 404
            
            lista_valor_g_certeza=[]
            lista_valor_g_incerteza=[]
            lista_datas=[]
            lista_resultados=[]

            lista_dados=list(dados_paranalisador)
            for item in lista_dados:
                item=list(item)
                lista_valor_g_certeza.append(float(item[3]))
                lista_valor_g_incerteza.append(float(item[4]))
                lista_resultados.append(item[5])
                lista_datas.append(item[6])

            
            lista_final_dados=ordenar_valores_paranalisador_p_data(lista_valor_g_certeza, lista_valor_g_incerteza, lista_resultados, lista_datas)    
            objeto_dados={
                "lista_datas":lista_final_dados[0],
                "lista_valores_grau_certeza":lista_final_dados[1],
                "lista_valores_grau_incerteza":lista_final_dados[2],
                "lista_resultados":gera_dados_grafico_paranalisador(lista_final_dados[3]),
            }
            conn.commit()

        return jsonify(objeto_dados), 200

    except Exception as e:
        print("Erro ao fazer o GET exame do banco de dados Paranalisador:", {str(e)})
        return jsonify({'mensagem': 'Erro ao GET do dados do exame do banco de dados'}), 500
    finally:
        if conn:
            conn.close() 


def gera_dados_grafico_paranalisador(lista):
    
    lista_nova=list(set(lista))
    lista_last_itens=copy.copy(lista_nova)
    lista_parametros=["0.1","0.1","0.1","0.1","0.1","0.1","0.1","0.1",]

    if len(lista_nova)>=6:
        lista_last_itens=lista_nova[-1:-6]  
    
    for item in lista_last_itens:
        match item:
            case "V":
                lista_parametros[2]="0.6"
            case "F":
                lista_parametros[6]="0.6"  
            case "P-ID":
                lista_parametros[0]="0.6"    
            case "IN":
                lista_parametros[4]="0.6" 
            case "QT -> V | QV -> T":
                lista_parametros[1]="0.6"   
            case "QV -> ID | QID -> V":
                lista_parametros[3]="0.6"   
            case "ID -> F | QF -> ID":
                lista_parametros[5]="0.6"   
            case "QF -> T | QT -> F":
                lista_parametros[7]="0.6"   
            case _:
                ...

    
    return lista_parametros
