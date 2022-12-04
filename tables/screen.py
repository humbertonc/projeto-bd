import sqlite3 as sl

class ScreenTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists CREATE TABLE sala (
            id_sala serial PRIMARY KEY,
            capacidade integer NOT NULL
        )
        """)

    def create(self, capacity):

        try:
            self.cur(f"INSERT INTO sala(capacidade) VALUES({capacity})")
            print(f"Sala cadastrada com sucesso")
        except:
            print("Não foi possível cadastrar a sala")
        print('')

    def get_capacity(self, id_screen):

        data = self.cur.execute(f"SELECT capacidade FROM sala WHERE id_sala == {id_screen}")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhuma sala encontrada com id {id_screen}\n")
        else:
            return ret_vals

'''
# Testando criação
table.create(100)
table.create(70)

# Testando leitura
print(table.get_capacity(1))
print(table.get_capacity(2))
'''

#table.con.commit()
#table.con.close()
