from ..abstract_database import AbstractDatabase
from ..models import Consts, Pizza, Drink, Dessert, Ingredient, PizzaOption


class DatabasePizziamoNet(AbstractDatabase):
    
    def __init__(self, json):
        consts = Consts(json=json['consts'])
        pizzas = [Pizza(json=x) for x in json['pizzas']]
        drinks = [Drink(json=x) for x in json['drinks']]
        desserts = [Dessert(json=x) for x in json['desserts']]
        ingredients = [Ingredient(json=x) for x in json['ingredients']]
        pizza_options = [PizzaOption(json=x) for x in json['pizza_options']]
        
        super().__init__(consts=consts, pizzas=pizzas, drinks=drinks, desserts=desserts, ingredients=ingredients,
                         pizza_options=pizza_options)
