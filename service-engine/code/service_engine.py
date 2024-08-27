from connexion import request
from flask import abort



def get_db_connection():
  """
    A function to get a database connection from the pool

    Parameters:
      none

    Returns:
      (MongoClient): A connection to the database

  """
  
  db_client = request.state.db_client
  connection = db_client.get_db_connection()

  return connection

def return_db_connection(connection):
  """
    Returns a DB connection to the pool after it is used

    Parameters:
      connection (MongoClient): A connection to the database

    Returns:
      None
  """

  db_client = request.state.db_client
  db_client.return_db_connection(connection)

  return


def do_something():
  return "Hello there"

def get_all_data_collections(pack_name):
  
  collection = 'data_collections'
  db_client = request.state.db_client

  filter = {'pack' : pack_name}
  data_collections = db_client.find_all_in_collection(collection,filter)
  
  print(data_collections)
  return data_collections

def create_data_collection(pack_name,data_collection_definition):

  if pack_name != data_collection_definition['pack']:
    abort(422, "The pack name specified in the URI and the data collection defination do not match")

  collection = 'data_collections'
  db_client = request.state.db_client
  
  #Check to see if this data collection already exists. If it does, stop.
  filter = {'pack': pack_name, 'collection_name': data_collection_definition['collection_name']}
  data_collection = db_client.find_all_in_collection(collection, filter)

  if len(data_collection):
    abort(409, f"The data collection {data_collection_definition['collection_name']} in pack {pack_name} already exists. Use patch method to update it")
  
  new_data_collection_id = db_client.insert_document(collection, data_collection_definition)


  return new_data_collection_id