from .models import Restaurant, Pizza, Ingredient, PizzaOption, PizzaIngredient


class AbstractDatabase:
    def __init__(self, json: dict):
        self.restaurant = Restaurant(json=json['consts'])
        self.pizzas = [Pizza(json=x) for x in json['pizzas']]
        self.ingredients = [Ingredient(json=x) for x in json['ingredients']]
        self.pizza_options = [PizzaOption(json=x) for x in json['pizza_options']]

        self.delivery_type_home = 2
        self.type_pizza = 1
        self.type_cecio = 3
        
        # self.delivery_type_home = next(x for x in delivery_types if x.name == 'Domicilio')
        # self.type_pizza = next(x for x in types_of_pizzas if x.name == 'Pizza')
        # self.type_cecio = next(x for x in types_of_pizzas if x.name == 'Cecio')
        
    def get_ingredient_from_pizza_ingredient(self, pizza_ingredient: PizzaIngredient) -> Ingredient:
        return next(x for x in self.ingredients if x.id == pizza_ingredient.id)
