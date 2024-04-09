
def funcao_or_dados(lista, exame, data, nome_exame):
    """SEM EXPLICAÇÃO"""

    lista_r = lista
    exame_r = exame
    nome_exame_r = nome_exame
    data_r = data

    def funcao_organiza(lista, exame, data, nome_exame):
        lista[nome_exame]['lista_dados_inferior'].append(
            exame['valoRA'])
        lista[nome_exame]['lista_dados_superior'].append(
            exame['valorB'])
        lista[nome_exame]['lista_datas'].append(
            str(data))

        if 'mm3' in exame.keys():
            lista[nome_exame]['lista_dados'].append(
                exame['mm3'])

            return

        lista[nome_exame]['lista_dados'].append(
            exame['valorPR'])

    return funcao_organiza(lista_r, exame_r, data_r, nome_exame_r)


def get_dados_info(lista_dados_novos, resulatdo_lista, funcao_organiza):
    """SEM EXPLICAÇÃO"""

    for exame in resulatdo_lista:
        for item in exame['lista_dados']:

            if item['nome'] == 'hemacias':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'hemacias')
            if item['nome'] == 'hemoglobina':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'hemoglobina')
            if item['nome'] == 'hematocrito':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'hematocrito')
            if item['nome'] == 'vcm':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'vcm')
            if item['nome'] == 'hcm':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'hcm')
            if item['nome'] == 'chcm':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'chcm')
            if item['nome'] == 'rdw':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'rdw')
            if item['nome'] == 'leucocitos - global':
                funcao_organiza(lista_dados_novos, item, exame['data_exame'],
                                'leucocitos - global')
            if item['nome'] == 'neutrofilos bastonetes':
                funcao_organiza(lista_dados_novos, item, exame['data_exame'],
                                'neutrofilos bastonetes')
            if item['nome'] == 'neutrofilos segmentados':
                funcao_organiza(lista_dados_novos, item, exame['data_exame'],
                                'neutrofilos segmentados')
            if item['nome'] == 'linfocitos':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'linfocitos')
            if item['nome'] == 'monocitos':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'monocitos')
            if item['nome'] == 'eosinofilos':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'eosinofilos')
            if item['nome'] == 'basafilos':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'basafilos')
            if item['nome'] == 'plaquetas':
                funcao_organiza(lista_dados_novos, item,
                                exame['data_exame'], 'plaquetas')
