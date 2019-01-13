from typing import List

from django_models.models import Pizza
from django_models.models_from_json import IngredientFromJson, PizzaOptionFromJson


def _name_with_pizza_options(pizza: PizzaOptionFromJson, initial_name: str) -> str:
    pass


def _name_of_missing_ingredient(ingredient: IngredientFromJson, pizza_menu: Pizza) -> str:
    pass


def _name_of_pizza_ingredient(ingredient: IngredientFromJson, pizza_menu: Pizza) -> str:
    pass


def ingredient_was_not_in_da_pizza(ingredient: IngredientFromJson, pizza_menu: Pizza) -> bool:
    pass


def _find_missing_ingredients(pizza: PizzaOptionFromJson, pizza_menu: Pizza) -> List[IngredientFromJson]:
    pass


def _find_added_ingredients(pizza: PizzaOptionFromJson, pizza_menu: Pizza) -> List[IngredientFromJson]:
    pass


def _find_similar_pizza(pizza: PizzaOptionFromJson):
    pass


def name_of_pizza(pizza: PizzaOptionFromJson) -> str:
    pass
