from flask import Flask, Response, request
from flask_restful import Api, Resource, reqparse
import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)
api = Api(app)

## Connect to DB ##
CONNECTION_STRING = "mongodb+srv://quotes_admin:fddyzyaqwMaTHQiR@quotes.ssb9s.mongodb.net/quotes?retryWrites=true&w=majority"

try:
    client = pymongo.MongoClient(CONNECTION_STRING)
    client.server_info()
    db = client.quotes
    print("CONNECTED to DB.")
except:
    print("ERROR - Cannot connect to DB!!")


## Flask_Restful API ##

# Get quotes by author name
class QuotesByName(Resource):
    def get(self, author):
        query = { "author": author }
        quotes = list(db.famous.find(query, {"_id": 0, "author": 1, "text": 1, "category": 1}))
        return Response(
            response= json.dumps(quotes),
            status=200,
            mimetype="application/json"
        )

class QuotesByCategory(Resource):
    def get(self, category):
        query = { "category": category }
        quotes = list(db.famous.find(query, {"_id": 0, "author": 1, "text": 1, "category": 1}))
        return Response(
            response= json.dumps(quotes),
            status=200,
            mimetype="application/json"
        )


# Get quotes by keyword search
class QuotesByKeyword(Resource):

    def get(self):
        words = ["love"]
        search = ''
        for word in words:
            search += '\\\"' + word + '\\\"'  
        print(search)

        # query = { "$and" : [{ "text" : { "$regex" : "love" }}, { "text" : { "$regex" : "age" }}]}
        # quotes = list(db.famous.find(query, {"_id": 0, "author": 1, "text": 1, "category": 1}))
        # quotes = list(db.famous.find({ "$text": { "$search" : '\"love\"'}},{"_id": 0, "author": 1, "text": 1, "category": 1}))
        quotes = list(db.famous.find({ "$text": { "$search" : search }},{"_id": 0, "author": 1, "text": 1, "category": 1}))
        response = Response(
            response= json.dumps(quotes),
            status=200,
            mimetype="application/json"
        )
        return response

api.add_resource(QuotesByName, "/quotesbyauthor/<string:author>")
api.add_resource(QuotesByKeyword, "/quotesbykeyword/")
api.add_resource(QuotesByCategory, "/quotesbycategory/<string:category>")


if __name__ == "__main__":
    app.run(port=5500, debug=True)