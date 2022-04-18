from dataclasses import dataclass
from enum import unique
from peewee import *
import uuid

psql_db=PostgresqlDatabase('mydb',user='hhimanshu',password='hhimanshu',host='localhost')

  

def generate_users(num_users):
    for i in range(num_users):
        user_name=str(uuid.uuid4())[0:8]
        OrgUser(username=user_name).save()

class PeeweeConnectionMiddleware(object):
    def process_request(self, req, resp):
        psql_db.connect()

    def process_response(self, req, resp, resource, req_succeeded):
        if not psql_db.is_closed():
            psql_db.close()

class BaseModel(Model):
    class Meta:
        database=psql_db

class OrgUser(BaseModel):
    username=CharField(unique=True)
    class Meta:
        db_tables='orguser'

# psql_db.create_tables([OrgUser])