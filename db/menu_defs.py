import sqlite3
import pandas as pd
from datetime import datetime
from db.scripts_for_db import select_all, del_data


def create_csv_file():
    conn = sqlite3.connect('data.db')

    try:
        df = pd.read_sql_query(select_all, conn)
        date_time =  datetime.now().strftime("%S:%M:%H:%d:%m:%Y")
        df.to_csv(f'выгрузка_загруженности_{date_time}.csv', index=False)
    except Exception as e:
        print(e)

    conn.close()

def clear_db():
    conn = sqlite3.connect('data.db')

    cursor = conn.cursor()
    cursor.execute(del_data)
    conn.close()