
from pydoc import doc
from typing import Any
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
    print('\n1.2 Reading Item by Id\n')

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
    #Deleting items
    for member in ids_members:
        delete_item(container, member)
        