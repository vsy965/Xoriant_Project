from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify, make_response
import json

db = client['Bankdb']

collection = db['bankacc']

user_data = {"_id": 1001,
             "name": "raj",
             "age": 27,
             "gender": "male",
             "phone": 123456789,
             "email": "raj@gmail.com"}
# print(type(user_data))
# collection.insert_one(user_data)

@app.route("/enter_data", methods = ["POST"])
def add_user():
    req = request.get_json()
    data = collection.find()
    y = [ each_rec for each_rec in data if req["_id"] == each_rec["_id"] ]
    if y:
        res = make_response({"Error": "Id already present"}, 406)
        return res
    if isinstance(req, type(user_data)):
        collection.insert_one(req)
        res = make_response({"msg": "collection Added"}, 201)
        return res
    else:
        res = make_response({"error": "Provide valid data"}, 406)

@app.route("/get_user/<id>", methods = ["GET"])
def get_user(id):
    user = collection.find_one({"_id": int(id)})
    if user:
        res = make_response(jsonify(user))
        return res
    else:
        res = make_response({"error": "User not found"}, 404)
        return res


@app.route("/update_record/<id>", methods = ["PUT"])
def update_record(id):
    data = request.get_json()
    user_present = collection.find_one({"_id": int(id)})
    if user_present:
        new = {"$set": data}
        collection.update_one({"_id": int(id)}, new)
        res = make_response({"msg": "Data updated"}, 200)
        return res
    else:
        res = make_response({"error": "Enter valid user Id"}, 404)
        return res

@app.route("/delete_record/<id>", methods = ["DELETE"])
def delete_record(id):
    user = collection.find_one({"_id": int(id)})
    if user:
        collection.delete_one({"_id": int(id)})
        res = make_response({"msg": "Record deleted"}, 200)
        return res
    else:
        res = make_response({"error": "Record not found"}, 404)
        return res


@app.route("/show_all", methods = ["GET"])
def all_records():
    data = collection.find()
    for rec in data:
        yield make_response(jsonify(rec), 200)


    return make_response({"msg": "record completed"})



