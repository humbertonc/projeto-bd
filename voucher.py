import sqlite3 as sl

class VoucherTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists CREATE TABLE voucher (
            id_voucher integer NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES lanche (id_produto),
            CONSTRAINT id_voucher_comp PRIMARY KEY (id_voucher, id_produto),
            quantidade integer NOT NULL
        )
        """)

    def create(self, id_voucher, id_product, quantity):

        try:
            self.cur(f"""INSERT INTO voucher(id_voucher, id_produto, quantidade) 
            VALUES({id_voucher}, {id_product}, {quantity})""")
            print(f"Voucher gerado com sucesso")
        except:
            print("Não foi possível gerar o voucher")
        print('')

    def read(self, id_voucher):

        data = self.cur.execute(f"""SELECT (nome, quantidade, preco) 
        FROM (produto JOIN lanche JOIN voucher) WHERE id_voucher == {id_voucher}""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum voucher encontrado com id {id_voucher}")
        else:
            for row in ret_vals:
                print(f"Nome do produto: {row[0]}, Quantidade do produto: {row[1]}, Preço do produto: {row[2]}")
        print('')

    def read_all(self):
        data = self.cur.execute(f"""SELECT (id_voucher, nome, quantidade, preco) 
        FROM (produto JOIN lanche JOIN voucher)""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum voucher encontrado")
        else:
            for row in ret_vals:
                print(f"ID: {row[0]}, Nome do produto: {row[1]}, Quantidade do produto: {row[2]}, Preço do produto: {row[3]}")
        print('')

    def read_last(self):
        data = self.cur.execute(f"SELECT (MAX(id_voucher), id_produto, quantidade) FROM voucher")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum voucher encontrado")
        else:
            return ret_vals
        
'''
# Testando criação
table.create(1, 1, 2)
table.create(1, 2, 4)

# Testando leitura
table.read(1)
table.read_all()

data = read_last()
print(data)
'''

#table.con.commit()
#table.con.close()