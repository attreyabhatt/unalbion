from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from .models import (
    Ingredient,
    IngredientCategory,
    UserIngredientPrice,
    PotionVariant,
    UserPotionPrice,
)
from .potion_recipes import potion_recipes
from animal_artifacts.models import (
    ArtifactItem,
    ArtifactPrice,
    ArtifactTier,
    ARTIFACT_TIER_PREFIX,
    ensure_artifact_catalog,
)
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET


INGREDIENT_CATALOG = [
    {"code": "agaric", "name": "Arcane Agaric", "category": IngredientCategory.HERB},
    {"code": "comfrey", "name": "Brightleaf Comfrey", "category": IngredientCategory.HERB},
    {"code": "burdock", "name": "Crenellated Burdock", "category": IngredientCategory.HERB},
    {"code": "teasel", "name": "Dragon Teasel", "category": IngredientCategory.HERB},
    {"code": "foxglove", "name": "Elusive Foxglove", "category": IngredientCategory.HERB},
    {"code": "mullein", "name": "Firetouched Mullein", "category": IngredientCategory.HERB},
    {"code": "yarrow", "name": "Ghoul Yarrow", "category": IngredientCategory.HERB},
    {"code": "cow_milk", "name": "Cow Milk", "category": IngredientCategory.ANIMAL_PRODUCT},
    {"code": "goat_milk", "name": "Goat Milk", "category": IngredientCategory.ANIMAL_PRODUCT},
    {"code": "sheep_milk", "name": "Sheep Milk", "category": IngredientCategory.ANIMAL_PRODUCT},
    {"code": "cow_butter", "name": "Cow Butter", "category": IngredientCategory.ANIMAL_PRODUCT},
    {"code": "goat_butter", "name": "Goat Butter", "category": IngredientCategory.ANIMAL_PRODUCT},
    {"code": "sheep_butter", "name": "Sheep Butter", "category": IngredientCategory.ANIMAL_PRODUCT},
    {"code": "hen_eggs", "name": "Hen Eggs", "category": IngredientCategory.ANIMAL_PRODUCT},
    {"code": "goose_eggs", "name": "Goose Eggs", "category": IngredientCategory.ANIMAL_PRODUCT},
    {"code": "potato_schnapps", "name": "Potato Schnapps", "category": IngredientCategory.SCHNAPPS},
    {"code": "corn_hooch", "name": "Corn Hooch", "category": IngredientCategory.SCHNAPPS},
    {"code": "pumpkin_moonshine", "name": "Pumpkin Moonshine", "category": IngredientCategory.SCHNAPPS},
    {"code": "animal_remains", "name": "Animal Remains", "category": IngredientCategory.OTHER},
]


def ensure_ingredient_catalog():
    existing = set(Ingredient.objects.values_list("code", flat=True))
    missing = [
        Ingredient(code=item["code"], name=item["name"], category=item["category"])
        for item in INGREDIENT_CATALOG
        if item["code"] not in existing
    ]
    if missing:
        Ingredient.objects.bulk_create(missing)


def ensure_potion_variants():
    existing = set(PotionVariant.objects.values_list("code", flat=True))
    missing = []
    for base_code in potion_recipes.keys():
        parts = base_code.split("_")
        if len(parts) != 3:
            continue
        tier = int(parts[0].replace("T", ""))
        name = parts[1].title()
        for enchant in range(4):
            code = f"{parts[0]}_{parts[1]}_{enchant}"
            if code in existing:
                continue
            missing.append(PotionVariant(code=code, tier=tier, name=name, enchant=enchant))
    if missing:
        PotionVariant.objects.bulk_create(missing)

def potion_calculator_view(request):

    if not request.user.is_authenticated:
        return render(request, "accounts/notloggedin.html") 
       
    """Main potion profit calculator view"""
    ensure_ingredient_catalog()
    ensure_potion_variants()
    ensure_artifact_catalog()
    
    if request.method == "POST":
        ingredient_updates = {}
        potion_updates = {}
        artifact_updates = {}

        for key, value in request.POST.items():
            if key == "csrfmiddlewaretoken":
                continue

            if key.startswith("ingredient_"):
                try:
                    ingredient_id = int(key.split("_", 1)[1])
                except ValueError:
                    continue
                ingredient_updates[ingredient_id] = value.strip()
            elif key.startswith("potion_"):
                try:
                    potion_id = int(key.split("_", 1)[1])
                except ValueError:
                    continue
                potion_updates[potion_id] = value.strip()
            elif key.startswith("artifact_"):
                parts = key.split("_", 2)
                if len(parts) != 3:
                    continue
                _, item_id, tier = parts
                if tier not in ArtifactTier.values:
                    continue
                try:
                    item_id = int(item_id)
                except ValueError:
                    continue
                artifact_updates[(item_id, tier)] = value.strip()

        ingredient_ids = set(ingredient_updates.keys())
        potion_ids = set(potion_updates.keys())
        artifact_item_ids = {item_id for item_id, _ in artifact_updates.keys()}

        ingredients_by_id = Ingredient.objects.in_bulk(ingredient_ids)
        potions_by_id = PotionVariant.objects.in_bulk(potion_ids)
        artifact_items_by_id = ArtifactItem.objects.in_bulk(artifact_item_ids)

        existing_ingredient_prices = UserIngredientPrice.objects.filter(
            user=request.user,
            ingredient_id__in=ingredient_ids,
        )
        existing_potion_prices = UserPotionPrice.objects.filter(
            user=request.user,
            potion_id__in=potion_ids,
        )
        existing_artifact_prices = ArtifactPrice.objects.filter(
            user=request.user,
            item_id__in=artifact_item_ids,
        )

        ingredient_by_key = {p.ingredient_id: p for p in existing_ingredient_prices}
        potion_by_key = {p.potion_id: p for p in existing_potion_prices}
        artifact_by_key = {(p.item_id, p.tier): p for p in existing_artifact_prices}

        ingredient_to_create = []
        ingredient_to_update = []
        ingredient_to_delete = []

        potion_to_create = []
        potion_to_update = []
        potion_to_delete = []

        artifact_to_create = []
        artifact_to_update = []
        artifact_to_delete = []

        for ingredient_id, raw_value in ingredient_updates.items():
            if ingredient_id not in ingredients_by_id:
                continue
            if raw_value == "":
                ingredient_to_delete.append(ingredient_id)
                continue
            try:
                price = int(raw_value)
            except ValueError:
                messages.error(request, f"Invalid value for ingredient {ingredient_id}: {raw_value}")
                continue

            existing = ingredient_by_key.get(ingredient_id)
            if existing:
                if existing.price != price:
                    existing.price = price
                    ingredient_to_update.append(existing)
            else:
                ingredient_to_create.append(
                    UserIngredientPrice(
                        user=request.user,
                        ingredient_id=ingredient_id,
                        price=price,
                    )
                )

        for potion_id, raw_value in potion_updates.items():
            if potion_id not in potions_by_id:
                continue
            if raw_value == "":
                potion_to_delete.append(potion_id)
                continue
            try:
                price = int(raw_value)
            except ValueError:
                messages.error(request, f"Invalid value for potion {potion_id}: {raw_value}")
                continue

            existing = potion_by_key.get(potion_id)
            if existing:
                if existing.price != price:
                    existing.price = price
                    potion_to_update.append(existing)
            else:
                potion_to_create.append(
                    UserPotionPrice(
                        user=request.user,
                        potion_id=potion_id,
                        price=price,
                    )
                )

        for (item_id, tier), raw_value in artifact_updates.items():
            if item_id not in artifact_items_by_id:
                continue
            if raw_value == "":
                artifact_to_delete.append((item_id, tier))
                continue
            try:
                price = int(raw_value)
            except ValueError:
                messages.error(request, f"Invalid value for artifact {item_id}: {raw_value}")
                continue

            existing = artifact_by_key.get((item_id, tier))
            if existing:
                if existing.price != price:
                    existing.price = price
                    artifact_to_update.append(existing)
            else:
                artifact_to_create.append(
                    ArtifactPrice(
                        user=request.user,
                        item_id=item_id,
                        tier=tier,
                        price=price,
                    )
                )

        with transaction.atomic():
            if ingredient_to_create:
                UserIngredientPrice.objects.bulk_create(ingredient_to_create)
            if ingredient_to_update:
                UserIngredientPrice.objects.bulk_update(ingredient_to_update, ["price"])
            if ingredient_to_delete:
                UserIngredientPrice.objects.filter(
                    user=request.user,
                    ingredient_id__in=ingredient_to_delete,
                ).delete()

            if potion_to_create:
                UserPotionPrice.objects.bulk_create(potion_to_create)
            if potion_to_update:
                UserPotionPrice.objects.bulk_update(potion_to_update, ["price"])
            if potion_to_delete:
                UserPotionPrice.objects.filter(
                    user=request.user,
                    potion_id__in=potion_to_delete,
                ).delete()

            if artifact_to_create:
                ArtifactPrice.objects.bulk_create(artifact_to_create)
            if artifact_to_update:
                ArtifactPrice.objects.bulk_update(artifact_to_update, ["price"])
            if artifact_to_delete:
                delete_q = Q()
                for item_id, tier in artifact_to_delete:
                    delete_q |= Q(item_id=item_id, tier=tier)
                ArtifactPrice.objects.filter(user=request.user).filter(delete_q).delete()

        updated_count = (
            len(ingredient_to_create)
            + len(ingredient_to_update)
            + len(ingredient_to_delete)
            + len(potion_to_create)
            + len(potion_to_update)
            + len(potion_to_delete)
            + len(artifact_to_create)
            + len(artifact_to_update)
            + len(artifact_to_delete)
        )
        if updated_count:
            messages.success(request, f"Updated {updated_count} price(s)")
        
        return redirect('potion_calculator')
    
    ingredient_prices = {
        price.ingredient.code: price.price
        for price in UserIngredientPrice.objects.filter(user=request.user)
    }

    ingredients = Ingredient.objects.all().order_by("name")
    herb_ingredients = [i for i in ingredients if i.category == IngredientCategory.HERB]
    animal_ingredients = [i for i in ingredients if i.category == IngredientCategory.ANIMAL_PRODUCT]
    schnapps_ingredients = [i for i in ingredients if i.category == IngredientCategory.SCHNAPPS]
    other_ingredients = [i for i in ingredients if i.category == IngredientCategory.OTHER]

    potion_variants = list(PotionVariant.objects.all().order_by("tier", "name", "enchant"))
    potion_price_map = {
        price.potion.code: price.price
        for price in UserPotionPrice.objects.filter(user=request.user).select_related("potion")
    }

    potion_names = sorted({p.name for p in potion_variants})

    artifact_items = ArtifactItem.objects.all().order_by("name")
    artifact_prices = ArtifactPrice.objects.filter(user=request.user, item__in=artifact_items)
    artifact_prices_by_item = {}
    for price in artifact_prices:
        artifact_prices_by_item.setdefault(price.item_id, {})[price.tier] = price.price

    calculation_data = prepare_calculation_data(request.user)
    
    context = {
        'herb_ingredients': herb_ingredients,
        'animal_ingredients': animal_ingredients,
        'schnapps_ingredients': schnapps_ingredients,
        'other_ingredients': other_ingredients,
        'ingredient_prices': ingredient_prices,
        'potion_variants': potion_variants,
        'potion_price_map': potion_price_map,
        'artifact_items': artifact_items,
        'artifact_tiers': [ArtifactTier.RUGGED, ArtifactTier.FINE, ArtifactTier.EXCELLENT],
        'artifact_prices_by_item': artifact_prices_by_item,
        'recipes_json': json.dumps(potion_recipes),
        'calculation_data_json': json.dumps(calculation_data),
        'tiers': ["T2", "T3", "T4", "T5", "T6", "T7", "T8"],
        'enchant_levels': ["0", "1", "2", "3"],
        'potion_names': potion_names,
    }
    
    return render(request, 'potions/calculator.html', context)


def prepare_calculation_data(user):
    """Prepare all data needed for frontend profit calculations"""
    
    ingredient_prices = {
        price.ingredient.code: price.price
        for price in UserIngredientPrice.objects.filter(user=user)
        if price.price is not None
    }

    artifact_prices = ArtifactPrice.objects.filter(user=user).select_related("item")
    for artifact_price in artifact_prices:
        if artifact_price.price is not None:
            ingredient_prices[f"{ARTIFACT_TIER_PREFIX[artifact_price.tier]}{artifact_price.item.code_base}"] = artifact_price.price
    
    return {
        'recipes': potion_recipes,
        'ingredient_prices': ingredient_prices,
    }


def get_recipe_cost(recipe_data, ingredient_prices):
    ingredients = recipe_data["ingredients"]
    yield_qty = recipe_data.get("yield", 1)

    total_cost = 0
    missing_ingredients = []

    for ingredient_code, quantity in ingredients:
        price = ingredient_prices.get(ingredient_code)
        if price is None:
            missing_ingredients.append(ingredient_code)
        else:
            total_cost += price * quantity

    if missing_ingredients:
        return None, missing_ingredients

    cost_per_potion = total_cost / yield_qty
    return round(cost_per_potion), []



def format_potion_name(potion_code, enchant_level):
    """Format potion code into readable name"""
    # Extract tier and potion name from code like "T4_HEALING_0"
    parts = potion_code.replace('_0', '').split('_')
    tier = parts[0]
    potion_name = parts[1].title()
    
    enchant_suffix = f" +{enchant_level}" if enchant_level > 0 else ""
    
    return f"{tier} {potion_name}{enchant_suffix}"


@login_required
def reset_prices_view(request):
    """Reset all prices for the user"""
    if request.method == 'POST':
        UserIngredientPrice.objects.filter(user=request.user).delete()
        UserPotionPrice.objects.filter(user=request.user).delete()
        ArtifactPrice.objects.filter(user=request.user).delete()
        
        messages.success(request, "All prices have been reset")
    
    return redirect('potion_calculator')


# Helper function that can be used by templates or other views
def get_user_artifact_prices(user):
    """Get all artifact prices for a user as a dictionary"""
    artifact_prices = ArtifactPrice.objects.filter(user=user).select_related("item")

    return {
        f"{ARTIFACT_TIER_PREFIX[price.tier]}{price.item.code_base}": {
            "market_price": price.price,
            "name": price.item.name,
            "type": price.tier,
        }
        for price in artifact_prices
        if price.price is not None
    }


@login_required
@require_GET
def potion_profit_api(request):
    calc_data = prepare_calculation_data(request.user)

    profit_data = []

    for potion_code, recipe in calc_data["recipes"].items():
        cost, missing = get_recipe_cost(recipe, calc_data["ingredient_prices"])
        if missing:
            profit_data.append({
                "potion_code": potion_code,
                "status": "data_insufficient",
                "missing": missing,
                "recipe": recipe,
            })
        else:
            profit_data.append({
                "potion_code": potion_code,
                "status": "ok",
                "cost": cost,
                "recipe": recipe,
            })

    return JsonResponse(profit_data, safe=False)


