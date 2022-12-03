import sqlite3 as sl

class ClientTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists CLIENTE (
            id_cliente integer PRIMARY KEY autoincrement,
            nome varchar(90) NOT NULL
        )
        """)

    def create(self,name):

        try:
            self.cur.execute(f"INSERT INTO CLIENTE(nome) VALUES('{name}')")
            print(f"Cliente {name} cadastrado com sucesso")
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
    
    def read_all(self):
        data = self.cur.execute(f"SELECT * FROM CLIENTE")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum cliente encontrado")
        else:
            for row in ret_vals:
                print(f"ID: {row[0]}, Nome do cliente: {row[1]}")
    
    def update(self, name='', id=0, new_name=''):

        if name:
            data = self.cur.execute(f"UPDATE CLIENTE SET nome = '{new_name}' WHERE nome == '{name}'")
            print(f'Cliente {name} trocado para {new_name}')
        elif id:
            data = self.cur.execute(f"UPDATE CLIENTE SET nome = '{new_name}' WHERE id_cliente == '{id}'")
            print(f'Cliente de id {id} trocado para {new_name}')
        else:
            print("Nao foi possivel atualizar as informacoes do cliente")
    
    def delete(self, name='', id=0):

        if name:
            data = self.cur.execute(f"DELETE FROM CLIENTE WHERE nome == '{name}'")
            print(f'Cliente(s) {name} deletado')
        elif id:
            data = self.cur.execute(f"DELETE FROM CLIENTE WHERE id_cliente == '{id}'")
            print(f'Cliente com id {id} deletado')
        else:
            print("Nao foi possivel deletar o cliente")
            
table = ClientTable()

# Testando criação
table.create('beto')
table.create('lara')

# Testando leitura
table.read('beto')
table.read('lara')
table.read('joaozinho')

# Testando update
table.update(name='lara',new_name='ponpon')
table.update(id=1,new_name='bebeto')
table.read('lara')
table.read('beto')
table.read('bebeto')
table.read('ponpon')

# Testando deleção
table.read_all()
table.delete('bebeto')
table.delete(id=2)
table.read_all()

#table.con.commit()
table.con.close()