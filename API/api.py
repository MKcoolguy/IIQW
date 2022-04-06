from flask import Flask, Response, request
from flask_restful import Api, Resource
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

## Connect to DB ##
CONNECTION_STRING = "mongodb+srv://quotes_admin:fddyzyaqwMaTHQiR@quotes.ssb9s.mongodb.net/quotes.famous?retryWrites=true&w=majority"

try:
    client = pymongo.MongoClient(CONNECTION_STRING)
    client.server_info()
    db = client.quotes
    print("CONNECTED to DB.")
except:
    print("ERROR - Cannot connect to DB!!")


## Flask_Restful API ##

class QuotesByName(Resource):
    def get(self, author):
        query = { "author": author }
        # quotes = list(db.famous.find({}, {"_id": 0, "author": 1, "text": 1, "category": 1}))
        quotes = list(db.famous.find(query, {"_id": 0, "author": 1, "text": 1, "category": 1}))
        return Response(
            response= json.dumps(quotes),
            status=200,
            mimetype="application/json"
        )



api.add_resource(QuotesByName, "/quotes/<string:author>")

if __name__ == "__main__":
    app.run(port=5500, debug=True)



