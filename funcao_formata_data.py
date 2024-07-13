"""Module providing a function printing python version."""
from datetime import datetime
import copy
from xmlrpc.client import Boolean


def format_date(date_string):
    """SEM EXPLICAÇÃO"""

    date_string = str(date_string)
    date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
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

    return data_formatada


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
        print("Erro ao determina datas: ", e)
