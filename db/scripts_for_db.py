create_db_if_not_exist = '''
    CREATE TABLE IF NOT EXISTS data_usage (
                    id INTEGER PRIMARY KEY,
                    cpu FLOAT,
                    ram FLOAT,
                    disk FLOAT,
                    time_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
    
'''

del_data = "DROP TABLE IF EXISTS data_usage"

select_all = "SELECT * FROM data_usage"

insert_data = 'INSERT INTO data_usage (cpu, ram, disk) VALUES (?, ?, ?)'