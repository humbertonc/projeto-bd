import sqlite3 as sl

class TicketTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists CREATE TABLE produto (
            id_produto serial PRIMARY KEY,
            cod_produto integer NOT NULL,
            preco numeric(7,2) NOT NULL,
        )
        """)
        self.cur.execute("""
        CREATE TABLE if not exists CREATE TABLE ingresso (
            FOREIGN KEY (id_produto) REFERENCES produto(id_produto) PRIMARY KEY,
            FOREIGN KEY (id_sessao) REFERENCES CRONOGRAMA (id_sessao),
            data date NOT NULL,
            tipo_ingresso varchar(15) NOT NULL
        )
        """)

    def create(self, price, id_session, date, type):

        try:
            self.cur(f"INSERT INTO produto(cod_produto, preco) VALUES(1, {price})")
            id_product = self.cur("SELECT SCOPE_IDENTITY();")
            self.cur.execute(f"""INSERT INTO ingresso(id_produto, id_sessao, data, tipo_ingresso) 
            VALUES({id_product}, {id_session}, {date}, {type})""")
            print(f"Ingresso gerado com sucesso")
        except:
            print("Não foi possível gerar o ingresso")
        print('')

    def read(self, id):

        data = self.cur.execute(f"""SELECT (preco, id_sessao, data, tipo_ingresso) 
        FROM (produto JOIN ingresso) WHERE id_produto == {id}""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum ingresso encontrado com id {id}\n")
        else:
            return ret_vals

    def read_all(self):
        data = self.cur.execute(f"""SELECT (id_produto, preco, id_sessao, data, tipo_ingresso) 
        FROM (produto JOIN ingresso)""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum ingresso encontrado\n")
        else:
            return ret_vals
        
'''
# Testando criação
table.create(15.50, 1, '2022-12-06', 'ESTUDANTE')
table.create(7.75, 1, '2022-12-06', 'INFANTIL')

# Testando leitura
print(table.read(1))
print(table.read(2))
print(table.read_all())
'''

#table.con.commit()
#table.con.close()
