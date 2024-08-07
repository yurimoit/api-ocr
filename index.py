# pylint: disable=missing-function-docstring
"""Module providing a function printing python version."""

import os
import tempfile
from io import BytesIO
import flask_cors

from dotenv import load_dotenv
import requests
from b2sdk._internal.transfer.outbound.upload_source import AbstractUploadSource
from b2sdk.v2 import B2Api
from b2sdk.v2 import InMemoryAccountInfo
from flask import Flask, jsonify, request, after_this_request


from autorization import verificar_autenticacao
from geradorRelatorioPdf import enviar_relatorio_gerado
from controladorArquivo.controlador_arquivos import analisa_text
from func_banco_dados import get_banco, inserir_exame_no_banco_dados, atualiza_exame_no_banco_dados
from func_banco_dados import deletar_exame_banco_dados, buscar_exames, get_banco_exames
from func_banco_dados import  get_dados_relatorio
from controladoresUuario.controlador_usuario import cadastrar_usuario, login_usuario
from controladoresUuario.controlador_usuario import atualizar_usuario
from contraloador_paciente.controlador import cadastrar_paciente, atualizar_paciente, get_pacientes
from contraloador_paciente.controlador import excluir_paciente, obter_paciente
from contraloador_paciente.controlador import  buscar_filtro_pacientes, consultar_endereco_por_cep
from controlado_dados_paranalisador import get_dados_paranalisador



app = Flask(__name__)
flask_cors.CORS(app)

load_dotenv()

UPLOAD_FOLDER = './imagens'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['NOME_IMAGEM'] = ''
app.config['TEXTO_GERADO'] = ''
app.config['LISTA_INFORMACAO'] = []


KEY_ID = os.getenv('applicationKeyId')
KEY = os.getenv('applicationKey')
NAME = os.getenv('bucketName')
URL = os.getenv('apiUrl')


HOST = os.environ.get('host')
DATA_BASE = os.environ.get('database')
USER = os.environ.get('user')
PASSWORD = os.environ.get('password')

PORT = os.getenv('PORT')

ACCOUNT_INFO_PATH = '/.b2_account_info'

info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.account_info._config_file = ACCOUNT_INFO_PATH


b2_api.authorize_account("production", KEY_ID, KEY)
bucket = b2_api.get_bucket_by_name(NAME)


def allowed_file(filename):
    """ALLOWED"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def get_data():
    """Verificar api backend"""
    data = {
        'message': 'Olá, esta é uma resposta da API!',
        'status': 'success'
    }
    return jsonify(data)


class BytesIOUploadSource(AbstractUploadSource):
    """Class representing a person"""

    def __init__(self, file_buffer):
        self.file_buffer = file_buffer

    def get_content_length(self):
        return len(self.file_buffer.getvalue())

    def get_content_sha1(self):
        # Implemente a lógica para calcular o SHA1 do conteúdo
        pass

    def open(self):
        return self.file_buffer


@app.route('/upload', methods=['POST'])
def upload_file():
    """DEF ----"""
    try:
        if 'file' in request.files:
            file_data = request.files['file']

            original_name = file_data.filename
            file_buffer = file_data.read()
            mime_type = file_data.mimetype

            app.config['NOME_IMAGEM'] = original_name

            file_buffer_io = BytesIO(file_buffer)
            custom_upload_source = BytesIOUploadSource(file_buffer_io)

            file_enviado = bucket.upload(
                upload_source=custom_upload_source,
                file_name=original_name,
                content_type=mime_type
            )
            file_info_serializable = file_enviado.as_dict()["fileId"]

            return jsonify({"file_enviado": file_info_serializable, "path": original_name})

    except Exception:
        return jsonify({'mensagem': "Erro no servidor"}), 500


@app.route('/getLeitura', methods=['GET'])
def get_string():
    """Enviar dados extraidos"""

    try:

        if app.config['NOME_IMAGEM']:
            file_url = f"https://f005.backblazeb2.com/file/TesteExameSangueOcr/{
                app.config['NOME_IMAGEM']}"

            # Baixar a imagem da URL
            response = requests.get(file_url)
            response.raise_for_status()

            _, file_extension = os.path.splitext(
                app.config['NOME_IMAGEM'].lower())

            lista_analisada_e_corrigida = analisa_text(
                file_extension=file_extension, response_content=response.content)

        resposta = {
            'nome_exame': app.config['NOME_IMAGEM'],
            'url_exame': f"https://f005.backblazeb2.com/file/TesteExameSangueOcr/{app.config['NOME_IMAGEM']}",
            'lista_dados': lista_analisada_e_corrigida[0],
            'observacao': lista_analisada_e_corrigida[1]
        }

        return jsonify(resposta), 200

    except Exception:
        return jsonify({'mensagem': "Erro no servidor"}), 500


@app.route('/listaFiles', methods=['GET'])
def get_lista():
    """GET LISTA"""
    try:
        # Listar os objetos no bucket
        file_versions = bucket.ls()

        file_names = [
            f'https://f005.backblazeb2.com/file/TesteExameSangueOcr/{file_version_tuple[0].file_name}' for file_version_tuple in file_versions]

        return jsonify({"file_names_url": file_names})
    except Exception:
        return jsonify({'mensagem': "Erro no servidor"}), 500


@app.route('/cadastrarUsuario', methods=['POST'])
def cadastra_usuario_route():
    """CADASTRA USUARIO"""
    return cadastrar_usuario()


@app.route('/login/usuario', methods=['POST'])
def rota_login_usuario():
    """PERMITI ACESSO USUARIO"""

    return login_usuario()


@app.route('/atualizar/usuario', methods=['POST'])
@verificar_autenticacao
def rota_atualizar_usuario():
    """PERMITI ATUALIZAÇÃO DO USÚARIO"""
    return atualizar_usuario()


@app.route('/obter/usuario', methods=['GET'])
@verificar_autenticacao
def rota_obter_usuario():
    """OBTER USUARIO USÚARIO"""
    return jsonify(request.usuario), 200


@app.route('/dados/exames', methods=['POST'])
@verificar_autenticacao
def post_inserir_dados_route():
    """Salva dados no banco"""
    return inserir_exame_no_banco_dados()


@app.route('/atualizar/exame/<int:id>', methods=['POST'])
@verificar_autenticacao
def post_atualiza_dados_route(id):
    """Salva dados no banco"""
    return atualiza_exame_no_banco_dados(id)


@app.route('/deletar/exame/<int:id>', methods=['DELETE'])
@verificar_autenticacao
def deletar_dados_route(id):
    """DELETAR EXAME DO BANCO"""
    return deletar_exame_banco_dados(id)


@app.route('/buscar/exames', methods=['GET'])
@verificar_autenticacao
def post_buscar_exames_dados_route():
    """Salva dados no banco"""
    return buscar_exames()


@app.route('/getBanco', methods=['GET'])
@verificar_autenticacao
def get_banco_route():
    """Fazer um get dos dados no banco"""
    return get_banco()


@app.route('/getBanco/exames', methods=['GET'])
@verificar_autenticacao
def get_banco_exame_route():
    """Fazer um get dos dados no banco"""
    return get_banco_exames()


@app.route('/getBanco/relatorio', methods=['GET'])
@verificar_autenticacao
def get_banco_relatorio_route():
    """Fazer um get dos dados no banco"""
    return get_dados_relatorio()


@app.route('/buscarcep', methods=['GET'])
def get_buscar_cep():
    """Fazer um get dos dados cep"""
    return consultar_endereco_por_cep()


@app.route('/cadastrar/paciente', methods=['POST'])
@verificar_autenticacao
def rota_cadastrar_paciente():
    """CADASTRAR PACIENTE"""
    return cadastrar_paciente()


@app.route('/buscar/pacientes', methods=['GET'])
@verificar_autenticacao
def rota_buscar_pacientes():
    """BUSCAR PACIENTE"""
    return get_pacientes()


@app.route('/obter/paciente', methods=['GET'])
@verificar_autenticacao
def rota_obter_paciente():
    """OBTER PACIENTE"""
    return obter_paciente()


@app.route('/buscarFiltro/pacientes', methods=['GET'])
@verificar_autenticacao
def rota_filtro_buscar_pacientes():
    """BUSCAR POR FILTRO PACIENTES"""
    return buscar_filtro_pacientes()


@app.route('/atualizar/paciente', methods=['PUT'])
@verificar_autenticacao
def rota_atualizar_paciente():
    """ATUALIZAR PACIENTE"""
    return atualizar_paciente()


@app.route('/deletar/paciente/<int:id>', methods=['DELETE'])
@verificar_autenticacao
def deletar_dados_paciente_route(id):
    """DELETAR PACIENTE DO BANCO"""
    return excluir_paciente(id)

@app.route('/gerar/dados_paranalisador', methods=['GET'])
@verificar_autenticacao
def gerar_dados_paranalisador():
    return get_dados_paranalisador()

@app.route('/gerar_relatorio', methods=['GET'])
@verificar_autenticacao
def gerar_relatorio_route():
    """ENVIAR RELATORIO"""

    try:
        
        id = request.args.get('id')

        if request.args.get('id') == 'null':
            id=None

        with tempfile.NamedTemporaryFile(delete=False,  suffix='.pdf') as temp_file:
            temp_filename = temp_file.name
            sucesso=enviar_relatorio_gerado(temp_filename, id)

            if not sucesso:
                raise Exception("Erro ao gerar o PDF")

            with open(temp_filename, 'rb') as f:
                file_data = f.read()
                bucket.upload_bytes(file_data, f'relatorios/{os.path.basename(temp_filename)}')
            
            @after_this_request
            def remover(response):
                try:
                    if temp_filename:
                        os.remove(temp_filename)
                except Exception as e:
                    print(f"Nao foi possivel excluir: {e}")
                return response
            
            name_file=os.path.basename(temp_filename)
            link_gerado=f'https://f005.backblazeb2.com/file/TesteExameSangueOcr/relatorios/{name_file}'

            return jsonify({'link': link_gerado}), 201
        
    except Exception as e:
        print(f"Erro ao gerar o PDF: {e}")
        return jsonify({"error": str(e)}), 500  


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
