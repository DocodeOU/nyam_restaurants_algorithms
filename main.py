import sys
import time
import json


def main(argv):
    start_time = time.time()
    # your code
    tmp_data_file = argv[1]
    app_data_file = argv[2]
    with open(app_data_file) as d:
        with open(tmp_data_file) as f:
            order_data = json.load(f)
            app_data = json.load(d)
            pizzeria = order_data['pizzeria']
            operation = order_data['operation']

            if pizzeria == 'docode.it':
                print(time.time() - start_time)
            elif pizzeria == 'pizziamo.net':
                from nyam_restaurants_algorithms.pizziamo_net.database import DatabasePizziamoNet
                database = DatabasePizziamoNet(json={})
                if operation == 'pizza_name':
                    from nyam_restaurants_algorithms.pizziamo_net.names import NamesPizziamoNet
                    names_algs = NamesPizziamoNet(database=database)
                    print('Margherita')
                elif operation == 'pizza_price':
                    from nyam_restaurants_algorithms.pizziamo_net.prices import PricesPizziamoNet
                    prices_algs = PricesPizziamoNet(database=database)
                    print('3.0')


if __name__ == "__main__":
    main(sys.argv)
