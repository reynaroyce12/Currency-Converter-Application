from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

parameters = {
    'access_key': 'e2547a7ff36d5eec4d5ff39c0a79ceff'
}

response = requests.get(url='http://api.exchangeratesapi.io/v1/latest', params=parameters)
data = response.json()
currency_rates = data['rates']


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/currency', methods=['POST'])
def get_details():
    try:
        fr_country = request.form['fr_country'].upper()
        to_country = request.form['to_country'].upper()
        user_amount = request.form['amount']
        from_amount = currency_rates[to_country] / currency_rates[fr_country]
        exchanged_rate = float(user_amount) * from_amount
        return render_template('currency.html', fr_country=fr_country, to_country=to_country, amount=user_amount,
                               converted=round(exchanged_rate, 2))
    except:
        return render_template('404.html')
