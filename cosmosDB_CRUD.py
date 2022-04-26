from pydoc import doc
from typing import Any
import uuid
from azure.cosmos import CosmosClient, PartitionKey

# Recebe o container do CosmosDB e retorna
# uma lista com os ids de todos os items
def returnIDS(container):
    ids_members = []
    item_list = list(container.read_all_items())
    for id in item_list:
        ids_members.append(id.get('id'))
    return ids_members

# Função disponibilizada na documentação do CosmosDB
# realiza a leitura de um determinado item pelo doc_id
# e imprime as informações do item (Id, lastName e collegeInformation)
def read_item(container, doc_id):
    print('\n1.2 Reading Item by Id')
    # Note that Reads require a partition key to be spcified.
    response = container.read_item(item=doc_id, partition_key=doc_id)
    print('Item read by Id {0}'.format(doc_id))
    print('lastName: {0}'.format(response.get('lastName')))
    print('collegeInformation: {0}'.format(response.get('collegeInformation')))

# Função disponibilizada na documentação do CosmosDB
# realiza a deleção de um determinado item pelo doc_id
# e imprime o id do item deletado
def delete_item(container, doc_id):
    print('\n1.7 Deleting Item by Id\n')
    container.delete_item(item=doc_id, partition_key=doc_id)

    print('Deleted item\'s Id is {0}'.format(doc_id))

# Recebe os dados para cadastrar um novo membro
# e retorna um dict formatado com os dados inseridos
def get_newmember(nome, sobrenome, anoIngresso, curso, RA):
    newMember = {
    'id': nome + str(uuid.uuid4()),
    'lastName': sobrenome,
    'collegeInformation':{
        'yearOfEntry': anoIngresso,
        'course': curso,
        'studentID': RA,
        },
    }
    return newMember

# Mostra o menu principal da aplicação
# e mantém o loop para realização das operações de CRUD
def showMenu(container, option = 1):

    # Opção que encerrará o loop
    SAIR = 5

    while(option != SAIR):

        # Opções e recebimento da opção selecionada
        print("\n1 - Listar itens do banco de dados")
        print("2 - Deletar item do banco de dados com ID")
        print("3 - Inserir item no banco de dados")
        print("4 - Atualizar item no banco de dados")
        print(SAIR, "- Sair")
        option = int(input("\nEscolha uma opção: "))

        # Atualiza a lista de membros assim que o usuário
        # escolhe a opção desejada
        members_ids = returnIDS(container)

        # Lista todos os itens
        if (option == 1):
            if (members_ids):
                for member in members_ids:
                    # read_item é a função do azure.cosmos que permite
                    # a leitura de um item
                    read_item(container, member)
            else:
                print('Banco de dados vazio!')

        # Deleta um item
        elif (option == 2):
            if (members_ids):
                for idx, member in enumerate(members_ids):
                    print(idx+1, '-', member)

                delMember = int(input("Escolha uma opção: "))

                # delete_item é a função do azure.cosmos que permite
                # a remoção de um item
                delete_item(container, members_ids[delMember-1])
            else:
                print('Banco de dados vazio!')

        # Cadastra um novo item
        elif (option == 3):
            firstName = str(input("Insira o primeiro nome: "))
            lastName = str(input("Insira o sobrenome: "))
            yearOfEntry = int(input("Insira o ano de ingresso: "))
            course = str(input("Insira o curso: "))
            studentId = int(input("Insira o RA: "))
            body = get_newmember(firstName, lastName, yearOfEntry, course, studentId)
            
            # create_item do azure.cosmos permite a criação de um item
            # com os dados que foram repassados no parâmetro
            container.create_item(body)

        # Atualiza um item existente
        elif (option == 4):
            if (members_ids):
                for idx, member in enumerate(members_ids):
                    print(idx+1, '-', member)

                updateMember = int(input("Escolha uma opção: "))
                readItem = container.read_item(item=members_ids[updateMember-1], 
                    partition_key=members_ids[updateMember-1])

                yearOfEntry = int(input("Insira o ano de ingresso: "))
                course = str(input("Insira o curso: "))
                studentId = int(input("Insira o RA: "))

                readItem['collegeInformation']['yearOfEntry'] = yearOfEntry
                readItem['collegeInformation']['course'] = course
                readItem['collegeInformation']['studentId'] = studentId
    
                # replace_item do azure.cosmos permite atualização
                # dos dados de um item
                container.replace_item(item=readItem, body=readItem)

if __name__ == '__main__':

    # Conexão com CosmosDB
    endpoint = 'https://sistemas-distribuidos-cosmosdb.documents.azure.com:443/'
    key = 'FLrFsEzm7N4eL8ECFpfxFEz5mcSHG6bFYpT47iEyJWbX9WmSTQAe1mSnZiO1Lm40YsX8pkYRSo0Bou91MbHxIg=='
    client = CosmosClient(endpoint, key)

    # Instância o database (cria um caso não exista)
    database_name = 'SeminarioSistemasDistribuidos-CosmosDB'
    database = client.create_database_if_not_exists(id=database_name)

    # Instância o container (cria um caso não exista)
    container_name = 'IntegrantesDoGrupo'
    container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    
    # Inicializa o menu de CRUD
    showMenu(container)