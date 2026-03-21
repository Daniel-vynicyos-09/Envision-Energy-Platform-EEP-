import sqlite3


def conectar():
    return sqlite3.connect("data/consumo.db")


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consumo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        valor REAL
    )
    """)

    conn.commit()
    conn.close()


def inserir(valor):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO consumo (valor) VALUES (?)", (valor,))

    conn.commit()
    conn.close()


def listar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT valor FROM consumo")
    dados = cursor.fetchall()

    conn.close()
    return [d[0] for d in dados]