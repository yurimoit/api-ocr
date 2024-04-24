import jwt
import os
from flask import request, jsonify
from dotenv import load_dotenv
from functools import wraps
from conexao_banco_dados import connectar_banco

load_dotenv()

SENHA_JWT = os.environ.get('senhaJWT')


def verificar_autenticacao(next):
    """MIDDLEWARE PARA CHAMAR A FUNCAO DE AUTENTICACAO"""

    @wraps(next)
    def verificar_usuario(*args, **kwargs):
        """VERIFICAR AUTENTICACAO DO USUARIO"""

        authorization = request.headers.get('Authorization')
        if not authorization:
            return jsonify({'mensagem': 'Não autorizado'}), 401

        token = authorization.split(' ')[1]

        cursor = None
        conn = None

        try:
            id = jwt.decode(token, SENHA_JWT, algorithms=['HS256'])['id']

            # Conectando ao banco de dados
            conn = connectar_banco()
            cursor = conn.cursor()

            # Inserindo o usuário no banco de dados
            cursor.execute("select * from usuarios where id=%s", (id,))
            resultado = cursor.fetchone()
            conn.commit()
            # print("Resultado: ", resultado)

            if not resultado:
                return jsonify({'mensagem': 'Não autorizado'}), 401

            usuario_logado = {k: v for k,
                              v in enumerate(resultado) if k != 3}

            request.usuario = usuario_logado

            return next(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Token inválido'}), 401
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return verificar_usuario
