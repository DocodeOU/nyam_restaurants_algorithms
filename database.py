from typing import List

from models import Consts, Pizza, Drink, Dessert, Ingredient, PizzaOption, DeliveryType, TypeOfPizza


class AbstractDatabase:
    def __init__(self, consts: Consts, pizzas: List[Pizza], drinks: List[Drink], desserts: List[Dessert],
                 ingredients: List[Ingredient], pizza_options: List[PizzaOption], delivery_types: List[DeliveryType],
                 types_of_pizzas: List[TypeOfPizza]):
        self.consts = consts
        self.pizzas = pizzas
        self.drinks = drinks
        self.desserts = desserts
        self.ingredients = ingredients
        self.pizza_options = pizza_options
        self.delivery_types = delivery_types
        self.types_of_pizzas = types_of_pizzas
        
        self.delivery_type_home = next(x for x in delivery_types if x.name == 'Domicilio')
        self.type_pizza = next(x for x in types_of_pizzas if x.name == 'Domicilio')
        self.type_cecio = next(x for x in types_of_pizzas if x.name == 'Cecio')
