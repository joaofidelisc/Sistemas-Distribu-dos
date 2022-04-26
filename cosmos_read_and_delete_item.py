import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import cosmos_get_started
# from container import list_Containers


HOST = 'https://sistemas-distribuidos-cosmosdb.documents.azure.com:443/'
MASTER_KEY = 'FLrFsEzm7N4eL8ECFpfxFEz5mcSHG6bFYpT47iEyJWbX9WmSTQAe1mSnZiO1Lm40YsX8pkYRSo0Bou91MbHxIg=='
DATABASE_ID = 'SeminarioSistemasDistribuidos-CosmosDB'
CONTAINER_ID = 'IntegrantesDoGrupo'

def read_items(container):
    print('\n1.3 - Reading all items in a container\n')

    # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
    #       Important to handle throttles whenever you are doing operations such as this that might
    #       result in a 429 (throttled request)
    item_list = list(container.read_all_items(max_item_count=10))

    print('Found {0} items'.format(item_list.__len__()))

    for doc in item_list:
        print('Item Id: {0}'.format(doc.get('id')))

def read_item(container, doc_id):
    print('\n1.2 Reading Item by Id\n')

    # Note that Reads require a partition key to be spcified.
    response = container.read_item(item=doc_id, partition_key=doc_id)

    print('Item read by Id {0}'.format(doc_id))
    print('lastName: {0}'.format(response.get('lastName')))
    print('informationsFromSchool: {0}'.format(response.get('informationsFromSchool')))

if __name__=='main':
    # read_items(cosmos_get_started.container)
    read_item(cosmos_get_started.container, cosmos_get_started.container_name)