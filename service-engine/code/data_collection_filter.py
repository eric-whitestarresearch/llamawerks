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
from modules.datacollectionfilter import DataCollectionFilter

def get_data_collection_filter(pack_name, filter_name = None):
  """
  Reurns the definition of the data collection filter(s)

  Parameters:
    pack_name (String): The name of the pack to return the data collections for
    filter_name (String): The name of the data collection filter to retreive (Optional)

  Returns:
    List: A list of dictonaries that contain the data collection filter definition(s)
    Int: HTTP status code
  """
  
  dcf = DataCollectionFilter(request.state.db_client)
  
  return dcf.get_data_collection_filters(pack_name, filter_name)



def create_data_collection_filter(pack_name,data_collection_filter_definition):
  """
  Creates a new data collection filter

  Parameters:
    pack_name (String): The name of the pack to create the data collections in
    data_collection_filter_definition (Dict): The definition of the data collection filter
  
  Returns:
    Dict: Key: id value: the id of the new data collection filter
    Int: HTTP status code
  """
  dcf = DataCollectionFilter(request.state.db_client)

  return dcf.create_data_collection_filter(pack_name,data_collection_filter_definition)

def update_data_collection_filter(pack_name, data_collection_filter_definition):
  """
  Updates a data collection_filter

  Parameters:
    pack_name (String): The name of the pack to create the data collection filter in
    data_collection_definition (Dict): The definition of the data collection filter
  
  Returns:
    Dict: Key: updated, value: a count of the updated data collection filter
    Int: HTTP status code
  """
  
  dcf = DataCollectionFilter(request.state.db_client)

  return dcf.update_data_collection_filter(pack_name,data_collection_filter_definition)

def delete_data_collection_filter(pack_name, filter_name):
  """
  Deletes a data collection filter

  Parameters:
    pack_name (String): The name of the pack the data collection filter is in
    filter_name (String): The name of the data collection filter to delete

  Returns:
    Dict: Key: deleted value: a count of the data collection filter deleted
    Int: HTTP status code
  """
  
  dcf = DataCollectionFilter(request.state.db_client)

  return dcf.delete_data_collection_filter(pack_name, filter_name)