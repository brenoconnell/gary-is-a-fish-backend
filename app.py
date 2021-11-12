from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

import credentials

app = Flask(__name__)
CORS(app)

creds = credentials.Credentials.get_creds()

mongoURI = f"mongodb+srv://{creds[0]}:{creds[1]}@gary-sandbox.b1jde.mongodb.net/{creds[2]}?retryWrites=true&w=majority&authSource=admin"

client = MongoClient(mongoURI)
db = client.test_drink

@app.route("/drink", methods=['GET'])
@cross_origin(origin='http://localhost:3000')
def get_all_drinks():
    documents = db.drinks.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    resp = jsonify(output)
    return resp

@app.route("/drink/<id>", methods=['GET'])
@cross_origin(origin='http://localhost:3000')
def get_drink_by_id(id):
    document = db.drinks.find_one({"id": id})
    output = {item: document[item] for item in document if item != '_id'}
    resp = jsonify(output)
    return resp

@app.route("/drink", methods=['POST'])
@cross_origin(origin='http://localhost:3000')
def post_new_drink():
    content = request.get_json(force=True)
    result = db.drinks.insert_one(content)
    if result.acknowledged:
        resp = jsonify( {"status": 200, "message": "OK"} )
    else:
        resp = jsonify( {"status": 500, "message": "MongoDB error"} )

    return resp

@app.route("/drink", methods=['PUT'])
@cross_origin(origin='http://localhost:3000')
def update_drink():
    content = request.get_json(force=True)
    document = db.drinks.find_one({"id": content['id']})
    new_data = {'$set': content}

    result = db.drinks.update_one(document, new_data)
    if result.acknowledged:
        resp = jsonify( {"status": 200, "message": "OK"} )
    else:
        resp = jsonify( {"status": 500, "message": "MongoDB error"} )
    return resp

@app.route("/drink/<id>", methods=['DELETE'])
@cross_origin(origin='http://localhost:3000')
def delete_drink(id):
    result = db.drinks.delete_one({"id": id})
    if result.acknowledged:
        resp = jsonify( {"status": 200, "message": "OK"} )
    else:
        resp = jsonify( {"status": 500, "message": "MongoDB error"} )
    return resp
