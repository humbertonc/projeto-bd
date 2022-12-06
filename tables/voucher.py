import sqlite3 as sl

class VoucherTable:
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
        self.cur.execute("""
        CREATE TABLE if not exists voucher (
            id_voucher integer NOT NULL,
            id_produto integer NOT NULL,
            quantidade integer NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES lanche (id_produto),
            CONSTRAINT id_voucher_comp PRIMARY KEY (id_voucher, id_produto)
        )
        """)

    def create(self, id_voucher, id_product, quantity):

        try:
            self.cur.execute(f"""INSERT INTO voucher(id_voucher, id_produto, quantidade) 
            VALUES({id_voucher}, {id_product}, {quantity})""")
            print(f"Voucher gerado com sucesso")
        except:
            print("Não foi possível gerar o voucher")
        print('')

    def read(self, id_voucher):

        data = self.cur.execute(f"""SELECT nome_lanche, quantidade, preco 
        FROM produto, lanche, voucher WHERE produto.id_produto == lanche.id_produto AND
        lanche.id_produto == voucher.id_produto AND id_voucher == {id_voucher}""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum voucher encontrado com id {id_voucher}")
        else:
            for row in ret_vals:
                print(f"Nome do produto: {row[0]}; Quantidade do produto: {row[1]}; Preço do produto: R${row[2]}")
        print('')

    def read_all(self):
        data = self.cur.execute(f"""SELECT id_voucher, nome_lanche, quantidade, preco 
        FROM produto, lanche, voucher WHERE produto.id_produto == lanche.id_produto AND lanche.id_produto == voucher.id_produto""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum voucher encontrado")
        else:
            for row in ret_vals:
                print(f"ID: {row[0]}; Nome do produto: {row[1]}; Quantidade do produto: {row[2]}; Preço do produto: R${row[3]}")
        print('')

    def read_last(self):
        data = self.cur.execute(f"SELECT MAX(id_voucher), id_produto, quantidade FROM voucher")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum voucher encontrado")
        else:
            return ret_vals
        
'''
# Testando criação
table = VoucherTable()
table.cur.execute(f"INSERT INTO produtora(nome_produtora) VALUES('produtora')")
table.create(1, 1, 2)
table.create(1, 2, 4)

# Testando leitura
table.read(1)
table.read_all()
#print(read_last())


#table.con.commit()
table.con.close()'''
