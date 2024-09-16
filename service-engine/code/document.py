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
from modules.datacollectiondocument import DataCollectionDocument

def get_documents(pack_name, data_collection_name):
  dcd = DataCollectionDocument(request.state.db_client)

  return dcd.get_documents(pack_name, data_collection_name)

def get_document_with_filter(pack_name, data_collection_name, filter_name, filter_variables, project):
  dcd = DataCollectionDocument(request.state.db_client)

  return dcd.get_document_with_filter(pack_name, data_collection_name, filter_name, filter_variables, project)

def create_document(pack_name, data_collection_name, document):
  dcd = DataCollectionDocument(request.state.db_client)

  return dcd.create_document(pack_name, data_collection_name, document)

def update_document_by_filter(pack_name, data_collection_name, filter_name, document_and_vars):
  dcd = DataCollectionDocument(request.state.db_client)

  return dcd.update_document(pack_name, data_collection_name, filter_name, document_and_vars['variables'], document_and_vars['document'])

def get_document_by_id(pack_name, data_collection_name, document_id):
  dcd = DataCollectionDocument(request.state.db_client)

  return dcd.get_document_by_id(pack_name, data_collection_name, document_id)

def update_document_by_id(pack_name, data_collection_name, document_id, document):
  dcd = DataCollectionDocument(request.state.db_client)

  return dcd.update_document_by_id(pack_name, data_collection_name, document_id, document['document'])

def delete_document_by_id(pack_name, data_collection_name, document_id ):
  dcd = DataCollectionDocument(request.state.db_client)

  return dcd.delete_document_by_id(pack_name, data_collection_name, document_id)