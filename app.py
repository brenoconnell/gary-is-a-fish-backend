from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://test:test@gary-sandbox.b1jde.mongodb.net/test\%5fdrink?retryWrites=true&w=majority&authSource=admin")
db = client.test_drink

@app.route("/drink", methods=['GET'])
def get_all_drinks():
    documents = db.drinks.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    resp = jsonify(output)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/drink/<id>", methods=['GET'])
def get_drink_by_id(id):
    
    document = db.drinks.find_one({"id": id})
    output = {item: document[item] for item in document if item != '_id'}

    resp = jsonify(output)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/drink", methods=['POST'])
def post_new_drink():
    content = request.get_json(force=True)

    result = db.drinks.insert_one(content)

    resp = jsonify( {"status": 200, "message": f"OK - New ID: {result.inserted_id}"} )
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
