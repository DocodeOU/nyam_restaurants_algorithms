from typing import List


class Ingredient:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']
        self.quantity: int = json['quantity'] if 'quantity' in json else 1
        self.cooked_in_oven_by_default: bool = json['cooked_in_oven_by_default']
        self.cooked_out: bool = json['cooked_out'] if 'cooked_out' in json else not self.cooked_in_oven_by_default
        self.just_a_little: bool = json['just_a_little'] if 'just_a_little' in json else False
        self.name_business_software_shortened: bool = json[
            'name_business_software_shortened'] if 'name_business_software_shortened' in json else None


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
        self.show_removed_toppings_in_name: bool = json[
            'show_removed_toppings_in_name'] if 'show_removed_toppings_in_name' in json else False
        self.name_business_software: str = json[
            'name_business_software'] if 'name_business_software' in json else None
    
    @property
    def key_without_pizza_options(self) -> str:
        """
        utile per trovare se uno pizza e del menu
        escluso il fatto che possa avere le pizza option diverse
        """
        ingredients_copied = self.ingredients.copy()
        ingredients_copied.sort(key=lambda x: x.id)
        # aggiungiamo alla key la stringa degli ingredients
        key = ''
        for ing in ingredients_copied:
            if ing.quantity > 0:
                key = f'{key}{ing.id}x{ing.quantity}-{ing.just_a_little}-{ing.cooked_out}-'
        key += str(self.type)
        return key
    
    @property
    def key(self) -> str:
        """
        genera una key univoca che identifica la pizza che ha certe opzioni, certi ingredienti
        """
        # aggiungiamo alla key le info su come deve essere la pizza
        # ortiamo perchè se no una pizza alta bencotta e la stessa pizza bencotta alta risultano diverse
        pizza_options_copied = self.pizza_options.copy()
        pizza_options_copied.sort(key=lambda x: x.name)
        key_pizza_option = ''
        for pizza_option in pizza_options_copied:
            key_pizza_option = f'{key_pizza_option}{pizza_option.name}'
        return f'{self.key_without_pizza_options}-{key_pizza_option}'


class CartItemPizza(Pizza):
    def __init__(self, json: dict):
        super(CartItemPizza, self).__init__(json=json)
        self.quantity: int = json['quantity']


class Drink:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']


class CartItemDrink(Drink):
    def __init__(self, json: dict):
        super(CartItemDrink, self).__init__(json=json)
        self.quantity: int = json['quantity']


class Dessert:
    def __init__(self, json):
        self.id: int = json['id']
        self.name: str = json['name']
        self.price: float = json['price']


class CartItemDessert(Dessert):
    def __init__(self, json: dict):
        super(CartItemDessert, self).__init__(json=json)
        self.quantity: int = json['quantity']


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
