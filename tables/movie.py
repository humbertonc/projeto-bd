import sqlite3 as sl

class MovieTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists filme (
            id_filme serial PRIMARY KEY,
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

        try:
            self.cur(f"""INSERT INTO filme(titulo, categoria, duracao, censura, nacional) 
            VALUES({title}, {genre}, {duration}, {rating}, {national})""")
            id_movie = self.cur("SELECT SCOPE_IDENTITY();")
            self.cur.execute(f"""INSERT INTO filme_produtora(id_filme, id_produtora) 
            VALUES({id_movie}, {id_producer})""")
            for id_actor in ids_actors:
                self.cur.execute(f"""INSERT INTO filme_ator(id_filme, id_ator) 
                VALUES({id_movie}, {id_actor})""")
            print(f"Filme cadastrado com sucesso")
        except:
            print("Não foi possível cadastrar o filme")
        print('')

    def read(self, id_movie):

        # Select movie and producer
        movie_data = self.cur.execute(f"""SELECT (titulo, categoria, duracao, censura, nacional, nome_produtora) 
        FROM (filme JOIN filme_produtora JOIN produtora) WHERE id_filme == {id_movie}""")
        ret_vals = movie_data.fetchall()
        if not ret_vals:
            print(f"Nenhum filme encontrado com id {id_movie}\n")
        else:
            # Select actors
            actors_data = self.cur.execute(f"""SELECT (nome_ator) FROM (filme_ator JOIN ator) 
            WHERE id_filme == {id_movie}""")
            actors_vals = actors_data.fetchall()

            # Display result
            for row in ret_vals:
                is_national = "Internacional"
                if row[4]:
                    is_national = "Nacional"
                print(f"Título: {row[0]}; Categoria: {row[1]}; Duração: {row[2]}; Censura: {row[3]}; {is_national}; Atores: ", end='')
                for i, actor in enumerate(actors_vals):
                    print(actor, end='')
                    if i != len(actors_vals) - 1:
                        print(", ", end='')
                print('')

'''
# Testando criação
table.create('Esqueceram de mim', 'Comédia', 60*1 + 43, 'L', false, 1, [1, 2, 3])

# Testando leitura
table.read(1)
'''

#table.con.commit()
#table.con.close()
