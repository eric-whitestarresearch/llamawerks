from connexion import request
from flask import abort

def get_data_collections(pack_name, data_collection_name = None):
  """
  Reurns the defination of the matchings data collections

  Parameters:
    pack_name (String): The name of the pack to return the data collections for
    collection_name (String): The name of the data collection to retreive (Optional)

  Returns:
    List: A list of dictonaries that contain the data collection definition(s)
  """
  
  db_collection = 'data_collections'
  db_client = request.state.db_client

  
  if data_collection_name:
    filter = {'pack' : pack_name, 'collection_name': data_collection_name}
    data_collections = [db_client.find_one_in_collection(db_collection,filter)]
    if not len(data_collections):
      abort(404,f"Could not find data collection {data_collection_name} in pack {pack_name}")
  else:
    filter = {'pack' : pack_name}
    data_collections = db_client.find_all_in_collection(db_collection,filter)


  if not len(data_collections):
    return data_collections, 204 #The pack has no data collections
  else:  
    return data_collections, 200
  
def delete_data_collection(pack_name, data_collection_name):
  """
  Reurns the defination of the matchings data collections

  Parameters:
    pack_name (String): The name of the pack the data collection is in
    collection_name (String): The name of the data collection to delete

  Returns:
    List: A list of dictonaries that contain the data collection definition(s)
  """
  
  db_collection = 'data_collections'
  db_client = request.state.db_client

  filter = {'pack' : pack_name, 'collection_name': data_collection_name}
  delete_count = db_client.delete_document(db_collection, filter)

  return {"data_collections_deleted" : delete_count}, 200

def create_data_collection(pack_name,data_collection_definition):
  """
  Creates a new data collection

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    String: a string containing the id of the new data collection
  """
  
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


  return { "id": new_data_collection_id } , 201

def update_data_collection(pack_name, data_collection_definition):
  """
  Creates a new data collection

  Parameters:
    pack_name (String): The name of the pack the data collections is in
    collection_name: THe name of the collection to update
    data_collection_definition (Dict): The definition of the data collection
  
  Returns:
    String: a string containing the id of the new data collection
  """
  
  if pack_name != data_collection_definition['pack']:
    abort(422, "The pack name specified in the URI and the data collection defination do not match")

  collection = 'data_collections'
  db_client = request.state.db_client

  #Check to see if this data collection already exists. If it does not, stop.
  filter = {'pack': pack_name, 'collection_name': data_collection_definition['collection_name']}
  data_collection = db_client.find_one_in_collection(collection, filter)

  if not data_collection:
    abort(404, f"The data collection {data_collection_definition['collection_name']} in pack {pack_name} does not exist. Use put method to create it")

  update_count = db_client.update_document(collection, filter, data_collection_definition)

  if update_count:
    return { 'data_collection_updated' : update_count }, 202
  else:
    return None, 208