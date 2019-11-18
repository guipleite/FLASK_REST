from flask import Flask, request, jsonify, abort, make_response
from flask_restful import Api, Resource,reqparse,fields, marshal
import json
from os import environ
from flask_pymongo import PyMongo
import pymongo  

try:
    serv_addr = environ["serv_addr"]
except:
    print("Servidor externo nao definido, testando com o localhost")
    serv_addr = "localhost"

app = Flask(__name__)
#app.config['MONGO_URI'] = "mongodb://{}:27017/todo".format(serv_addr)

api = Api(app)

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

class HealthCheck(Resource):

    def get(self):
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp

api.add_resource(HealthCheck, '/healthcheck/', endpoint = 'healthcheck')

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = "", location = 'json')

        serv_addr = environ["serv_addr"]

        client = pymongo.MongoClient("mongodb://{}:27017/todo".format(serv_addr)) # defaults to port 27017

        db = client.todo
        self.collection = db.tasks #makes a collection called "test" in the "test" db
        

        super(TaskListAPI, self).__init__()

    def get(self):
        return {'tasks': [marshal(task, task_fields)  for task in self.collection.find()]}

    def post(self):
        args = self.reqparse.parse_args()
        tasks = self.collection.find()
        
        task = {
            'id': tasks.sort([("id", -1)])[0]["id"] + 1 if self.collection.count() > 0 else 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        self.collection.insert_one(task)
        return {'task': marshal(task, task_fields)}

api.add_resource(TaskListAPI, '/todo/api/tasks/', endpoint = 'tasks')

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')

        serv_addr = environ["serv_addr"]

        client = pymongo.MongoClient("mongodb://{}:27017/todo".format(serv_addr)) # defaults to port 27017

        db = client.todo
        self.collection = db.tasks #makes a collection called "test" in the "test" db

        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task  for task in self.collection.find() if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task[0], task_fields)}

    def put(self, id):
        task =  self.collection.find({"id": id})
        if (self.collection.find({"id": id})).count() == 0:
            abort(404)
        if not request.json:
            abort(400)
    
        newvalues = { "$set": { "title":  request.json.get('title', task[0]['title']),
                                "description": request.json.get('description',task[0]['description']),
                                "done":  request.json.get('done', task[0]['done'])} }

        req = jsonify({'task': marshal(task[0], task_fields)})
        self.collection.update_one(task[0], newvalues)

        return req

    def delete(self, id):
        if (self.collection.find({"id": id})).count() == 0:
            abort(404)
        self.collection.delete_one({"id": id})
        return {'result': True}

api.add_resource(TaskAPI, '/todo/api/tasks/<int:id>', endpoint = 'task')

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
