import pytesseract
from PIL import Image, ImageEnhance
import PyPDF2
import csv
import os
import tempfile
from flask import jsonify
import docx2txt
from io import StringIO, BytesIO
import xlrd
from controlador_dado import buscar_dados, corrigir_dados, analisa_dados_range_referencia
from listas.lista_exame_hemograma import list_captura_dados
from listas.lista_exame_hemograma import lista_informacoes_buscada


def ocr_image_to_text(image):
    """Extração de dados com a biblioteca pytesseract"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_image:
            image.save(temp_image.name, optimize=True,
                       quality=100)

        image_open = Image.open(temp_image.name)

        new_image = image_open.resize(
            (image_open.width * 3, image_open.height * 3),
            # pylint: disable=E1101
            Image.LANCZOS)

        # width, height = image_open.size
        # new_width = 4000
        # new_height = round(height*new_width/width)

        # new_image = image_open.resize((new_width, new_height),
        #                               # pylint: disable=E1101
        #                               Image.LANCZOS)

        enhancer = ImageEnhance.Contrast(new_image)
        image_enhanced = enhancer.enhance(2)

        text = pytesseract.image_to_string(image_enhanced)
        # print(text)
        return jsonify({'text': text}), 200
    except Exception:
        # print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500
    finally:
        # Excluir o arquivo temporário depois de abrir a imagem
        if 'temp_image' in locals():
            try:
                os.unlink(temp_image.name)
            except Exception:
                # print(f"Erro ao extrair texto do arquivo: {e}")
                return jsonify({'mensagem': "Erro no servidor"}), 500


def ocr_pdf_to_text(pdf_path):
    """Extração de dados com a biblioteca PyPDF2"""
    try:
        text = ""
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
        # print(text)
        return text
    except Exception:
        # print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500


def read_text_from_txt(file_bytes):
    """Extrai o texto do arquivo .txt com a biblioteca"""
    try:
        text = ""
        with file_bytes as file:
            for line in file:
                text += line.decode('utf-8')
        return text
    except Exception:
        # print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500


def read_text_from_docx(docx_file):
    """Extrai o texto do arquivo .docx com a biblioteca docx2txt"""
    try:
        text = docx2txt.process(docx_file)
        return text
    except Exception:
        # print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500


def read_text_from_csv(file_text):
    """Extrai o texto do arquivo .csv com a biblioteca csv"""
    try:
        text = ""

        content = file_text.decode()  # Converte bytes para string
        file = StringIO(content)  # Cria um objeto de fluxo de texto em memória
        csv_data = csv.reader(file, delimiter=",")

        for row in csv_data:
            text += ','.join(row) + '\n'
        return text
    except Exception:
        # print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500


def read_text_from_xls(file_content):
    """Extrai o texto do arquivo .xls com a biblioteca xlrd"""

    try:
        # Abre o arquivo XLS usando xlrd
        workbook = xlrd.open_workbook(file_contents=file_content)

        # Acesse a primeira planilha (pode ajustar conforme necessário)
        sheet = workbook.sheet_by_index(0)

        # Leia os dados da planilha e converta para uma string
        text = ""
        for row in range(sheet.nrows):
            text += ",".join(str(cell.value) for cell in sheet.row(row)) + "\n"

        return text
    except Exception as e:
        print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500


def analisa_text(file_extension, response_content):
    """Analisa e extrair informacoes"""
    try:
        if file_extension in ('.png', '.jpg', '.jpeg'):
            image = Image.open(BytesIO(response_content))
            ocr_text = ocr_image_to_text(image)
        elif file_extension == '.pdf':
            ocr_text = ocr_pdf_to_text(BytesIO(response_content))
        elif file_extension == '.txt':
            ocr_text = read_text_from_txt(BytesIO(response_content))
        elif file_extension == '.xls':
            ocr_text = read_text_from_xls(response_content)
        elif file_extension == '.docx':
            ocr_text = read_text_from_docx(BytesIO(response_content))
        elif file_extension == '.csv':
            ocr_text = read_text_from_csv(response_content)
        else:
            return "Tipo de arquivo não suportado."

        if ocr_text:
            lista_informacao_text = buscar_dados(
                ocr_text, lista_informacoes_buscada, list_captura_dados)

            lista_corrigida = corrigir_dados(lista_informacao_text)

            nota = analisa_dados_range_referencia(
                lista_corrigida)

        return [lista_corrigida, nota]

    except Exception:
        # print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500
