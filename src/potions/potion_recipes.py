# potions/potion_recipes.py

_raw_potion_recipes = {
    "T2_ENERGY_0": [("agaric", 8)],
    "T2_HEALING_0": [("agaric", 8)],
    "T3_GIGANTIFY_0": [("comfrey", 8)],
    "T3_RESISTANCE_0": [("comfrey", 8)],
    "T3_STICKY_0": [("comfrey", 8)],
    "T3_ACID_0": [("t3spirit", 1), ("comfrey", 16)],
    "T3_CALMING_0": [("t3shadow", 1), ("comfrey", 16)],
    "T3_CLEANSING_0": [("t3root", 1), ("comfrey", 16)],
    "T4_BERSERK_0": [("t3werewolf", 1), ("burdock", 16)],
    "T4_POISON_0": [("burdock", 8), ("comfrey", 4)],
    "T4_ENERGY_0": [("burdock", 24), ("goat_milk", 6)],
    "T4_GATHERING_0": [("t3runestone", 1), ("goat_butter", 16)],
    "T4_HEALING_0": [("burdock", 24), ("hen_eggs", 6)],
    "T4_HELLFIRE_0": [("t3imp", 1), ("goat_milk", 16)],
    "T4_TORNADO_0": [("t3dawn", 1), ("burdock", 16)],
    "T5_ACID_0": [("t5spirit", 1), ("teasel", 48), ("burdock", 24), ("goat_milk", 12)],
    "T5_CLEANSING_0": [("t5root", 1), ("teasel", 48), ("comfrey", 24), ("goat_butter", 12)],
    "T5_CALMING_0": [("t5shadow", 1), ("teasel", 48), ("burdock", 24), ("agaric", 12)],
    "T5_GIGANTIFY_0": [("teasel", 24), ("burdock", 12), ("goose_eggs", 6)],
    "T5_STICKY_0": [("teasel", 24), ("comfrey", 12), ("goose_eggs", 6)],
    "T5_RESISTANCE_0": [("teasel", 24), ("comfrey", 12), ("goat_milk", 6)],
    "T6_BERSERK_0": [("t5werewolf", 1), ("foxglove", 48), ("agaric", 24), ("potato_schnapps", 12)],
    "T6_POISON_0": [("foxglove", 24), ("teasel", 12), ("comfrey", 12), ("sheep_milk", 6)],
    "T6_ENERGY_0": [("foxglove", 72), ("sheep_milk", 18), ("potato_schnapps", 18)],
    "T6_GATHERING_0": [("t5runestone", 1), ("foxglove", 24), ("sheep_butter", 48), ("teasel", 12)],
    "T6_HEALING_0": [("foxglove", 72), ("potato_schnapps", 18), ("goose_eggs", 18)],
    "T6_HELLFIRE_0": [("t5imp", 1), ("foxglove", 24), ("sheep_milk", 48), ("hen_eggs", 12)],
    "T6_TORNADO_0": [("t5dawn", 1), ("foxglove", 48), ("teasel", 24), ("hen_eggs", 12)],
    "T7_ACID_0": [("t7spirit", 1), ("mullein", 144), ("foxglove", 72), ("potato_schnapps", 72), ("sheep_milk", 36), ("corn_hooch", 36)],
    "T7_CLEANSING_0": [("t7root", 1), ("mullein", 144), ("burdock", 72), ("comfrey", 72), ("sheep_butter", 36), ("corn_hooch", 36)],
    "T7_CALMING_0": [("t7shadow", 1), ("mullein", 144), ("foxglove", 72), ("comfrey", 72), ("agaric", 36), ("corn_hooch", 36)],
    "T7_GIGANTIFY_0": [("mullein", 72), ("foxglove", 36), ("goose_eggs", 18), ("corn_hooch", 18)],
    "T7_STICKY_0": [("mullein", 72), ("foxglove", 36), ("burdock", 36), ("goose_eggs", 18), ("corn_hooch", 18)],
    "T7_RESISTANCE_0": [("mullein", 72), ("foxglove", 36), ("burdock", 36), ("sheep_milk", 18), ("corn_hooch", 18)],
    "T8_BERSERK_0": [("t7werewolf", 1), ("yarrow", 144), ("comfrey", 72), ("potato_schnapps", 72), ("corn_hooch", 36), ("pumpkin_moonshine", 36)],
    "T8_INVISIBILITY_0": [("yarrow", 72), ("teasel", 36), ("mullein", 36), ("cow_milk", 18), ("pumpkin_moonshine", 18)],
    "T8_POISON_0": [("yarrow", 72), ("teasel", 36), ("mullein", 36), ("cow_milk", 18), ("pumpkin_moonshine", 18)],
    "T8_GATHERING_0": [("t7runestone", 1), ("yarrow", 72), ("cow_butter", 144), ("mullein", 72), ("foxglove", 36), ("pumpkin_moonshine", 36)],
    "T8_HELLFIRE_0": [("t7imp", 1), ("yarrow", 72), ("cow_milk", 144), ("mullein", 72), ("goose_eggs", 36), ("pumpkin_moonshine", 36)],
    "T8_TORNADO_0": [("t7dawn", 1), ("yarrow", 144), ("mullein", 72), ("corn_hooch", 72), ("goose_eggs", 36), ("pumpkin_moonshine", 36)],
}

_potion_extracts = {
    "T2_ENERGY": 5,
    "T2_HEALING": 5,
    "T3_GIGANTIFY": 5,
    "T3_RESISTANCE": 5,
    "T3_STICKY": 5,
    "T3_ACID": 10,
    "T3_CALMING": 10,
    "T3_CLEANSING": 10,
    "T4_BERSERK": 10,
    "T4_POISON": 5,
    "T4_ENERGY": 15,
    "T4_GATHERING": 10,
    "T4_HEALING": 15,
    "T4_HELLFIRE": 10,
    "T4_TORNADO": 10,
    "T5_ACID": 30,
    "T5_CLEANSING": 30,
    "T5_CALMING": 30,
    "T5_GIGANTIFY": 15,
    "T5_STICKY": 15,
    "T5_RESISTANCE": 15,
    "T6_BERSERK": 30,
    "T6_POISON": 15,
    "T6_ENERGY": 45,
    "T6_GATHERING": 30,
    "T6_HEALING": 45,
    "T6_HELLFIRE": 30,
    "T6_TORNADO": 30,
    "T7_ACID": 90,
    "T7_CLEANSING": 90,
    "T7_CALMING": 90,
    "T7_GIGANTIFY": 45,
    "T7_STICKY": 45,
    "T7_RESISTANCE": 45,
    "T8_BERSERK": 90,
    "T8_INVISIBILITY": 45,
    "T8_POISON": 45,
    "T8_GATHERING": 90,
    "T8_HELLFIRE": 90,
    "T8_TORNADO": 90
}

potion_recipes = {}

for code, ingredients in _raw_potion_recipes.items():
    has_artifact = any(ing[0].startswith(("t3", "t4", "t5", "t6", "t7", "t8")) for ing in ingredients)
    yield_qty = 10 if has_artifact else 5

    recipe = {
        "ingredients": ingredients,
        "yield": yield_qty,
    }

    # Only add extracts for base enchant version (_0)
    if code.endswith("_0"):
        tier_name_key = code.rsplit("_", 1)[0]  # e.g. "T6_POISON"
        recipe["extracts"] = _potion_extracts.get(tier_name_key, 0)

    potion_recipes[code] = recipe

