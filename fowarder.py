from flask import Flask, request, jsonify, abort, make_response
from flask_restful import Api, Resource,reqparse,fields, marshal
import json
from os import environ
import requests as req

app = Flask(__name__)

api = Api(app)

global serv_addr
serv_addr = "http://"+environ["serv_addr"]+"/" #addr

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

        super(TaskListAPI, self).__init__()

    def get(self):
        res = req.get(serv_addr + "todo/api/tasks/")
        print(res)
        return jsonify(res.json())

    def post(self):
        args = self.reqparse.parse_args()
        
        res = req.post(url = serv_addr + "todo/api/tasks/", json= args)
       
        return res.json()

api.add_resource(TaskListAPI, '/todo/api/tasks/', endpoint = 'tasks')

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')

        super(TaskAPI, self).__init__()

    def get(self, id):
        res = req.get(serv_addr + "todo/api/tasks/"+str(id))
        return jsonify(res.json())

    def put(self, id):

        args = self.reqparse.parse_args()

        if not request.json:
            abort(400)

        res = req.put(url = serv_addr + "todo/api/tasks/"+str(id), data= args)

        #return jsonify({'task': marshal(task[0], task_fields)})
        return jsonify(res.json())

    def delete(self, id):
        res = req.delete(serv_addr + "todo/api/tasks/"+str(id))
        return {'result': True}

api.add_resource(TaskAPI, '/todo/api/tasks/<int:id>', endpoint = 'task')

if __name__ == '__main__':
    app.run(host="0.0.0.0,debug=True)
