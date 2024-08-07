# pylint: disable=missing-function-docstring

"""Bibliotecas para uso"""
import re
import copy
from difflib import SequenceMatcher
from flask import jsonify


def remove_nao_letras(texto):
    """Função que remove todos caracteres que não são letras."""
    return re.sub(r'[^a-zA-Z]', '', texto)


def remover_caracteres_especiais(texto):
    return re.sub(r'[^a-zA-Z0-9.,]', '', texto)


def remover_caracteres(texto):
    """Função para remover caracteres"""
    texto_limpo = re.sub(r'[^\d.,]', '', texto)
    return texto_limpo


def buscar_dados(texto_gerado, lista, list_captura_dados):
    """Função para separa dados do exame."""

    try:
        lista_padrao = lista.copy()
        lista_dados_finais = copy.deepcopy(list_captura_dados)
        parametro: float = 0.6
        nova_palavra: str = ''
        lista_de_referencia = ["/mm3", '/mm', 'g/dl', '%', 'fl',
                               'pg', 'u3', 'g3', '&', 'de', "‘", "`", 't', 'u³', '/mm³', 'milhões/mm³', '£1', '£2']

        for dicionario in lista_dados_finais:
            for chave, _ in dicionario.items():
                if chave == 'mm3':
                    dicionario['mm3'] = '--'

            dicionario['valorPR'] = '--'
            dicionario['valoRA'] = '--'
            dicionario['valorB'] = '--'

        if isinstance(texto_gerado, tuple):
            texto_gerado = list(texto_gerado)
            texto_gerado = texto_gerado[0]

        textos_lines = texto_gerado.lower().splitlines()

        for line in textos_lines:

            if len(line) < 6:
                continue

            for index, caractere in enumerate(line):
                if caractere.isdigit():
                    nova_palavra = line[0:index-1]
                    nova_palavra = remove_nao_letras(nova_palavra)

                    numero_dado = re.split(
                        '|'.join(lista_de_referencia), line[index:].replace(',', '.').replace(' ', ''))

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
            f"Erro no controlador de dado: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500


def corrigir_dados(lista_dados):
    """CORRIGIR DADOS """

    try:
        for dicionario in lista_dados:
            for chave in dicionario.keys():
                if chave in ('nome', 'unidade'):
                    continue

                if '.' in dicionario[chave]:
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
    except Exception as e:
        print(f"Erro ao corrigir o dado: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500
    
class ClassesValores:
    """Classe 1"""

    def __init__(self) -> None:
        self._p1=0.9 
        self._p2=0.8 
        self._p3=0.7 
        self._p4=0.7 
        self._p5=0.6 
        self._p6=0.5 




class IndicadoresValoresPesos(ClassesValores):
    """ Class"""

    def __init__(self) -> None:
        super().__init__()
        self.nome=""
        self.valor=0.0
        self.referencia=0.0
        self._hemacias=[0,0]
        self._hemoglobina=[0,0]
        self._hematocrito=[0,0]
        self._leucocitos_global=[0,0]
        self._neutrofilos_segmentados=[0,0]
        self._plaquetas=[0,0]

    def verificar_alteracao_indicadores(self)->bool:

        if self.valor>self.referencia:
            return True
        
        return False
    

    def atribuir_pesos_indicadores(self, valor_p):
        valor_certeza=valor_p
        valor_incerteza=0.0
        if self.verificar_alteracao_indicadores():
            lista_valores=[valor_certeza, valor_incerteza]
            return lista_valores

        return [valor_incerteza, valor_certeza]


    def atribuir_valor(self, nome, valor, referencia)->None:
        self.nome=nome
        self.valor=valor
        self.referencia=referencia

        match self.nome:
            case "hematocrito":
                self._hematocrito=self.atribuir_pesos_indicadores(self._p1)
                return   
            case "hemoglobina":
                self._hemoglobina=self.atribuir_pesos_indicadores(self._p2) 
                return  
            case "hemacias":
                self._hemacias=self.atribuir_pesos_indicadores(self._p3)
                return      
            case "leucocitos - global":
                self._leucocitos_global=self.atribuir_pesos_indicadores(self._p4)
                return      
            case "neutrofilos segmentados":
                self._neutrofilos_segmentados=self.atribuir_pesos_indicadores(self._p5)
                return      
            case "plaquetas":
                self._plaquetas=self.atribuir_pesos_indicadores(self._p6)
                return      
            case _:
                return  None  
            
    def valor_max_g2(self):
        lista_valor_maior=[]
        lista_valor_maior.append(self._hemacias[0])        
        lista_valor_maior.append(self._hemoglobina[0]) 

        lista_valor_menor=[]
        lista_valor_menor.append(self._hemacias[1])        
        lista_valor_menor.append(self._hemoglobina[1])              
       
        maior_valor=max(lista_valor_maior)
        menor_valor=min(lista_valor_menor)

        return [maior_valor, menor_valor]      
     
    def valor_max_g3(self):
        lista_valor_maior=[]
        lista_valor_maior.append(self._leucocitos_global[0])        
        lista_valor_maior.append(self._neutrofilos_segmentados[0]) 

        lista_valor_menor=[]
        lista_valor_menor.append(self._leucocitos_global[1])        
        lista_valor_menor.append(self._neutrofilos_segmentados[1])              
       
        maior_valor=max(lista_valor_maior)
        menor_valor=min(lista_valor_menor)

        return [maior_valor, menor_valor]       

            
    def calculo_logica_paraconsistente_anotada(self):
        g1=self._hematocrito
        g4=self._plaquetas
        g3=self.valor_max_g3()
        g2=self.valor_max_g2()

        m1_min=[min(g1[0],g2[0]), max(g1[1], g2[1])]
        m2_min=[min(g3[0], g4[0]), max(g3[1], g4[1])]

        valor_final_max=[max(m1_min[0], m2_min[0]), min(m1_min[1], m2_min[1])]

        return valor_final_max
    




def chamar_calculo_paraconsistente( lista_dados, indentificar_valores_pesos=IndicadoresValoresPesos):

    valores=indentificar_valores_pesos()

    for dicionario in lista_dados:
        referencia = 'valorPR'
        # referencia_a = ''
        referencia_b = ''

        if 'mm3' in list(dicionario.keys()):
            referencia = 'mm3'

        if '--' in list(dicionario.values()):
            continue

        # referencia_a = float(dicionario['valoRA'])
        referencia_b = float(dicionario['valorB'])
        referencia_valor = float(dicionario[referencia])
        nome=dicionario["nome"]
        valores.atribuir_valor(nome, referencia_valor, referencia_b)

    lista_valores_certo_incerto=valores.calculo_logica_paraconsistente_anotada()

    valor_certeza=lista_valores_certo_incerto[0]
    valor_incerteza=lista_valores_certo_incerto[1]
    
    grau_certeza=valor_certeza-valor_incerteza
    abs_certeza=round(abs(grau_certeza),2)
    grau_incerteza=(valor_certeza+valor_incerteza)-1
    abs_incerteza=round(abs(grau_incerteza),2)

    texto=f"""O sistema identificou que o índices dos glóbulos vermelhos estão elevados \n
                  com bases nos dados do exame, considerando o grau de certeza de {abs_certeza*100}%, considerado verdadeiro
                  , e {abs_incerteza*100}% de incerteza.\n Sugerimos que seja feita uma avaliação clínica mais detalha e exames adicionais.\n
                  
                  Sugestões:\n
                    Verificar exames anterios ou repetir o exame em 1 Mês.\n
                    Avaliar possiveis sintomas:
                            - Fraqueza
                            - Cansaço
                            - Dor de cabeça
                            - Tontura ou sensação de desmaio iminente
                            - Faltar de ar
                            - Suor noturno
                            - Coceiras após banho de chuveiro


                    
                  Novo exame: Para identificar uma possivél mutação no gene (JKA2). \n
                  Avaliar novamente os sisntomas. 

                  \n
                  Suspeitas: Policitemia vera** Ou possibilidades**
                  \n
                  Observação: ISSO NÃO SE TRATA DE UM DIAGNÓSTICO CABE AO SEU\n MÉDICO AVALIAR SEU QUADRO CLÍNICO.
            """ 
    
    texto_2=f"Valor gerado:{valor_certeza, valor_incerteza}"  

    if valor_certeza>=0.6:
        return [texto, [valor_certeza, valor_incerteza]]

    return [texto_2, [valor_certeza, valor_incerteza]] 


        



def analisa_dados_range_referencia(lista_dados):

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
                    f'{(dicionario["nome"]).upper()} ------- Está fora dos valores de referência.\n DADO: {referencia_valor} está ABAIXO do valor de referência.\n'
                    f'  ---- Referência ----- {referencia_a} ATÉ {referencia_b} ------\n')

                continue

            if referencia_valor > referencia_b:
                lista_dados_fora_referencia.append(
                    f'{(dicionario["nome"]).upper()} ------- Está fora dos valores de referência.\n DADO: {referencia_valor} está ACIMA do valor de referência.\n'
                    f'  ---- Referência ----- {referencia_a} ATÉ {referencia_b} ------\n')

                continue


        analise_de_indices=chamar_calculo_paraconsistente(lista_dados)
        texto_analise_de_indices=analise_de_indices[0]
        lista_dados_fora_referencia.append(texto_analise_de_indices)
        valor_certeza=analise_de_indices[1][0]
        valor_incerteza=analise_de_indices[1][1]
        lista_valores=[valor_certeza, valor_incerteza]

        texto_analizado = '\n'.join(lista_dados_fora_referencia)

        return [texto_analizado, lista_valores]
    except Exception as e:
        print(f"Erro no controlado de referencias: {str(e)}")
        return jsonify({'mensagem': "Erro no servidor"}), 500
