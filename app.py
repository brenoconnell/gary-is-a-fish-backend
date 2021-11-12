from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

from credentials import username, pwd, dbname

app = Flask(__name__)
CORS(app)

mongoURI = f"mongodb+srv://{username}:{pwd}@gary-sandbox.b1jde.mongodb.net/{dbname}?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(mongoURI)
db = client.test_drink

@app.route("/drink", methods=['GET'])
@cross_origin(origin='http://localhost:3000')
def get_all_drinks():
    documents = db.drinks.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    resp = jsonify(output)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/drink/<id>", methods=['GET'])
@cross_origin(origin='http://localhost:3000')
def get_drink_by_id(id):
    
    document = db.drinks.find_one({"id": id})
    output = {item: document[item] for item in document if item != '_id'}

    resp = jsonify(output)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/drink", methods=['POST'])
@cross_origin(origin='http://localhost:3000')
def post_new_drink():
    content = request.get_json(force=True)

    result = db.drinks.insert_one(content)

    resp = jsonify( {"status": 200, "message": "OK"} )
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/drink", methods=['PUT'])
@cross_origin(origin='http://localhost:3000')
def update_drink():
    content = request.get_json(force=True)

    document = db.drinks.find_one({"id": content['id']})
    new_data = {'$set': content}

    result = db.drinks.update_one(document, new_data)

    resp = jsonify( {"status": 200, "message": "OK"} )
    return resp

@app.route("/drink/<id>", methods=['DELETE'])
@cross_origin(origin='http://localhost:3000')
def delete_drink(id):

    result = db.drinks.delete_one({"id": id})

    resp = jsonify( {"status": 200, "message": "OK"} )
    return resp
