"""Module providing a function printing python version."""
import re
import copy
from difflib import SequenceMatcher
from flask import jsonify

texto_capturado = """
 Nome
LABORATORIO
Paulo C.
Azevedo
VALDA MARIA DOS REIS SILVA
Solicitante
Av. Braz de Aguiar, 99
Belem-PA CEP 66035-385
RT-lan Eliezer Levy-CRBM-4: 1076
CNPJ 04 078 805 0001-45
Registro N° 1358 PJ do CRBU
CNES 0004771
Central Atendimento: (91) 4009-8889
Data de Nascimento
3/11
01/05/1971 (52 anos)
Dala Entrada Pedido
JAIRA ATAIDE DOS SANTOS DE BRITO FILHA - CRM-PA 14063 28/12/2023 7012094-LPCNF
MATERIAL-SANGUE
HEMOGRAMA
[DATA DA COLETA: 28/12/2023 07:33] COLETA DE AMOSTRA REALIZADA PELO LABORATORIO PAULO AZEVEDO
METODO: CONTAGEM AUTOMATIZADA ATRAVES DE CITOMETRIA DE FLUXO
Hemacias 4.710.000/mm3
Hemoglobina: 14,4 g/dl
Hematocrito:
VCM: 87,9 fl
HCM: 30,6 pg
CHCM: 34,8 g/dl
RDW: 11,9%
Leucocitos Global:
41,4%
Neutrofilos Bastonetes: 0,0%
Neutrofilos Segmentados: 57,6 %
:36,0%
Linfocitos
Monocitos
: 5,3%
Eosinofilos
: 0,7%
Basofilos
: 0,4%
Plaquetas: 235.000/mm3
VALORES DE REFERENCIA
3.800.000 A 4.800.000/mm3
12,0 A 16,0 g/dl
36,0 A 46,0 %
80,0 A 100,0 £1
26,0 A 32,0 pg
32,0 A 36,0 g/dl
11,5 A 14,8 %
5.700/mm3 4.000 A 11.000/mm3
0/mm3 ATE 840/mm3
3.290/mm3 || 2.000 A 7.000/mm3
2.050/mm3|| 1.000 A 3.500/mm3
300/mm3 200 A 1.000/mm3
40/mm3 20 A 500/mm3
20/mm3||ATE 200/mm3
||150.000 A 450.000/mm3
Da Impresso: 11/01/24
"""

lista_informacoes_buscada = ['hemacias',
                             'hemoglobina',
                             'hematocrito',
                             'vcm',
                             'hcm',
                             'chcm',
                             'rdw',
                             'linfocitos',
                             'monocitos',
                             'eosinofilos',
                             'basafilos',
                             'plaquetas']

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


def analisador_palavra(info, dado, contador):
    """"""

    for palavra in info:
        comparador = SequenceMatcher(
            None,   palavra, (dado.lower()).replace('á', 'a'))

        # Obtendo a semelhança entre as duas palavras
        semelhanca = comparador.ratio()
        if semelhanca >= 0.6:
            dado = info[contador]
            break

    return dado


def verifica_nome(dicionario, info, contador):
    """"""
    if (dicionario['nome'] == info[contador]):
        print(dicionario['nome'], info[contador])
        return True

    return False


def analisa_dados(dados, informacoes_buscada, list_captura_dados):
    """Separa e analisa dados"""

    try:
        info = copy.copy(informacoes_buscada)
        lista_palavras_compostas = ['leucocitos - global',
                                    'neutrofilos bastonetes', 'neutrofilos segmentados']
        lista_dados = copy.deepcopy(list_captura_dados)
        lista_frases = dados.lower().splitlines()

        semelhanca_rr = 0
        lista_referencia = []

        for i, bloco in enumerate(lista_frases):
            lista_dados_bloco = bloco.strip().split(' ')

            comparador = SequenceMatcher(
                None,   'valores de referencia', (bloco).replace(":", "").replace('ê', 'e'))
            semelhanca_rr = comparador.ratio()

            if semelhanca_rr >= 0.6:
                lista_referencia = lista_frases[lista_frases.index(
                    bloco)+1:lista_frases.index(bloco)+15]

                # print(lista_referencia)

            if not (1 < len(lista_dados_bloco) < 4):
                continue

            palavra_p = ''
            verificado_palavra = False
            semelhanca = 0
            semelhanca_2 = 0

            for palavra in lista_palavras_compostas:
                comparador = SequenceMatcher(
                    None,   palavra, (lista_dados_bloco[0]+" "+lista_dados_bloco[1]).replace(":", "").replace('á', 'a'))
                semelhanca_2 = comparador.ratio()

                if semelhanca_2 >= 0.6:
                    palavra_p = palavra
                    verificado_palavra = True
                    break

            if semelhanca_2 < 0.6:
                for palavra_padrao in info:
                    comparador = SequenceMatcher(
                        None,   palavra_padrao, (lista_dados_bloco[0]).replace(":", "").replace('á', 'a'))
                    semelhanca = comparador.ratio()

                    if semelhanca >= 0.6:
                        palavra_p = palavra_padrao
                        info.remove(palavra_padrao)
                        break

            if semelhanca < 0.6 and semelhanca_2 < 0.6:
                continue

            for dicionario in lista_dados:

                if (dicionario['nome'] == palavra_p) and verificado_palavra:
                    if len(lista_dados_bloco) > 2:
                        dicionario['valorPR'] = remover_unidades(
                            lista_dados_bloco[2])
                        break
                    dicionario['valorPR'] = '--'
                    break

                if dicionario['nome'] == palavra_p:
                    dicionario['valorPR'] = remover_unidades(
                        lista_dados_bloco[1])

        return [lista_dados, lista_referencia]
    except Exception:
        return jsonify({'mensagem': "Erro no servidor"}), 500


def separa_dados_referencia(lista_referencia):

    try:
        lista = copy.copy(lista_referencia)

        lista_fatorada = []

        for item in lista:
            if 'ate' in item:
                v4 = item.strip().split('a')
                lista_fatorada.append([*v4])
                continue

            if '||' in item:
                v1 = item.strip().split('||')
                v2 = (v1[1]).strip().split('a')
                lista_fatorada.append([v1[0], *v2])
                continue

            v3 = item.strip().split('a')

            if ' ' in v3[0]:
                v5 = v3[0].split(' ')
                lista_fatorada.append([v5[0], v5[1], v3[1]])
                continue

            lista_fatorada.append([*v3])

        for itens in lista_fatorada:
            for item in itens:
                if item == '':
                    itens.remove(item)

        return lista_fatorada
    except Exception:
        return jsonify({'mensagem': "Erro no servidor"}), 500


def remover_unidades(item):

    try:
        padrao = r'\b(?:/mm3|g/dl|%,|pg|£1|\|\||te|\.| ?%|fl)\b'

        itens_limpos = re.sub(padrao, '', item)
        itens_limpos = itens_limpos.replace('||', '')
        itens_limpos = itens_limpos.replace('%', '')
        itens_limpos = itens_limpos.replace('£1', '')
        itens_limpos = itens_limpos.strip()
        itens_limpos = itens_limpos.replace(',', '.')

        return itens_limpos
    except Exception:
        return jsonify({'mensagem': "Erro no servidor"}), 500


def classifica_dados(lista_fatorada, list_captura_dados):
    """"""
    try:
        lista = copy.deepcopy(lista_fatorada)
        lista_2 = copy.deepcopy(lista_fatorada)
        lista_dados = copy.deepcopy(list_captura_dados)

        for itens in lista:
            for item in itens:
                if '/mm3' in item:
                    item = remover_unidades(item)

                    # Hemacias------------------------------------------
                    if len(item) > 7 and float(item) > 3000000:
                        itens[0] = remover_unidades(itens[0])
                        lista_dados[0]['valoRA'] = str(float(itens[0])/10**6)
                        lista_dados[0]['valorB'] = str(float(item)/10**6)
                        break

                    if 3.8 <= float(item) <= 6.5:
                        itens[0] = remover_unidades(itens[0])
                        lista_dados[0]['valoRA'] = str(float(itens[0])/10**6)
                        lista_dados[0]['valorB'] = str(float(item)/10**6)
                        break

                    # Leuocitos Global---------------------------------

                    if 10000 <= float(item) <= 15000:
                        if len(itens) > 2:
                            itens[0] = remover_unidades(itens[0])
                            itens[1] = remover_unidades(itens[1])
                            lista_dados[7]['valorPR'] = itens[0]
                            lista_dados[7]['valoRA'] = itens[1]
                            lista_dados[7]['valorB'] = item
                        else:
                            itens[0] = remover_unidades(itens[0])
                            lista_dados[7]['valoRA'] = itens[0]
                            lista_dados[7]['valorB'] = item

                        break

                    # Neutrofilos bastonetes-----------------------------
                    if float(item) == 0:
                        itens[1] = remover_unidades(itens[1])
                        lista_dados[8]['valoRA'] = item
                        lista_dados[8]['valorB'] = itens[1]
                        break

                    # Neutrofilos Segmentados-----------------------------
                    if 4000 <= float(item) <= 7000:

                        itens[len(itens) -
                              2] = remover_unidades(itens[len(itens)-2])
                        if float(itens[len(itens)-2]) > 3000:
                            continue

                        if len(itens) > 2:
                            itens[0] = remover_unidades(itens[0])
                            itens[1] = remover_unidades(itens[1])
                            itens[2] = remover_unidades(itens[2])
                            lista_dados[9]['mm3'] = itens[0]
                            lista_dados[9]['valoRA'] = itens[1]
                            lista_dados[9]['valorB'] = itens[2]
                        else:
                            itens[0] = remover_unidades(itens[0])
                            lista_dados[9]['valoRA'] = itens[0]
                            lista_dados[9]['valorB'] = item
                        break

                    # Linfocitos----------------------
                    if float(item) == 3500 or float(item) == 2500:

                        itens[len(itens) -
                              2] = remover_unidades(itens[len(itens)-2])
                        if not (1000 <= float(itens[len(itens)-2]) <= 1200):
                            continue

                        if len(itens) > 2:
                            itens[0] = remover_unidades(itens[0])
                            itens[1] = remover_unidades(itens[1])
                            itens[2] = remover_unidades(itens[2])
                            lista_dados[10]['mm3'] = itens[0]
                            lista_dados[10]['valoRA'] = itens[1]
                            lista_dados[10]['valorB'] = itens[2]
                        else:
                            itens[0] = remover_unidades(itens[0])
                            lista_dados[10]['valoRA'] = itens[0]
                            lista_dados[10]['valorB'] = item
                        break

                    # Monocitos-------------------------------------------
                    if float(item) <= 1000:
                        itens[len(itens) -
                              2] = remover_unidades(itens[len(itens)-2])
                        if (80 <= float(itens[len(itens)-2]) <= 200):
                            if len(itens) > 2:
                                itens[0] = remover_unidades(itens[0])
                                itens[1] = remover_unidades(itens[1])
                                itens[2] = remover_unidades(itens[2])
                                lista_dados[11]['mm3'] = itens[0]
                                lista_dados[11]['valoRA'] = itens[1]
                                lista_dados[11]['valorB'] = itens[2]

                            else:
                                itens[0] = remover_unidades(itens[0])
                                lista_dados[11]['valoRA'] = itens[0]
                                lista_dados[11]['valorB'] = item

                            break

                    # Eosinofilos --------------------------------------------
                    if float(item) == 500 or float(item) == 300:
                        if len(itens) > 2:
                            itens[0] = remover_unidades(itens[0])
                            itens[1] = remover_unidades(itens[1])
                            itens[2] = remover_unidades(itens[2])
                            lista_dados[12]['mm3'] = itens[0]
                            lista_dados[12]['valoRA'] = itens[1]
                            lista_dados[12]['valorB'] = itens[2]
                        else:
                            itens[0] = remover_unidades(itens[0])
                            lista_dados[12]['valoRA'] = itens[0]
                            lista_dados[12]['valorB'] = item
                        break

                    # Basofilos --------------------------------------------
                    if float(item) == 200:
                        itens[len(itens) -
                              2] = remover_unidades(itens[len(itens)-2])
                        if (float(itens[len(itens)-2]) != 20):
                            continue

                        if len(itens) > 2:
                            itens[0] = remover_unidades(itens[0])
                            itens[1] = remover_unidades(itens[1])
                            itens[2] = remover_unidades(itens[2])
                            lista_dados[13]['mm3'] = itens[0]
                            lista_dados[13]['valoRA'] = itens[1]
                            lista_dados[13]['valorB'] = itens[2]
                        else:
                            itens[0] = remover_unidades(itens[0])
                            lista_dados[13]['valoRA'] = itens[0]
                            lista_dados[13]['valorB'] = item
                        break

            lista_dados[14]['valoRA'] = 150000
            lista_dados[14]['valorB'] = 450000

        for j, itens in enumerate(lista):
            if j == 7:
                break

        for item in itens:
            # Hemoglobina-------------CHCM--------------
            if ('g/dl' in item) and (len(itens) > 1):
                item = remover_unidades(item)
                if (float(item) <= 18):
                    itens[0] = remover_unidades(itens[0])
                    lista_dados[1]['valoRA'] = itens[0]
                    lista_dados[1]['valorB'] = item
                    break
                elif ((float(item) >= 31)):
                    itens[0] = remover_unidades(itens[0])
                    lista_dados[5]['valoRA'] = itens[0]
                    lista_dados[5]['valorB'] = item
                    break

            # Hematocrito--------------RDW-------------
            if ('%' in item) and (len(itens) > 1):
                item = remover_unidades(item)
                if (float(item) <= 16):
                    itens[0] = remover_unidades(itens[0])
                    lista_dados[2]['valoRA'] = itens[0]
                    lista_dados[2]['valorB'] = item
                    break
                elif ((float(item) >= 35)):
                    itens[0] = remover_unidades(itens[0])
                    lista_dados[6]['valoRA'] = itens[0]
                    lista_dados[6]['valorB'] = item
                    break
            # VCM---------------------------
            if (('£1' in item) or ('fl' in item)) and (len(itens) > 1):
                item = remover_unidades(item)
                if (float(item) >= 78):
                    itens[0] = remover_unidades(itens[0])
                    lista_dados[3]['valoRA'] = itens[0]
                    lista_dados[3]['valorB'] = item
                    break

            # Hematocrito--------------RDW-------------
            if ('pg' in item) and (len(itens) > 1):
                item = remover_unidades(item)
                if (float(item) >= 26):
                    itens[0] = remover_unidades(itens[0])
                    lista_dados[4]['valoRA'] = itens[0]
                    lista_dados[4]['valorB'] = item
                    break

        return lista_dados
    except Exception:
        return jsonify({'mensagem': "Erro no servidor"}), 500


def retunr_lista(texto):
    """"""

    try:
        resultado = analisa_dados(texto,
                                  lista_informacoes_buscada, list_captura_dados)
        lista_f = separa_dados_referencia(resultado[1])
        return classifica_dados(lista_f, resultado[0])
    except Exception:
        return jsonify({'mensagem': "Erro no servidor"}), 500
