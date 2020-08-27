from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class Coin(Resource):
    def get(self, coin):
        """
        method which retrieves the information for a coin
        from the data file stored locally ./data.txt

        params:
            string coin: the name of the coin
        """
        with open("data.txt") as data_file:
            coins = json.load(data_file)
            coins = json.loads(coins)
        try:
            body = coins[coin]
        except:
            body = {
                "error" : "invalid symbol " + coin
            }
            return body, 400
        return body

api.add_resource(Coin, '/getCoinInfo/<coin>')

if __name__ == '__main__':
    app.run(port=8000)
