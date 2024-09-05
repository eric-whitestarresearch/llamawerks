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

from flask import abort

class ServiceComponent:
  """
  The superclass for all service  components i.e. Data Collections, Documents, Filters, Packs, Services
  This class is not meant to be used directly. It should be inherited by child class.

  Attributes:
    db_client (Database): A Database object that hosts the connection to the database
    db_collection (String): The collection in the database for this item type. It will be defined in the child class
    component_type (String): What kind of item this is. It will be defined in the child class.
    component_type_name (String): Display name for this item type. It will be defined in the child class.
  """

  db_client = None
  db_collection = ""
  component_type = ""
  component_type_name = ""

  def __init__(self,db_client) -> None:
    """
    The constructor for the ServiceComponent class.

    Parameters:
      self (ServiceItem): The object itself
      db_client (Str): A Database object that hosts the connection to the database
    """

    self.db_client = db_client

  def get_service_component(self, pack_name, service_component_name = None):
    """
    Retrieve the service component from the database

    Parameters:
      pack_name (String): The name of the pack the service item is in
      service_component_name (String): The name of the service component (Optional)

    Returns:
      List: A list of dictonaries that contain the service component definition(s)
      Int: HTTP status code
    """

    if service_component_name:
      db_filter = {"pack": pack_name, "name": service_component_name}
      service_items = [self.db_client.find_one_in_collection(self.db_collection,db_filter)]
      if not service_items[0]:
        abort(404,f"Could not find {self.component_type_name} {service_component_name} in pack {pack_name}")
    else:
      db_filter = {"pack": pack_name}
      service_items = self.db_client.find_all_in_collection(self.db_collection,db_filter)

    if not len(service_items):
      return service_items, 204 #The pack has no service items
    else:  
      return service_items, 200
    
  def delete_service_component(self, pack_name, service_component_name):
    """
    Deletes a service component

    Parameters:
      pack_name (String): The name of the pack the data collection is in
      service_component_name (String): The name of the service component to delete

    Returns:
      Dict: Key: deleted value: a count of the components deleted
      Int: HTTP status code
    """

    db_filter = {'pack' : pack_name, 'name': service_component_name}
    delete_count = self.db_client.delete_document(self.db_collection, db_filter)

    return {"deleted" : delete_count}, 200
  

  def create_service_component(self,pack_name,service_component_definition):
    """
    Creates a new service component

    Parameters:
      pack_name (String): The name of the pack to create the service component in
      service_component_definition (Dict): The definition of the service component
    
    Returns:
      Dict: Key: id value: the id of the new service component
      Int: HTTP status code
    """
    
    if pack_name != service_component_definition['pack']:
      abort(422, f"The pack name specified in the URI and the {self.component_type_name} definition do not match")
    
    #Check to see if this data collection already exists. If it does, don't create it again.
    filter = {'pack': pack_name, 'name': service_component_definition['name']}
    data_collection = self.db_client.find_all_in_collection(self.db_collection, filter)

    if len(data_collection):
      return { "id": data_collection[0]['_id']['$oid'] } , 200
    
    new_service_component_id = self.db_client.insert_document(self.db_collection, service_component_definition)


    return { "id": new_service_component_id } , 201
  
  def update_serivce_component(self, pack_name, service_component_definition):
    """
    Updates a service component

    Parameters:
      pack_name (String): The name of the pack to update the service component in
      service_component_definition (Dict): The definition of the service component
    
    Returns:
      Dict: Key: updated, value: a count of the updated components
      Int: HTTP status code
    """
    
    if pack_name != service_component_definition['pack']:
      abort(422, f"The pack name specified in the URI and the {self.component_type_name} definition do not match")

    #Check to see if this service component already exists. If it does not, stop.
    filter = {'pack': pack_name, 'name': service_component_definition['name']}
    data_collection = self.db_client.find_one_in_collection(self.db_collection, filter)

    if not data_collection:
      abort(404, f"The {self.component_type_name}  {service_component_definition['collection_name']} in pack {pack_name} does not exist. Use put method to create it")

    update_count = self.db_client.update_document(self.db_collection, filter, service_component_definition)

    if update_count:
      return { "updated" : update_count }, 202
    else:
      return { "updated" : 0 }, 208
      




