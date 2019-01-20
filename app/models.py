from typing import List


class Ingredient:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']
        self.quantity: int = json['quantity'] if 'quantity' in json else 1
        self.cooked_in_oven_by_default: bool = json['cooked_in_oven_by_default']
        self.uscita: bool = json['uscita'] if 'uscita' in json else not self.cooked_in_oven_by_default
        self.just_a_little: bool = json['just_a_little'] if 'just_a_little' in json else False


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
        self.quantity: int = json['quantity'] if 'quantity' in json else 1
    
    @property
    def key_without_pizza_options(self):
        return None


# class Drink:
#     def # __init__(self, json):
#         self.id: int = json['id']
#         self.name: str = json['name']
#         self.price: float = json['price']
#
#
# class Dessert:
#     def __init__(self, json):
#         self.id: int = json['id']
#         self.name: str = json['name']
#         self.price: float = json['price']


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
