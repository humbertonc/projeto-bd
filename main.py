import sqlite3 as sl

class ClientTable:
    def __init__(self):
        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        try:
            self.cur.execute("""
            CREATE TABLE CLIENTE (
                id_cliente integer PRIMARY KEY autoincrement,
                nome varchar(90) NOT NULL
            )
            """)
        except:
            pass

    def create(self,name):
        try:
            self.cur.execute(f"INSERT INTO CLIENTE(nome) VALUES('{name}')")
            print("Cliente cadastrado com sucesso")
        except:
            print("Não foi possível cadastrar o cliente")

    def read(self,name):
        data = self.cur.execute(f"SELECT * FROM CLIENTE WHERE nome == '{name}'")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum cliente encontrado com nome {name}")
        else:
            for row in ret_vals:
                print(f"ID: {row[0]}, Nome do cliente: {row[1]}")
            

table = ClientTable()

table.create('beto')
table.create('lara')
table.read('beto')
table.read('lara')
table.read('joaozinho')
table.con.close()