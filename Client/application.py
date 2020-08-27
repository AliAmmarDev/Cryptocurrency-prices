from flask import Flask, render_template, url_for, request, redirect
import time
import requests
import json

app = Flask(__name__)
endpoints = {
    "coin" : "http://localhost:8000/getCoinInfo/",
    "prices" : "https://api.coinstats.app/public/v1/charts?period=1m&coinId=",
    "charts" : "https://quickchart.io/chart/create"
}

def getCoin(coin):
    """
    Gets the information of a cryptocurrency.

    params:
        String coin: string containing name of a cryptocurrency.

    returns:
        dictionary body: dictionary containing information
            of a cryptocurrency.
    """
    url = endpoints["coin"]
    url += coin
    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    body = json.loads(response.text)
    return body

def getPrices(id):
    """
    Gets the price history of a cryptocurrency.

    params:
        Int id: id of a cryptocurrency.

    returns:
        body: dictionary containing price
            information for the past 31 days.
    """
    url = endpoints["prices"]
    url += id
    try:
        response = requests.get(url)
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    body = json.loads(response.text)
    return body

def getChart(prices):
    """
    Generates a chart for given data.

    params:
        Int[] prices: array containing price information
            of a cryptocurrency.

    returns:
        body: dictionary containing price
            information for the past 31 days.
    """
    url = endpoints["charts"]
    xaxis, yaxis = [], []
    for price in prices:
        date = time.ctime(price[0]).split()
        date = date[1] + " " + date[2]
        xaxis.append(date)
        yaxis.append(price[1])

    data = {
        "chart": {
            "type": "bar",
            "data": {
                "labels":xaxis,
                "datasets": [{
                    "label": "price ($)", "data": yaxis, "backgroundColor":'#8000ff'
                }]
            }
        }
    }
    data = json.dumps(data)
    try:
        response = requests.post(
            'https://quickchart.io/chart/create',
            headers={
                "Content-Type": "application/json",
            },
            data=data
        )
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)
    body = json.loads(response.text)
    return body

def getLatestPrice(prices):
    """
    Gets the latest price from the historical price dataset.

    params:
        list prices: price history dating back 31 days.

    returns:
        int latest_price: latest price of a coin.
    """
    latest_data = prices[-1]
    latest_price = latest_data[1]
    return latest_price

@app.route('/comare/<coin_one>/<coin_two>')
def compare(coin_one, coin_two):
    """
    Serves the page for comparing two coins.
    params:
        string coin_one: the first coin that the user selected.
        string coin_two: the second coin that the user selected.
    returns:
        compare.html: template for the compare page.

    """

    coin_one = getCoin(coin_one)
    coin_two = getCoin(coin_two)

    coin_one_id = coin_one["id"]
    coin_two_id = coin_two["id"]

    coin_one_prices = getPrices(coin_one_id)
    coin_two_prices = getPrices(coin_two_id)
    coin_one_chart = getChart(coin_one_prices["chart"])
    coin_two_chart = getChart(coin_two_prices["chart"])

    one = {
        "name" : coin_one["name"],
        "symbol" : coin_one["symbol"],
        "logo" : coin_one["logo"],
        "price" : getLatestPrice(coin_one_prices["chart"]),
        "chart" : coin_one_chart["url"]
    }
    two = {
        "name" : coin_two["name"],
        "symbol" : coin_two["symbol"],
        "logo" : coin_two["logo"],
        "price" : getLatestPrice(coin_two_prices["chart"]),
        "chart" : coin_two_chart["url"]
    }

    return render_template("compare.html", one = one, two = two)

@app.route('/', methods = ['GET','POST'])
def index():
    """
    Serves the home page of the application.
    returns:
        index.html: template for home page.
    """
    if request.method == 'POST':
        coin_one = request.form.get("coin_one")
        coin_two = request.form.get("coin_two")
        return redirect(url_for('compare', coin_one=coin_one, coin_two=coin_two))
    else:
        location = None
    return render_template("index.html")



if __name__ == '__main__':
    app.run(port=5000)
