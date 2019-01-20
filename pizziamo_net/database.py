from app.abstract_database import AbstractDatabase
from app.models import Consts, Pizza, Ingredient, PizzaOption


class DatabasePizziamoNet(AbstractDatabase):
    
    def __init__(self, json):
        consts = Consts(json=json['consts'])
        pizzas = [Pizza(json=x) for x in json['pizzas']]
        ingredients = [Ingredient(json=x) for x in json['ingredients']]
        pizza_options = [PizzaOption(json=x) for x in json['pizza_options']]
        
        super().__init__(consts=consts, pizzas=pizzas, ingredients=ingredients,
                         pizza_options=pizza_options)
