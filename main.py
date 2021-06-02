from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
from werkzeug.wrappers import response
import db_config as database 

app=Flask(__name__)
api=Api(app)

""" 
    database.db.Badge.
    .database is the config file
    .db is the database name
    .collectionName the next part is the collection
"""

class Test(Resource):
    def  get(self):
        return jsonify({"message": "Test ok, you are ok"})

class Badge(Resource):
    def post(self):
        database.db.Users.insert_one({
            'Header_P': request.json["Header_P"],
            'picture': request.json["picture"],
            'name':request.json["name"],
            'age':request.json["age"],
            'city':request.json["city"],
            'followers':request.json["followers"],
            'likes':request.json["likes"],
            'post':request.json["post"],
        })

class AllBadge(Resource):
    def get(self):
        pass

api.add_resource(Badge,'/new/')
api.add_resource(Test,'/test/')

@app.route('all/adults')
def get_kids():
    response = list(database.db.Badges.find({'age':{"$gte": 25}}))
    for document in response:
        document["_id"] = str(document["_id"])
        return jsonify(response)


@app.route('all/kids')
def get_kids():
    response = list(database.db.Badges.find({'age':{"$gte": 10}}))
    for document in response:
        document["_id"] = str(document["_id"])
        return jsonify(response)

if __name__ == "__main__":
    app.run(load_dotenv=True)