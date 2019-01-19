from database import AbstractDatabase
from models import Consts, Pizza, Drink, Dessert, Ingredient, PizzaOption, DeliveryType, TypeOfPizza


class DatabasePizziamoNet(AbstractDatabase):
    
    def __init__(self):
        consts = Consts(json={
            "ingredient_pomodoro": 48,
            "ingredient_mozzarella": 49
        })
        pizzas = [Pizza(json=x) for x in []]
        drinks = [Drink(json=x) for x in []]
        desserts = [Dessert(json=x) for x in []]
        ingredients = [Ingredient(json=x) for x in []]
        pizza_options = [PizzaOption(json=x) for x in []]
        delivery_types = [DeliveryType(json=x) for x in []]
        types_of_pizzas = [TypeOfPizza(json=x) for x in []]
        
        super().__init__(consts=consts, pizzas=pizzas, drinks=drinks, desserts=desserts, ingredients=ingredients,
                         pizza_options=pizza_options, delivery_types=delivery_types, types_of_pizzas=types_of_pizzas)
