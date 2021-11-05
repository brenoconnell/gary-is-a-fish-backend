from flask import Flask, jsonify, request
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route("/drink", methods=['GET'])
def get_all_drinks():
    f = open('allDrinks.json',)
    allDrinks = json.load(f)
    f.close()
    resp = jsonify(allDrinks)
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
    json_object = json.dumps(content, indent = 4)

    fin = open("allDrinks.json", "rt")
    data = fin.read()
    data = data.replace(']', '')
    fin.close()

    fin = open("allDrinks.json", "wt")
    fin.write(data)
    fin.close()

    with open("allDrinks.json", "a+") as outfile:
        outfile.write(",\n" + json_object + "\n]")
    outfile.close()

    resp = jsonify( {"status": 200, "message": "OK"} )
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

# @app.route("/getAllDrinks", methods=['GET'])
# def get_all_drinks_json():
#     f = open('allDrinks.json',)
#     allDrinks = json.load(f)
#     f.close()
#     resp = jsonify(allDrinks)
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/postNewDrink", methods=['POST'])
# def post_new_drink_json():

#     content = request.get_json(force=True)
#     json_object = json.dumps(content, indent = 4)

#     fin = open("allDrinks.json", "rt")
#     data = fin.read()
#     data = data.replace(']', '')
#     fin.close()

#     fin = open("allDrinks.json", "wt")
#     fin.write(data)
#     fin.close()

#     with open("allDrinks.json", "a+") as outfile:
#         outfile.write(",\n" + json_object + "\n]")
#     outfile.close()

#     resp = jsonify( {"status": 200, "message": "OK"} )
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/removeDrink", methods=['POST'])
# def remove_drink_json():

#     content = request.get_json(force=True)
#     print(content)

#     f = open('allDrinks.json',)
#     allDrinks = json.load(f)
#     indexToRemove = -1
#     for i in range(len(allDrinks)):
#         if(allDrinks[i]['id'] == content['drinkID']):
#             indexToRemove = i
#             break
#     if(not indexToRemove > -1):
#         resp = jsonify( {"status": 404, "message": "File not found"} )
#         resp.headers['Access-Control-Allow-Origin'] = '*'
#         return resp

#     allDrinks.pop(indexToRemove)
#     f.close()
#     f = open('testMe.json', 'w')
#     f.write(json.dumps(allDrinks, sort_keys=True, indent=4, separators=(',', ': ')))
#     f.close()

#     resp = jsonify( {"status": 200, "message": "OK"} )
#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp

# @app.route("/postNewDrinkTest", methods=['POST'])
# def post_new_drink_test_json():

    # content = request.get_json(force=True)
    # print(content)

    # json_object = json.dumps(content, indent = 4)

    # fin = open("testMe.json", "rt")
    # data = fin.read()
    # data = data.replace(']', '')
    # fin.close()

    # fin = open("allDrinks.json", "wt")
    # fin.write(data)
    # fin.close()

    # with open("allDrinks.json", "a+") as outfile:
    #     outfile.write(",\n" + json_object + "\n]")
    # outfile.close()

    # resp = jsonify( {"status": 200, "message": "OK"} )
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    # return resp