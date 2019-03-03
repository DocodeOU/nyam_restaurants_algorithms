import re
from typing import List

from nyam_restaurants_algorithms.app.abstract_names import AbstractNames
from nyam_restaurants_algorithms.app.models import Pizza, Ingredient, PizzaIngredient
from .database import DatabasePizziamoNet


class NamesPizziamoNet(AbstractNames):
    def __init__(self, database: DatabasePizziamoNet, use_business_software_algs: bool):
        self.DATABASE = database
        self.use_business_software_algs = use_business_software_algs
    
    @staticmethod
    def _name_with_pizza_options(pizza: Pizza, initial_name: str) -> str:
        sorted_pizza_options = pizza.pizza_options
        sorted_pizza_options.sort(key=lambda x: x.name)
        name = initial_name
        for pizza_option in sorted_pizza_options:
            name = f'{pizza_option.name} {name}' \
                if pizza_option.place_at_beggining_of_name else f'{name} {pizza_option.name}'
        return name
    
    def _name_of_missing_ingredient(self, current_name: str, ingredient: PizzaIngredient,
                                    now_it_has_pomodoro: bool,
                                    now_it_has_mozzarella: bool) -> str:
        db_ingredient = self.DATABASE.get_ingredient_from_pizza_ingredient(ingredient)
        if ingredient.id == self.DATABASE.consts.ingredient_mozzarella and now_it_has_pomodoro:
            return f'ROSSA {current_name}'
        elif ingredient.id == self.DATABASE.consts.ingredient_pomodoro and now_it_has_mozzarella:
            return f'BIANCA {current_name}'
        else:
            ing_name = db_ingredient.name_business_software_shortened \
                if self.use_business_software_algs and db_ingredient.name_business_software_shortened \
                else ingredient.name
            return f'{current_name} - {ing_name}'
    
    def _name_of_pizza_ingredient(self, ingredient: PizzaIngredient, pizza_menu: Pizza) -> str:
        db_ingredient = self.DATABASE.get_ingredient_from_pizza_ingredient(ingredient)
        just_name = db_ingredient.name_business_software_shortened \
            if self.use_business_software_algs and db_ingredient.name_business_software_shortened \
            else ingredient.name
        if not db_ingredient.cooked_out_by_default and ingredient.cooked_out:
            # se in origine era all'entrata e ora è all'uscita
            just_name = f'{just_name} Usc.'
        elif db_ingredient.cooked_out_by_default and not ingredient.cooked_out:
            # se in origine era all uscita e ora è all'entrata
            just_name = f'{just_name} Ent.'
        its_a_new_ingredient = self._ingredient_was_not_in_da_pizza(ingredient=ingredient, pizza=pizza_menu)
        quantity_to_write = ingredient.quantity if its_a_new_ingredient else ingredient.quantity - 1
        # se ne vogliamo solo un po
        if ingredient.just_a_little:
            return f' (Poco {just_name})'
        elif quantity_to_write > 1:
            # se bisogna esprimere la quantita
            return f' + {quantity_to_write} {just_name}'
        elif its_a_new_ingredient or ingredient.quantity == 2:
            # se e un ingrediente nuovo mettiamo il piu, o se porco dio
            return f' + {just_name}'
        else:
            # se c'e gia, ma e cambiato entrata uscita, allora mettiamo una parentesi
            return f' ({just_name})'
    
    @staticmethod
    def _ingredient_was_not_in_da_pizza(ingredient: PizzaIngredient, pizza: Pizza) -> bool:
        return len([ing for ing in pizza.ingredients if ing.id == ingredient.id]) == 0
    
    def _find_missing_ingredients(self, pizza: Pizza, pizza_menu: Pizza) -> List[PizzaIngredient]:
        return [ing for ing in pizza_menu.ingredients if
                self._ingredient_was_not_in_da_pizza(ingredient=ing, pizza=pizza)]
    
    def _find_added_ingredients(self, pizza: Pizza, pizza_menu: Pizza) -> List[PizzaIngredient]:
        return [ing for ing in pizza.ingredients if
                ing.quantity > 1  # se la quantita è aumentata
                or ing.just_a_little  # se ne vogliamo poco ora
                # se l uscita è cambiata da quella di base
                or self.DATABASE.get_ingredient_from_pizza_ingredient(ing).cooked_out_by_default != ing.cooked_out
                or self._ingredient_was_not_in_da_pizza(ingredient=ing, pizza=pizza_menu)]  # oppure se prima non c'era
    
    def _find_similar_pizza(self, pizza: Pizza) -> Pizza:
        # Troviamo nel menu tutte le pizze che hanno tutti gli ingredienti della pizza ma non ne hanno altri in più
        def is_similar_pizza(pizza_menu: Pizza):
            # se la pizza del menu ha più ingredienti della pizza creata o il tipo non corrisponde la scartiamo
            if len(pizza_menu.ingredients) > len(pizza.ingredients) or pizza_menu.type != pizza.type:
                return False
            # Verifichiamo se ogni ingrediente corrisponde
            pizza_ingredients_ids = [ing.id for ing in pizza.ingredients]
            return all(ing.id in pizza_ingredients_ids for ing in pizza_menu.ingredients)
        
        similar_pizzas = [x for x in self.DATABASE.pizzas if is_similar_pizza(x)]
        # sortiamo per numero di ingredienti
        similar_pizzas.sort(key=lambda x: len(x.ingredients), reverse=True)
        # ritorniamo la pizza che ha più ingredienti corrispondenti
        return similar_pizzas[0]
    
    def name_of_pizza(self, pizza: Pizza) -> str:
        # troviamo la pizza di partenza
        original_pizza = next(x for x in self.DATABASE.pizzas if x.id == pizza.id)
        # controlliamo che la pizza abbia il pomodoro e la mozzarella
        now_it_has_pomodoro = any([ing.id == self.DATABASE.consts.ingredient_pomodoro for ing in pizza.ingredients])
        now_it_has_mozzarella = any([ing.id == self.DATABASE.consts.ingredient_mozzarella for ing in pizza.ingredients])
        # se dobbiamo mostrare gli ingredienti tolti dalla pizza perche nel db è configurata cosi
        # o è stato tolto il pomodoro
        # o è stato tolta la mozzarella
        if original_pizza.show_removed_toppings_in_name:
            # usiamo come pizza di partenza quella del menu che è stata cliccata
            pizza_menu = original_pizza
        else:
            # altrimenti prendiamo come pizza di base un altra
            # e mostriamo gli ingredienti aggiunti a partire da quella
            # Prendo il tipo in modo dinamico
            pizza.type = original_pizza.type
            # usiamo come pizza di partenza quella che contiene il maggior numero di ingredienti
            pizza_menu = self._find_similar_pizza(pizza=pizza)
        name = pizza_menu.name_business_software \
            if self.use_business_software_algs and pizza_menu.name_business_software \
            else pizza_menu.name
        # Verifichiamo se sono stati tolti degli ingredienti dalla pizza originale
        # diamo il nome agli ingredienti tolti
        missing_ingredients = self._find_missing_ingredients(pizza=pizza, pizza_menu=pizza_menu)
        name_of_missing_ingredients = name
        for ing in missing_ingredients:
            name_of_missing_ingredients = self._name_of_missing_ingredient(
                current_name=name_of_missing_ingredients, ingredient=ing,
                now_it_has_pomodoro=now_it_has_pomodoro, now_it_has_mozzarella=now_it_has_mozzarella)
        # diamo il nome agli ingredienti aggiunti
        added_ingredients = self._find_added_ingredients(pizza=pizza, pizza_menu=pizza_menu)
        name_of_added_ingredients = ''
        for ing in added_ingredients:
            name_of_pizza_ingredient = self._name_of_pizza_ingredient(ingredient=ing, pizza_menu=pizza_menu)
            name_of_added_ingredients = f'{name_of_added_ingredients} {name_of_pizza_ingredient}'
        name = f'{name_of_missing_ingredients} {name_of_added_ingredients}'
        # aggiungo altre caratteristiche come Integrale, Morbida ecc...
        name = self._name_with_pizza_options(pizza=pizza, initial_name=name)
        # e rimuovo gli spazi di troppo
        name = re.sub(' +', ' ', name).strip()
        return name
    
    @staticmethod
    def name_formatted(pizza: Pizza, current_name: str):
        new_name = current_name
        ingredients_cooked_out = [x for x in pizza.ingredients if x.cooked_out]
        has_cooked_in_oven_ingredients_in_name = len(
            [x for x in pizza.ingredients if not x.cooked_out and x.name in current_name]) > 0
        has_cooked_out_ingredients = len(ingredients_cooked_out) > 0
        # se nel nome non ci sono ingredienti che poi sono all entrata
        if not has_cooked_in_oven_ingredients_in_name and has_cooked_out_ingredients:
            # sottilineamo tutto il nome
            new_name = f'<u>{current_name}</u>'
        elif has_cooked_out_ingredients:
            # altrimenti sottilineamo gli ingredienti all uscita
            for ing in ingredients_cooked_out:
                new_name = new_name.replace(ing.name, f'<u>{ing.name}</u>')
        return new_name
