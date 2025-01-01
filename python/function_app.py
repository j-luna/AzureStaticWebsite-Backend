import logging
import os
import azure.functions as func
from azure.data.tables import TableServiceClient, TableEntity
from azure.core.exceptions import ResourceNotFoundError

app = func.FunctionApp()

@app.route(route="visitorCount", auth_level=func.AuthLevel.ANONYMOUS)
def VisitorCounterFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Initialize Table Service Client
    # Comment - might delete later
    connection_string = os.getenv("VisitorCountTableDB")
    table_name = "VisitorCountTable"
    table_service_client = TableServiceClient.from_connection_string(connection_string)
    table_client = table_service_client.get_table_client(table_name)

    try:
        # Try to get the entity from the table
        entity = table_client.get_entity(row_key="1", partition_key="visitorCount")
        # Update the count
        entity['count'] = entity.get('count', 0) + 1

    except ResourceNotFoundError:
        # If the entity does not exist, create a new one with count 1
        entity = {"PartitionKey": "visitorCount", "RowKey": "1", "count": 1}
    
    # Update the entity in the table
    table_client.upsert_entity(entity)

    return func.HttpResponse(f"{entity['count']}")