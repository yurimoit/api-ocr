list_captura_dados = [{'nome': 'hemacias', 'valorPR': '--', 'valoRA': '--', 'valorB': '--', 'unidade': '10⁶/mm³'},
                      {'nome': 'hemoglobina', 'valorPR': '--',
                          'valoRA': '--', 'valorB': '--', 'unidade': 'g/dl'},
                      {'nome': 'hematocrito', 'valorPR': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '%'},
                      {'nome': 'vcm', 'valorPR': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': 'fl'},
                      {'nome': 'hcm', 'valorPR': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': 'pg'},
                      {'nome': 'chcm', 'valorPR': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': 'g/dl'},
                      {'nome': 'rdw', 'valorPR': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '%'},
                      {'nome': 'leucocitos - global', 'valorPR': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '/mm³'},
                      {'nome': 'neutrofilos bastonetes', 'valorPR': '--', 'mm3': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '%'},
                      {'nome': 'neutrofilos segmentados', 'valorPR': '--', 'mm3': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '%'},
                      {'nome': 'linfocitos', 'valorPR': '--', 'mm3': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '%'},
                      {'nome': 'monocitos', 'valorPR': '--', 'mm3': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '%'},
                      {'nome': 'eosinofilos', 'valorPR': '--', 'mm3': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '%'},
                      {'nome': 'basafilos', 'valorPR': '--', 'mm3': '--', 'valoRA': '--',
                          'valorB': '--', 'unidade': '%'},
                      {'nome': 'plaquetas', 'valorPR': '--', 'valoRA': '--', 'valorB': '--', 'unidade': '/mm³'}]


lista_informacoes_buscada = ['hemacias',
                             'hemoglobina',
                             'hematocrito',
                             'vcm',
                             'hcm',
                             'chcm',
                             'rdw',
                             'leucocitos - global',
                             'neutrofilos bastonetes',
                             'neutrofilos segmentados',
                             'linfocitos',
                             'monocitos',
                             'eosinofilos',
                             'basafilos',
                             'plaquetas']


lista_dados = {
    'hemacias': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'hemoglobina': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'hematocrito': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'vcm': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },

    'hcm': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'chcm': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'rdw': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'leucocitos - global': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'neutrofilos bastonetes': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'neutrofilos segmentados': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'linfocitos': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'monocitos': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'eosinofilos': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'basafilos': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    },
    'plaquetas': {
        'lista_dados': [],
        'lista_dados_inferior': [],
        'lista_dados_superior': [],
        'lista_datas': [],
        'dados_referencia': {
            "maior_valor": 0,
            "menor_valor": 0,
            "media": 0,
            "registro_maior_valor": "0000-00-00",
            "registro_menor_valor": "0000-00-00",
            "periodo_analisado": [],
        },
    }
}
