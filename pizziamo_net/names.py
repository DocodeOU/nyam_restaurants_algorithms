from typing import List

from .database import DatabasePizziamoNet
from ..models import Pizza, Ingredient


class NamesPizziamoNet:
    def __init__(self, database: DatabasePizziamoNet):
        self.DATABASE = database
    
    def _name_with_pizza_options(self, pizza: Pizza, initial_name: str) -> str:
        pass
    
    def _name_of_missing_ingredient(self, ingredient: Ingredient, pizza_menu: Pizza) -> str:
        pass
    
    def _name_of_pizza_ingredient(self, ingredient: Ingredient, pizza_menu: Pizza) -> str:
        pass
    
    @staticmethod
    def _ingredient_was_not_in_da_pizza(ingredient: Ingredient, pizza: Pizza) -> bool:
        return len([x for x in pizza.ingredients if x.id == ingredient.id]) == 0
    
    def _find_missing_ingredients(self, pizza: Pizza, pizza_menu: Pizza) -> List[Ingredient]:
        return [x for x in pizza_menu.ingredients if self._ingredient_was_not_in_da_pizza(ingredient=x, pizza=pizza)]
    
    def _find_added_ingredients(self, pizza: Pizza, pizza_menu: Pizza) -> List[Ingredient]:
        return [x for x in pizza.ingredients if
                x.quantity > 1  # se la quantita è aumentata
                or x.just_a_little  # se ne vogliamo poco ora
                or x.cooked_in_oven_by_default != x.uscita  # se l uscita è cambiata da quella di base
                or self._ingredient_was_not_in_da_pizza(ingredient=x, pizza=pizza_menu)]  # oppure se prima non c'era
    
    def _find_similar_pizza(pizza: Pizza):
        pass
    
    def name_of_pizza(pizza: Pizza) -> str:
        pass
