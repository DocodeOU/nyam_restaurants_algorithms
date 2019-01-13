from django.test import TestCase


# Create your tests here.
from prices_and_names_module.pizziamo_net.prices import price_pizza


class PricePizziamoTestCase(TestCase):
    def setUp(self):
        pass
    
    def test_pizza_menu(self):
        pizza = {
            'ingredients': [{
                'price': 1,
                'quantity': 2
            }]
        }
        pizza_menu = {
            'price': 2
        }
        self.assertEqual(price_pizza(pizza=pizza, pizzas_in_cart=[pizza]), 3)
