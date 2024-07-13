# pylint: disable=missing-function-docstring

from __future__ import annotations
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from func_banco_dados import connectar_banco
from pathlib import Path 
from flask import request, jsonify, send_file
import tempfile


ROOT_FOLDER=Path(__file__).parent
pdf_gerado=ROOT_FOLDER / 'relatorio_exames.pdf'


class Conexao():
    def __init__(self) -> None:
        self.conn = connectar_banco()
        self.parametros = ()
        self.row = []
        self._comandoSQL_1 = "SELECT * FROM relatorios WHERE id_usuario=%s"
        self._comandoSQL_2 = "SELECT * FROM relatorios WHERE id_usuario=%s AND id_paciente=%s"
        self._lista_dados = []
        self._nome_paciente="Indefinido"
        self._data_nascimento="0000-00-00"
        self._data_valor_1="0000-00-00"
        self._data_valor_2="0000-00-00"
        self._data_valor_3="0000-00-00"
        self._sexo_paciente="I"
        self._periodo_analisado=["0000-00-00","0000-00-00"]

    def select(self, parametro_1, parametro_2=None):
        self.parametros = (parametro_1,)
        if parametro_2:
            self.parametros = (parametro_1, parametro_2,)

        with self.conn.cursor() as cursor:
            if parametro_2:
                cursor.execute(self._comandoSQL_2, self.parametros)
            else:
                cursor.execute(self._comandoSQL_1, self.parametros)
            self.conn.commit()

            self.row = cursor.fetchone()
            print()
        self.conn.close()

    def vizualizar_resposta(self):
        for item in self.row:
            print(item)

    def get_lista_dados(self):
        for item in (self.row[9]).items():
            self._lista_dados.append([item[0], item[1]])
        return self._lista_dados
    
    def get_nome(self):
        self._nome_paciente=self.row[1]
        return self._nome_paciente
    
    def _normaliza_data(self,_data):

        if _data==0:
            return "---"
        
        lista_indices_data=_data.split('-')
        nova_data=lista_indices_data[2] + "/"+lista_indices_data[1]+"/"+lista_indices_data[0]
        return nova_data

    def get_data_nascimento(self):
        data=str(self.row[2])
        self._data_nascimento=self._normaliza_data(data)
        return self._data_nascimento
    
    def get_data_1(self):
        data=str(self.row[4])
        self._data_valor_1=self._normaliza_data(data)
        return self._data_valor_1
    
    def get_data_2(self):
        data=str(self.row[5])
        self._data_valor_2=self._normaliza_data(data)
        return self._data_valor_2
    
    def get_data_3(self):
        data=str(self.row[6])
        self._data_valor_3=self._normaliza_data(data)
        return self._data_valor_3
    
    def get_periodo_analisado(self):
        primeira_data=str(self.row[7])
        ultima_data=str(self.row[8])
        normalizada_data_1=self._normaliza_data(primeira_data)
        normalizada_data_2=self._normaliza_data(ultima_data)
        self._periodo_analisado=[normalizada_data_1, normalizada_data_2]
        return self._periodo_analisado
        
    def _categorizar_sexo_paciente(self, sexo):
        match sexo:
            case "M":
                return "Masculino"
            case "F":
                  return "Feminino"  
            case "I":
                  return "Indefinido"


    def get_sexo_paciente(self):
        self._sexo_paciente=self._categorizar_sexo_paciente(self.row[3])
        return self._sexo_paciente
        



class FormatoPDF:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.elements = []
        self.data = []
        self.color_1 = 'grey'
        self.color_2 = 'whitesmoke'
        self.titulo = "Titulo padrão"
        self.styles = getSampleStyleSheet()
        self._col_widths_1 = [550]
        self._data1 = [['Nome Paciente: Indefinido']]
        self._data2 = [['Data nascimento: 00/00/0000', 'Sexo: Indefinido'],]
        self._col_widths_2 = [275, 275]
        self._data3 = [['Últimos três exames', f'Estatística: (00/00/0000) a (00/00/0000)'],]
        self._col_widths_3 = [340, 210]
        self._data4 = [['Nome', "00/00/0000", "00/00/0000", "00/00/0000", 'Maior', 'Média', 'Menor'],]
        self._col_widths_4 = [145, 65, 65, 65, 70, 70, 70]
        self.col_widths = []
        self.style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('BACKGROUND', (0, 1), (-1, 1), self.color_1),
            ('TEXTCOLOR', (0, 1), (-1, 1), self.color_2),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])

    def criar_arquivo(self,pdf):
        pdf = SimpleDocTemplate(self.filename, pagesize=letter)
        pdf.build(self.elements)

    def criar_titulo(self, nome):
        title = Paragraph(nome, self.styles['Title'])
        self.elements.append(title)
        self.elements.append(Spacer(1, 0.2 * inch))

    def criar_padrao_relatorio(self):
        print(self._data1)
        self.add_line_table(self._data1, self._col_widths_1)    
        self.add_line_table(self._data2, self._col_widths_2)    
        self.add_line_table(self._data3, self._col_widths_3)    
        self.add_line_table(self._data4, self._col_widths_4)    

    def add_line_table(self, data, col_widths, color_1=None, color_2=None):
        if color_1:
            self.color_1 = color_1
        if color_2:
            self.color_2 = color_2

        tablelinha = Table(data, colWidths=col_widths,)
        tablelinha.setStyle(self.style)

        self.elements.append(tablelinha)

    def set_data_1(self,nome):
          self._data1 = [[f'Nome Paciente: {nome}']] 

    def set_data_2(self,data_nascimento, sexo):
          self._data2 = [[f'Data nascimento: {data_nascimento}', f'Sexo: {sexo}'],] 

    
    def set_data_3(self,lista_data):
          self._data3 = [['Últimos três exames', f'Estatística: ({lista_data[0]}) a ({lista_data[1]})'],]

    def set_data_4(self,data_1,data_2,data_3):
          self._data4 = [['Nome', data_1, data_2, data_3, 'Maior', 'Média', 'Menor'],]       



def organiza_dados_estatisticos(dados,data5):
    for dado in dados:
        for item in data5:
            original_name = item[0]

            normaliza_name = original_name.replace('á', 'a').replace('ó', 'o').lower()
            if normaliza_name == dado[0]:
                if original_name=="Basafilos":
                    original_name="Basófilos"

                item[0] = original_name
                item[1] = dado[1]["lista_dados"][0]
                item[2] = dado[1]["lista_dados"][1]
                item[3] = dado[1]["lista_dados"][2]
                item[4] = dado[1]['dados_referencia']["maior_valor"]
                item[5] = dado[1]['dados_referencia']["media"]
                item[6] = dado[1]['dados_referencia']["menor_valor"]
                break





def enviar_relatorio_gerado(pdf):
    """SEM EXPLICAÇÃO"""

    data5 = [
    ['Hemácias', '', '', '', '', '', ''],
    ['Hemoglobina', '', '', '', '', '', ''],
    ['Hematócrito', '', '', '', '', '', ''],
    ['VCM', '', '', '', '', '', ''],
    ['HCM', '', '', '', '', '', ''],
    ['CHCM', '', '', '', '', '', ''],
    ['RDW', '', '', '', '', '', ''],
    ['Leucócitos - Global', '', '', '', '', '', ''],
    ['Neutrofilos Bastonetes', '', '', '', '', '', ''],
    ['Neutrofilos segmentados', '', '', '', '', '', ''],
    ['Linfocitos', '', '', '', '', '', ''],
    ['Monócitos', '', '', '', '', '', ''],
    ['Eosinófilos', '', '', '', '', '', ''],
    ['Basafilos', '', '', '', '', '', ''],
    ['Plaquetas', '', '', '', '', '', '']
]

    col_widths_4 = [145, 65, 65, 65, 70, 70, 70]

    filename = "relatorio_exames.pdf"
    titulo = "Relatório Exame Sangue<br/>(Hemograma completo)"

    try:

        conexao1 = Conexao()
        conexao1.select(1, 1)
        dados = conexao1.get_lista_dados()
        nome_paciente=conexao1.get_nome()
        data_nascimento=conexao1.get_data_nascimento()
        sexo_paciente=conexao1.get_sexo_paciente()
        data_1=conexao1.get_data_1()
        data_2=conexao1.get_data_2()
        data_3=conexao1.get_data_3()
        lista_registros=conexao1.get_periodo_analisado()


        organiza_dados_estatisticos(dados=dados, data5=data5)


        relatorio1 = FormatoPDF(filename)
        relatorio1.criar_titulo(titulo)
        relatorio1.set_data_1(nome_paciente)
        relatorio1.set_data_2(data_nascimento, sexo_paciente)
        relatorio1.set_data_3(lista_registros)
        relatorio1.set_data_4(data_1=data_1, data_2=data_2, data_3=data_3)


        relatorio1.criar_padrao_relatorio()
        relatorio1.add_line_table(data5, col_widths_4, color_1='white', color_2='black')

        return relatorio1.criar_arquivo(pdf)
        
    except Exception as e:
        print("Erro ao gera PDF",str(e))
        return jsonify({'mensagem': "Erro no servidor"}), 500
    