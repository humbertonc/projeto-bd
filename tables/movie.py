import sqlite3 as sl
from tables.producer import ProducerTable
from tables.actor import ActorTable

class MovieTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists filme (
            id_filme integer PRIMARY KEY autoincrement NOT NULL,
            titulo varchar(90) NOT NULL,
            categoria varchar(90) NOT NULL,
            duracao integer NOT NULL,
            censura char NOT NULL,
            nacional BOOLEAN
        )
        """)
        self.cur.execute("""
        CREATE TABLE if not exists filme_produtora (
            id_filme integer,
            id_produtora integer,
            FOREIGN KEY (id_filme) REFERENCES filme (id_filme),
            FOREIGN KEY (id_produtora) REFERENCES produtora (id_produtora)
        )
        """)
        self.cur.execute("""
        CREATE TABLE if not exists filme_ator (
            id_filme integer,
            id_ator integer,
            FOREIGN KEY (id_filme) REFERENCES filme (id_filme),
            FOREIGN KEY (id_ator) REFERENCES ator (id_ator)
        )
        """)

    def create(self, title, genre, duration, rating, national, id_producer, ids_actors):

        #try:
        self.cur.execute(f"""INSERT INTO filme (titulo, categoria, duracao, censura, nacional) 
        VALUES('{title}', '{genre}', {duration}, '{rating}', {national})""")
        id_movie = self.cur.execute("SELECT last_insert_rowid();").fetchall()[0][0]
        
        self.cur.execute(f"""INSERT INTO filme_produtora(id_filme, id_produtora) 
        VALUES({id_movie}, {id_producer})""")
        for id_actor in ids_actors:
            self.cur.execute(f"""INSERT INTO filme_ator(id_filme, id_ator) 
            VALUES({id_movie}, {id_actor})""")
        print(f"Filme cadastrado com sucesso")
        #except:
        #    print("Não foi possível cadastrar o filme")
        print('')

    def read(self, id_movie):

        # Select movie and producer
        movie_data = self.cur.execute(f"""SELECT titulo, categoria, duracao, censura, nacional, nome_produtora
        FROM filme, filme_produtora, produtora WHERE filme.id_filme == filme_produtora.id_filme AND 
        produtora.id_produtora == filme_produtora.id_produtora AND filme.id_filme == {id_movie}""")
        ret_vals = movie_data.fetchall()
        if not ret_vals:
            print(f"Nenhum filme encontrado com id {id_movie}\n")
        else:
            # Select actors
            actors_data = self.cur.execute(f"""SELECT nome_ator FROM filme_ator, ator
            WHERE ator.id_ator == filme_ator.id_ator AND filme_ator.id_filme == {id_movie}""")
            actors_vals = actors_data.fetchall()

            # Display result
            for row in ret_vals:
                is_national = "Internacional"
                if row[4]:
                    is_national = "Nacional"
                print(f"Título: {row[0]}; Categoria: {row[1]}; Duração: {row[2]}; Censura: {row[3]}; {is_national}; Atores: ", end='')
                for i, actor in enumerate(actors_vals):
                    print(actor[0], end='')
                    if i != len(actors_vals) - 1:
                        print(", ", end='')
                print('')
        
    def read_all(self):

        # Select movie and producer
        movie_data = self.cur.execute(f"""SELECT filme.id_filme, titulo, categoria, duracao, censura, nacional, nome_produtora
        FROM filme, filme_produtora, produtora WHERE filme.id_filme == filme_produtora.id_filme AND 
        produtora.id_produtora == filme_produtora.id_produtora""")
        ret_vals = movie_data.fetchall()
        if not ret_vals:
            print(f"Nenhum filme encontrado\n")
        else:
            # Select actors
            actors_data = self.cur.execute(f"""SELECT nome_ator FROM filme_ator, ator
            WHERE ator.id_ator == filme_ator.id_ator""")
            actors_vals = actors_data.fetchall()

            # Display result
            for row in ret_vals:
                is_national = "Internacional"
                if row[5]:
                    is_national = "Nacional"
                print(f"ID: {row[0]}; Título: {row[1]}; Categoria: {row[2]}; Duração: {row[3]}; Censura: {row[4]}; {is_national}; Atores: ", end='')
                for i, actor in enumerate(actors_vals):
                    print(actor[0], end='')
                    if i != len(actors_vals) - 1:
                        print(", ", end='')
                print('')
'''
prod_table = ProducerTable()
prod_table.create('20th Century Studios')
prod_table.create('Disney')

# # Testando leitura
# print(prod_table.get_id('20th Century Studios'))
# print(prod_table.get_id('Disney'))
prod_table.con.commit()
prod_table.con.close()

actor_table = ActorTable()
actor_table.create('Macaulin Culkin')
actor_table.create('Joe Pesci')
actor_table.create('Daniel Stern')

# # Testando leitura
# print(actor_table.get_id('Macaulin Culkin'))
# print(actor_table.get_id('Joe Pesci'))
# print(actor_table.get_id('Daniel Stern'))
actor_table.con.commit()
actor_table.con.close()

table = MovieTable()
# Testando criação
table.create('Esqueceram de mim', 'Comédia', 60*1 + 43, 'L', False, 1, [1, 2, 3])

# Testando leitura
table.read(1)
table.read_all()

#table.con.commit()
table.con.close()'''
