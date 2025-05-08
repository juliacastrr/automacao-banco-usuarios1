import mysql.connector
import requests

def conectar_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="banco_teste_automacao"
    )

def extrair_campos(usuario):
    return (
        usuario.get("id", ""),
        usuario.get("name", ""),
        usuario.get("email", ""),
        usuario.get("userName", ""),
        usuario.get("Password", "")
    )

# Cenário 1 #

def popular_tabela():
    conn = conectar_mysql()
    cursor = conn.cursor()

    url = "https://n8n.apptrix.app/webhook/a1841391-56ad-4a75-bfeb-e005b673c756"
    response = requests.get(url)
    dados = response.json()

    for usuario in dados:
        try:
            cursor.execute("""
                INSERT INTO usuarios (id, name, email, userName, Password)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                usuario.get("id", ""),
                usuario.get("name", ""),
                usuario.get("email", ""),
                usuario.get("userName", ""),
                usuario.get("Password", ""),
            ))
        except mysql.connector.IntegrityError:
            print(f"Usuário com ID {usuario['id']} já existe.")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tabela populada com sucesso.")

if __name__ == "__main__":
    popular_tabela()

# Cenário 1.2 #

def atualizar_usuario_novo(id, name, email, userName, password):
    conn = conectar_mysql()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    usuario = cursor.fetchone()

    if usuario:
        print(f"Usuário com ID {id} já existe.")
    else:
        cursor.execute("""
            INSERT INTO usuarios (id, name, email, userName, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (id, name, email, userName, password))
        conn.commit()
        print(f"Usuário com ID {id} foi inserido.")

    cursor.close()
    conn.close()

atualizar_usuario_novo(
    id="23423537",
    name="Novo Usuário1",
    email="novo1@teste.com",
    userName="novo_user1",
    password="654321"
)

# Cenário 1.3 #

def inserir_usuario_sem_duplicar(id, name, email, userName, password):
    conn = conectar_mysql()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    existe = cursor.fetchone()

    if existe:
        print(f"❌ ERRO: Usuário com ID {id} já existe. Inserção bloqueada.")
    else:
        try:
            cursor.execute("""
                INSERT INTO usuarios (id, name, email, userName, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (id, name, email, userName, password))
            conn.commit()
            print(f"✅ Usuário com ID {id} inserido com sucesso.")
        except mysql.connector.IntegrityError as e:
            print(f"❌ Erro ao inserir: {e}")

    cursor.close()
    conn.close()

inserir_usuario_sem_duplicar(
    id="23423532",
    name="Duplicado",
    email="duplicado@teste.com",
    userName="duplicado_user",
    password="123456"
)

# Cenário 1.4 #

def deletar_usuario(id):
    conn = conectar_mysql()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    conn.commit()

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    resultado = cursor.fetchone()

    if resultado is None:
        print(f"✅ Usuário com ID {id} foi deletado com sucesso.")
    else:
        print(f"❌ Usuário com ID {id} ainda existe na tabela.")

    cursor.close()
    conn.close()

deletar_usuario("23423532")