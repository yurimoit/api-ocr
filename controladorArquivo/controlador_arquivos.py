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
from dotenv import load_dotenv

from google.cloud import vision
from google.oauth2 import service_account

load_dotenv()

TYPE_VALUE = os.getenv('typeValue')
PROJECT_ID = os.getenv('projectId')
PRIVATE_KEY_ID = os.getenv('privateKeyId')
PRIVATE_KEY = os.getenv('privateKey')
CLIENT_EMAIL = os.getenv('clientEmail')
CLIENT_ID = os.getenv('clientId')
AUTH_URI = os.getenv('authUri')
TOKEN_URI = os.getenv('tokenUri')
AUTH_PROVIDER_X509_CERT_URL = os.getenv('authProviderX509CertUrl')
CLIENT_X_CERT_URL = os.getenv('clientX509CertUrl')
UNIVERSE_DOMAIN = os.getenv('universeDomain')


def detect_text(image):
    """Detects text in the file."""

    print("Aqui: ", TYPE_VALUE, PRIVATE_KEY, PRIVATE_KEY_ID, PROJECT_ID, CLIENT_EMAIL, CLIENT_ID,
          AUTH_URI, TOKEN_URI, AUTH_PROVIDER_X509_CERT_URL, CLIENT_X_CERT_URL, UNIVERSE_DOMAIN)

    credentials_json = {
        "type": TYPE_VALUE,
        "project_id": PROJECT_ID,
        "private_key_id": PRIVATE_KEY_ID,
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCk6OgRhauexyeG\nQpCcenQxT1074TFQ9uLXZrS1ij/HhpSnp842gTzUuYBK2/UdeWu2am8BAXowJa+1\nxy8XDAkWZg/sMXL84eZg02CSjvVEdgAhBWgG0mozX9/tvsAdp+sHaZPMu0kVixT1\ni1gUVCurdBfAdaG7p7BSeRmjjypI9POjDFVXWMx+A62Z8bi/9eRXZe0Dj7k1gS83\nqQ1aqHivw19/d05Qg8xXJ/GTJmRJrX6eOsm7ZsQrP+VyOievhsmlhiXK/cLfiJUt\ndeNStt9Ia8Pym4MpnRJyqoxvEevstE8EklY0AukrkThYeeZmAmjn8s0RVsrGrD1M\nWvmD4GhtAgMBAAECggEAJgSWycFYBy8RHtv2NEjrxBlwnFcmdCyyr6d7JjYUzZYq\na7tdKEYjpMQOPlPWvsCJE0EWzbPOPE7X4w+kPMs2xh3p8lEVGhUnNC/O/gKsqyeM\nEJDLQnVca/MgsBHvfvbBEZCmtQaBSxDpGFGTUP51od2OAz3rNxSp6t2FymX9QNuu\n3z4B/jL79TXekiNaJ1rnTSlRqTRKeTafEj4iX6hv4zcBDG+nFmDjQNE/Y6asSZLI\ngVESxR10AtZzPlYrVF3GaLE5YW3TQUIpVzHzSHXT0Abah1dvUw1guqrGoUy6oldU\nyVG0fZUL3tjjg5yii4Lv2ScvgiEg9/Vx0ueGwVB0GQKBgQDcOhwfa6aMrItAwH82\n3FN37jDsU+a2IJgjSlU2IbhcXbK9zhLzD9H8OC7npC1QevqpiIhyPGFt4Tna/kA8\nNDP1KlqBVPkb9dOj2waBF6DEblWW8oIFqtlrJJgqezLbT2yGk4oH/zrKQ/y6/plG\nmBvqHQIYw7EKR0f7KUAnQBIARQKBgQC/sn5V7rrINnViHHLe93HvorMbGehCpGKB\n/4e4gbxtTQ5AMv3uPnzyLcgdPzavqCIa+Ntfv7Vl8LjJz8zwjTOmEX1V+YDEQhmU\nLhTYQj5FFBDJZaT/pSfSFl1aoJuIPJDN8QWhsBGPb0DZS/bK5f/An0iusIeAVp4n\no7lAeoouCQKBgHlxYgjBqHpyu+fdP0nVfgHoy/nG2rccikkLuKm9NplY4jRg63o2\nAyn/IX6Dvqle59ONgxDb0y5wwSLOikWo0+4iiP5BCY4tpaP6KEAP84ve/DvdR24w\npOy8pVzny0e9KK+dtMRsLtNTYo8LzyJqxxn3HSzi3UI5xKvwN3xtjH+xAoGAJc/Q\naaTYROuxBbQ02FQYrjr6dysKDDMelyPPIo68mxaq6/Di855xyNdM9K/mWomgiI9z\nvhQzdLMhz/TkKMLBYE1s2ouHYa7kGr1oMSwH2lpV4VPiUubBzwfITDsH0ryXl3em\nM7lmDVPVh8cbG/R4GQeSL5r0b1Umhw0dWmGRZfkCgYBmkMoqhVsQrMNEKiDvJoyD\nkTH7ZlBDeoeqaf2xpaposyym0Y9bBpiLIGMVSURLYnXK/gzgxEbfguSTkgIlp/Ek\n3UA+obFoLwaSkNDw7Kr2oCCDGH9lQX1uNbwWZvBcv7YkFvX8Xt9aDm5zN4ynU0Ar\n5PNVsILRyz3HsWO3/dyi9A==\n-----END PRIVATE KEY-----\n",
        "client_email": CLIENT_EMAIL,
        "client_id": CLIENT_ID,
        "auth_uri": AUTH_URI,
        "token_uri": TOKEN_URI,
        "auth_provider_x509_cert_url": AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": CLIENT_X_CERT_URL,
        "universe_domain": UNIVERSE_DOMAIN
    }

    try:
        # Configurar as credenciais com base nos dados fornecidos
        print("CREEE", credentials_json)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_json
        )

        print("CRE_TRY: ", credentials)

        # Configurar o cliente com as credenciais
        client = vision.ImageAnnotatorClient(credentials=credentials)

        # Converter a imagem para bytes
        with BytesIO() as output:
            image.save(output, format='JPEG')
            content = output.getvalue()

        # Configurar a imagem para análise
        gcp_image = vision.Image(content=content)

        response = client.text_detection(image=gcp_image)
        texts = response.text_annotations
        print("Texts:")
        text = ''

        for text in texts:
            print(f'\n"{text.description}"')
            text = text.description
            break

        #     vertices = [
        #         f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        #     ]

        # print("bounds: {}".format(",".join(vertices)))

        return text

    except Exception as e:
        print('Erro na função do Google: ', str(e))
        return jsonify({'mensagem': str(e)}), 500


# Credenciais JSON em formato de dicionário


# Chamar a função com o caminho da imagem e as credenciais em formato de dicionário


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
        return text
    except Exception as e:
        print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor ocr file image"}), 500
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
    except Exception as e:
        print(f"Erro ao extrair texto do arquivo: {e}")
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
            # ocr_text = ocr_image_to_text(image)
            ocr_text = detect_text(image)
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

            print('LISTA:', lista_corrigida)

            nota = analisa_dados_range_referencia(
                lista_corrigida)

        return [lista_corrigida, nota]

    except Exception as e:
        print(f"Erro ao extrair texto do arquivo: {e}")
        return jsonify({'mensagem': "Erro no servidor"}), 500
