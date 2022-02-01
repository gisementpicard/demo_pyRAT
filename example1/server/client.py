from pymongo import MongoClient
from pymongo.database import Database 
from typing import Optional

from server.models import Command, Result, RATModel

class CollectionCrudClient:
    def __init__(self, database:Database, collection: str, cls) -> None:
        self.database = database
        self.collection = collection
        self.cls = cls

    def create(self, item: RATModel):
        new_item = self.database[self.collection].insert_one(
            item.dict(by_alias=True)
        ) 
    
    def read(self, item_id: str) -> Optional[RATModel]:
        item = self.database[self.collection].find_one(item_id)
        if item:
            return self.cls(**item)
        return None
    
    def find(self, filter: dict):
        return [x for x in self.database[self.collection].find(filter)]

    def delete(self, item_id: str):
        self.database[self.collection].delete_one({'_id': item_id})

    def update(self, item_id: str, updates: dict):
        self.database[self.collection].update_one({'_id': item_id}, {"$set": updates})

class pyRATDBClient:
    def __init__(self,
                 host='localhost',
                 port=27017,
                 database='pyrat',
                 username=None,
                 password=None) -> None:
        if username and password:
            self.client = MongoClient(host=host,
                                      port=port,
                                      username=username,
                                      password=password)
        else:
            self.client = MongoClient(host=host, port=port)
        self.database = self.client[database]
        print(self.database)
        self.command = CollectionCrudClient(self.database, 'command', Command)
        self.result = CollectionCrudClient(self.database, 'result', Result)

        print(self.command)
        print(self.result)