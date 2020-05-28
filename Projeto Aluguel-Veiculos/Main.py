import pymongo
from bson import ObjectId
import datetime

from Cliente import Cliente
from Aluguel import Aluguel
from Funcionario import Funcionario
from Carro import Carro
from Seguro import Seguro

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["aluguel-veiculos"]
col_cliente = mydb["cliente"]
col_aluguel = mydb["aluguel"]
col_funcionario = mydb["funcionario"]
col_carro = mydb["carro"]
col_seguro = mydb ["seguro"]

def mensagem_erro():
    print('\nOcorreu um problema na aplicação, tente novamente.')


# Metodos do Cliente

def inserir_cliente(cliente):
    result = col_cliente.insert_one(cliente.__dict__)
    if result.inserted_id:
        print(f'\nO cliente {cliente.get_nome()} foi inserido com sucesso.')


def preencher_cliente():
    cliente = Cliente()
    cliente.set_id(input('Informe o ID: '))
    while cliente._id.isdigit()==False:
        print("\nDados incorretos, favor, reinseri-los\n")
        cliente.set_id(input('Informe o ID: '))
    cliente.set_nome(input('Informe o nome: '))
    while cliente.nome.isalpha() == False:
        print("\nDados incorretos, favor, reinseri-los\n")
        cliente.set_nome(input('Informe o nome: '))
    cliente.set_telefone(input('Informe o telefone: '))
    while (len(cliente.telefone) != 11) or cliente.telefone.isdigit() == False:
        print("\nDados incorretos, favor, reinseri-los\n")
        cliente.set_telefone(input('Informe o telefone: '))
    cliente.set_email(input('Informe o email: '))
    while "@" not in cliente.email or ".com" not in cliente.email.lower():
        print("\nDados incorretos, favor, reinseri-los\n")
        cliente.set_email(input('Informe o email: '))
    cliente.set_cpf(input('Informe o CPF: '))
    while (len(cliente.cpf)!=11) or cliente.cpf.isdigit()==False:
        print("\nDados incorretos, favor, reinseri-los\n")
        cliente.set_cpf(input('Informe o CPF: '))
    return cliente


def excluir_cliente(id_cliente):
    col_cliente.delete_one({"_id": (id_cliente)})
    print("Cliente excluído com sucesso!")


def atualizar_cliente(id_cliente, cliente):
    result = col_cliente.update_one({'_id':(id_cliente)}, {"$set": cliente.__dict__})
    if result.modified_count > 0:
        print(f'\nO cliente {cliente.get_nome()} foi alterado com sucesso.')


def listar_clientes():
    if col_cliente.estimated_document_count() > 0:
        for cliente in col_cliente.find():
            print("\nID: ", cliente["_id"], "\nNome: ", cliente["nome"], "\nTelefone: ", cliente["telefone"],
                  "\nEmail: ", cliente["email"], "\nCPF: ", cliente["cpf"])
    else:
        print("Não existem clientes cadastrados no banco de dados")

# Metodos do Aluguel

def inserir_aluguel(aluguel):
    result = col_aluguel.insert_one(aluguel.__dict__)
    if result.inserted_id:
        print(f'\nO Aluguel {aluguel.get_id()} foi inserido com sucesso.')


def preencher_aluguel():
    aluguel = Aluguel()
    aluguel.set_id(input('Informe o ID: '))
    while aluguel._id.isdigit() == False:
        print("\nDados incorretos, favor, reinseri-los\n")
        aluguel.set_id(input('Informe o ID: '))

    id_seguro = str(input('Informe o ID do seguro '))
    while id_seguro.isdigit() == False:
        print("\nDados incorretos, favor, reinseri-los\n")
        id_seguro = str(input('Informe o ID do seguro '))
    seguro = [i for i in col_seguro.find({"_id": id_seguro})]

    placa_car = str(input('Informe a Placa do carro alugado: '))
    carro = [i for i in col_carro.find({"placa": placa_car})]

    id_funcionario = str(input('Informe o ID do Funcionario que realizou o aluguel: '))
    while id_funcionario.isdigit() == False:
        print("\nDados incorretos, favor, reinseri-los\n")
        id_funcionario = str(input('Informe o ID do Funcionario que realizou o aluguel: '))
    funcionario = [i for i in col_funcionario.find({"_id": id_funcionario})]

    id_cliente = (input('Informe o ID do Cliente: '))
    while id_cliente.isdigit()==False:
        print("\nDados incorretos, favor, reinseri-los\n")
        id_cliente.set_id(input('Informe o ID do cliente: '))
    cliente = [i for i in col_cliente.find({"_id": id_cliente})]

    aluguel.set_data(input("Informe a data no tipo dd/mm/aa: "))
    aluguel.set_horario(input("Informe o horario da venda no tipo HH:MM: "))
    aluguel.set_periodo(input("Informe por quanto tempo o cliente ficará com o veiculo: "))

    aluguel.set_seguro(seguro[0])
    aluguel.set_carro(carro[0])
    aluguel.set_funcionario(funcionario[0])
    aluguel.set_cliente(cliente[0])

    return aluguel


def excluir_aluguel(id_aluguel):
    col_aluguel.delete_one({"_id": (id_aluguel)})
    print("Aluguel excluído com sucesso!")


def atualizar_aluguel(id_aluguel, aluguel):
    result = col_aluguel.update_one({'_id': (id_aluguel)}, {"$set": aluguel.__dict__})
    if result.modified_count > 0:
        print(f'\nO aluguel {aluguel.get_id()} foi alterado com sucesso.')


def listar_aluguel():
    if col_aluguel.estimated_document_count() > 0:
        for aluguel in col_aluguel.find():
            print("\nID: ", aluguel["_id"], "\nSeguro: ", aluguel["seguro"], "\nCarro: ", aluguel["carro"],
                  "\nFuncionario: ", aluguel["funcionario"], "\nCliente: ", aluguel["cliente"],
                  "\nData: ", aluguel["data"],"\nHorario: ", aluguel["horario"],"\nPeriodo: ", aluguel["periodo"])
    else:
        print("Não existem alugueles cadastrados no banco de dados")

# Metodos de Carro

def inserir_carro(carro):
    result = col_carro.insert_one(carro.__dict__)
    if result.inserted_id:
        print(f'\nO produto {carro.get_modelo()} da marca {carro.get_marca()} foi inserido com sucesso.')


def preencher_carro():
    carro = Carro()
    carro.set_id(input('Informe o ID: '))
    while carro._id.isdigit()==False:
        print("\nDados incorretos, favor, reinseri-los\n")
        carro.set_id(input('Informe o ID: '))
    carro.set_marca(input('Informe a Marca: '))
    carro.set_modelo(input('Informe o Modelo: '))
    carro.set_placa(input('Informe a placa: '))
    carro.set_preco(input('Informe o Preço da diaria: '))
    return carro


def excluir_carro(id_carro):
    col_carro.delete_one({"_id": (id_carro)})
    print("Carro excluído com sucesso!")


def atualizar_carro(id_carro, carro):
    result = col_carro.update_one({'_id': (id_carro)}, {"$set": carro.__dict__})
    if result.modified_count > 0:
        print(f'\nO carro {carro.get_id()} foi alterado com sucesso.')


def listar_carros():
    if col_carro.estimated_document_count() > 0:
        for carro in col_carro.find():
            print("\nID: ", carro["_id"], "\nMarca: ", carro["marca"], "\nModelo: ", carro["modelo"],
                  "\nPlaca: ", carro["placa"], "\nPreço: ", carro["preco"])
    else:
        print("Não existem carros cadastradas no banco de dados")

# Metodos de Seguro

def inserir_seguro(seguro):
    result = col_seguro.insert_one(seguro.__dict__)
    if result.inserted_id:
        print(f'\nO Seguro do tipo {seguro.get_tipo()} foi inserido com sucesso.')


def preencher_seguro():
    seguro = Seguro()
    seguro.set_id(input('Informe o ID: '))
    while seguro._id.isdigit() == False:
        print("\nDados incorretos, favor, reinseri-los\n")
        seguro.set_id(input('Informe o ID: '))
    seguro.set_tipo(input('Informe o Tipo do Seguro: '))
    seguro.set_preco(input('Informe o Preço do Seguro: '))
    return seguro


def excluir_seguro(id_seguro):
    col_seguro.delete_one({"_id": (id_seguro)})
    print("Seguro excluído com sucesso!")


def atualizar_seguro(id_seguro, seguro):
    result = col_seguro.update_one({'_id': (id_seguro)}, {"$set": seguro.__dict__})
    if result.modified_count > 0:
        print(f'\nO seguro do tipo {seguro.get_tipo()} foi alterado com sucesso.')


def listar_seguros():
    if col_seguro.estimated_document_count() > 0:
        for seguro in col_seguro.find():
            print("\nID: ", seguro["_id"], "\nTipo: ", seguro["tipo"], "\nPreço: ", seguro["preco"])
    else:
        print("Não existem seguros cadastradas no banco de dados")

# Metodos de Funcionario

def inserir_funcionario(funcionario):
    result = col_funcionario.insert_one(funcionario.__dict__)
    if result.inserted_id:
        print(f'\nO Funcionario {funcionario.get_nome()} foi inserido com sucesso.')


def preencher_funcionario():
    funcionario = Funcionario()
    funcionario.set_id(input('Informe o ID: '))
    while funcionario._id.isdigit() == False:
        print("\nDados incorretos, favor, reinseri-los\n")
        funcionario.set_id(input('Informe o ID: '))
    funcionario.set_nome(input('Informe o Nome do Funcionario: '))
    funcionario.set_turno(input('Informe o Turno do Funcionario: '))
    return funcionario


def excluir_funcionario(id_funcionario):
    col_funcionario.delete_one({"_id": (id_funcionario)})
    print("Funcionario excluído com sucesso!")


def atualizar_funcionario(id_funcionario, funcionario):
    result = col_funcionario.update_one({'_id': (id_funcionario)}, {"$set": funcionario.__dict__})
    if result.modified_count > 0:
        print(f'\nO funcionario {funcionario.get_nome()} foi alterado com sucesso.')


def listar_funcionarios():
    if col_funcionario.estimated_document_count() > 0:
        for funcionario in col_funcionario.find():
            print("\nID: ", funcionario["_id"], "\nNome: ", funcionario["nome"], "\nTurno: ", funcionario["turno"])
    else:
        print("Não existem funcionarios cadastradas no banco de dados")


continuar = True
while continuar:
    menu_cliente = True
    print('\n1 - Menu Cliente')
    print('2 - Menu Aluguel')
    print('3 - Menu Carro')
    print('4 - Menu Seguro')
    print('5 - Menu Funcionario')
    print('0 - Sair')
    opcao = input('\nInforme a opção desejada: ')
    if opcao == '1':
        while menu_cliente:
            print('\n---------- Menu Cliente ---------- ')
            print('\n1 - Inserir cliente')
            print('2 - Listar clientes')
            print('3 - Excluir cliente')
            print('4 - Alterar cliente')
            print('0 - Voltar')
            opcao = input('\nInforme a opção desejada: ')
            if opcao == '1':
                try:
                    print("\n====================Adicionar Cliente====================")
                    inserir_cliente(preencher_cliente())
                except:
                    mensagem_erro()
            elif opcao == '2':
                try:
                    print("\n====================Lista de Clientes====================")
                    listar_clientes()
                except:
                    mensagem_erro()
            elif opcao == '3':
                try:
                    print("\n=====================Excluir Cliente=====================")
                    id_cliente = str(input("\nInforme o id do Cliente: "))
                    excluir_cliente(id_cliente)
                except:
                    mensagem_erro()
            elif opcao == '4':
                try:
                    print("\n=====================Alterar Cliente=====================")
                    id_cliente = str(input("\nInforme o id do Cliente: "))
                    atualizar_cliente(id_cliente, preencher_cliente())
                except:
                    mensagem_erro()
            elif opcao == '0':
                menu_cliente = False
    elif opcao == '2':
        menu_aluguel = True
        while menu_aluguel:
            print('\n---------- Menu Aluguel ---------- ')
            print('\n1 - Inserir aluguel')
            print('2 - Listar alugueis')
            print('3 - Excluir aluguel')
            print('4 - Alterar aluguel')
            print('0 - Voltar')
            opcao = input('\nInforme a opção desejada: ')

            if opcao == '1':
                try:
                    print("\n====================Inserir Aluguel====================")
                    inserir_aluguel(preencher_aluguel())
                except:
                    mensagem_erro()

            elif opcao == '2':
                try:
                    print("\n=====================Lista de Aluguel=====================")
                    listar_aluguel()
                except:
                    mensagem_erro()

            elif opcao == '3':
                try:
                    print("\n=====================Excluir Aluguel=====================")
                    id_aluguel = str(input("\nInforme o id do Aluguel: "))
                    excluir_aluguel(id_aluguel)
                except:
                    mensagem_erro()

            elif opcao == '4':
                try:
                    print("\n====================Alterar Aluguel====================")
                    id_aluguel = str(input("\nInforme o id do Aluguel: "))
                    atualizar_aluguel(id_aluguel, preencher_aluguel())
                except:
                    mensagem_erro()

            elif opcao == '0':
                menu_aluguel = False
    elif opcao == '3':
        menu_carro = True
        while menu_carro:
            print('\n---------- Menu Carro ---------- ')
            print('\n1 - Inserir carro')
            print('2 - Listar carros')
            print('3 - Excluir carro')
            print('4 - Alterar carro')
            print('0 - Voltar')
            opcao = input('\nInforme a opção desejada: ')

            if opcao == '1':
                try:
                    print("\n=====================Inserir Carro=====================")
                    inserir_carro(preencher_carro())
                except:
                    mensagem_erro()

            elif opcao == '2':
                try:
                    print("\n=====================Lista de Carros=====================")
                    listar_carros()
                except:
                    mensagem_erro()

            elif opcao == '3':
                try:
                    print("\n=====================Excluir Carro=====================")
                    id_carro = str(input("\nInforme o id do Carro: "))
                    excluir_carro(id_carro)
                except:
                    mensagem_erro()

            elif opcao == '4':
                try:
                    print("\n=====================Alterar Carro=====================")
                    id_carro = str(input("\nInforme o id do Carro: "))
                    atualizar_carro(id_carro, preencher_carro())
                except:
                    mensagem_erro()

            elif opcao == '0':
                menu_carro = False

    elif opcao == '4':
        menu_seguro = True
        while menu_seguro:
            print('\n---------- Menu Seguro ---------- ')
            print('\n1 - Inserir seguro')
            print('2 - Listar seguros')
            print('3 - Excluir seguro')
            print('4 - Alterar seguro')
            print('0 - Voltar')
            opcao = input('\nInforme a opção desejada: ')

            if opcao == '1':
                try:
                    print("\n=====================Inserir Seguro=====================")
                    inserir_seguro(preencher_seguro())
                except:
                    mensagem_erro()

            elif opcao == '2':
                try:
                    print("\n=====================Listar Seguros=====================")
                    listar_seguros()
                except:
                    mensagem_erro()

            elif opcao == '3':
                try:
                    print("\n=====================Excluir Seguro=====================")
                    id_seguro = str(input("\nInforme o id do Seguro: "))
                    excluir_seguro(id_seguro)
                except:
                    mensagem_erro()

            elif opcao == '4':
                try:
                    print("\n=====================Alterar Seguro=====================")
                    id_seguro = str(input("\nInforme o id do Seguro: "))
                    atualizar_seguro(id_seguro, preencher_seguro())
                except:
                    mensagem_erro()

            elif opcao == '0':
                menu_seguro = False
    elif opcao == '5':
        menu_funcionario = True
        while menu_funcionario:
            print('\n---------- Menu Funcionario ---------- ')
            print('\n1 - Inserir funcionario')
            print('2 - Listar funcionarios')
            print('3 - Excluir funcionario')
            print('4 - Alterar funcionario')
            print('0 - Voltar')
            opcao = input('\nInforme a opção desejada: ')
            if opcao == '1':
                try:
                    print("\n=====================Inserir Funcionario=====================")
                    inserir_funcionario(preencher_funcionario())
                except:
                    mensagem_erro()
            elif opcao == '2':
                try:
                    print("\n=====================Listar Funcionarios=====================")
                    listar_funcionarios()
                except:
                    mensagem_erro()
            elif opcao == '3':
                try:
                    print("\n=====================Excluir Funcionario=====================")
                    id_funcionario = str(input("\nInforme o id do Funcionario: "))
                    excluir_funcionario(id_funcionario)
                except:
                    mensagem_erro()
            elif opcao == '4':
                try:
                    print("\n=====================Alterar Funcionario=====================")
                    id_funcionario = str(input("\nInforme o id do Funcionario: "))
                    atualizar_funcionario(id_funcionario, preencher_funcionario())
                except:
                    mensagem_erro()
            elif opcao == '0':
                menu_funcionario = False

    elif opcao == '0':
        continuar= False