from functools import reduce
from typing import List

from nyam_restaurants_algorithms.app.abstract_prices import AbstractPrices
from nyam_restaurants_algorithms.app.models import Pizza, CartItemPizza
from .database import DatabasePizziamoNet

COSTO_CONSEGNA = 0.5


class PricesPizziamoNet(AbstractPrices):
    def __init__(self, database: DatabasePizziamoNet, use_business_software_algs: bool):
        self.DATABASE = database
        self.use_business_software_algs = use_business_software_algs
    
    def _price_pizza_menu(self, pizza: Pizza, pizza_menu: Pizza) -> float:
       
        """
        Prezzo di una pizza che ha gli ingredienti di una pizza del menu
        Si parte dal prezzo del menu e si aggiunge il prezzo degli ingredienti in piu
        """
        price_with_ingredients = pizza_menu.price
        for ing in pizza.ingredients:
            db_ingredient = self.DATABASE.get_ingredient_from_pizza_ingredient(ing)
            price_with_ingredients += db_ingredient.price * (ing.quantity - 1)
        return price_with_ingredients
    
    def _price_pizza_not_in_menu(self, pizza: Pizza) -> float:
        all_pizzas = self.DATABASE.pizzas
        ing_mozzarella = self.DATABASE.restaurant.ingredient_mozzarella
        ing_pomodoro = self.DATABASE.restaurant.ingredient_pomodoro
        
        pizza_ingredients_ids = [x.id for x in pizza.ingredients]
        # Verifichiamo se è una schiaccitina non deve avere ne pomodoro ne mozzarella
        e_schiacciatina = all(x not in pizza_ingredients_ids for x in [ing_mozzarella, ing_pomodoro])
        # le schiacciatine, i calzoni e i ceci hanno dei prezzi di base scritti nel db
        if e_schiacciatina or pizza.type != self.DATABASE.type_pizza:
            price_base = next(
                x for x in all_pizzas if x.type == pizza.type and len(x.ingredients) == 0).price
        else:
            # prezzo base per la pizza
            price_base = 4
        
        # aggiungiamo il prezzo degli ingredienti
        price_with_ingredients = price_base
        for ing in pizza.ingredients:
            db_ingredient = self.DATABASE.get_ingredient_from_pizza_ingredient(ing)
            price_with_ingredients += db_ingredient.price * ing.quantity
        return price_with_ingredients
    
    def price_pizza(self, pizza: Pizza) -> float:
        all_pizzas = self.DATABASE.pizzas
        try:
            # cerchiamo se è presente nel menu
            pizza_trovata = next(
                x for x in all_pizzas if pizza.key_without_pizza_options == x.key_without_pizza_options)
            price_without_options = self._price_pizza_menu(pizza=pizza, pizza_menu=pizza_trovata)
        except StopIteration:
            # pizza non trovata
            price_without_options = self._price_pizza_not_in_menu(pizza=pizza)
        
        price_with_option = price_without_options
        for pizza_option in pizza.pizza_options:
            price_with_option += self.DATABASE.get_pizza_option_from_id(pizza_option.id).price
        return price_with_option
    
    def delivery_cost(self, pizzas_in_cart: List[CartItemPizza], delivery_type: int) -> float:
        
        def _reduce_pizza_quantity(acc: int, pizza: CartItemPizza) -> int:
            return acc + pizza.quantity
        
        price_of_delivery = 0.0
        n_of_pizzas = reduce(_reduce_pizza_quantity, pizzas_in_cart, 0)
        
        # la consegna costa solo se a domicilio
        if delivery_type == self.DATABASE.delivery_type_home:
            n_of_ceci = reduce(_reduce_pizza_quantity,
                               [x for x in pizzas_in_cart if x.type == self.DATABASE.type_cecio], 0)
            # se sono tutti ceci
            if n_of_pizzas == n_of_ceci:
                # la loro consegna costa
                price_of_delivery = n_of_pizzas * COSTO_CONSEGNA
            else:
                # altrimenti la loro consegna non costa
                price_of_delivery = (n_of_pizzas - n_of_ceci) * COSTO_CONSEGNA
        
        return price_of_delivery
