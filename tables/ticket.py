import sqlite3 as sl

class TicketTable:
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
        CREATE TABLE if not exists ingresso (
            id_produto integer,
            id_sessao integer,
            data_sessao date NOT NULL,
            tipo_ingresso varchar(15) NOT NULL,
            FOREIGN KEY (id_produto) REFERENCES produto (id_produto),
            FOREIGN KEY (id_sessao) REFERENCES programacao (id_sessao)
        )
        """)

    def create(self, price, id_session, date, type):

        try:
            tickets_sold = self.cur.execute(f"""COUNT(id_produto) FROM ingresso 
            WHERE id_sessao == {id_session} AND data == {date}""").fetchall()[0][0]
            session_capacity = self.cur.execute(f"""SELECT capacidade FROM sala, programacao
            WHERE sala.id_sala == programacao.id_sala AND id_sessao == {id_session}""").fetchall()[0][0]
            if tickets_sold < session_capacity:
                self.cur.execute(f"INSERT INTO produto(cod_produto, preco) VALUES(1, {price})")
                id_product = self.cur.execute("SELECT last_insert_rowid();").fetchall()[0][0]
                self.cur.execute(f"""INSERT INTO ingresso(id_produto, id_sessao, data_sessao, tipo_ingresso) 
                VALUES({id_product}, {id_session}, '{date}', '{type}')""")
                print(f"Ingresso gerado com sucesso")
                return id_product
            else:
                print("Sessão esgotada, não foi possível gerar o ingresso")
        except:
            print("Não foi possível gerar o ingresso")
        print('')

    def read(self, id):

        data = self.cur.execute(f"""SELECT id_sessao, data_sessao, tipo_ingresso, preco 
        FROM produto, ingresso WHERE produto.id_produto == ingresso.id_produto AND produto.id_produto == {id}""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum ingresso encontrado com id {id}")
        else:
            for row in ret_vals:
                print(f"ID da sessão: {row[0]}; Data da sessão: {row[1]}; Tipo de ingresso: {row[2]}; Preço: R${row[3]}")
        print('')

    def read_all(self):
        data = self.cur.execute(f"""SELECT produto.id_produto, id_sessao, data_sessao, tipo_ingresso, preco 
        FROM produto, ingresso WHERE produto.id_produto == ingresso.id_produto""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhum ingresso encontrado")
        else:
            for row in ret_vals:
                print(f"ID: {row[0]}; ID da sessão: {row[1]}; Data da sessão: {row[2]}; Tipo de ingresso: {row[3]}; Preço: R${row[4]}")
        print('')
        

# Testando criação
'''table = TicketTable()
table.create(15.50, 1, '2022-12-06', 'ESTUDANTE')
table.create(7.75, 1, '2022-12-06', 'INFANTIL')

# Testando leitura
table.read(1)
table.read(2)
table.read_all()


#table.con.commit()
table.con.close()'''
