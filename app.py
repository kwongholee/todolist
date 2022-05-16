from flask import Flask
from flask_restx import Resource, Api
from todo import Todo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(
    app,
    version='0.1',
    title="API Server",
    description="Todo API Server!",
    terms_url="/",
    contact="ghlee9883@khu.ac.kr",
    license="MIT"
)

api.add_namespace(Todo, '/todos')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
    
CORS(app)
