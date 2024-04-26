"""Bibliotecas para uso"""
import re
import copy
from difflib import SequenceMatcher
from flask import jsonify


def buscar_dados(texto_gerado, lista, list_captura_dados):
    """Função para separa dados do exame."""

    try:
        lista_padrao = lista.copy()
        lista_dados_finais = copy.deepcopy(list_captura_dados)
        parametro: float = 0.6

        for dicionario in lista_dados_finais:

            for chave, _ in dicionario.items():
                if chave == 'mm3':
                    dicionario['mm3'] = '--'

            dicionario['valorPR'] = '--'
            dicionario['valoRA'] = '--'
            dicionario['valorB'] = '--'

        def remove_nao_letras(texto):
            """Função que remove todos caracteres que não são letras."""
            return re.sub(r'[^a-zA-Z]', '', texto)

        def remover_caracteres_especiais(texto):
            return re.sub(r'[^a-zA-Z0-9.,]', '', texto)

        def remover_caracteres(texto):
            """Use expressões regulares para substituir todos os caracteres não desejados"""
            texto_limpo = re.sub(r'[^\d.,]', '', texto)
            return texto_limpo

        nova_palavra: str = ''

        print("TEXTO GERADO: ", texto_gerado)

        if isinstance(texto_gerado, tuple):
            texto_gerado = texto_gerado[0]

        textos_lines = texto_gerado.splitlines()

        lista_de_referencia = ["/mm3", '/mm', 'g/dl', '%', 'fl',
                               'pg', 'u3', 'g3', '&', 'de', "‘", "`", 't', 'u³', '/mm³', 'milhões/mm³', '£1', '£2']

        for line in textos_lines:

            if len(line) < 6:
                continue

            for index, caractere in enumerate(line):
                if caractere.isdigit():
                    nova_palavra = line[0:index-1]
                    nova_palavra = remove_nao_letras(nova_palavra).lower()

                    numero_dado = re.split(
                        '|'.join(lista_de_referencia), line[index:].lower().replace(',', '.').replace(' ', ''))

                    for item in numero_dado.copy():
                        numero_dado.remove(item)
                        item = remover_caracteres_especiais(item)
                        if item and not item.isalpha():
                            numero_dado.append(item.strip())

                    # print(nova_palavra, numero_dado)

                else:
                    continue
                break

            if len(nova_palavra) < 3:
                continue

            for palavra_padrao in lista_padrao:

                if len(palavra_padrao) > 4:
                    parametro = 0.7

                if (len(palavra_padrao) < 4) or (palavra_padrao in ['leucocitos - global', 'neutrofilos bastonetes', 'neutrofilos segmentados']):
                    parametro = 0.6

                # Criando um objeto SequenceMatcher com as duas palavras
                comparador = SequenceMatcher(
                    None,   palavra_padrao, nova_palavra)

                # Obtendo a semelhança entre as duas palavras
                semelhanca = comparador.ratio()

                if semelhanca >= parametro:
                    if len(numero_dado) < 2:
                        continue

                    for item in lista_dados_finais:
                        if palavra_padrao == item['nome']:
                            # print("Entrou ", palavra_padrao, numero_dado)
                            if isinstance(numero_dado, list):
                                item['nome'] = palavra_padrao

                                item['valorPR'] = remover_caracteres(
                                    numero_dado[0])

                                padrao_2 = re.compile(
                                    r'\d{1}[.]\d{4,9}[.]\d{1}')
                                if padrao_2.search(item['valorPR']):

                                    item['mm3'] = item['valorPR'][(
                                        len(item['valorPR'])-5):]

                                    item['valorPR'] = item['valorPR'][0:(
                                        len(item['valorPR'])-5)]

                                # print(item['valorPR'])

                                if len(numero_dado) == 3:
                                    padrao_ed = re.compile(r'^[a-zA-Z]\d{3}$')
                                    if padrao_ed.search(numero_dado[2]):
                                        # print('Foi aqui', numero_dado[2])

                                        item['valoRA'] = '0.0'
                                        item['valorB'] = remover_caracteres(
                                            numero_dado[2])
                                        break

                                if len(numero_dado) == 2:
                                    padrao = re.compile(r'\d{1}[a-zA-Z]\d{1}')
                                    if padrao.search(numero_dado[1]):
                                        # print('Foi aqui', numero_dado[1])
                                        separa_valores_referencia = numero_dado[1].split(
                                            'a')
                                        if len(separa_valores_referencia) > 1:
                                            item['valoRA'] = remover_caracteres(
                                                separa_valores_referencia[0])
                                            item['valorB'] = remover_caracteres(
                                                separa_valores_referencia[1])
                                        break

                                if len(numero_dado) >= 3 and palavra_padrao not in ('hemacias', 'hemoglobina', 'hematocrito', 'vcm', 'hcm', 'chcm', 'rdw', 'leucocitos - global'):
                                    if item['mm3'] == '--':
                                        item['mm3'] = remover_caracteres(
                                            numero_dado[1])

                                if len(numero_dado) > 1 and palavra_padrao in ('hemacias', 'hemoglobina', 'hematocrito', 'vcm', 'hcm', 'chcm', 'rdw', 'leucocitos - global'):
                                    padrao = re.compile(r'\d{1}[a-zA-Z]\d{1}')
                                    if padrao.search(numero_dado[1]):
                                        separa_valores_referencia = numero_dado[1].split(
                                            'a')
                                        if len(separa_valores_referencia) > 1:
                                            item['valoRA'] = remover_caracteres(
                                                separa_valores_referencia[0])
                                            item['valorB'] = remover_caracteres(
                                                separa_valores_referencia[1])

                                if len(numero_dado) > 2 and palavra_padrao not in ('hemacias', 'hemoglobina', 'hematocrito', 'vcm', 'hcm', 'chcm', 'rdw', 'leucocitos - global'):
                                    padrao = re.compile(r'\d{1}[a-zA-Z]\d{1}')
                                    if padrao.search(numero_dado[2]):
                                        separa_valores_referencia = numero_dado[2].split(
                                            'a')
                                        if len(separa_valores_referencia) > 1:
                                            item['valoRA'] = remover_caracteres(
                                                separa_valores_referencia[0])
                                            item['valorB'] = remover_caracteres(
                                                separa_valores_referencia[1])

                            break

                    lista_padrao.remove(palavra_padrao)
                    # print(lista_padrao)
                    break
        # print(*lista_dados_finais, sep='\n')
        return lista_dados_finais
    except Exception as e:
        print(
            f"Erro no controlador de dado: {e} E texto gerado {texto_gerado}")
        return jsonify({'mensagem': "Erro no servidor"}), 500


def corrigir_dados(lista_dados):
    try:
        for dicionario in lista_dados:
            for chave in dicionario.keys():
                if chave in ('nome', 'unidade'):
                    continue

                if '.' in (dicionario[chave]):
                    separador = (dicionario[chave]).split('.')

                    if (dicionario['nome'] == 'hemacias') and (len(dicionario[chave]) >= 4):
                        lista_palavra_hemacias = list(
                            (dicionario[chave]).replace('.', ''))
                        dicionario[chave] = lista_palavra_hemacias[0] + '.' + \
                            lista_palavra_hemacias[1]+lista_palavra_hemacias[2]
                        continue

                    padrao = re.compile(r'\d{1}[.]\d{3}[.]\d{1}')
                    if padrao.search(dicionario[chave]):

                        # print(dicionario[chave])

                        dicionario[chave] = (dicionario[chave][0:(
                            len(dicionario[chave])-1)]).replace('.', '')

                        dicionario[chave] = f'{round(float(dicionario[chave]),2)}'
                        continue

                    if len(separador) == 2:

                        if dicionario['nome'] == 'plaquetas':

                            if len(separador[1]) == 2:
                                dicionario[chave] = separador[0] + \
                                    separador[1][0] + \
                                    separador[1][0] + "0"

                            if len(separador[1]) > 2:
                                dicionario[chave] = separador[0] + \
                                    separador[1][0] + \
                                    separador[1][1]+separador[1][2]

                            continue

                        if dicionario['nome'] == 'hematocrito':

                            if (len(separador[0]) <= 2) and (len(separador[1]) == 3):
                                dicionario[chave] = round(
                                    float(dicionario[chave]), 2)

                            continue

                        if (len(separador[0]) <= 2) and (len(separador[1]) == 3):
                            dicionario[chave] = (
                                dicionario[chave]).replace('.', '')

                            if (dicionario[chave]).isdigit():
                                dicionario[chave] = f'{round(float(dicionario[chave]),2)}'

                        continue

                    dicionario[chave] = (dicionario[chave][0:(len(dicionario[chave])-1)]).replace(
                        '.', '') + dicionario[chave][len(dicionario[chave])-1]

        return lista_dados
    except Exception:
        # print(f"Erro ao corrigir o dado: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500


def analisa_dados_range_referencia(lista_dados):
    """"""

    try:
        lista_dados_fora_referencia = []

        for dicionario in lista_dados:
            referencia = 'valorPR'
            referencia_a = ''
            referencia_b = ''
            if 'mm3' in list(dicionario.keys()):
                referencia = 'mm3'

            if '--' in list(dicionario.values()):
                continue

            referencia_a = float(dicionario['valoRA'])
            referencia_b = float(dicionario['valorB'])
            referencia_valor = float(dicionario[referencia])

            if referencia_a <= referencia_valor <= referencia_b:

                continue

            if referencia_valor < referencia_a:
                lista_dados_fora_referencia.append(
                    f'{(dicionario["nome"]).upper()} ------- Está fora dos valores de referência.\n DADO: {referencia_valor} esta ABAIXO do valor de referência.\n'
                    f'  ---- Referência ----- {referencia_a} ATÉ {referencia_b} ------\n')

                continue

            if referencia_valor > referencia_b:
                lista_dados_fora_referencia.append(
                    f'{(dicionario["nome"]).upper()} ------- Está fora dos valores de referência.\n DADO: {referencia_valor} esta ACIMA do valor de referência.\n'
                    f'  ---- Referência ----- {referencia_a} ATÉ {referencia_b} ------\n')

                continue

        texto_analizado = '\n'.join(lista_dados_fora_referencia)

        return texto_analizado
    except TypeError:
        return jsonify({'mensagem': "Erro no servidor"}), 500
