from typing import List


class Ingredient:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']
        self.quantity: float = json['quantity']


class PizzaOption:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']


class Pizza:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']
        self.ingredients: List[Ingredient] = [Ingredient(json=x) for x in json['ingredients']]
        self.pizza_options: List[PizzaOption] = [PizzaOption(json=x) for x in json['pizza_options']]
        self.type: int = json['type']
        self.key_without_pizza_options: str = json['key_without_pizza_options']
        self.quantity: int = json['quantity']


class Drink:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']


class Dessert:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']


class DeliveryType:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']


class TypeOfPizza:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']


class Consts:
    def __init__(self, json):
        self.ingredient_mozzarella: int = json['ingredient_mozzarella']
        self.ingredient_pomodoro: int = json['ingredient_pomodoro']
