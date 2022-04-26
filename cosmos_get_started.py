from azure.cosmos import exceptions, CosmosClient, PartitionKey
import members

if __name__ == '__main__':
    
    # Initialize the Cosmos client
    endpoint = 'https://sistemas-distribuidos-cosmosdb.documents.azure.com:443/'
    key = 'FLrFsEzm7N4eL8ECFpfxFEz5mcSHG6bFYpT47iEyJWbX9WmSTQAe1mSnZiO1Lm40YsX8pkYRSo0Bou91MbHxIg=='

    # <create_cosmos_client>
    client = CosmosClient(endpoint, key)
    # </create_cosmos_client>

    # Create a database
    # <create_database_if_not_exists>
    database_name = 'SeminarioSistemasDistribuidos-CosmosDB'
    database = client.create_database_if_not_exists(id=database_name)
    # </create_database_if_not_exists>

    # Create a container
    # Using a good partition key improves the performance of database operations.
    # <create_container_if_not_exists>
    container_name = 'IntegrantesDoGrupo'
    container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    # </create_container_if_not_exists>

    # Add items to the container
    member_items_to_create = [members.get_member_joaofidelis(), members.get_member_rafaeltury(), members.get_member_thiagoaraujo()]

    # <create_item>
    for member_item in member_items_to_create:
        container.create_item(body=member_item)
    # </create_item>

    # Read items (key value lookups by partition key and id, aka point reads)
    # <read_item>
    for members in member_items_to_create:
        item_response = container.read_item(item=members['id'], partition_key=members['id'])
        request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
        print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
    # </read_item>

    # Query these items using the SQL query syntax. 
    # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
    # <query_items>
    query = "SELECT * FROM c WHERE c.lastName IN ('Fidelis Cardozo', 'Tury Minatel', 'Araujo')"

    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))

    request_charge = container.client_connection.last_response_headers['x-ms-request-charge']

    print('Query returned {0} items. Operation consumed {1} request units'.format(len(items), request_charge))
    

