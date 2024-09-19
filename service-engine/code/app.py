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

from flask import render_template # Remove: import Flask
from connexion import FlaskApp, ConnexionMiddleware, request, App
from modules.database import Database
import contextlib
import typing

@contextlib.asynccontextmanager
async def lifespan_handler(app: ConnexionMiddleware) -> typing.AsyncIterator:
    """
    Called at startup and shutdown
    """
    db_client = Database()
    yield {"db_client": db_client}
    # Close the DB connections
    db_client.close_all_connections()

app = App(__name__, specification_dir="./", lifespan=lifespan_handler)
app.add_api("openapi.yaml")

@app.route("/")
def home():
    
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)