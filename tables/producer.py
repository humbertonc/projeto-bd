import sqlite3 as sl

class ProducerTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists produtora (
            id_produtora serial PRIMARY KEY,
            nome_produtora varchar(90) NOT NULL
        )
        """)

    def create(self, name):

        try:
            self.cur(f"INSERT INTO produtora(nome_produtora) VALUES({name})")
            print(f"Produtora cadastrada com sucesso")
        except:
            print("Não foi possível cadastrar a produtora")
        print('')

    def get_id(self, name):

        data = self.cur.execute(f"SELECT id_produtora FROM produtora WHERE nome_produtora == {name}")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhuma produtora encontrada com nome {name}\n")
        else:
            return ret_vals

'''
# Testando criação
table.create('20th Century Studios')
table.create('Disney')

# Testando leitura
print(table.get_id('20th Century Studios'))
print(table.get_id('Disney'))
'''

#table.con.commit()
#table.con.close()
