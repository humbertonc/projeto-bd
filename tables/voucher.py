import sqlite3 as sl
from tables.snack import SnackTable

class VoucherTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
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

        #try:
        self.cur.execute(f"""INSERT INTO voucher(id_voucher, id_produto, quantidade) 
        VALUES({id_voucher}, {id_product}, {quantity})""")
        #except:
        #    print("Não foi possível gerar o voucher")
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
        FROM produto, lanche, voucher WHERE produto.id_produto == lanche.id_produto AND produto.id_produto == voucher.id_produto""")
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
        

# Testando criação
'''
snack_table = SnackTable()
snack_table.create(12,'biscoito')
snack_table.create(15,'bolacha')
snack_table.con.commit()
snack_table.con.close()
table = VoucherTable()
table.create(1, 1, 2)
table.create(1, 2, 4)

# Testando leitura
table.read(1)
table.read_all()
#print(read_last())


#table.con.commit()
table.con.close()'''
