from typing import List

from .models import Pizza


class AbstractPrices:
    def price_pizza(self, pizza: Pizza) -> float:
        raise NotImplementedError("Please Implement this method")

    def total_price_of_pizzas(self, pizzas_in_cart: List[Pizza], delivery_type: int) -> float:
        raise NotImplementedError("Please Implement this method")
