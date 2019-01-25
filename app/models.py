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
        self.name_business_software_shortened: bool = json[
            'name_business_software_shortened'] if 'name_business_software_shortened' in json else ''


class PizzaOption:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']
        self.place_at_beggining_of_name: bool = json[
            'place_at_beggining_of_name'] if 'place_at_beggining_of_name' in json else False


class Pizza:
    def __init__(self, json):
        self.id: int = json['id'] if 'id' in json else None
        self.name: str = json['name'] if 'name' in json else None
        self.price: float = json['price'] if 'price' in json else None
        self.ingredients: List[Ingredient] = [Ingredient(json=x) for x in json['ingredients']]
        self.pizza_options: List[PizzaOption] = [PizzaOption(json=x) for x in
                                                 json['pizza_options']] if 'pizza_options' in json else []
        self.type: int = json['type']
        self.quantity: int = json['quantity'] if 'quantity' in json else 1
        self.show_removed_toppings_in_name: bool = json[
            'show_removed_toppings_in_name'] if 'show_removed_toppings_in_name' in json else False
    
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
