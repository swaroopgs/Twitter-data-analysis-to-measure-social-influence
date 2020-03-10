from flask import Flask
from flask_restplus import Api, Resource
from apis.twitterapi import get_tweets, get_retweets

app = Flask(__name__)
api = Api(app=app)


# api to show up 10 twitter results
@api.route("/tweets/")
class Tweets(Resource):
    def get(self):
        return get_tweets(100)


@api.route("/retweets/<id>")
class Retweets(Resource):
    def get(self, id):
        return get_retweets(id)


if __name__ == '__main__':
    app.run(debug=True)
