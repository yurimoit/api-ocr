import copy
from funcao_formata_data import determina_data_maior_menor


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


def get_valores_maior_menor_media(lista_dados, indice_data_maior, indice_data_menor, maior_valor, menor_valor, media):
    """SEM EXPLICAÇÃO"""

    total_valores = len(lista_dados)
    soma = 0

    for indice, item in enumerate(lista_dados):
        item = float(item)

        if maior_valor <= item:
            maior_valor = item
            indice_data_maior = indice

        if menor_valor >= item:
            menor_valor = item
            indice_data_menor = indice

        soma += item

    media = round(soma/total_valores, 2)

    return [maior_valor, menor_valor, media, indice_data_maior, indice_data_menor]


def valor_max_min_med(lista_dados: dict):
    """SEM EXPLICAÇÃO"""

    try:
        for key in lista_dados.keys():
            maior_valor = 0
            menor_valor = 0
            media = 0
            total_valores = len(lista_dados[key]["lista_dados"])
            lista_datas = copy.deepcopy(lista_dados[key]["lista_datas"])

            if total_valores < 1:
                lista_dados[key]["dados_referencia"] = {
                    "maior_valor": 0,
                    "menor_valor": 0,
                    "media": 0,
                    "registro_maior_valor": "0000-00-00",
                    "registro_menor_valor": "0000-00-00",
                    "periodo_analisado": "0000-00-00",
                }
                continue

            datas = determina_data_maior_menor(lista_datas)

            primeiro_valor = copy.deepcopy(
                float(lista_dados[key]["lista_dados"][0]))

            maior_valor = primeiro_valor
            menor_valor = primeiro_valor
            indice_data_maior = 0
            indice_data_menor = 0

            resutado_referencia = get_valores_maior_menor_media(
                lista_dados=lista_dados[key]["lista_dados"],
                indice_data_maior=indice_data_maior,
                indice_data_menor=indice_data_menor,
                maior_valor=maior_valor,
                menor_valor=menor_valor,
                media=media)

            indice_data_maior = resutado_referencia[3]
            indice_data_menor = resutado_referencia[4]

            lista_dados[key]["dados_referencia"] = {
                "maior_valor": resutado_referencia[0],
                "menor_valor": resutado_referencia[1],
                "media": resutado_referencia[2],
                "registro_maior_valor": str(lista_datas[indice_data_maior]),
                "registro_menor_valor": str(lista_datas[indice_data_menor]),
                "periodo_analisado": datas,
            }

    except Exception as e:
        print("Error valor maz e min: ", e)


def verifica_lista(lista):
    """SEM EXPLICAÇÃO"""

    value = len(lista)
    match value:
        case 2:
            return [lista[0], lista[1], 0]
        case 1:
            return [lista[0], 0, 0]
        case 0:
            return [0, 0, 0]
        case _:
            return [lista[-1], lista[-2], lista[-3]]


def ordena_novo_json(json_dados):
    """SEM EXPLICAÇÃO"""

    novo_json_dados = {}
    data_1=''
    data_2=''
    data_3=''
    data_primeiro_registro=''
    data_ultimo_registro=''

    verifica=True

    for item in json_dados.items():
        item = list(item)

        if verifica:
            data_1=verifica_lista(item[1]['lista_datas'])[0]
            data_2=verifica_lista(item[1]['lista_datas'])[1]
            data_3=verifica_lista(item[1]['lista_datas'])[2]
            data_primeiro_registro=item[1]['dados_referencia']["periodo_analisado"][0]
            data_ultimo_registro=item[1]['dados_referencia']["periodo_analisado"][1]
            verifica=False

        novo_json_dados[f'{item[0]}'] = {
            'lista_dados': verifica_lista(item[1]['lista_dados']),
            'lista_datas': verifica_lista(item[1]['lista_datas']),
            'dados_referencia': {
                "maior_valor": item[1]['dados_referencia']["maior_valor"],
                "menor_valor":  item[1]['dados_referencia']["menor_valor"],
                "media":  item[1]['dados_referencia']["media"],
                "data_maior_valor":  item[1]['dados_referencia']["registro_maior_valor"],
                "data_menor_valor":  item[1]['dados_referencia']["registro_menor_valor"],
                "periodo_analisado": item[1]['dados_referencia']["periodo_analisado"],
            },
        }

    return {
        "dados_estatistico":novo_json_dados,
        "data_1":data_1,
        "data_2":data_2,
        "data_3":data_3,
        "data_primeiro_registro":data_primeiro_registro,
        "data_ultimo_registro":data_ultimo_registro,
    }


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
