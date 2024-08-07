# pylint: disable=missing-function-docstring
"""Module providing a function printing python version."""
from datetime import datetime
import copy


def format_date(date_string, format_strind_data='%Y-%m-%d'):
    """SEM EXPLICAÇÃO"""

    date_string = str(date_string)
    date = datetime.strptime(date_string, format_strind_data)
    year = date.year
    month = f'{date.month:02}'
    day = f'{date.day:02}'

    return f'{year}-{month}-{day}'


def formataData(data: str):
    """Formata data"""
    if not data:
        return datetime.now()

    data_list = data.split('-')

    data_list_mes = data_list[1] if data_list[1][0] != '0' else data_list[1][1]

    data_formatada = datetime(int(data_list[0]), int(
        data_list_mes), int(data_list[2]))

    return data_formatada.date()


def determina_data_maior_menor(result_list):
    try:
        lista_datas = []
        for item in result_list:
            data = formataData(item)
            lista_datas.append(data)

        maior_data = copy.deepcopy(lista_datas[0])
        menor_data = copy.deepcopy(lista_datas[0])
        for item in lista_datas:
            if maior_data <= item:
                maior_data = item

            if menor_data >= item:
                menor_data = item

        return [format_date(menor_data),  format_date(maior_data)]
    except Exception as e:
        print("Erro ao determina datas yu: ", e)


def ordenar_valores_p_data(lista_data, lista_valores):

    lista_datas=[formataData(data) for data in lista_data]
    lista_resultado_final=[]
    lista_datas_final=[]
    lista_valores_final=[]


    for data in lista_datas:
        for valor in lista_valores:
            lista_resultado_final.append([data, valor])
        
    sorted_datas = sorted(lista_resultado_final, key=lambda data: data[0])

    for item in sorted_datas:
        lista_datas_final.append(item[0])
        lista_valores_final.append(item[1])

           
    lista_ordenada_datas=[format_date(data) for data in lista_datas_final] 
    return [lista_ordenada_datas, lista_valores_final]    

  
  
  
def ordenar_valores_paranalisador_p_data( lista_g_certeza, lista_g_incerteza,lista_resultados, lista_data):


    lista_datas=lista_data
    lista_final_datas=[]
    lista_final_valores_su=[]
    lista_final_valores_in=[]
    lista_final_resultados=[]
    lista_dados_final=[]

    for i, data in enumerate(lista_datas):
        lista_dados_final.append([data, lista_g_certeza[i], lista_g_incerteza[i], lista_resultados[i]])
        
    sorted_datas=sorted(lista_dados_final, key=lambda data:data[0])

    for dado in sorted_datas:
        lista_final_datas.append(dado[0])
        lista_final_valores_su.append(dado[1])
        lista_final_valores_in.append(dado[2])
        lista_final_resultados.append(dado[3])

    lista_ordenada_datas=[format_date(data) for data in lista_final_datas] 

    return [lista_ordenada_datas, lista_final_valores_su, lista_final_valores_in, lista_final_resultados] 


def ordenar_dados_lista(dicionario):

    for dado in dicionario.values():
        lista_dados_ordenados=ordenar_exames_p_data(dado['lista_datas'], dado['lista_dados_superior'], dado['lista_dados_inferior'],  dado['lista_dados'] )
        dado['lista_datas']=lista_dados_ordenados[0]
        dado['lista_dados_superior']=lista_dados_ordenados[1]
        dado['lista_dados_inferior']=lista_dados_ordenados[2]
        dado['lista_dados']=lista_dados_ordenados[3]


def ordenar_exames_p_data(lista_data, lista_valores_superiores, lista_valores_inferiores, lista_valores):
    
    lista_datas=[formataData(data) for data in lista_data]
    lista_resultado_final=[]
    lista_valores_superior=[]
    lista_valores_inferior=[]
    lista_datas_final=[]
    lista_valores_final=[]

    for i, data in enumerate(lista_datas):
            lista_resultado_final.append([data, lista_valores_superiores[i], lista_valores_inferiores[i], lista_valores[i]])

    sorted_datas = sorted(lista_resultado_final, key=lambda data: data[0])

    for item in sorted_datas:
        lista_datas_final.append(item[0])
        lista_valores_superior.append(item[1])
        lista_valores_inferior.append(item[2])
        lista_valores_final.append(item[3])
 
      
    lista_ordenada_datas=[format_date(data) for data in lista_datas_final]  

    return [lista_ordenada_datas, lista_valores_superior, lista_valores_inferior, lista_valores_final]
       