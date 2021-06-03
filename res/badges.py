
from flask import jsonify, request
from flask_restful import Resource, abort
from flask_pymongo import pymongo
from bson.json_util import dumps, ObjectId
from pymongo import results
from werkzeug.wrappers import response
import db_config as database

class Badges(Resource):
    "get all badges"
    def get(self):
        response = list(database.db.Badges.find())
        for doc in response:
            doc['_id'] = str(doc['_id'] )
        return jsonify(response)
    
    def post(self):
        _ids = list(database.db.Badges.insert_many([
            {
                'header_url': request.json[8]['header_url'],
                'picture': request.json[8]['picture'],
                'name': request.json[8]['name'],
                'age': request.json[8]['age'],
                'city': request.json[8]['city'],
                'followers': request.json[8]['followers'],
                'likes': request.json[8]['likes'],
                'post': request.json[8]['post'],
            }
        ]).inserted_ids)

        results = []
        for _id in _ids:
            results.append(str(_id))

            return jsonify({'inserted_ids': results})

    def delete(self):
        return database.db.Badges.delete_many({}).deleted_count

        