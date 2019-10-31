from flask import Flask, request, jsonify, abort, make_response
from flask_restful import Api, Resource,reqparse,fields, marshal
import json

app = Flask(__name__)
api = Api(app)

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

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
        #return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

api.add_resource(HealthCheck, '/healthcheck/', endpoint = 'healthcheck')

class TaskListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'No task title provided', location = 'json')
        self.reqparse.add_argument('description', type = str, default = "", location = 'json')
        super(TaskListAPI, self).__init__()

    def get(self):
        with open("db.json", "r") as jsonFile:
            tasks = json.load(jsonFile)
        return {'tasks': [marshal(task, task_fields) for task in tasks]}


    def post(self):
        args = self.reqparse.parse_args()

        with open("db.json", "r") as jsonFile:
            tasks = json.load(jsonFile)

        task = {
            'id': tasks[-1]['id'] + 1 if len(tasks) > 0 else 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        return {'task': marshal(task, task_fields)}

api.add_resource(TaskListAPI, '/todo/api/tasks/', endpoint = 'tasks')

class TaskAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        with open("db.json", "r") as jsonFile:
           tasks = json.load(jsonFile)

        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task[0], task_fields)}

    def put(self, id):
        with open("db.json", "r") as jsonFile:
           tasks = json.load(jsonFile)
           
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        if not request.json:
            abort(400)
        task[0]['title'] = request.json.get('title', task[0]['title'])
        task[0]['description'] = request.json.get('description',
                                                task[0]['description'])
        task[0]['done'] = request.json.get('done', task[0]['done'])
        return jsonify({'task': marshal(task[0], task_fields)})

    def delete(self, id):
        with open("db.json", "r") as jsonFile:
           tasks = json.load(jsonFile)
           
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}

api.add_resource(TaskAPI, '/todo/api/tasks/<int:id>', endpoint = 'task')

if __name__ == '__main__':
    app.run(debug=True)