from email.quoprimime import quote
from flask import Flask, Response, request
from flask_restful import Api, Resource, reqparse
import pymongo
import json
from bson.objectid import ObjectId

import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
import pickle

app = Flask(__name__)
api = Api(app)

## Connect to DB ##
#CONNECTION_STRING = "mongodb+srv://quotes_admin:fddyzyaqwMaTHQiR@quotes.ssb9s.mongodb.net/quotes?retryWrites=true&w=majority"
CONNECTION_STRING = "mongodb+srv://matteo:VAFC2VKyMK0XAqdH@quotes.ssb9s.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

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

class OneQuote(Resource):
    def get(self):
        query = { "author": "Mark Twain" }
        quotes = list(db.famous.find(query, {"_id": 0, "author": 1, "text": 1, "category": 1}).limit(1))
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


# Return AI generated quote #
class RandomGeneratedQuote(Resource):
    def get(self, string):
        model = load_model(os.path.join("API\models", "quote_model.h5"))
        with open('API\models/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        max_sequence_len = 65
        seed_text = string
        next_words = 20

        for _ in range(next_words):
            token_list = tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
            predicted = np.argmax(model.predict(token_list), axis=-1)
            output_word = ""
            for word, index in tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            seed_text += " " + output_word
        print(seed_text)
        quote = {"_id":0, "author": "user", "text": seed_text}
        response = Response(
            response= json.dumps(seed_text),
            status=200,
            mimetype="application/json"
        )
        return seed_text


# Add api resources #
api.add_resource(QuotesByName, "/quotesbyauthor/<string:author>")
api.add_resource(QuotesByKeyword, "/quotesbykeyword/")
api.add_resource(QuotesByCategory, "/quotesbycategory/<string:category>")
api.add_resource(OneQuote, "/onequote/")
api.add_resource(RandomGeneratedQuote, "/random/<string:string>")


# Function to add quotes to db
def add_user_quote(user_name, quote):
    user_collection = db["users"]
    post = {"user": user_name, "quote": quote}
    user_collection.insert_one(post)

# Function generate ai quote
def get_ai_quote(my_text):
    my_quote = RandomGeneratedQuote()
    return my_quote.get(my_text)

# Function to get a random quote
def get_random_quote():
    famous_collection = db['famous']
    quotes = famous_collection.aggregate([ { "$sample": { "size": 1 } } ])
    quote_set = {}
    for quote in quotes:
        text = quote['text']
        author = quote['author']
        quote_set[text] = author
    return quote_set