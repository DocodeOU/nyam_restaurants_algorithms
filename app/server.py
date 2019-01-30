import json
import sys

from flask import Flask, request
from flask_cors import CORS, cross_origin

# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
sys.path.append("..")

from nyam_restaurants_algorithms.app.models import Pizza
from nyam_restaurants_algorithms.pizziamo_net.database import DatabasePizziamoNet
from nyam_restaurants_algorithms.pizziamo_net.names import NamesPizziamoNet
from nyam_restaurants_algorithms.pizziamo_net.prices import PricesPizziamoNet

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/pizza", methods=['POST'])
@cross_origin()
def getPizzaNamePrice():
    data = request.get_json()
    pizzeria = data['pizzeria']
    menu = data['menu']
    pizza = Pizza(json=data['pizza'])
    if pizzeria == 'docode.it':
        name = 'ciao'
        price = 2
        
    elif pizzeria == 'pizziamo.net':
        database = DatabasePizziamoNet(json=menu)
        names_algs = NamesPizziamoNet(database=database, use_business_software_algs=True)
        name = (names_algs.name_of_pizza(pizza=pizza))
        prices_algs = PricesPizziamoNet(database=database, use_business_software_algs=True)
        price = prices_algs.price_pizza(pizza=pizza)
    else:
        name = None
        price = None
    return json.dumps({'name': name, 'price': price})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
