from client import ClientTable
import sqlite3 as sl

def retornar():
    print('Aperte C para voltar para tela de cadastro e V para voltar para a tela inicial:')
    flag_voltar = input()
    if flag_voltar.upper() == 'V':
        return True
    else:
        return False

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


def tela_compra():
    pass

if __name__ == '__main__':

    tabela_cliente = ClientTable()

    while(True):
        print('Bem-vindo/a ao cinema nome do cinema! Você gostaria de ir para a tela de cadastro ou fazer uma compra?')
        print('Digite C para se cadastrar, B para fazer uma compra ou E para sair da plataforma: ')
        flag_1 = input()

        if flag_1.upper() == 'C':
            tela_cadastro(tabela_cliente)

        elif flag_1.upper() == 'B':
            tela_compra()

        elif flag_1.upper() == 'E':
            print('Obrigado por usar nossa plataforma! Até a próxima!')
            break

        else:
            print('Input inválido digitado, aperte Enter para tentar novamente!')
            _val = input()

    tabela_cliente.con.commit()
    tabela_cliente.con.close()
    