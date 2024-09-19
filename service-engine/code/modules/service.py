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

class Service(ServiceComponent):
  """
  The class for interacting with Data Collection Filters

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

  db_collection = "__system.service"
  component_type = "service"
  component_type_name = "service"

  def get_services(self, pack_name, service_name = None):
    """
    Retrieve the service definition from the database

    Parameters:
      pack_name (String): The name of the pack the service(s) is in
      service_name (String): The name of the service (Optional)

    Returns:
      List: A list of dictonaries that contain the service definition(s)
      Int: HTTP status code
    """

    return self.get_service_component(pack_name, service_name)
  
  def delete_service(self, pack_name, service_name):
    """
    Deletes a service

    Parameters:
      pack_name (String): The name of the pack the service is in
      service_name (String): The name of the service to delete

    Returns:
      Dict: Key: deleted value: a count of the services deleted
      Int: HTTP status code
    """

    return self.delete_service_component(pack_name, service_name)

  
  def create_service(self,pack_name,service_definition):
    """
    Creates a new service

    Parameters:
      pack_name (String): The name of the pack to create the service in
      data_collection_definition (Dict): The definition of the service
    
    Returns:
      Dict: Key: id value: the id of the new service
      Int: HTTP status code
    """

    return self.create_service_component(pack_name, service_definition)  

  def update_service(self,pack_name,service_definition):
    """
    Updates a service definition

    Parameters:
      pack_name (String): The name of the pack the service is in
      service_definition (Dict): The definition of the service
    
    Returns:
      Dict: Key: updated, value: a count of the updated service
      Int: HTTP status code
    """

    return self.update_serivce_component(pack_name, service_definition)