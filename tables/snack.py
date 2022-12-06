import sqlite3 as sl

class SnackTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists produto (
            id_produto integer PRIMARY KEY autoincrement NOT NULL,
            cod_produto integer NOT NULL,
            preco numeric(7,2) NOT NULL
        )
        """)
        self.cur.execute("""
        CREATE TABLE if not exists lanche (
            id_produto integer,
            nome_lanche varchar(90) NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES produto (id_produto)
        )
        """)

    def create(self, price, name):

        try:
            self.cur.execute(f"INSERT INTO produto(cod_produto, preco) VALUES(2, {price})")
            id_product = self.cur.execute("SELECT last_insert_rowid();").fetchall()[0][0]
            self.cur.execute(f"""INSERT INTO lanche(id_produto, nome_lanche) 
            VALUES({id_product}, '{name}')""")
            print(f"Lanche cadastrado com sucesso")
        except:
            print("Não foi possível cadastrar o lanche")
        print('')

    def read(self, name):

        data = self.cur.execute(f"""SELECT produto.id_produto, nome_lanche, preco 
        FROM produto, lanche WHERE produto.id_produto == lanche.id_produto AND nome_lanche == '{name}'""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum lanche encontrado com nome {name}\n")
        else:
            for row in ret_vals:
                print(f"ID: {row[0]}; Nome do produto: {row[1]}; Preço do produto: R${row[2]}\n")
            return ret_vals

    def read_all(self):
        data = self.cur.execute(f"SELECT produto.id_produto, nome_lanche, preco FROM produto, lanche WHERE produto.id_produto == lanche.id_produto")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum lanche encontrado")
        else:
            for row in ret_vals:
                print(f"ID: {row[0]}; Nome do produto: {row[1]}; Preço do produto: R${row[2]}")
        print('')
        
'''table = SnackTable()
# Testando criação
table.create(11.50, 'pão de queijo')
table.create(9.00, 'pipoca pequena')
table.create(3.00, 'jujuba')

# Testando leitura
table.read('pão de queijo')
table.read('pipoca grande')
table.read('pipoca pequena')
table.read_all()

#table.con.commit()
table.con.close()'''
