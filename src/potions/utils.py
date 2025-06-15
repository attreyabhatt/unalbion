# potions/utils.py

from .models import PotionInput
from .potion_recipes import potion_recipes

def calculate_production_costs_enchant_0(potion_input):
    results = []

    for code, recipe in potion_recipes.items():
        total_cost = 0
        missing = []

        for ingredient, qty in recipe["ingredients"]:
            value = getattr(potion_input, ingredient, None)
            if value is None:
                missing.append(ingredient)
            else:
                total_cost += qty * value

        if missing:
            results.append({
                "potion_code": code,
                "status": "data_insufficient",
                "missing": missing
            })
        else:
            results.append({
                "potion_code": code,
                "status": "ok",
                "cost": total_cost
            })

    return results
