import sqlite3


class SqliteDB:
    conn = None
    cursor = None
    name = None

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.name = db_name.split('.')[0]

    def __str__(self):
        return self.name

    def check_table_exists(self, table_name):
        sql = f'select * from sqlite_master where type = "table" and name = "{table_name}"'
        rst = self.cursor.execute(sql).fetchall()
        if rst:
            return True
        else:
            return False

    def export(self, table_name, file_name):
        sql = f'select * from {table_name};'
        rst = self.cursor.execute(sql).fetchall()
        if rst:
            f = open(file_name, 'w', encoding='utf-8')
            for line in rst:
                f.writelines(f'{line[0]}\t{line[1]}\n')

    def create_table(self, sql):
        if sql:
            self.cursor.execute(sql)
            return True
        else:
            return False

    def query_sql(self, sql):
        return self.execute(sql)

    def query_recorder(self, table: str, filter: str):
        sql=f"select * from {table} where {filter};"
        return self.execute(sql)

    def execute(self, sql):
        return self.cursor.execute(sql).fetchall()

    def commit(self):
        return self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
