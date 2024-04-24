"""Module providing a function printing python version."""
from datetime import datetime


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
