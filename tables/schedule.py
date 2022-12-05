import sqlite3 as sl
import movie

class ScheduleTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists programacao (
            id_sessao serial PRIMARY KEY,
            id_filme integer,
            id_sala integer,
            horario time NOT NULL,
            data_inicio date NOT NULL,
            data_fim date NOT NULL,
            FOREIGN KEY (id_filme) REFERENCES filme (id_filme),
            FOREIGN KEY (id_sala) REFERENCES sala (id_sala)
        )
        """)

    def create(self, id_movie, id_screen, time, date_beginning, date_end):

        try:
            self.cur(f"""INSERT INTO programacao(id_filme, id_sala, horario, data_inicio, data_fim) 
            VALUES({id_movie}, {id_screen}, {time}), {date_beginning}, {date_end}""")
            print(f"Sessão cadastrada com sucesso")
        except:
            print("Não foi possível cadastrar a sessão")
        print('')

    def read_by_id(self, id_session, movie_table : movie.MovieTable):

        data = self.cur.execute(f"""SELECT (id_movie, id_sala, horario, data_inicio, data_fim) 
        FROM (programacao) WHERE id_sessao == {id_session}""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhuma sessão encontrada com id {id_session}")
        else:
            for row in ret_vals:
                movie_table.read(row[0])
                print(f"Sala: {row[1]}; Horário: {row[2]}; Data de estreia: {row[3]}; Fim da sessão: {row[4]}")
        print("")

    def read_by_date(self, date, movie_table : movie.MovieTable):

        data = self.cur.execute(f"""SELECT (id_movie, id_sala, horario, data_inicio, data_fim) 
        FROM (programacao) WHERE data_inicio <= {date} AND data_fim <= {date}""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhuma sessão encontrada na data {date}")
        else:
            for row in ret_vals:
                movie_table.read(row[0])
                print(f"Sala: {row[1]}; Horário: {row[2]}; Data de estreia: {row[3]}; Fim da sessão: {row[4]}")
        print("")

    def read_all(self, movie_table : movie.MovieTable):
        
        data = self.cur.execute(f"""SELECT (id_sessao, id_movie, id_sala, horario, data_inicio, data_fim) 
        FROM (programacao)""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhuma sessão encontrada")
        else:
            for row in ret_vals:
                movie_table.read(row[1])
                print(f"ID: {row[0]}; Sala: {row[2]}; Horário: {row[3]}; Data de estreia: {row[4]}; Fim da sessão: {row[5]}")
        print("")
        
'''
# Testando criação
table.create(1, 1, '12:00:00', '06-12-2022', '20-12-2022')
table.create(1, 2, '12:45:00', '06-12-2022', '20-12-2022')

# Testando leitura
table.read(1)
table.read(2)
table.read_all()
'''

#table.con.commit()
#table.con.close()
