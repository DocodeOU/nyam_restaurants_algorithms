from functools import reduce
from typing import List

from nyam_restaurants_algorithms.app.abstract_prices import AbstractPrices
from nyam_restaurants_algorithms.app.models import Pizza, CartItemPizza, PizzaIngredient
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
        ing_mozzarella = self.DATABASE.get_ingredient_mozzarella()
        ing_pomodoro = self.DATABASE.get_ingredient_pomodoro()

        pizza_ingredients_ids = [x.id for x in pizza.ingredients]
        # Verifichiamo se è una schiaccitina non deve avere ne pomodoro ne mozzarella
        e_schiacciatina = all(x not in pizza_ingredients_ids for x in [ing_mozzarella.id, ing_pomodoro.id])
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

    # Da usare quando una pizza non deve avere il prezzo calcolato matematicamente ma solo aggiungere il prezzo degli
    # eventuali prezzi aggiunti
    def _price_pizza_michele(self, pizza: Pizza, pizza_menu: Pizza) -> float:
        price_base = pizza.price
        price_with_ingredients = price_base
        # aggiungiamo eventuali ingredienti con quantità maggiorata
        for ing in pizza.ingredients:
            is_in_pizza_menu = PricesPizziamoNet._check_if_in_pizza(ingredient=ing,
                                                                    pizza=pizza_menu)

            db_ingredient = self.DATABASE.get_ingredient_from_pizza_ingredient(ing)
            # se l'ingrediente faceva parte della pizza aggiungiamo solo l'eventuale quantità aggiunta altrimenti
            # aggiungiamo il prezzo intero dell'ingrediente per la quantità
            price_with_ingredients += db_ingredient.price * (ing.quantity - (1 if is_in_pizza_menu else 0))

        return price_with_ingredients

    @staticmethod
    def _check_if_in_pizza(ingredient: PizzaIngredient, pizza: Pizza) -> bool:
        return any(ing.id == ingredient.id for ing in pizza.ingredients)

    def price_pizza(self, pizza: Pizza) -> float:
        all_pizzas = self.DATABASE.pizzas
        try:
            # cerchiamo se è presente nel menu
            pizza_trovata = next(
                x for x in all_pizzas if pizza.key_without_pizza_options == x.key_without_pizza_options)
            price_without_options = self._price_pizza_menu(pizza=pizza, pizza_menu=pizza_trovata)
        except StopIteration:
            # Se dobbiamo calcolare il prezzo partendo dalla base di partenza della pizza del menu
            # TODO: capire in base a cosa fare sto if
            if False:
                pizza_menu = next(x for x in all_pizzas if pizza.id == x.id)
                price_without_options = self._price_pizza_michele(pizza, pizza_menu)
            else:
                # se dobbiamo calcolare il prezzo matematico
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
