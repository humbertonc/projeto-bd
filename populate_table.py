from tables.client import ClientTable
from tables.movie import MovieTable
from tables.actor import ActorTable
from tables.schedule import ScheduleTable
from tables.producer import ProducerTable
from tables.purchase import PurchaseTable
from tables.screen import ScreenTable
from tables.snack import SnackTable
from tables.ticket import TicketTable
from tables.voucher import VoucherTable
from datetime import date
import sqlite3 as sl
import pandas as pd

if __name__ == '__main__':

    tabelas = {}
    tabelas['ator'] = ActorTable()
    tabelas['produtora'] = ProducerTable()
    tabelas['filme'] = MovieTable()
    tabelas['sala'] = ScreenTable()
    tabelas['programacao'] = ScheduleTable()
    tabelas['cliente'] = ClientTable()
    tabelas['lanche'] = SnackTable()
    tabelas['ingresso'] = TicketTable()
    tabelas['compra'] = PurchaseTable()
    tabelas['voucher'] = VoucherTable()

    tabelas['produtora'].create('20th Century Studios')
    tabelas['produtora'].create('Disney')
    tabelas['produtora'].create('Marvel Studios')
    tabelas['produtora'].create('Warner Bros')
    tabelas['produtora'].create('Universal')
    tabelas['produtora'].con.commit()
    tabelas['produtora'].con.close()
    tabelas['ator'].create('Macaulin Culkin')
    tabelas['ator'].create('Joe Pesci')
    tabelas['ator'].create('Daniel Stern')
    tabelas['ator'].create('Al Pacino')
    tabelas['ator'].create('Marlon Brando')
    tabelas['ator'].create('Adam Sandler')
    tabelas['ator'].create('Jennifer Aniston')
    tabelas['ator'].create('James Earl Jones')
    tabelas['ator'].create('Wagner Moura')
    tabelas['ator'].con.commit()
    tabelas['ator'].con.close()
    tabelas['filme'].create('Esqueceram de mim', 'Comédia', 60*1 + 43, 'L', False, 1, [1, 2, 3])
    tabelas['filme'].create('O Rei Leão', 'Animacao', 60*1 + 33, 'L', False, 2, [8])
    tabelas['filme'].create('Esposa de Mentirinha', 'Comédia', 60*2 + 3, '12', False, 4, [6,7])
    tabelas['filme'].create('O Poderoso Chefão', 'Drama', 60*3 + 21, '16', False, 1, [4,5])
    tabelas['filme'].create('Tropa de Elite', 'Ação', 60*2 + 15, '18', True, 5, [9])
    tabelas['filme'].con.commit()
    tabelas['filme'].con.close()
    tabelas['sala'].create(50)
    tabelas['sala'].create(150)
    tabelas['sala'].create(90)
    tabelas['sala'].create(40)
    tabelas['sala'].con.commit()
    tabelas['sala'].con.close()
    tabelas['programacao'].create(1, 1, '12:00:00', '2022-12-05', '2022-12-20')
    tabelas['programacao'].create(1, 2, '16:30:00', '2022-12-05', '2022-12-12')
    tabelas['programacao'].create(2, 3, '18:30:00', '2022-12-08', '2022-12-15')
    tabelas['programacao'].create(2, 1, '15:00:00', '2022-12-08', '2022-12-14')
    tabelas['programacao'].create(3, 4, '19:00:00', '2022-12-05', '2022-12-31')
    tabelas['programacao'].create(3, 2, '19:00:00', '2022-12-05', '2022-12-29')
    tabelas['programacao'].create(4, 1, '19:00:00', '2022-12-21', '2022-12-21')
    tabelas['programacao'].create(5, 1, '21:00:00', '2022-12-05', '2022-12-23')
    tabelas['programacao'].con.commit()
    tabelas['programacao'].con.close()
    tabelas['lanche'].create(21,'Pipoca Grande')
    tabelas['lanche'].create(15,'Pipoca Média')
    tabelas['lanche'].create(12,'Pipoca Pequena')
    tabelas['lanche'].create(9,'Chocolate')
    tabelas['lanche'].create(12,'Refrigerante médio')
    tabelas['lanche'].con.commit()
    tabelas['lanche'].con.close()