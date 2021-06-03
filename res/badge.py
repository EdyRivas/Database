import re
from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import dumps, ObjectId
from werkzeug.wrappers import response
import db_config as database

class Badge(Resource):
    def get(self, by, data):
        response = self.abort_if_not_exist(by, data)
        response["_id"] = str(response['_id'])
        return jsonify(response)

    def post(self):
        _id = str(database.db.Users.insert_one({
            'Header_P': request.json["Header_P"],
            'picture': request.json["picture"],
            'name':request.json["name"],
            'age':request.json["age"],
            'city':request.json["city"],
            'followers':request.json["followers"],
            'likes':request.json["likes"],
            'post':request.json["post"],
        }).inserted_id)

        return jsonify({"_id": _id})
    
    def put(self, by, data):
        response= self.abort_if_not_exist(by, data)

        for key, value in request.json.items():
            response[key]=value 
        
        database.db.Users.insert_one({'_id':ObjectId(response['_id'])},
            {'$set':{
            'Header_P': response["Header_P"],
            'picture': response["picture"],
            'name':response["name"],
            'age':response["age"],
            'city':response["city"],
            'followers':response["followers"],
            'likes':response["likes"],
            'post':response["post"],
        }})

        response['_id'] = str(response['_id'])
        return jsonify(response)

    def delete(self, by, data):
        response = self.abort_if_not_exist(by, data)
        database.db.Badges.delete_one({'_id': response['_id']})
        response['_id'] = str(response['_id'])
        return jsonify({"deleted":response})

    def abort_if_not_exist(self,by,data):
        if by == "_id":
            response = database.db.Badges.find_one({"_id":ObjectId(data)})
        else: 
            response =database.db.Badges.find_one({f"{by}": data})

        if response:
            return response
        else: 
            abort(jsonify({"status":404, f"{by}":f"{data} not found"}))
    