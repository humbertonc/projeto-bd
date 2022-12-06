import sqlite3 as sl
from tables.movie import MovieTable
import time

class ScheduleTable:
    def __init__(self):

        self.con = sl.connect('cinema_data.db')
        self.cur = self.con.cursor()
        self.cur.execute("""
        CREATE TABLE if not exists programacao (
            id_sessao integer PRIMARY KEY autoincrement NOT NULL,
            id_filme integer NOT NULL,
            id_sala integer NOT NULL,
            horario time NOT NULL,
            data_inicio date NOT NULL,
            data_fim date NOT NULL,
            FOREIGN KEY (id_filme) REFERENCES filme (id_filme),
            FOREIGN KEY (id_sala) REFERENCES sala (id_sala)
        )
        """)

    def create(self, id_movie, id_screen, time, date_beginning, date_end):

        try:
            self.cur.execute(f"""INSERT INTO programacao (id_filme, id_sala, horario, data_inicio, data_fim) 
                VALUES({id_movie}, {id_screen}, '{time}', '{date_beginning}', '{date_end}')""")
            print(f"Sessão cadastrada com sucesso")
        except:
            print("Não foi possível cadastrar a sessão")
        print('')

    def read_by_id(self, id_session, movie_table : MovieTable):

        data = self.cur.execute(f"""SELECT id_filme, id_sala, horario, data_inicio, data_fim
        FROM programacao WHERE id_sessao == {id_session}""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhuma sessão encontrada com id {id_session}")
        else:
            movie_table.con = sl.connect('cinema_data.db')
            movie_table.cur = movie_table.con.cursor()
            for row in ret_vals:
                movie_table.read(row[0])
                print(f"Sala: {row[1]}; Horário: {row[2]}; Data de estreia: {row[3]}; Fim da sessão: {row[4]}")
                #print('')
            movie_table.con.close()
        #print("")

    def read_by_date(self, date, movie_table : MovieTable):

        data = self.cur.execute(f"""SELECT id_filme, id_sala, horario, data_inicio, data_fim, id_sessao
        FROM programacao WHERE '{date}' between data_inicio AND data_fim""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhuma sessão encontrada na data {date}")
        else:
            movie_table.con = sl.connect('cinema_data.db')
            movie_table.cur = movie_table.con.cursor()
            for row in ret_vals:
                movie_table.read(row[0])
                print(f"ID: {row[5]}; Sala: {row[1]}; Horário: {row[2]}; Data de estreia: {row[3]}; Fim da sessão: {row[4]}")
                print('')
            movie_table.con.close()
        print("")

    def read_all(self, movie_table : MovieTable):
        
        data = self.cur.execute(f"""SELECT * FROM programacao""")
        ret_vals = data.fetchall()
        if not ret_vals:
            print(f"Nenhuma sessão encontrada")
        else:
            movie_table.con = sl.connect('cinema_data.db')
            movie_table.cur = movie_table.con.cursor()
            for row in ret_vals:
                movie_table.read(row[1])
                print(f"ID: {row[0]}; Sala: {row[2]}; Horário: {row[3]}; Data de estreia: {row[4]}; Fim da sessão: {row[5]}")
                print('')
            movie_table.con.close()
        print("")
        

# Testando criação
'''mv_table = MovieTable()
table = ScheduleTable()
mv_table.create('tite','hexa',401,'m',True,1,[1])
mv_table.create('neymar','hexa',410,'n',True,1,[1])
mv_table.con.close()
table.create(1, 1, '12:00:00', '2022-12-06', '2022-12-20')
table.create(1, 2, '12:45:00', '2022-12-09', '2022-12-20')

# Testando leitura
table.read_by_id(1,mv_table)
table.read_by_id(2,mv_table)
table.read_all(mv_table)
table.read_by_date('2022-12-08',mv_table)
'''
'''
#table.con.commit()
table.con.close()'''
