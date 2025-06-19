from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Field
from django.contrib import messages
from .models import PotionInput
from .potion_recipes import potion_recipes
from animal_artifacts.models import AnimalArtifactItem
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from collections import OrderedDict


@login_required
def potion_calculator_view(request):
    """Main potion profit calculator view"""
    potion_input, created = PotionInput.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        # Handle regular ingredient price updates
        updated_fields = []
        updated_artifacts = []
        
        for key, value in request.POST.items():
            print(key, value)  # Debugging output
            if key in ('csrfmiddlewaretoken', 'user', 'id'):
                continue
                
            # Handle animal artifact updates
            if key.startswith('artifact_'):
                artifact_code = key.replace('artifact_', '')
                try:
                    artifact_item = AnimalArtifactItem.objects.get(
                        artifact__user=request.user,
                        code_name=artifact_code
                    )
                    if value.strip():
                        artifact_item.market_price = int(value)
                        artifact_item.save()
                        updated_artifacts.append(artifact_code)
                    else:
                        artifact_item.market_price = None
                        artifact_item.save()
                except (AnimalArtifactItem.DoesNotExist, ValueError) as e:
                    messages.error(request, f"Error updating {artifact_code}: {str(e)}")
                    
            # Handle regular potion input fields
            elif hasattr(potion_input, key):
                if value.strip():
                    try:
                        setattr(potion_input, key, int(value))
                        updated_fields.append(key)
                    except ValueError:
                        messages.error(request, f"Invalid value for {key}: {value}")
                else:
                    setattr(potion_input, key, None)
        
        # Save potion input changes
        potion_input.save()
        
        # Show success messages
        total_updates = len(updated_fields) + len(updated_artifacts)
        if total_updates > 0:
            messages.success(request, f"Updated {total_updates} price(s)")
        
        return redirect('potion_calculator')
    
    # Get user's animal artifacts for price lookup and form display
    user_artifacts = AnimalArtifactItem.objects.filter(
        artifact__user=request.user
    ).select_related('artifact').order_by('name','id')
    
    # Create artifacts dictionary for easy lookup
    artifacts_dict = {}
    artifacts_needing_prices = []
    all_artifacts_for_display = []

    for artifact in user_artifacts:
        artifacts_dict[artifact.code_name] = {
            'market_price': artifact.market_price,
            'name': artifact.name,
            'artifact_type': artifact.artifact.artifact_type,
            'needs_price': artifact.market_price is None or artifact.market_price == 0
        }
        
        if artifacts_dict[artifact.code_name]:
            artifacts_needing_prices.append({
                'code_name': artifact.code_name,
                'name': artifact.name,
                'artifact_type': artifact.artifact.artifact_type,
                'current_price': artifact.market_price
            })

        # Prepare all artifacts for display (not just those needing prices)
        
        
        all_artifacts_for_display.append({
                'code_name': artifact.code_name,
                'name': artifact.name,
                'artifact_type': artifact.artifact.artifact_type,
                'current_price': artifact.market_price
            })
    
    # Get all ingredient fields (excluding potion sale price fields)
    ingredient_fields = []
    potion_sale_fields = []
    
    for field in potion_input._meta.get_fields():
        if isinstance(field, Field) and field.editable and field.name not in ('id', 'user', 'updated_at'):
            if field.name.startswith('T') and any(potion in field.name for potion in 
                ['ENERGY', 'HEALING', 'GIGANTIFY', 'RESISTANCE', 'ACID', 'CALMING', 
                 'CLEANSING', 'STICKY', 'POISON', 'GATHERING', 'HELLFIRE', 'BERSERK', 
                 'TORNADO', 'INVISIBILITY']):
                potion_sale_fields.append(field)
            else:
                ingredient_fields.append(field)

    # Extract potion name from sale fields like "T4_HEALING_0"
    potion_names_set = set()

    for field in potion_sale_fields:
        parts = field.name.split("_")
        if len(parts) == 3:
            potion_names_set.add(parts[1].capitalize())

    
    # Group ingredient fields by category
    herb_fields = [f for f in ingredient_fields if f.name in 
                   ['agaric', 'comfrey', 'burdock', 'teasel', 'foxglove', 'mullein', 'yarrow']]
    animal_fields = [f for f in ingredient_fields if any(x in f.name for x in ['milk', 'butter', 'eggs'])]
    schnapps_fields = [f for f in ingredient_fields if 
                       'schnapps' in f.name or 'hooch' in f.name or 'moonshine' in f.name]
    other_fields = [f for f in ingredient_fields if 
                    f not in herb_fields + animal_fields + schnapps_fields]
    
    # Prepare data for frontend calculations
    calculation_data = prepare_calculation_data(potion_input, artifacts_dict)
    
    context = {
        'potion_input': potion_input,
        'herb_fields': herb_fields,
        'animal_fields': animal_fields,
        'schnapps_fields': schnapps_fields,
        'other_fields': other_fields,
        'potion_sale_fields': potion_sale_fields,
        'artifacts_needing_prices': artifacts_needing_prices,
        'artifacts_dict': artifacts_dict,
        'all_artifacts': all_artifacts_for_display,
        'recipes_json': json.dumps(potion_recipes),
        'calculation_data_json': json.dumps(calculation_data),
        'tiers': ["T2", "T3", "T4", "T5", "T6", "T7", "T8"],
        'enchant_levels': ["0", "1", "2", "3"],
        'potion_names': sorted(potion_names_set),
    }
    
    return render(request, 'potions/calculator.html', context)


def prepare_calculation_data(potion_input, artifacts_dict):
    """Prepare all data needed for frontend profit calculations"""
    
    # Get all ingredient prices
    ingredient_prices = {}
    
    # Regular ingredients from potion_input
    for field in potion_input._meta.get_fields():
        if isinstance(field, Field) and field.editable and field.name not in ('id', 'user', 'updated_at'):
            value = getattr(potion_input, field.name)
            if value is not None:
                ingredient_prices[field.name] = value
    
    # Animal artifact prices
    for code_name, artifact_data in artifacts_dict.items():
        if artifact_data['market_price'] is not None and artifact_data['market_price'] > 0:
            ingredient_prices[code_name] = artifact_data['market_price']
    
    return {
        'recipes': potion_recipes,
        'ingredient_prices': ingredient_prices,
        'artifacts_info': artifacts_dict
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
        potion_input, _ = PotionInput.objects.get_or_create(user=request.user)
        
        # Reset potion input fields
        for field in potion_input._meta.get_fields():
            if isinstance(field, Field) and field.editable and field.name not in ('id', 'user', 'updated_at'):
                setattr(potion_input, field.name, None)
        
        potion_input.save()
        
        # Reset animal artifact prices
        AnimalArtifactItem.objects.filter(artifact__user=request.user).update(market_price=None)
        
        messages.success(request, "All prices have been reset")
    
    return redirect('potion_calculator')


# Helper function that can be used by templates or other views
def get_user_artifact_prices(user):
    """Get all artifact prices for a user as a dictionary"""
    artifacts = AnimalArtifactItem.objects.filter(
        artifact__user=user
    ).select_related('artifact')
    
    return {
        artifact.code_name: {
            'market_price': artifact.market_price,
            'name': artifact.name,
            'type': artifact.artifact.artifact_type
        }
        for artifact in artifacts
    }


@login_required
@require_GET
def potion_profit_api(request):
    potion_input, _ = PotionInput.objects.get_or_create(user=request.user)
    artifacts_dict = get_user_artifact_prices(request.user)

    calc_data = prepare_calculation_data(potion_input, artifacts_dict)

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


