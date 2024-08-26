from connexion import request

def do_something():
  db_client = request.state.db_client
  connection = db_client.get_db_connection()
  connection2 = db_client.get_db_connection()
  connection3 = db_client.get_db_connection()
  connection4 = db_client.get_db_connection()
  connection5 = db_client.get_db_connection()
  connection6 = db_client.get_db_connection()
  db_client.return_db_connection(connection)
  return "Hello there"