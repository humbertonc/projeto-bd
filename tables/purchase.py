import sqlite3 as sl

class PurchaseTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists compra (
            id_compra integer PRIMARY KEY autoincrement NOT NULL,
            id_cliente integer,
            forma_de_pagamento varchar(45) NOT NULL,
            data_compra datetime NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
        )
        """)
        self.cur.execute("""
        CREATE TABLE if not exists compra_produto (
            id_compra integer,
            id_produto integer,
            FOREIGN KEY (id_compra) REFERENCES compra (id_compra),
            FOREIGN KEY (id_produto) REFERENCES produto (id_produto)
        )
        """)

    def create(self, id_client, form_of_payment, date, ids_products):

        try:
            self.cur(f"""INSERT INTO compra(id_cliente, forma_de_pagamento, data_compra) 
            VALUES({id_client}, {form_of_payment}, {date})""")
            id_purchase = self.cur("SELECT SCOPE_IDENTITY();")
            for id_product in ids_products:
                self.cur.execute(f"""INSERT INTO compra_produto(id_compra, id_produto) 
                VALUES({id_purchase}, {id_product})""")
            print(f"Compra cadastrada com sucesso")
        except:
            print("Não foi possível cadastrar a compra")
        print('')
        
'''
# Testando criação
table.create(1, 'CARTÃO DE CRÉDITO', '06-12-2022', true, [1, 2, 3, 4])
'''

#table.con.commit()
#table.con.close()
