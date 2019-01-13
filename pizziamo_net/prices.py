from functools import reduce
from typing import List

from models import Pizza, Ingredient, PizzaOption

COSTO_CONSEGNA = 0.5


def _price_pizza_menu(pizza: Pizza, pizza_menu: Pizza) -> float:
    """
    Prezzo di una pizza che ha gli ingredienti di una pizza del menu
    Si parte dal prezzo del menu e si aggiunge il prezzo degli ingredienti in piu
    """
    
    def _get_ingredient_price(acc: float, ing: Ingredient):
        return acc + ing.price * (ing.quantity - 1)
    
    return reduce(_get_ingredient_price, pizza.ingredients, initial=pizza_menu.price)


def _price_pizza_not_in_menu(pizza: Pizza) -> float:
    all_pizzas: List[Pizza] = Pizza.objects.all()
    consts: Consts = Consts.objects.first()
    ing_mozzarella = consts.ingredient_mozzarella
    ing_pomodoro = consts.ingredient_pomodoro
    
    pizza_ingredients_ids = [x.id for x in pizza.ingredients]
    # Verifichiamo se è una schiaccitina non deve avere ne pomodoro ne mozzarella
    e_schiacciatina = all(x.id not in pizza_ingredients_ids for x in [ing_mozzarella, ing_pomodoro])
    # le schiacciatine, i calzoni e i ceci hanno dei prezzi di base scritti nel db
    if e_schiacciatina or pizza.type != TypeOfPizza.objects.get(name='Pizza').id:
        price_base = next(
            x for x in all_pizzas if x.type_id == pizza.type and len(x.ingredients) == 0).price
    else:
        # prezzo base per la pizza
        price_base = 4
    
    # aggiungiamo il prezzo degli ingredienti
    def _get_ingredient_price(acc: float, ing: Ingredient):
        return acc + ing.price * ing.quantity
    
    price_with_ingredients = reduce(_get_ingredient_price, pizza.ingredients, initial=price_base)
    return price_with_ingredients


def price_pizza(pizza: Pizza) -> float:
    all_pizzas: List[Pizza] = Pizza.objects.all()
    try:
        # cerchiamo se è presente nel menu
        pizza_trovata: Pizza = next(
            x for x in all_pizzas if pizza.key_without_pizza_options == x.generate_key_without_options())
        price_without_options = _price_pizza_menu(pizza=pizza, pizza_menu=pizza_trovata)
    except StopIteration:
        # pizza non trovata
        price_without_options = _price_pizza_not_in_menu(pizza=pizza)
    
    def _get_pizza_option_price(acc: float, option: PizzaOption):
        return acc + option.price
    
    price_with_option = reduce(_get_pizza_option_price, pizza.pizza_options, initial=price_without_options)
    return price_with_option


def total_price_of_pizzas(pizzas_in_cart: List[Pizza], delivery_type: int) -> float:
    def _get_pizza_price(acc: float, pizza: Pizza):
        return acc + pizza.price
    
    def _get_pizza_quantity(acc: int, pizza: Pizza):
        return acc + pizza.quantity
    
    price_of_pizzas = reduce(_get_pizza_price, pizzas_in_cart, initial=0)
    price_of_delivery = 0
    n_of_pizzas = reduce(_get_pizza_quantity, pizzas_in_cart, initial=0)
    
    # la consegna costa solo se a domicilio
    if delivery_type == DeliveryType.objects.get(name='Domicilio'):
        n_of_ceci = reduce(_get_pizza_quantity,
                           filter(lambda x: x.type == TypeOfPizza.objects.get(name='Cecio').id, pizzas_in_cart),
                           initial=0)
        # se sono tutti ceci
        if n_of_pizzas == n_of_ceci:
            # la loro consegna costa
            price_of_delivery = n_of_pizzas * COSTO_CONSEGNA
        else:
            # altrimenti la loro consegna non costa
            price_of_delivery = (n_of_pizzas - n_of_ceci) * COSTO_CONSEGNA
    
    return price_of_pizzas + price_of_delivery
