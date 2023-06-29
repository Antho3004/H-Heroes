import sqlite3

connection = sqlite3.connect("HallyuHeroes.db")
cursor = connection.cursor()

def table_users():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            description TEXT,
            argent INTEGER,
            nombre_de_cartes INTEGER,
            carte_favori TEXT
        )
    """)
    connection.commit()
