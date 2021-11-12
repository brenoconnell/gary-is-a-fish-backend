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
    # f = open('allDrinks.json',)
    # allDrinks = json.load(f)
    # f.close()
    documents = db.drinks.find()
    output = [{item: data[item] for item in data if item != '_id'} for data in documents]
    resp = jsonify(output)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/drink/<id>", methods=['GET'])
def get_drink_by_id(id):
    f = open('allDrinks.json',)
    allDrinks = json.load(f)
    f.close()
    respDrink = None

    for drink in allDrinks:
        for attribute, value in drink.items():
            if(attribute == "id" and value == id):
                respDrink = drink
                break
    
    if(not respDrink == None):
        resp = jsonify(respDrink)
    else:
        resp = jsonify()
    
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/drink", methods=['POST'])
def post_new_drink():
    content = request.get_json(force=True)
    # json_object = json.dumps(content, indent = 4)

    # fin = open("allDrinks.json", "rt")
    # data = fin.read()
    # data = data.replace(']', '')
    # fin.close()

    # fin = open("allDrinks.json", "wt")
    # fin.write(data)
    # fin.close()

    # with open("allDrinks.json", "a+") as outfile:
    #     outfile.write(",\n" + json_object + "\n]")
    # outfile.close()

    result = db.drink.insert_one(content)

    resp = jsonify( {"status": 200, "message": f"OK - New ID: {result.inserted_id}"} )
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/drink/<id>", methods=['DELETE'])
@cross_origin(origin='http://localhost:3000')
def delete_drink(id):

    f = open('allDrinks.json',)
    allDrinks = json.load(f)
    indexToRemove = -1
    for i in range(len(allDrinks)):
        if(allDrinks[i]['id'] == id):
            indexToRemove = i
            break
    if(not indexToRemove > -1):
        resp = jsonify( {"status": 404, "message": "File not found"} )
        return resp

    allDrinks.pop(indexToRemove)
    f.close()
    f = open('allDrinks.json', 'w')
    f.write(json.dumps(allDrinks, sort_keys=True, indent=4, separators=(',', ': ')))
    f.close()

    resp = jsonify( {"status": 200, "message": "OK"} )
    return resp
