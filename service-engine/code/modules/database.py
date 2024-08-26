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

import yaml
from pymongo import MongoClient
from bson import ObjectId, json_util
import urllib.parse
import json
import re
from jsonschema import validate, ValidationError
import json
import queue
from flask import current_app

class DBConfigValidationError(ValidationError):
  pass

class Database:
  """
  This is a class used for accessing the database. When initialize it it open a connection to the database. 
  The config for the database connection comes from /opt/self-service-portal/conf/db.conf

  Attributes:
      mongo_client (MongoClient): The client class for the db connection
      datbase (Database): The database the client is connected to
      collection (Collection): The collection that the client is connect to
  """
  
  conf_home = "/opt/llamawerks/conf"
  connection_pool = queue.Queue()

  def __init__(self) -> None:
    """
    The constructor for the Database class.

    Parameters:
      self (Database): The object itself
      database (Str): The name of the database to connect to
      collection (Str): The name of the collection to connect to
    """

    db_conf_file=self.conf_home+"/db.yaml"
    with open(db_conf_file,'r') as file:
      db_config = yaml.safe_load(file)

    try:
      self.validate_config(db_config)
    except ValidationError as e:
      raise DBConfigValidationError(f"The DB config file {db_conf_file} is invalid:\n" + str(e))

    username = urllib.parse.quote_plus(db_config['username'])
    password = urllib.parse.quote_plus(db_config['password'])
    for _ in range(db_config['max_connections']):
      connection =  MongoClient(f"mongodb://{username}:{password}@{db_config['host']}:{db_config['port']}")
      self.connection_pool.put(connection)


  def validate_config(self, config) -> None:
    """
    This is a method that validates the contents of the DB config file

    Parameters:
      self (Database): The object itself.
      config (Dict): A dictonary containing the config
    
    Returns:
      None
    """

    schema = {
      '$schema': 'http://json-schema.org/draft-04/schema#',
      'type': 'object',
      'properties': {
        'host': {'type': 'string'},
        'port': {'type': 'integer'},
        'username': {'type': 'string'},
        'password': {'type': 'string'},
        'max_connections': {'type': 'integer'}
      },
      'required': ['host', 'port', 'username', 'password', 'max_connections']}

    validate(config, schema) #If we validate nothing happend, if we fail a ValidationError exception is thrown

    return None
  
  def get_db_connection(self) -> MongoClient:
    """
    Get a connection from the database pool

    Parameters:
      self (Database): The object itself.

    Returns:
      (MongoClient): A connection to the database
    """
    
    if self.connection_pool.qsize() == 0:
      current_app.logger.warn("The db connection pool is empty, waiting for a connection")
    
    connection = self.connection_pool.get()
    

    return connection
  
  def return_db_connection(self, connection):
    """
    Returns a DB connection to the pool

    Parameters:
      self (Database): The object itself.
      connection (MongoClient): A connection to the database

    Returns
      None
    """

    self.connection_pool.put(connection)

    return
  
  def close_all_connections(self):
    """
    Close all connections to the database in prep for shutdown

    Parameters:
      self (Database): The object itself.
    """

    for _ in range(self.connection_pool.qsize()):
      connection = self.connection_pool.get()
      connection.close()

    return


    