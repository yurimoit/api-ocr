from flask import request, jsonify
from conexao_banco_dados import connectar_banco
from validate_docbr import CPF
import brazilcep


def cadastrar_paciente():
    """"""
    data = request.get_json()
    usuario = request.usuario

    nome = data['nome']
    email = data['email']
    data_nascimento = data['data_nascimento']
    sexo = data['sexo']
    cpf = data['cpf']
    telefone = data['telefone']
    cep = data['cep']
    logradouro = data['logradouro']
    complemento = data['complemento']
    bairro = data['bairro']
    cidade = data['cidade']
    estado = data['estado']

    cursor = None
    conn_conecta = connectar_banco()

    try:

        paciente = {
            'nome': nome,
            'email': email,
            'data_nascimento': data_nascimento,
            'sexo': sexo,
            'cpf': cpf,
            'telefone': telefone,
            'cep': cep,
            'logradouro': logradouro,
            'complemento': complemento,
            'bairro': bairro,
            'cidade': cidade,
            'estado': estado,
            'id_usuario': usuario[0]
        }

        cpf_validador = CPF()
        if not cpf_validador.validate(cpf):
            return jsonify({'mensagem': 'CPF é invalido!'}), 500

        cursor = conn_conecta.cursor()

        cursor.execute("""INSERT INTO pacientes (nome, email, data_nascimento, sexo,
                       cpf,
                       telefone,
                       cep,
                       logradouro,
                       complemento,
                       bairro,
                       cidade,
                       estado,
                       id_usuario
                       ) VALUES (%s, %s, %s, %s,%s, %s,%s, %s, %s,%s, %s, %s, %s)""",
                       (paciente['nome'], paciente['email'], paciente['data_nascimento'],
                        paciente['sexo'], paciente['cpf'], paciente['telefone'],
                        paciente['cep'], paciente['logradouro'], paciente['complemento'],
                        paciente['bairro'],
                        paciente['cidade'], paciente['estado'], paciente['id_usuario']
                        ))

        # id_inserido = cursor.lastrowid
        # print(id_inserido)

        conn_conecta.commit()

        return jsonify({'mensagem': 'Paciente cadastrado'}), 201

    except Exception:
        # print("Erro ao cadastrar usuário:", e)
        return jsonify({'error': 'Erro no servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn_conecta:
            conn_conecta.close()


def atualizar_paciente():
    """"""

    data = request.get_json()
    usuario = request.usuario

    if data is None:
        return jsonify({'mensagem': 'Dados não fornecidos'}), 400

    id = data['id']
    nome = data['nome']
    email = data['email']
    data_nascimento = data['data_nascimento']
    sexo = data['sexo']
    cpf = data['cpf']
    telefone = data['telefone']
    cep = data['cep']
    logradouro = data['logradouro']
    complemento = data['complemento']
    bairro = data['bairro']
    cidade = data['cidade']
    estado = data['estado']

    cursor = None
    conn_conecta = connectar_banco()

    try:

        paciente = {
            'id': id,
            'nome': nome,
            'email': email,
            'data_nascimento': data_nascimento,
            'sexo': sexo,
            'cpf': cpf,
            'telefone': telefone,
            'cep': cep,
            'logradouro': logradouro,
            'complemento': complemento,
            'bairro': bairro,
            'cidade': cidade,
            'estado': estado,
            'id_usuario': usuario[0]
        }

        cpf_validador = CPF()
        if not cpf_validador.validate(cpf):
            return jsonify({'mensagem': 'CPF é invalido!'}), 500

        cursor = conn_conecta.cursor()

        cursor.execute("""
            UPDATE pacientes SET
            nome=%(nome)s, email=%(email)s, data_nascimento=%(data_nascimento)s, sexo=%(sexo)s,
            cpf=%(cpf)s, telefone=%(telefone)s, cep=%(cep)s, logradouro=%(logradouro)s,
            complemento=%(complemento)s, bairro=%(bairro)s, cidade=%(cidade)s, estado=%(estado)s, id_usuario=%(id_usuario)s
            WHERE id=%(id)s
            RETURNING *;
        """, paciente)

        paciente_atualizado = cursor.fetchone()

        conn_conecta.commit()

        if not paciente_atualizado:
            return jsonify({'mensagem': 'Erro no servidor ao tentar atualiza cadastro paciente'}), 500

        return jsonify({'mensagem': 'Paciente atualizado'}), 201

    except Exception:
        # print("Erro ao cadastrar usuário:", e)
        return jsonify({'mensagem': 'Erro no servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn_conecta:
            conn_conecta.close()


def excluir_paciente(id):
    """"""
    if id is None:
        return jsonify({'mensagem': 'Id não fornecido'}), 400

    id_paciente = int(id)
    id_usuario = request.usuario[0]

    cursor = None
    conn_conecta = None

    try:
        conn_conecta = connectar_banco()
        cursor = conn_conecta.cursor()

        cursor.execute(
            "DELETE FROM pacientes where id=%s and id_usuario=%s", (id_paciente, id_usuario))
        conn_conecta.commit()

        return jsonify({"mensagem": "Paciente deletado com sucesso.", "id": id_paciente}), 200

    except Exception:
        # print("Deleta paciente:", e)
        return jsonify({'mensagem': 'Erro no servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn_conecta:
            conn_conecta.close()


def get_pacientes():
    """"""
    usuario = request.usuario
    id_usuario = usuario[0]

    cursor = None
    conn_conecta = None

    try:
        conn_conecta = connectar_banco()

        cursor = conn_conecta.cursor()
        cursor.execute(
            'SELECT * FROM pacientes WHERE id_usuario=%s', (id_usuario,))
        pacientes = cursor.fetchall()

        if not pacientes:
            return jsonify({'mensagem': 'Lista de pacintes não encontrada'}), 404

        lista_objeto = []
        lista_revertida = pacientes[::-1]
        for obj in lista_revertida:
            lista_objeto.append({
                "id": obj[0],
                "nome": obj[1],
                "email": obj[2],
                "data_nascimento": obj[3],
                'sexo': obj[4],
                'cpf': obj[5],
                'telefone': obj[6],
                'cep': obj[7],
                'logradouro': obj[8],
                'complemento': obj[9],
                'bairro': obj[10],
                'cidade': obj[11],
                'estado': obj[12],
                'id_usuario': obj[14]
            })

        return jsonify(lista_objeto), 200

    except Exception:
        # print("Erro ao cadastrar usuário:", e)
        return jsonify({'mensagem': 'Erro no servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn_conecta:
            conn_conecta.close()


def obter_paciente():
    """"""

    if request.args.get('id') == 'null':
        return jsonify({'mensagem': 'Id não fornecido'}), 400

    id = request.args.get('id')
    id_usuario = request.usuario[0]

    cursor = None
    conn_conecta = None

    try:
        conn_conecta = connectar_banco()

        cursor = conn_conecta.cursor()
        cursor.execute(
            'SELECT * FROM pacientes WHERE id=%s and id_usuario=%s', (id, id_usuario))
        paciente = cursor.fetchone()

        if not paciente:
            return jsonify({
                'validador': False,
                'mensagem': 'Paciente não encontrada'
            }), 404

        lista_objeto = []
        lista_revertida = list(paciente)

        lista_objeto.append({
            "id": lista_revertida[0],
            "nome": lista_revertida[1],
            "email": lista_revertida[2],
            "data_nascimento": lista_revertida[3],
            'sexo': lista_revertida[4],
            'cpf': lista_revertida[5],
            'telefone': lista_revertida[6],
            'cep': lista_revertida[7],
            'logradouro': lista_revertida[8],
            'complemento': lista_revertida[9],
            'bairro': lista_revertida[10],
            'cidade': lista_revertida[11],
            'estado': lista_revertida[12],
            'id_usuario': lista_revertida[14]
        })

        return jsonify(lista_objeto), 200

    except Exception:
        # print("Erro ao buscar o paciente:", e)
        return jsonify({'mensagem': 'Erro no servidor'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn_conecta:
            conn_conecta.close()


def buscar_filtro_pacientes():
    """BUSCAR PACIENTES NO BANCO DE DADOS FILTRO"""

    id_usuario = int(request.usuario[0])
    busca = request.args.get('busca')

    cursor = None
    conn = None

    try:
        query = "SELECT * FROM pacientes WHERE id_usuario = %s"
        params = [id_usuario]

        if busca:
            query += " AND (nome ILIKE %s OR email ILIKE %s OR id::text ILIKE %s OR cpf::text ILIKE %s OR telefone::text ILIKE %s)"
            params.extend([f"%{busca}%", f"%{busca}%",
                          f"%{busca}%", f"%{busca}%", f"%{busca}%"])

        conn = connectar_banco()
        cursor = conn.cursor()

        cursor.execute(query, params)
        exames = cursor.fetchall()

        conn.commit()

        if not exames:
            return jsonify({"mensagem": "Nenhum resultado encontrado."}), 404

        lista_objeto = []
        lista_revertida = exames[::-1]
        for obj in lista_revertida:
            lista_objeto.append({
                "id": obj[0],
                "nome": obj[1],
                "email": obj[2],
                "data_nascimento": obj[3],
                'sexo': obj[4],
                'cpf': obj[5],
                'telefone': obj[6],
                'cep': obj[7],
                'logradouro': obj[8],
                'complemento': obj[9],
                'bairro': obj[10],
                'cidade': obj[11],
                'estado': obj[12],
                'id_usuario': obj[14]
            })

        return jsonify(lista_objeto), 200

    except Exception:
        # print("Erro ao consultar o banco de dados:", e)
        return jsonify({'error': 'Erro ao consultar o banco de dados'}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def consultar_endereco_por_cep():
    """"""
    cep = request.args.get('codigoPostal')

    try:
        endereco = brazilcep.get_address_from_cep(cep)
        # print(endereco)
        return jsonify(endereco), 200

    except Exception:
        # print("Erro ao busca o cep:", e)
        return jsonify({'mensagem': 'Erro no servidor'}), 500
