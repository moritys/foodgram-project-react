from typing import TYPE_CHECKING

from recipes.models import AmountIngredient, Recipe

if TYPE_CHECKING:
    from recipes.models import Ingredient


def recipe_ingredients_set(recipe, ingredients):
    objs = []

    for ingredient, amount in ingredients.values():
        objs.append(AmountIngredient(
            recipe=recipe,
            ingredients=ingredient,
            amount=amount
        ))

    AmountIngredient.objects.bulk_create(objs)


# Словарь для сопостановления латинской и русской стандартных раскладок.
incorrect_layout = str.maketrans(
    'qwertyuiop[]asdfghjkl;\'zxcvbnm,./',
    'йцукенгшщзхъфывапролджэячсмитьбю.'
)
