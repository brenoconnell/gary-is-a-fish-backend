from flask import Flask, jsonify, request
import json

app = Flask(__name__)

@app.route("/getAllDrinks", methods=['GET'])
def get_all_drinks_json():
    f = open('allDrinks.json',)
    allDrinks = json.load(f)
    f.close()
    resp = jsonify(allDrinks)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/postNewDrink", methods=['POST'])
def post_new_drink_json():

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

@app.route("/removeDrink", methods=['POST'])
def remove_drink_json():

    content = request.get_json(force=True)
    print(content)

    f = open('allDrinks.json',)
    allDrinks = json.load(f)
    indexToRemove = -1
    for i in range(len(allDrinks)):
        if(allDrinks[i]['id'] == content['drinkID']):
            indexToRemove = i
            break
    if(not indexToRemove > -1):
        resp = jsonify( {"status": 404, "message": "File not found"} )
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    allDrinks.pop(indexToRemove)
    f.close()
    f = open('testMe.json', 'w')
    f.write(json.dumps(allDrinks, sort_keys=True, indent=4, separators=(',', ': ')))
    f.close()

    resp = jsonify( {"status": 200, "message": "OK"} )
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/postNewDrinkTest", methods=['POST'])
def post_new_drink_test_json():

    content = request.get_json(force=True)
    print(content)

    json_object = json.dumps(content, indent = 4)

    fin = open("testMe.json", "rt")
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