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

def retornar():
    print('Aperte C para voltar para tela de cadastro e V para voltar para a tela inicial:')
    flag_voltar = input()
    if flag_voltar.upper() == 'V':
        return True
    else:
        return False

def mostrar_filmes(data, tabelas):
    
    print('Por favor, digite a sessão que você deseja comprar pelo número do id:')
    tabelas['programacao'].con = sl.connect('cinema_data.db')
    tabelas['programacao'].cur = tabelas['programacao'].con.cursor()
    tabelas['programacao'].read_by_date(data, tabelas['filme'])
    tabelas['programacao'].con.close()
    return int(input())

def tela_lanche(tabelas):
    input_id = 0
    lista_ids = []
    dict_id = {}
    while input_id.upper() != 'E':
        tabelas['lanche'].read_all()
        lista_ids(int(input()))
        print('\n\n')

    print('Obrigado por selecionar seus lanches!')
    dict_id = dict()
    for i in lista_ids:
        dict_id[i] = dict_id.get(i, 0) + 1
    

def tela_cadastro(table):

    while(True):

        print('Bem-vindo(a) à tela de cadastro de clientes, você gostaria de se cadastrar (C), checar seu cadastro (R), atualizar seu cadastro (U) ou deletar seu cadastro (D)?')
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
        
        ids_compras = []

        print('Bem-vindo(a) à tela de compra, você gostaria de fazer uma compra antecipada? S para sim ou N para não')
        antecipada = input()
        data = date.today().strftime("%d/%m/%Y")
        if antecipada.upper() == 'S':
            print('Para que dia será sua compra? Digite o dia do mês, seguido do mês e do ano no formato dd/mm/yyyy')
            data = input()

        dia, mes, ano = data.split('/')
        d_semana = pd.to_datetime(f"{ano}-{mes}-{dia}").day_name()
        preco_dict = {'Monday': 15, 'Tuesday': 18, 'Quarta': 12, 'Thursday': 18, 'Friday': 20, 'Saturday': 23, 'Sunday': 20}
        preco = (1 + 0.1*(antecipada.upper() == 'S'))*preco_dict[d_semana]

        id_sessao = mostrar_filmes(data,tabelas)

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

        ids_compras.append(tabelas['ingresso'].create(preco, id_sessao, f"{ano}-{mes}-{dia}", nome_dict[tipo.upper()]))

        print('Você gostaria de comprar um lanche junto ao seu ingresso? S para sim ou N para não')
        flag_confirmar = input()

        if flag_confirmar.upper() == 'S':
            print('Por favor, digite os lanches que você deseja comprar pelo número do id, um de cada vez:')
            print('Caso não deseje mais nenhum lanche, digite E')
            tela_lanche(tabelas)

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

    tabelas['produtora'].create('20th Century Studios')
    tabelas['produtora'].create('Disney')
    tabelas['produtora'].con.commit()
    tabelas['produtora'].con.close()
    tabelas['ator'].create('Macaulin Culkin')
    tabelas['ator'].create('Joe Pesci')
    tabelas['ator'].create('Daniel Stern')
    tabelas['ator'].con.commit()
    tabelas['ator'].con.close()
    tabelas['filme'].create('Esqueceram de mim', 'Comédia', 60*1 + 43, 'L', False, 1, [1, 2, 3])
    tabelas['filme'].con.commit()
    tabelas['filme'].con.close()
    tabelas['sala'].create(200)
    tabelas['sala'].con.commit()
    tabelas['sala'].con.close()
    tabelas['programacao'].create(1, 1, '12:00:00', '2022-12-05', '2022-12-20')
    tabelas['programacao'].con.commit()
    tabelas['programacao'].con.close()

    while(True):
        print('Bem-vindo(a) ao cinema nome do cinema! Você gostaria de ir para a tela de cadastro ou fazer uma compra?')
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
