#     Llamaflow - A self service portal with runbook automation
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

from connexion import request
from modules.service import Service


def get_services(pack_name, service_name = None):
  """
  Reurns the definition of the service(s)

  Parameters:
    pack_name (String): The name of the pack to return the service(s) for
    collection_name (String): The name of the service to retreive (Optional)

  Returns:
    List: A list of dictonaries that contain the service definition(s)
    Int: HTTP status code
  """
  
  service = Service(request.state.db_client)
  
  return service.get_services(pack_name, service_name)
  
def delete_service(pack_name, service_name):
  """
  Deletes a service

  Parameters:
    pack_name (String): The name of the pack the service is in
    collection_name (String): The name of the service to delete

  Returns:
    Dict: Key: deleted value: a count of the service deleted
    Int: HTTP status code
  """
  
  service = Service(request.state.db_client)

  return service.delete_service(pack_name, service_name)

def create_service(pack_name,service_definition):
  """
  Creates a new service

  Parameters:
    pack_name (String): The name of the pack to create the services in
    service_definition (Dict): The definition of the service
  
  Returns:
    Dict: Key: id value: the id of the new service
    Int: HTTP status code
  """
  service = Service(request.state.db_client)

  return service.create_service(pack_name,service_definition)

def update_service(pack_name, service_definition):
  """
  Updates a service

  Parameters:
    pack_name (String): The name of the pack to the service is in
    service_definition (Dict): The definition of the service
  
  Returns:
    Dict: Key: updated, value: a count of the updated service
    Int: HTTP status code
  """
  
  service = Service(request.state.db_client)

  return service.update_service(pack_name,service_definition)