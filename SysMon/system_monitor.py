import tkinter as tk
import psutil
from db.menu_defs import *
from SysMon.dop_methods import save_metrics

class SystemMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Системный монитор")

        self.menu = tk.Menu(self.root)
        self.pod_menu = tk.Menu(self.menu, tearoff=0)
        self.pod_menu.add_command(label="Создать csv файл по имеющимся данным", command=create_csv_file)
        self.pod_menu.add_command(label="Очистить имеющиеся данные", command=clear_db)
        self.menu.add_cascade(label="Файл", menu=self.pod_menu)

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
