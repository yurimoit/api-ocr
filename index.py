import os
from dotenv import load_dotenv
import requests
from b2sdk.transfer.outbound.upload_source import AbstractUploadSource
from b2sdk.v1 import B2Api
from io import BytesIO
from flask import Flask, jsonify, request
import flask_cors
from controladorArquivo.controlador_arquivos import analisa_text
from func_banco_dados import get_banco, inserir_exame_no_banco_dados, atualiza_exame_no_banco_dados, deletar_exame_banco_dados, buscar_exames, get_banco_exames
from controladoresUuario.controlador_usuario import cadastrar_usuario, login_usuario, atualizar_usuario
from autorization import verificar_autenticacao


app = Flask(__name__)
flask_cors.CORS(app)

load_dotenv()

UPLOAD_FOLDER = './imagens'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['NOME_IMAGEM'] = ''
app.config['TEXTO_GERADO'] = ''
app.config['LISTA_INFORMACAO'] = []


KEY_ID = os.environ.get('application_key_id')
KEY = os.environ.get('application_key')
NAME = os.environ.get('bucket_name')
URL = os.environ.get('api_url')


HOST = os.environ.get('host')
DATA_BASE = os.environ.get('database')
USER = os.environ.get('user')
PASSWORD = os.environ.get('password')



# Criar uma instância do B2Api
b2_api = B2Api()
b2_api.authorize_account('production', KEY_ID, KEY)
# Obter a instância do bucket
bucket = b2_api.get_bucket_by_name(NAME)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def get_data():
    data = {
        'message': 'Olá, esta é uma resposta da API!',
        'status': 'success'
    }
    return jsonify(data)


class BytesIOUploadSource(AbstractUploadSource):
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

    except Exception as e:
        return jsonify({'mensagem': "Erro no servidor", 'erro': str(e)}), 500


@app.route('/getLeitura', methods=['GET'])
def get_string():
    """Enviar dados extraidos"""

    try:

        if app.config['NOME_IMAGEM']:
            file_url = f"https://f005.backblazeb2.com/file/TesteExameSangueOcr/{app.config['NOME_IMAGEM']}"

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
            'lista_dados': lista_analisada_e_corrigida,
            'observacao': ''
        }

        return jsonify(resposta), 200

    except Exception as e:
        print(f'Erro na funcao: {e}')
        return str(e), 500


@app.route('/listaFiles', methods=['GET'])
def getLista():
    try:
        # Listar os objetos no bucket
        file_versions = bucket.ls()

        # Exibir os nomes dos objetos no bucket
        file_names = [
            f'https://f005.backblazeb2.com/file/TesteExameSangueOcr/{file_version_tuple[0].file_name}' for file_version_tuple in file_versions]

        return jsonify({"file_names_url": file_names})
    except Exception as e:
        return jsonify({'mensagem': "Erro no servidor", 'erro': str(e)}), 500


@app.route('/cadastrarUsuario', methods=['POST'])
def cadastra_usuario_route():
    """CADASTRA USUARIO"""
    return cadastrar_usuario()


@app.route('/login/usuario', methods=['POST'])
def rota_login_usuario():
    """PERMITI ACESSO USUARIO"""

    print('Entrou na rota login')

    return login_usuario()


@app.route('/atualizar/usuario', methods=['POST'])
@verificar_autenticacao
def rota_atualizar_usuario():
    """PERMITI ATUALIZAÇÃO DO USÚARIO"""

    print('Entrou na rota atualiza usuario')

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
def post_deletar_dados_route(id):
    """Salva dados no banco"""
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
