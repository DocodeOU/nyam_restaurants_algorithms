from .models import Pizza


class AbstractNames:
    def name_of_pizza(self, pizza: Pizza) -> str:
        raise NotImplementedError("Please Implement this method")
