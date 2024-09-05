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

class DataCollectionFilter(ServiceComponent):
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

  db_collection = "__system.filters"
  component_type = "data_collection_filter"
  component_type_name = "data collection filter"

  def get_data_collection_filters(self, pack_name, filter_name = None):
    """
    Retrieve the data collection dfilter efinition from the database

    Parameters:
      pack_name (String): The name of the pack the data collection is in
      filter_name (String): The name of the data collection filter (Optional)

    Returns:
      List: A list of dictonaries that contain the data collection filter definition(s)
      Int: HTTP status code
    """

    return self.get_service_component(pack_name, filter_name)

  def create_data_collection_filter(self,pack_name,data_collection_filter_definition):
    """
    Creates a new data collection filter

    Parameters:
      pack_name (String): The name of the pack to create the data collections in
      data_collection_filter_definition (Dict): The definition of the data collection
    
    Returns:
      Dict: Key: id value: the id of the new data collection filter
      Int: HTTP status code
    """

    dcf_id = self.create_service_component(pack_name, data_collection_filter_definition)

    return dcf_id
  
  def update_data_collection_filter(self,pack_name,data_collection_filter_definition):
    """
    Updates a data collection filter

    Parameters:
      pack_name (String): The name of the pack to create the data collection filter in
      data_collection_definition (Dict): The definition of the data collection filter
    
    Returns:
      Dict: Key: updated, value: a count of the updated data collection filter
      Int: HTTP status code
    """

    update_result = self.update_serivce_component(pack_name, data_collection_filter_definition)

    return update_result
  
  def delete_data_collection_filter(self, pack_name, filter_name):
    """
    Deletes a data collection filter

    Parameters:
      pack_name (String): The name of the pack the data collection is in
      data_collection_name (String): The name of the data collection to delete

    Returns:
      Dict: Key: deleted value: a count of the data collection filter deleted
      Int: HTTP status code
    """
    result = self.delete_service_component(pack_name, filter_name)

    return result