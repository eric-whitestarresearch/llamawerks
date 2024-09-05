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
from .datacollectionfilter import DataCollectionFilter
from ast import literal_eval
from bson.objectid import ObjectId


class DataCollectionDocument():

  db_client = None
  dcf = None

  def __init__(self,db_client):
    """
    The constructor for the ServiceComponent class.

    Parameters:
      self (ServiceItem): The object itself
      db_client (Str): A Database object that hosts the connection to the database
    """

    self.db_client = db_client
    self.dcf =  DataCollectionFilter(self.db_client)

  def get_documents(self, pack_name, data_collection_name):
    db_collection = f"{pack_name}.{data_collection_name}"

    db_filter = {}
    documents = self.db_client.find_all_in_collection(db_collection,db_filter)

    return documents
  
  def get_document_with_filter(self, pack_name, data_collection_name, filter_name, filter_variables ):
    db_collection = f"{pack_name}.{data_collection_name}"

    db_filter = self.generate_db_filter(pack_name, filter_name, filter_variables)
    documents = self.db_client.find_all_in_collection(db_collection,db_filter)

    return documents
  
  def generate_db_filter(self, pack_name, filter_name, filter_variables):
    
    result = self.dcf.get_data_collection_filters(pack_name,filter_name)
    
    if result[1] == 200: #If the filter was found
      db_filter = result[0][0]['filter']
      db_filter_string = str(db_filter)
      variables = result[0][0]['variables']
      for var in variables:
        db_filter_string = db_filter_string.replace(f"#{var['name']}#",filter_variables[var['name']])
      db_filter = literal_eval(db_filter_string)
    else:
      abort(404, f"Could not find the filter {filter_name} in pack {pack_name}") #The only other option is no filter was found

    return db_filter
    

  
  def create_document(self, pack_name, data_collection_name, document):
    db_collection = f"{pack_name}.{data_collection_name}"
    result = self.db_client.insert_document(db_collection, document)

    return {"id":result}, 200
  
  def update_document(self, pack_name, data_collection_name, filter_name, filter_variables, document_updates):
    db_filter = self.generate_db_filter(pack_name, filter_name, filter_variables)
    db_collection = f"{pack_name}.{data_collection_name}"

    result = self.db_client.update_document(db_collection, db_filter, document_updates, upsert=False)

    return {"updated" : result}, 200

  def get_document_by_id(self, pack_name, data_collection_name, document_id):
    db_collection = f"{pack_name}.{data_collection_name}"

    db_filter = {"_id": ObjectId(document_id)}
    documents = self.db_client.find_one_in_collection(db_collection,db_filter)

    return documents
  
  def update_document_by_id(self, pack_name, data_collection_name, document_id, document):
    db_collection = f"{pack_name}.{data_collection_name}"
    db_filter = {"_id": ObjectId(document_id)}

    result = self.db_client.update_document(db_collection, db_filter, document, upsert=False)

    return {"updated" : result}, 200
  
  def delete_document_by_id(self, pack_name, data_collection_name, document_id ):
    db_collection = f"{pack_name}.{data_collection_name}"
    db_filter = {"_id": ObjectId(document_id)}

    result = self.db_client.delete_document(db_collection, db_filter)

    return {"deleted": result}, 200
  