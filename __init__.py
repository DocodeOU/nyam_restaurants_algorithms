import sys

import json


def main(argv):
    json_args = json.loads(argv[1])
    pizzeria = json_args['pizzeria']
    operation = json_args['operation']
    if pizzeria == 'docode.it':
        print('Ciaoonnee')
    elif pizzeria == 'pizziamo.net':
        from pizziamo_net.database import DatabasePizziamoNet
        database = DatabasePizziamoNet(json={})
        if operation == 'pizza_name':
            from pizziamo_net.names import NamesPizziamoNet
            names_algs = NamesPizziamoNet(database=database)
            print('Margherita')
        elif operation == 'pizza_price':
            from pizziamo_net.prices import PricesPizziamoNet
            prices_algs = PricesPizziamoNet(database=database)
            print('3.0')


if __name__ == "__main__":
    main(sys.argv)
