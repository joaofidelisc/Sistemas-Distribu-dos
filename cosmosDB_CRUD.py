
from pydoc import doc
from typing import Any
import uuid
from azure.cosmos import CosmosClient, PartitionKey

def read_items(container):
    print('\n1.3 - Reading all items in a container\n')

    # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
    #       Important to handle throttles whenever you are doing operations such as this that might
    #       result in a 429 (throttled request)
    item_list = list(container.read_all_items(max_item_count=10))

    print('Found {0} items'.format(item_list.__len__()))

    for doc in item_list:
        print('Item Id: {0}'.format(doc.get('id')))

def returnIDS(container):
    ids_members = []
    item_list = list(container.read_all_items())
    for id in item_list:
        ids_members.append(id.get('id'))
    return ids_members

def read_item(container, doc_id):
    print('\n1.2 Reading Item by Id')
    # Note that Reads require a partition key to be spcified.
    response = container.read_item(item=doc_id, partition_key=doc_id)
    print('Item read by Id {0}'.format(doc_id))
    print('lastName: {0}'.format(response.get('lastName')))
    print('collegeInformation: {0}'.format(response.get('collegeInformation')))
    # print('collegeInformation: {0}'.format(response.get('collegeInformation')))

def delete_item(container, doc_id):
    print('\n1.7 Deleting Item by Id\n')

    response = container.delete_item(item=doc_id, partition_key=doc_id)

    print('Deleted item\'s Id is {0}'.format(doc_id))


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

""" def upsert_item(container, doc_id):
    print('\n1.6 Upserting an item\n')
    read_item = container.read_item(item=doc_id, partition_key=doc_id)
    read_item['subtotal'] = read_item['subtotal'] + 1
    response = container.upsert_item(body=read_item)
    print('Upserted Item\'s Id is {0}, new subtotal={1}'.format(response['id'], response['subtotal'])) """


def showMenu(container, option = 1):
    SAIR = 5

    while(option != SAIR):
        members_ids = returnIDS(container)

        print("\n1 - Listar itens do banco de dados")
        print("2 - Deletar item do banco de dados com ID")
        print("3 - Inserir item no banco de dados")
        print("4 - Atualizar item no banco de dados")
        print(SAIR, "- Sair")
        option = int(input("\nEscolha uma opção: "))

        if (option == 1):
            if (members_ids):
                for member in members_ids:
                    read_item(container, member)
            else:
                print('Banco de dados vazio!')

        elif (option == 2):
            if (members_ids):
                for idx, member in enumerate(members_ids):
                    print(idx+1, '-', member)

                delMember = int(input("Escolha uma opção: "))
                delete_item(container, members_ids[delMember-1])
            else:
                print('Banco de dados vazio!')

        elif (option == 3):
            firstName = str(input("Insira o primeiro nome: "))
            lastName = str(input("Insira o sobrenome: "))
            yearOfEntry = int(input("Insira o ano de ingresso: "))
            course = str(input("Insira o curso: "))
            studentId = int(input("Insira o RA: "))
            body = get_newmember(firstName, lastName, yearOfEntry, course, studentId)
            container.create_item(body)

        elif (option == 4):
            if (members_ids):
                for idx, member in enumerate(members_ids):
                    print(idx+1, '-', member)

                updateMember = int(input("Escolha uma opção: "))
                readItem = container.read_item(item=members_ids[updateMember-1], partition_key=members_ids[updateMember-1])

                yearOfEntry = int(input("Insira o ano de ingresso: "))
                course = str(input("Insira o curso: "))
                studentId = int(input("Insira o RA: "))

                readItem['collegeInformation']['yearOfEntry'] = yearOfEntry
                readItem['collegeInformation']['course'] = course
                readItem['collegeInformation']['studentId'] = studentId
    
                response = container.replace_item(item=readItem, body=readItem)
                # print(readItem['id'], readItem[''])
if __name__ == '__main__':
    endpoint = 'https://sistemas-distribuidos-cosmosdb.documents.azure.com:443/'
    key = 'FLrFsEzm7N4eL8ECFpfxFEz5mcSHG6bFYpT47iEyJWbX9WmSTQAe1mSnZiO1Lm40YsX8pkYRSo0Bou91MbHxIg=='

    client = CosmosClient(endpoint, key)
    database_name = 'SeminarioSistemasDistribuidos-CosmosDB'
    database = client.create_database_if_not_exists(id=database_name)

    container_name = 'IntegrantesDoGrupo'
    container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    ids_members = returnIDS(container)
    
    showMenu(container)
        
