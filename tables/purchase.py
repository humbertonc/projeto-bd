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
        self.cur.execute("""
        CREATE TABLE if not exists compra_voucher (
            id_compra integer,
            id_voucher integer,
            FOREIGN KEY (id_compra) REFERENCES compra (id_compra),
            FOREIGN KEY (id_voucher) REFERENCES voucher (id_voucher)
        )
        """)

    def create(self, id_client, form_of_payment, date, ids_products, id_voucher = None):

        try:
            self.cur(f"""INSERT INTO compra(id_cliente, forma_de_pagamento, data_compra) 
            VALUES({id_client}, '{form_of_payment}', '{date}')""")
            id_purchase = self.cur("SELECT last_insert_rowid();").fetchall()[0][0]
            for id_product in ids_products:
                self.cur.execute(f"""INSERT INTO compra_produto(id_compra, id_produto) 
                VALUES({id_purchase}, {id_product})""")
            if id_voucher != None:
                self.cur(f"INSERTO INTO compra_voucher(id_compra, id_voucher) VALUES({id_voucher})")
            print(f"Compra cadastrada com sucesso")
            return id_purchase
        except:
            print("Não foi possível cadastrar a compra")
        print('')

    def read_by_id(self, id_purchase):

        # Select purchase
        data_purchase = self.cur(f"""SELECT id_cliente, forma_de_pagamento, data_compra FROM compra 
        WHERE id_compra == {id_purchase}""")
        ret_vals = data_purchase.fetchall()
        if not ret_vals:
            print(f"Nenhuma compra encontrada com id {id_purchase}")
        else:
            ## Tickets
            data_tickets = self.cur(f"""SELECT preco FROM compra_produto, produto 
            WHERE compra_produto.id_produto == produto.id_produto AND id_compra == {id_purchase} 
            AND cod_produto == 1""")
            tickets_vals = data_tickets.fetchall()
            total_price = sum(tickets_vals)

            ## Snacks
            # Select ids and quantities of snacks bought in purchase from voucher table
            data_snacks = self.cur(f"""SELECT id_produto, quantidade FROM compra_voucher, voucher 
            WHERE compra_voucher.id_voucher == voucher.id_voucher AND id_compra == {id_purchase}""")
            snack_vals = data_snacks.fetchall()

            # Get the price for each snack from produto table
            for row_snack in snack_vals:
                data_price = self.cur(f"SELECT preco FROM produto WHERE id_produto == {row_snack[0]}")
                price_vals = data_price.fetchall()
                for row_price in price_vals:
                    total_price += row_snack[1]*row_price[0] # quantity*price

            # Display result
            for row in ret_vals:
                print(f"ID do(a) cliente: {row[0]}; Forma de pagamento: {row[1]}; Data da compra: {row[2]}; Valor pago: R${total_price}")
        print("")

    def read_by_client(self, id_client):

        data_client = self.cur(f"""SELECT id_compra, forma_de_pagamento, data_compra FROM compra 
        WHERE id_cliente == {id_client}""")
        ret_vals = data_client.fetchall()
        if not ret_vals:
            print(f"Nenhuma compra encontrada sob cliente de id {id_client}\n")
        else:
            for row in ret_vals:
                ## Tickets
                data_tickets = self.cur(f"""SELECT preco FROM compra_produto, produto 
                WHERE compra_produto.id_produto == produto.id_produto AND id_compra == {row[0]} AND 
                cod_produto == 1""")
                tickets_vals = data_tickets.fetchall()
                total_price = sum(tickets_vals)

                ## Snacks
                # Select ids and quantities of snacks bought in purchase from voucher table
                data_snacks = self.cur(f"""SELECT id_produto, quantidade FROM (compra_voucher, voucher 
                WHERE compra_voucher.id_voucher == voucher.id_voucher AND id_compra == {row[0]}""")
                snack_vals = data_snacks.fetchall()

                # Get the price for each snack from produto table
                for row_snack in snack_vals:
                    data_price = self.cur(f"SELECT preco FROM produto WHERE id_produto == {row_snack[0]}")
                    price_vals = data_price.fetchall()
                    for row_price in price_vals:
                        total_price += row_snack[1]*row_price[0] # quantity*price

                # Display result
                print(f"ID da compra: {row[0]}; Forma de pagamento: {row[1]}; Data da compra: {row[2]}; Valor pago: R${total_price}\n")
        
'''
# Testando criação
id = table.create(1, 'CARTÃO DE CRÉDITO', '06-12-2022', [1, 2, 3, 4], [1, 2])

# Testando leitura
table.read_by_id(id)
table.read_by_client(1)
'''

#table.con.commit()
#table.con.close()
