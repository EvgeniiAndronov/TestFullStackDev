import tkinter as tk
import psutil
import sqlite3
import pandas as pd
from datetime import datetime

class SystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Системный монитор")

        self.menu = tk.Menu(self.root)
        self.podmenu = tk.Menu(self.menu, tearoff=0)
        self.podmenu.add_command(label="Создать csv файл по имеющимся данным", command=create_scvfile)
        self.podmenu.add_command(label="Очистить имеющиеся данные", command=clear_db)
        self.menu.add_cascade(label="Файл", menu=self.podmenu)

        self.cpu_label = tk.Label(root, text="Загрузка ЦП: 0%", font=("Helvetica", 16))
        self.cpu_label.pack(pady=10)

        self.ram_label = tk.Label(root, text="Использование ОЗУ: 0%", font=("Helvetica", 16))
        self.ram_label.pack(pady=10)

        self.disk_label = tk.Label(root, text="Использование ПЗУ: 0%", font=("Helvetica", 16))
        self.disk_label.pack(pady=10)

        self.time_interval_label = tk.Label(root, text="Введите интервал времени обновлений", font=("Helvetica", 16))
        self.time_interval_label.pack(pady=10)

        self.time_interval_entry = tk.Entry(root)
        self.time_interval_entry.pack(pady=10)

        self.start_write = tk.Button(root, text="Начать запись", command=self.update_and_save_metrics)
        self.start_write.pack(pady=10)

        self.stop_button = None
        self.after_id = None

        self.root.config(menu=self.menu)

    def update_and_save_metrics(self):
        time_interval = self.time_interval_entry.get()
        try:
            time_interval = int(time_interval)

            self.start_write.pack_forget()
            if not self.stop_button:
                self.stop_button = tk.Button(self.root, text="Остановить запись", command=self.stop_write)
                self.stop_button.pack(pady=10)

            cpu_usage = psutil.cpu_percent(interval=0)
            ram_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent

            self.cpu_label.config(text=f"Загрузка ЦП: {cpu_usage}%")
            self.ram_label.config(text=f"Использование ОЗУ: {ram_usage}%")
            self.disk_label.config(text=f"Использование ПЗУ: {disk_usage}%")

            save_metrics(cpu_usage, ram_usage, disk_usage)

            self.after_id = self.root.after(time_interval, self.update_and_save_metrics)
        except ValueError:
            self.time_interval_label.config(text="Некорректно задан интервал обновлений.")
            self.start_write.pack()

    def stop_write(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        if self.stop_button:
            self.stop_button.pack_forget()
            self.stop_button = None

        self.start_write.pack(pady=10)

def create_scvfile():
    conn = sqlite3.connect('data.db')
    print("CREATE CSV FILE")
    df = pd.read_sql_query("SELECT * FROM data_usage", conn)
    date_time =  datetime.now().strftime("%S/%M/%H/%d/%m/%Y")
    df.to_csv(f'выгрузка_загруженyости_{date_time}.csv', index=False)
    conn.close()

def clear_db():
    conn = sqlite3.connect('data.db')
    print("CLEAR DB")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS data_usage")
    conn.close()

def save_metrics(cpu, ram, disk):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_usage (
                    id INTEGER PRIMARY KEY,
                    cpu FLOAT,
                    ram FLOAT,
                    disk FLOAT,
                    time_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    cursor.execute('INSERT INTO data_usage (cpu, ram, disk) VALUES (?, ?, ?)', (cpu, ram, disk))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    monitor = SystemMonitor(root)
    root.mainloop()
