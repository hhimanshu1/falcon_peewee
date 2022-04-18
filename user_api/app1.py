import json
import falcon
from peewee import *
 

db=PostgresqlDatabase(database='mydb',user='hhimanshu',password='hhimanshu',host='localhost')



class BaseModel(Model):
    class Meta:
        database=db

class UserModel(BaseModel):
    role=CharField(default='user')
    username=CharField()
    firstName=CharField()
    lastName=CharField()

    class Meta:
        db_table='user1'


db.create_tables([UserModel])


 
from wsgiref.simple_server import make_server

class ThingResource:
    def on_get(self,req,resp,username):
        print()
        user=UserModel.select(UserModel.username)
        print()
        print(user)
        if user==username:
            resp.body=json.dumps({
                'status':'success',
                'data':{
                    'username':user,
                   
                }
            })
        else:
            resp.body=json.dumps({
                'status':'Failed'
            })

class PeeweeConnectionMiddleware(object):
    def process_request(self,req,resp):
        if db.is_closed():
            db.connect()

    def process_response(self,req,resp,resource, req_succeeded):
        if not db.is_closed():
            db.close()

app=falcon.API(middleware=[PeeweeConnectionMiddleware()])

thing=ThingResource()

app.add_route('/user/{username}',thing)

if __name__=='__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()