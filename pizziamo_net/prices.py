from functools import reduce
from typing import List

from nyam_restaurants_algorithms.app.abstract_prices import AbstractPrices
from nyam_restaurants_algorithms.app.models import Pizza, Ingredient, PizzaOption
from .database import DatabasePizziamoNet

COSTO_CONSEGNA = 0.5


class PricesPizziamoNet(AbstractPrices):
    def __init__(self, database: DatabasePizziamoNet, use_business_software_algs: bool):
        self.DATABASE = database
        self.use_business_software_algs = use_business_software_algs
    
    @staticmethod
    def _reduce_ingredient_price(acc: float, ing: Ingredient):
        return acc + ing.price * (ing.quantity - 1)
    
    def _price_pizza_menu(self, pizza: Pizza, pizza_menu: Pizza) -> float:
        """
        Prezzo di una pizza che ha gli ingredienti di una pizza del menu
        Si parte dal prezzo del menu e si aggiunge il prezzo degli ingredienti in piu
        """
        
        return reduce(self._reduce_ingredient_price, pizza.ingredients, pizza_menu.price)
    
    def _price_pizza_not_in_menu(self, pizza: Pizza) -> float:
        all_pizzas = self.DATABASE.pizzas
        ing_mozzarella = self.DATABASE.consts.ingredient_mozzarella
        ing_pomodoro = self.DATABASE.consts.ingredient_pomodoro
        
        pizza_ingredients_ids = [x.id for x in pizza.ingredients]
        # Verifichiamo se è una schiaccitina non deve avere ne pomodoro ne mozzarella
        e_schiacciatina = all(x.id not in pizza_ingredients_ids for x in [ing_mozzarella, ing_pomodoro])
        # le schiacciatine, i calzoni e i ceci hanno dei prezzi di base scritti nel db
        if e_schiacciatina or pizza.type != self.DATABASE.type_pizza.id:
            price_base = next(
                x for x in all_pizzas if x.type_id == pizza.type and len(x.ingredients) == 0).price
        else:
            # prezzo base per la pizza
            price_base = 4
        
        # aggiungiamo il prezzo degli ingredienti
        price_with_ingredients = reduce(self._reduce_ingredient_price, pizza.ingredients, price_base)
        return price_with_ingredients
    
    def price_pizza(self, pizza: Pizza) -> float:
        all_pizzas = self.DATABASE.pizzas
        try:
            # cerchiamo se è presente nel menu
            # TODO key_without_pizza_options non e buona
            pizza_trovata = next(
                x for x in all_pizzas if pizza.key_without_pizza_options == x.key_without_pizza_options)
            price_without_options = self._price_pizza_menu(pizza=pizza, pizza_menu=pizza_trovata)
        except StopIteration:
            # pizza non trovata
            price_without_options = self._price_pizza_not_in_menu(pizza=pizza)
        
        def _get_pizza_option_price(acc: float, option: PizzaOption):
            return acc + option.price
        
        price_with_option = reduce(_get_pizza_option_price, pizza.pizza_options, price_without_options)
        return price_with_option
    
    def delivery_cost(self, pizzas_in_cart: List[Pizza], delivery_type: int) -> float:
        
        def _reduce_pizza_quantity(acc: int, pizza: Pizza):
            return acc + pizza.quantity
        
        price_of_delivery = 0
        n_of_pizzas = reduce(_reduce_pizza_quantity, pizzas_in_cart, 0)
        
        # la consegna costa solo se a domicilio
        if delivery_type == self.DATABASE.delivery_type_home:
            n_of_ceci = reduce(_reduce_pizza_quantity,
                               [pizza for pizza in pizzas_in_cart if pizza.type == self.DATABASE.type_cecio], 0)
            # se sono tutti ceci
            if n_of_pizzas == n_of_ceci:
                # la loro consegna costa
                price_of_delivery = n_of_pizzas * COSTO_CONSEGNA
            else:
                # altrimenti la loro consegna non costa
                price_of_delivery = (n_of_pizzas - n_of_ceci) * COSTO_CONSEGNA
        
        return price_of_delivery
