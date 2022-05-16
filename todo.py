from flask import request
from flask_restx import Resource, Api, Namespace, fields
from flask_cors import CORS, cors_origin


todos = {}
count = 1


Todo = Namespace(
    name="Todos",
    description="Todo 리스트를 작성하기 위해 사용하는 API.",
)

todo_fields = Todo.model('Todo', {  
    'data': fields.String(description='a Todo', required=True, example="what to do")
})

todo_fields_with_id = Todo.inherit('Todo With ID', todo_fields, {
    'todo_id': fields.Integer(description='a Todo ID')
})

@Todo.route('')
class TodoPost(Resource):
    @Todo.expect(todo_fields)
    @Todo.response(201, 'Success', todo_fields_with_id)
    def post(self):
        """Todo 리스트에 할 일을 등록"""
        global count
        global todos
        
        idx = count
        count += 1
        todos[idx] = request.json.get('data')
        
        return {
            'todo_id': idx,
            'data': todos[idx]
        }, 201

@Todo.route('/<int:todo_id>')
@Todo.doc(params={'todo_id': 'An ID'})
class TodoSimple(Resource):
    @Todo.response(200, 'Success', todo_fields_with_id)
    @Todo.response(400, 'Failed')
    def get(self, todo_id):
        """Todo 리스트에 todo_id와 일치하는 ID를 가진 할 일을 불러옴(조회)"""
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }
    
    @Todo.response(202, 'Success', todo_fields_with_id)
    @Todo.response(400, 'Failed')
    def put(self, todo_id):
        """Todo 리스트에 todo_id와 일치하는 ID를 가진 할 일을 수정"""
        todos[todo_id] = request.json.get('data')
        return {
            'todo_id': todo_id,
            'data': todos[todo_id]
        }, 202
    
    @Todo.doc(responses={202: 'Success'})
    @Todo.doc(responses={400: 'Failed'})
    def delete(self, todo_id):
        """Todo 리스트에 todo_id와 일치하는 ID를 가진 할 일을 삭제"""
        del todos[todo_id]
        return {
            "delete" : "success"
        }, 202

CORS(app)
