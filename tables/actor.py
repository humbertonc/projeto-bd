import sqlite3 as sl

class ActorTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists ator (
            id_ator integer PRIMARY KEY autoincrement NOT NULL,
            nome_ator varchar(90) NOT NULL
        )
        """)

    def create(self, name):

        try:
            self.cur(f"INSERT INTO ator(nome_ator) VALUES({name})")
            print(f"Ator cadastrado com sucesso")
        except:
            print("Não foi possível cadastrar o ator")
        print('')

    def get_id(self, name):

        data = self.cur.execute(f"SELECT id_ator FROM ator WHERE nome_ator == {name}")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum ator encontrado com nome {name}\n")
        else:
            return ret_vals
            
'''
# Testando criação
table.create('Macaulin Culkin')
table.create('Joe Pesci')
table.create('Daniel Stern')

# Testando leitura
print(table.get_id('Macaulin Culkin'))
print(table.get_id('Joe Pesci'))
print(table.get_id('Daniel Stern'))
'''

#table.con.commit()
#table.con.close()
