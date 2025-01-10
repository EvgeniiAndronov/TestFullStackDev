import sqlite3
from db.scripts_for_db import create_db_if_not_exist, insert_data

def save_metrics(cpu, ram, disk):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute(create_db_if_not_exist)

    cursor.execute(f'{insert_data}', (cpu, ram, disk))
    conn.commit()
    conn.close()