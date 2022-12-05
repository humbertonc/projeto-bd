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
import sqlite3 as sl
import pandas as pd

def retornar():
    print('Aperte C para voltar para tela de cadastro e V para voltar para a tela inicial:')
    flag_voltar = input()
    if flag_voltar.upper() == 'V':
        return True
    else:
        return False

def show_movies(day):
    pass

def tela_lanche():
    pass

def tela_cadastro(table):

    while(True):

        print('Bem-vindo/a à tela de cadastro de clientes, você gostaria de se cadastrar (C), checar seu cadastro (R), atualizar seu cadastro (U) ou deletar seu cadastro (D)?')
        flag_cadastro = input()

        if flag_cadastro.upper() == 'C':

            print('Digite o seu nome para se cadastrar: ')
            nome = input()
            table.create(nome)

            if retornar():
                break
            else:
                continue
            

        elif flag_cadastro.upper() == 'R':

            print('Digite o nome do usuário que você deseja checar o cadastro')
            nome = input()
            table.read(name=nome)

            if retornar():
                break
            else:
                continue

        elif flag_cadastro.upper() == 'U':
        #Ideia para mais tarde: Checar se usuario existe

            print('Digite o nome do usuário que você deseja atualizar:')
            nome_antigo = input()
            print('Digite o novo nome do usuário:')
            nome_novo = input()
            table.update(name=nome_antigo, new_name=nome_novo)

            if retornar():
                break
            else:
                continue

        elif flag_cadastro.upper() == 'D':
        #Ideia para mais tarde, checar se usuario existe

            print('Digite o nome do usuário que você deseja deletar:')
            nome = input()
            table.delete(name=nome)

            if retornar():
                break
            else:
                continue


def tela_compra(tabelas):
    
    while(True):
        print('Em que dia será sua compra? Digite o dia do mês, seguido do mês e do ano no formato dd/mm/yyyy')
        data = input()
        dia, mes, ano = data.split('/')
        d_semana = pd.to_datetime(f"{ano}-{mes}-{dia}").day_name()

        preco_dict = {'Monday': 15, 'Tuesday': 18, 'Quarta': 12, 'Thursday': 18, 'Friday': 20, 'Saturday': 23, 'Sunday': 20}
        preco = preco_dict[d_semana]

        id_sessao = show_movies(d_semana)

        print('Digite seu tipo de ingresso: adulto (A), estudante (E), infantil (I), idoso (O) e flamenguista (F)')
        tipo = input()

        multiplier = {'A': 1, 'I': 0.25, 'O': 0.5, 'E': 0.5, 'F': 0}
        nome_dict = {'A': 'Adulto', 'E': 'Estudante', 'I': 'Infantil', 'O': 'Idoso', 'F': 'Flamenguista'}
        preco *= multiplier[tipo.upper()]

        print(f'O seu ingresso custará {preco} reais, você confirma a compra? S para sim ou N para não')
        flag_confirmar = input()

        if flag_confirmar.upper() == 'N':
            print('Compra cancelada, obrigado por usar a plataforma!')
            break

        tabelas['ingresso'].create(preco, id_sessao, f"{ano}-{mes}-{dia}", nome_dict[tipo.upper()])

        print('Você gostaria de comprar um lanche junto ao seu ingresso? S para sim ou N para não')
        flag_confirmar = input()

        if flag_confirmar.upper() == 'S':
            tela_lanche()

        print('Obrigado pela compra, você gostaria de realizar outra? S ou N')
        flag_yes = input()

        if flag_yes.upper() == 'N':
            print('Você será direcionado a tela inicial!\n')
            break



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

    while(True):
        print('Bem-vindo/a ao cinema nome do cinema! Você gostaria de ir para a tela de cadastro ou fazer uma compra?')
        print('Digite C para se cadastrar, B para fazer uma compra ou E para sair da plataforma: ')
        flag_1 = input()

        if flag_1.upper() == 'C':
            tela_cadastro(tabelas['cliente'])

        elif flag_1.upper() == 'B':
            tela_compra(tabelas)

        elif flag_1.upper() == 'E':
            print('Obrigado por usar nossa plataforma! Até a próxima!')
            break

        else:
            print('Input inválido digitado, aperte Enter para tentar novamente!')
            _val = input()

    tabelas['cliente'].con.commit()
    tabelas['cliente'].con.close()
