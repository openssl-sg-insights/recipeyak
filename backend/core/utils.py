from typing import List, Dict

from pint import UnitRegistry, UndefinedUnitError
from pint.quantity import _Quantity as Quantity

from .inflect import singularize, pluralize

ureg = UnitRegistry()


def not_real_quantity(quantity) -> bool:
    basic_quantities = ['some', 'sprinkle']
    return isinstance(quantity, str) and quantity.lower() in basic_quantities


def simplify_units(units):
    """
    tablespoon, sprinkle, some, pinch => tablespoon, some
    """
    combineable_ingredients = ['sprinkle', 'some', 'pinch']
    simplified = []
    some = False
    for u in units:
        if isinstance(u, str) and any(i in u for i in combineable_ingredients):
            some = True
        else:
            simplified.append(str(u))
    if some:
        simplified.append('some')
    return simplified


def max_quantity(quantity: str) -> str:
    """
    take the '4-5' medium button mushrooms and find the max
    """
    return quantity.split('-')[-1]


def ingredient_quantity(ingredient):
    try:
        quantity = ureg.parse_expression(max_quantity(ingredient.quantity))
        try:
            if str(quantity.units) in ['picoinch']:
                quantity = 'pinch'
        except AttributeError:
            pass
        return quantity
    except UndefinedUnitError:
        return ingredient.quantity


def quantity_baseunit(quantity):
    if not_real_quantity(quantity):
        return 'some'
    try:
        return quantity.to_base_units().units
    except AttributeError:
        return ''


def normalize_name(ingredient):
    return ingredient.name.replace('-', ' ')


def should_pluralize(s) -> bool:
    for u in s:
        try:
            if u > 1:
                return True
        except (ValueError, TypeError):
            pass
    return False


def combine_ingredients(ingredients: List) -> List:

    combined: Dict[str, Dict[str, Quantity]] = {}

    for ingredient in ingredients:

        quantity = ingredient_quantity(ingredient)
        base_unit = quantity_baseunit(quantity)

        name = normalize_name(ingredient)
        singular_name = singularize(name)

        if combined.get(singular_name):
            if combined[singular_name].get(base_unit):
                combined[singular_name][base_unit] += quantity
            else:
                combined[singular_name][base_unit] = quantity
        else:
            combined[singular_name] = {
                base_unit: quantity
            }

    simple_ingredients = []
    for name, v in combined.items():
        combined_units = " + ".join(simplify_units(v.values()))
        plural = should_pluralize(v.values())
        simple_ingredients.append({
            'unit': combined_units,
            'name': name if not plural else pluralize(name)
        })

    return simple_ingredients
