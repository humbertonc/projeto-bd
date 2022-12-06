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

id_voucher = 1

def mostrar_comprovantes(tabelas,id_cliente,ids_compras,id_voucher):
    tabelas['ingresso'].con = sl.connect('cinema_data.db')
    tabelas['ingresso'].cur = tabelas['ingresso'].con.cursor()
    tabelas['programacao'].con = sl.connect('cinema_data.db')
    tabelas['programacao'].cur = tabelas['programacao'].con.cursor()
    print("Ingressos:")
    for i in ids_compras:
        print('=========================================')
        sess = tabelas['ingresso'].read(i)
        tabelas['programacao'].read_by_id(sess,tabelas['filme'])
    print('=========================================')
    tabelas['ingresso'].con.commit()
    tabelas['ingresso'].con.close()
    tabelas['programacao'].con.commit()
    tabelas['programacao'].con.close()

    if id_voucher:
        tabelas['voucher'].con = sl.connect('cinema_data.db')
        tabelas['voucher'].cur = tabelas['voucher'].con.cursor()
        print('Comprovante do lanche:')
        tabelas['voucher'].read(id_voucher)
        tabelas['voucher'].con.commit()
        tabelas['voucher'].con.close()


def retornar(tabela):
    print('Aperte C para voltar para tela de cadastro e V para voltar para a tela inicial:')
    flag_voltar = input()
    if flag_voltar.upper() == 'V':
        tabela.con.commit()
        tabela.con.close()
        return True
    else:
        return False
    
def tela_login(tabela):
    tabela.con = sl.connect('cinema_data.db')
    tabela.cur = tabela.con.cursor()
    print('Por favor digite seu nome para fazer login')
    nome = input()
    ret_read = tabela.get_id_by_name(nome)

    if ret_read >= 0:
        tabela.con.commit()
        tabela.con.close()
        print('Login realizado!')
        return ret_read, True
    else:
        print('Nome não cadastrado, por favor realize seu cadastro na página principal')
        print('')
        return '', False

def mostrar_filmes(data, tabelas):
    
    print('\nPor favor, digite a sessão que você deseja comprar pelo número do id:')
    tabelas['programacao'].con = sl.connect('cinema_data.db')
    tabelas['programacao'].cur = tabelas['programacao'].con.cursor()
    tabelas['programacao'].read_by_date(data, tabelas['filme'])
    tabelas['programacao'].con.close()
    return int(input())

def tela_lanche(tabelas):
    tabelas['lanche'].con = sl.connect('cinema_data.db')
    tabelas['lanche'].cur = tabelas['lanche'].con.cursor()
    input_id = -1
    lista_ids = []
    dict_id = {}
    while input_id != 0:
        tabelas['lanche'].read_all()
        input_id = int(input())
        lista_ids.append(input_id)
        print('\n\n')
    tabelas['lanche'].con.commit()
    tabelas['lanche'].con.close()

    print('Obrigado por selecionar seus lanches!')
    dict_id = dict()
    for i in lista_ids:
        dict_id[i] = dict_id.get(i, 0) + 1
    dict_id.pop(0, None)

    list_unique_id = []
    
    global id_voucher
    
    for id_product, quantidade in dict_id.items():
        tabelas['voucher'].create(id_voucher, id_product, quantidade)
        list_unique_id.append(id_product)
    id_voucher += 1
    tabelas['voucher'].con.commit()
    tabelas['voucher'].con.close()
    
    return list_unique_id, id_voucher - 1

def tela_pagamento(tabelas, id_cliente, ids_compras, id_voucher, antecipado):

    while(True):
        forma_pagamento = 'CREDITO'
        
        if not antecipado:
            print('Por favor, digite como será a forma de pagamento da compra: (C) crédito; (D) débito; (E) espécie; (P) pix')
            forma_pagamento_char = input().upper()

            forma_dict = {'C': 'CREDITO', 'D': 'DEBITO', 'E':'ESPECIE','P':'PIX'}
            if forma_pagamento_char not in forma_dict:
                print("Forma inválida. Digite novamente.")
                continue

            forma_pagamento = forma_dict[forma_pagamento_char]

        id_compra = tabelas['compra'].create(id_cliente, forma_pagamento, date.today(), ids_compras, id_voucher)
        tabelas['compra'].read_by_id(id_compra)
        tabelas['compra'].con.commit()
        tabelas['compra'].con.close()
        break

def tela_cadastro(tabela):

    while(True):

        print('Bem-vindo(a) à tela de cadastro de clientes, você gostaria de se cadastrar (C), checar seu cadastro (R), atualizar seu cadastro (U) ou deletar seu cadastro (D)?')
        flag_cadastro = input()

        if flag_cadastro.upper() == 'C':

            print('Digite o seu nome para se cadastrar: ')
            nome = input()
            tabela.create(nome)

            if retornar(tabela):
                break
            else:
                continue
            

        elif flag_cadastro.upper() == 'R':

            print('Digite o nome do usuário que você deseja checar o cadastro')
            nome = input()
            ap = tabela.read(name=nome)
            if ap:
                print(f'Usuário com nome {nome} encontrado!')
            else:
                print('Usuário não encontrado')

            if retornar(tabela):
                break
            else:
                continue

        elif flag_cadastro.upper() == 'U':
        #Ideia para mais tarde: Checar se usuario existe

            print('Digite o nome do usuário que você deseja atualizar:')
            nome_antigo = input()
            print('Digite o novo nome do usuário:')
            nome_novo = input()
            tabela.update(name=nome_antigo, new_name=nome_novo)

            if retornar(tabela):
                break
            else:
                continue

        elif flag_cadastro.upper() == 'D':
        #Ideia para mais tarde, checar se usuario existe

            print('Digite o nome do usuário que você deseja deletar:')
            nome = input()
            tabela.delete(name=nome)

            if retornar(tabela):
                break
            else:
                continue


def tela_compra(id_cliente, tabelas):
    
    ids_compras = []
    while(True):

        print('Bem-vindo(a) à tela de compra, você gostaria de fazer uma compra antecipada? S para sim ou N para não')
        antecipada_in = input()
        antecipada = False
        data = date.today().strftime("%d/%m/%Y")
        if antecipada_in.upper() == 'S':
            antecipada = True
            print('Para que dia será sua compra? Digite o dia do mês, seguido do mês e do ano no formato dd/mm/yyyy')
            data = input()

        dia, mes, ano = data.split('/')
        d_semana = pd.to_datetime(f"{ano}-{mes}-{dia}").day_name()
        preco_dict = {'Monday': 15, 'Tuesday': 18, 'Wednesday': 12, 'Thursday': 18, 'Friday': 20, 'Saturday': 23, 'Sunday': 20}
        preco = (1 + 0.1*(antecipada_in.upper() == 'S'))*preco_dict[d_semana]
        preco = round(preco,2)

        id_sessao = mostrar_filmes(f"{ano}-{mes}-{dia}",tabelas)

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

        ret_ingresso = tabelas['ingresso'].create(preco, id_sessao, f"{ano}-{mes}-{dia}", nome_dict[tipo.upper()])

        if ret_ingresso == -1:
            print('Você será redirecionado para a tela de compra')
            continue
        
        ids_compras.append(ret_ingresso)

        print('Obrigado pela compra, você gostaria de comprar mais um ingresso? S ou N')
        flag_yes = input()

        if flag_yes.upper() == 'S':
            continue

        tabelas['ingresso'].con.commit()
        tabelas['ingresso'].con.close()
        print('Você gostaria de comprar um lanche junto a compra do ingresso? S para sim ou N para não')
        flag_confirmar = input()

        ids_ingressos = ids_compras.copy()
        if flag_confirmar.upper() == 'S':
            print('Por favor, digite os lanches que você deseja comprar pelo número do id, um de cada vez:')
            print('Caso não deseje mais nenhum lanche, digite 0')
            ids_snacks, id_voucher = tela_lanche(tabelas)
            ids_compras.extend(ids_snacks)
        else:
            id_voucher=None

        tela_pagamento(tabelas, id_cliente, ids_compras, id_voucher, antecipada)
        mostrar_comprovantes(tabelas,id_cliente,ids_ingressos,id_voucher)

        print('Obrigado pela preferência, você será redirecionado(a) para o menu principal!')
        print('')
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
        print('Bem-vindo(a) ao Cinema Sauro! Você gostaria de ir para a tela de cadastro ou fazer login?')
        print('Digite C para se cadastrar, L para fazer login ou E para sair da plataforma: ')
        flag_1 = input()

        if flag_1.upper() == 'C':
            tela_cadastro(tabelas['cliente'])

        elif flag_1.upper() == 'L':
            nome, aprovado = tela_login(tabelas['cliente'])
            if aprovado:
                tela_compra(nome, tabelas)

        elif flag_1.upper() == 'E':
            print('Obrigado por usar nossa plataforma! Até a próxima!')
            break

        else:
            print('Input inválido digitado, aperte Enter para tentar novamente!')
            _val = input()
