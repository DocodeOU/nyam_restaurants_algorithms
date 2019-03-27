import json
import sys

from flask import Flask, request
from flask_cors import CORS, cross_origin

# https://stackoverflow.com/questions/30669474/beyond-top-level-package-error-in-relative-import
sys.path.append("..")

from nyam_restaurants_algorithms.app.sentry_dsn import SENTRY_DSN
from nyam_restaurants_algorithms.app.models import Pizza, CartItemPizza
from nyam_restaurants_algorithms.pizziamo_net.database import DatabasePizziamoNet
from nyam_restaurants_algorithms.pizziamo_net.names import NamesPizziamoNet
from nyam_restaurants_algorithms.pizziamo_net.prices import PricesPizziamoNet
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/pizza_name_and_price/", methods=['POST'])
@cross_origin()
def pizza_name_and_price():
    data = request.get_json()
    pizzeria = data['pizzeria']
    menu = data['menu']
    pizza = Pizza(json=data['pizza'])
    if pizzeria == 'docodeit':
        database = DatabasePizziamoNet(json=menu)
        names_algs = NamesPizziamoNet(database=database, use_business_software_algs=True)
        name = names_algs.name_of_pizza(pizza=pizza)
        name_formatted = names_algs.name_formatted(pizza=pizza, current_name=name)
        prices_algs = PricesPizziamoNet(database=database, use_business_software_algs=True)
        price = prices_algs.price_pizza(pizza=pizza)

    elif pizzeria == 'pizziamonet':
        database = DatabasePizziamoNet(json=menu)
        names_algs = NamesPizziamoNet(database=database, use_business_software_algs=True)
        name = names_algs.name_of_pizza(pizza=pizza)
        name_formatted = names_algs.name_formatted(pizza=pizza, current_name=name)
        prices_algs = PricesPizziamoNet(database=database, use_business_software_algs=True)
        price = prices_algs.price_pizza(pizza=pizza)
    else:
        raise Exception('wtf?')
    return json.dumps({'name': name, 'name_formatted': name_formatted, 'price': price})


@app.route("/extra_costs/", methods=['POST'])
@cross_origin()
def extra_costs():
    data = request.get_json()
    pizzeria = data['pizzeria']
    menu = data['menu']
    pizzas_in_cart = [CartItemPizza(json=x) for x in data['pizzas_in_cart']]
    delivery_type = data['delivery_type']
    if pizzeria == 'docodeit':
        database = DatabasePizziamoNet(json=menu)
        prices_algs = PricesPizziamoNet(database=database, use_business_software_algs=True)
        delivery_cost = prices_algs.delivery_cost(pizzas_in_cart=pizzas_in_cart, delivery_type=delivery_type)
    elif pizzeria == 'pizziamonet':
        database = DatabasePizziamoNet(json=menu)
        prices_algs = PricesPizziamoNet(database=database, use_business_software_algs=True)
        delivery_cost = prices_algs.delivery_cost(pizzas_in_cart=pizzas_in_cart, delivery_type=delivery_type)
    else:
        raise Exception('wtf?')
    return json.dumps({'delivery_cost': delivery_cost})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
