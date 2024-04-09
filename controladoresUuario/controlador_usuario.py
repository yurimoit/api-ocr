
from flask import request, jsonify
from flask_bcrypt import Bcrypt
import psycopg2
import jwt
import os
from dotenv import load_dotenv


SENHA_JWT = os.environ.get('senhaJWT')


def connectar_banco():
    """CONNECTA COM BANCO DE DADOS"""

    load_dotenv()

    conn = psycopg2.connect(
        host=os.environ.get('host'),
        database=os.environ.get('database'),
        user=os.environ.get('user'),
        password=os.environ.get('password')
    )

    return conn


def cadastrar_usuario():
    """Recebendo os dados do corpo da requisição"""

    bcrypt = Bcrypt()

    nome = request.json.get('nome')
    email = request.json.get('email')
    senha = request.json.get('senha')
    is_doutor = request.json.get('is_doutor')

    # print(nome, email, senha, is_doutor)

    cursor = None
    conn_conecta = connectar_banco()

    try:
        # Criptografando a senha
        senha_criptografada = bcrypt.generate_password_hash(
            senha).decode('utf-8')

        # Criando um dicionário com os dados do usuário
        usuario = {'nome': nome, 'email': email,
                   'senha': senha_criptografada, 'is_doutor': is_doutor}

        # Conectando ao banco de dados
        cursor = conn_conecta.cursor()

        # Inserindo o usuário no banco de dados
        cursor.execute("INSERT INTO usuarios (nome, email, senha, is_doutor) VALUES (%s, %s, %s, %s)",
                       (usuario['nome'], usuario['email'], usuario['senha'], usuario['is_doutor']))

        id_inserido = cursor.lastrowid

        conn_conecta.commit()

        return jsonify({'mensagem': 'Usuário cadastrado'}), 201

    except Exception as e:
        print("Erro ao cadastrar usuário:", e)
        return jsonify({'error': 'Erro no servidor'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn_conecta:
            conn_conecta.close()


# pylint: disable=E0401

def login_usuario():
    """Recebendo os dados do corpo da requisição"""

    bcrypt = Bcrypt()

    email = request.json.get('email')
    senha = request.json.get('senha')

    # print("Aqui: ", email, senha)

    cursor = None
    conn = None

    try:
        # Conectando ao banco de dados
        cursor = connectar_banco().cursor()

        cursor.execute(
            "select * from usuarios where email=%s", (email,))
        usuario = cursor.fetchone()

        if not usuario or usuario is None:
            return jsonify({'mensagem': 'E-mail ou Senha, invalidos'}), 404

        usuario = list(usuario)

        hash_senha = str(usuario[3])

        if not bcrypt.check_password_hash(hash_senha, senha.encode('utf-8')):
            return jsonify({'mensagem': 'Email ou senha inválidos'}), 404

        token = jwt.encode({'id': usuario[0]}, SENHA_JWT, algorithm='HS256')

        return jsonify({'usuario': {'id': usuario[0], 'nome': usuario[1], 'email': usuario[2]}, 'token': token}), 200

    except Exception as e:
        # print("Erro ao tentar fazer o Login usuário:", e)
        return jsonify({'error': 'Erro no servidor'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            connectar_banco().close()


def atualizar_usuario():
    data = request.get_json()
    usuario = request.usuario

    novo_nome = data['novo_nome']
    novo_email = data['novo_email']
    nova_senha = data['nova_senha']
    novo_cpf = data['novo_cpf']
    novo_telefone = data['novo_telefone']

    bcrypt = Bcrypt()

    cursor = None
    conn_conecta = connectar_banco()

    try:
        cursor = conn_conecta.cursor()

        if nova_senha:
            senha_criptografada = bcrypt.generate_password_hash(
                nova_senha).decode('utf-8')
            usuario_atualizado = {
                'nome': novo_nome if novo_nome else usuario[1],
                'email': novo_email if novo_email else usuario[2],
                'senha': senha_criptografada,
                'cpf': novo_cpf if novo_cpf else usuario[5],
                'telefone': novo_telefone if novo_telefone else usuario[6]
            }
            cursor.execute("""
            UPDATE usuarios 
            SET nome = %s, email = %s, senha = %s, cpf = %s, telefone = %s
            WHERE id = %s
            RETURNING *;
        """, (usuario_atualizado['nome'], usuario_atualizado['email'], usuario_atualizado['senha'],
              usuario_atualizado['cpf'], usuario_atualizado['telefone'], usuario[0]))
        else:
            usuario_atualizado = {
                'nome': novo_nome if novo_nome else usuario[1],
                'email': novo_email if novo_email else usuario[2],
                'cpf': novo_cpf if novo_cpf else usuario[5],
                'telefone': novo_telefone if novo_telefone else usuario[6]
            }
            cursor.execute("""
            UPDATE usuarios 
            SET nome = %s, email = %s, cpf = %s, telefone = %s
            WHERE id = %s
            RETURNING *;
        """, (usuario_atualizado['nome'], usuario_atualizado['email'],
              usuario_atualizado['cpf'], usuario_atualizado['telefone'], usuario[0]))

        conn_conecta.commit()

        atualizacao = cursor.fetchone()

        if not atualizacao:
            return jsonify({'error': 'Erro no servidor ao tentar atualiza cadastro usuario'}), 500

        return jsonify(atualizacao), 201

    except Exception as e:
        # print("Erro ao tentar atualiza usuario usuário:", e)
        return jsonify({'error': 'Erro no servidor'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn_conecta:
            conn_conecta.close()
