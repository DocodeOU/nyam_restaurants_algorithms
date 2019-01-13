from typing import List


class IngredientFromJson:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']
        self.quantity: float = json['quantity']


class PizzaOptionFromJson:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']


class PizzaFromJson:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']
        self.ingredients: List[IngredientFromJson] = [IngredientFromJson(json=x) for x in json['ingredients']]
        self.pizza_options: List[PizzaOptionFromJson] = [PizzaOptionFromJson(json=x) for x in json['pizza_options']]
        self.type: int = json['type']
        self.key_without_pizza_options: str = json['key_without_pizza_options']
        self.quantity: int = json['quantity']
