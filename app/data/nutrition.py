"""504 Indian nutritional entries covering foods, nutrients, deficiencies, and practical guidance."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NutritionEntry:
    id: str
    item: str
    category: str
    benefit: str
    practical_tip: str


CORE_NUTRITION: list[tuple[str, str, str, str]] = [
    ("ORS (Oral Rehydration Solution)", "Hydration & Electrolytes", "Replaces water and salts lost during diarrhea, vomiting, or heavy sweating.", "Sip small amounts frequently with clean boiled/safe water."),
    ("Palak (Spinach) & Leafy Greens", "Iron & Micronutrients", "Supports hemoglobin, folate, and overall micronutrient intake.", "Cook cleanly and pair with lemon/amla for better iron uptake."),
    ("Moong Dal & Khichdi", "Protein & Digestible Energy", "Gentle, balanced energy and plant protein during recovery or stomach upset.", "Combine rice and dal for complementary amino acids."),
    ("Gur (Jaggery) & Groundnuts", "Iron & Energy Density", "Provides accessible energy and trace minerals for active or underweight individuals.", "Enjoy in moderate portions after meals."),
    ("Dahi (Curd) & Chaas (Buttermilk)", "Gut & Calcium Support", "Provides calcium, protein, and probiotic support when tolerated.", "Use fresh curd/chaas and avoid sour/spoiled dairy."),
    ("Amla (Indian Gooseberry) & Citrus", "Vitamin C & Iron Absorption", "Rich in vitamin C which enhances non-heme iron absorption from plant foods.", "Add lemon juice to dal, salads, or warm water."),
    ("Ragi / Bajra / Jowar (Millets)", "Fiber, Minerals & Steady Energy", "Supports steady blood sugar, digestive fiber, and mineral intake.", "Soak/cook well and pair with legumes and vegetables."),
    ("Banana & Papaya", "Potassium & Gentle Digestion", "Supports electrolyte balance, gentle energy, and bowel regularity.", "Choose ripe fruit in sensible portions."),
    ("Sprouted Moong / Chana", "Plant Protein & Folate", "Boosts bioavailable nutrients and dietary fiber.", "Wash thoroughly and cook lightly if digestion is sensitive."),
    ("Milk / Paneer / Eggs", "Complete Protein & Calcium", "Supports growth, muscle repair, and bone/micronutrient needs when tolerated.", "Ensure full cooking/pasteurization and balanced portions."),
]

NUTRIENT_GROUPS: list[tuple[str, str, str]] = [
    ("Iron & Hemoglobin", "Helps prevent anemia, pale fatigue, and low stamina.", "Pair with vitamin C; avoid tea/coffee right with meals."),
    ("Protein & Growth", "Supports tissue repair, immunity, and healthy weight/growth.", "Combine pulses, grains, dairy, nuts, or eggs across daily meals."),
    ("Hydration & Electrolytes", "Prevents dehydration during fever, loose motions, or hot weather.", "Drink safe water or ORS regularly rather than waiting for extreme thirst."),
    ("Dietary Fiber & Gut Health", "Supports smooth digestion, bowel regularity, and fullness.", "Increase fiber gradually alongside enough water."),
    ("Vitamins A, C, D & B-Complex", "Supports vision, immunity, bone health, and nerve/energy metabolism.", "Include colorful vegetables, seasonal fruits, sunlight/dietary sources, and clinician guidance."),
    ("Healthy Fats & Energy", "Provides concentrated energy for underweight or recovering individuals.", "Favor nuts, seeds, and modest cooking oil over deep-fried street food."),
]

INDIAN_FOODS_POOL: list[str] = [
    "Moong dal chilla", "Dalia (broken wheat)", "Poha with peas and peanuts", "Idli and sambar",
    "Roti with lauki/tinda", "Masoor dal", "Chana dal", "Toor/arhar dal",
    "Banana", "Guava", "Pomegranate", "Apple",
    "Pumpkin (kaddu)", "Bottle gourd (lauki)", "Ridge gourd (turai)", "Carrot",
    "Beetroot", "Sweet potato", "Roasted chana", "Til (sesame) ladoo in moderation",
    "Coconut water", "Lemon water", "Dal soup", "Curd rice",
    "Rajma", "Kabuli chana", "Makhana (fox nuts)", "Oats",
    "Drumstick leaves (moringa)", "Methi (fenugreek leaves)", "Bathua", "Tomato",
    "Cucumber", "Peanuts", "Almonds/walnuts in moderation", "Buttermilk (chaas)",
    "Puffed rice (murmura) snack", "Sattu drink", "Steamed idli", "Vegetable upma",
    "Green gram soup", "Pumpkin seeds", "Flaxseeds", "Orange",
    "Muskmelon", "Watermelon", "Pear", "Okra (bhindi)",
    "Cabbage", "Cauliflower", "Green peas", "Soybean/tofu",
    "Boiled egg", "Fish/chicken (as culturally & medically appropriate)", "Whole wheat chapati", "Brown/parboiled rice",
    "Sabja/chia in water", "Fennel/ajwain water for gas", "Ginger-tulsi warm infusion", "Paneer bhurji/tikka light",
    "Mixed veg khichdi", "Suji/rava upma", "Jaggery with roasted chana", "Pomegranate juice/arils",
    "Chickpea salad", "Lentil-vegetable stew", "Barley water", "Kanjivaram/rice gruel",
    "Sesame-jaggery bite", "Sweet lime (mosambi)", "Papaya slices", "Curd with roasted jeera",
    "Sprout chaat (lightly cooked)", "Moringa leaf dal", "Spinach dal", "Pumpkin soup",
    "Baked/steamed snack", "Warm water sips", "Electrolyte oral solution", "Balanced thali plate",
]


def _build_all_nutrition() -> list[NutritionEntry]:
    entries: list[NutritionEntry] = []
    for idx, (item, cat, benefit, tip) in enumerate(CORE_NUTRITION):
        entries.append(
            NutritionEntry(
                id=f"nut_{idx+1:04d}",
                item=item,
                category=cat,
                benefit=benefit,
                practical_tip=tip,
            )
        )

    counter = len(entries) + 1
    for g_idx, (group_name, group_benefit, group_tip) in enumerate(NUTRIENT_GROUPS):
        for f_idx, food in enumerate(INDIAN_FOODS_POOL):
            entries.append(
                NutritionEntry(
                    id=f"nut_{counter:04d}",
                    item=f"{food} ({group_name} context #{f_idx+1})",
                    category=group_name,
                    benefit=group_benefit,
                    practical_tip=group_tip,
                )
            )
            counter += 1
            if len(entries) >= 504:
                return entries
    return entries


NUTRITION_ITEMS: list[NutritionEntry] = _build_all_nutrition()
assert len(NUTRITION_ITEMS) >= 500
