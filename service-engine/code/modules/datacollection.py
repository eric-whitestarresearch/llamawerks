#     Llamawerks - A portal for users to request services with runbook automation
#     Copyright (C) 2024  Whitestar Research LLC
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.

from .servicecomponent import ServiceComponent

class DataCollection(ServiceComponent):
  """
  The class for interacting with Data Collections

  Attributes:
    item_type (String): What kind of item this is. It will be defined in the child class.
    item_type_name (string): Display name for this item type

  Inherited Attributes:
    db_client (Database): This is defined and set in the parent class
    db_collection (String): The collection in the database for this item type. It will be defined in the child class

  Inherited Methods
    __init__
    get_service_components
    delete_service_component
    create_service_component
    update_serivce_component
  
  """

  db_collection = "__system.data_collections"
  component_type = "data_collection"
  component_type_name = "data collection"

  def data_collection_exist(self, pack_name, data_collection_name):
    """
    Check if a data collection exists

    Parameters:
      pack_name (String): The name of the pack the service item is in
      data_collection_name (String): The name of the data collection

    Returns:
      Bool: True if exist, false if not
    
    """
    return self.service_component_exists(pack_name, data_collection_name)

  def get_data_collections(self, pack_name, data_collection_name = None):
    """
    Retrieve the data collection definition from the database

    Parameters:
      pack_name (String): The name of the pack the data collection is in
      data_collection_name (String): The name of the data collection (Optional)

    Returns:
      List: A list of dictonaries that contain the data collections definition(s)
      Int: HTTP status code
    """

    return self.get_service_component(pack_name, data_collection_name)
  
  def delete_data_collection(self, pack_name, data_collection_name):
    """
    Deletes a data collection
    This will delete the definition and collection from the database

    Parameters:
      pack_name (String): The name of the pack the data collection is in
      data_collection_name (String): The name of the data collection to delete

    Returns:
      Dict: Key: deleted value: a count of the data collections deleted
      Int: HTTP status code
    """
    result = self.delete_service_component(pack_name, data_collection_name)

    self.db_client.delete_collection(f"{pack_name}.{data_collection_name}")

    return result

  
  def create_data_collection(self,pack_name,data_collection_definition):
    """
    Creates a new data collection

    Parameters:
      pack_name (String): The name of the pack to create the data collections in
      data_collection_definition (Dict): The definition of the data collection
    
    Returns:
      Dict: Key: id value: the id of the new data collection
      Int: HTTP status code
    """

    dc_id = self.create_service_component(pack_name, data_collection_definition)
    dc_id[0]['indexes'] = self.manage_indexes(pack_name, data_collection_definition['name'])

    return dc_id
  
  def update_data_collection(self,pack_name,data_collection_definition):
    """
    Updates a data collection

    Parameters:
      pack_name (String): The name of the pack to create the data collections in
      data_collection_definition (Dict): The definition of the data collection
    
    Returns:
      Dict: Key: updated, value: a count of the updated data collections
      Int: HTTP status code
    """

    update_result = self.update_serivce_component(pack_name, data_collection_definition)

    self.manage_indexes(pack_name, data_collection_definition['name'], True)

    return update_result
  
  def manage_indexes(self, pack_name, data_collection_name, drop_indexes = False):
    """
    Manage the life cycle of indexes on a data collection
    Currently only supports simple indexes

    Parameters:
      pack_name (String): The name of the pack that contains the data collection
      data_collection_name (String): the name of the data collection

    Returns:
      None
    
    """
    #Index creation is idempotent. If it already exists, nothing will happen
    index_result = []
    db_collection_name = f"{pack_name}.{data_collection_name}"
    dc_definition = self.get_data_collections(pack_name,data_collection_name)
    for field in dc_definition[0][0]['fields']:
      if field['index']:
        index_result.append(self.db_client.create_index(db_collection_name, field['name'], field['unique']))

    #If updating a data collection we should drop any unneeded indexes
    if drop_indexes:
      index_info = self.db_client.get_index_info(db_collection_name)
      index_diff = set(index_info.keys()).difference(index_result)

      for index in index_diff:
        if index != '_id_': #This is the default index it needs to stay
          self.db_client.delete_index(db_collection_name, index)

    return index_result