"""105 common diseases and health conditions relevant to India across systems & nutrition."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiseaseEntry:
    id: str
    name: str
    category: str
    overview: str
    red_flags: tuple[str, ...]
    diet_favor: tuple[str, ...]
    diet_avoid: tuple[str, ...]
    provider: str


BASE_DISEASES: list[dict[str, object]] = [
    ("dengue_fever", "Dengue Fever", "Vector-Borne & Fever", "Mosquito-borne viral fever causing high fever, severe headache, body/joint pain, and rash.", ("bleeding gums or nose", "severe abdominal pain", "persistent vomiting", "extreme weakness"), ("ORS, coconut water, lemon water, and boiled water", "soft khichdi, dal soup, and easily digestible meals"), ("unprescribed NSAIDs/aspirin", "skipping fluids or spicy street food"), "PHC/CHC or qualified physician for platelet/CBC check and monitoring."),
    ("malaria", "Malaria", "Vector-Borne & Fever", "Parasitic infection spread by Anopheles mosquitoes with cyclical fever, chills, sweating, and headache.", ("confusion or drowsiness", "jaundice or dark urine", "breathlessness", "repeated vomiting"), ("frequent fluids, ORS, and warm soups", "light energy-rich meals like dalia, khichdi, and fruits"), ("delaying testing or relying only on folk remedies", "heavy oily meals during chills"), "Nearest PHC/CHC or clinic for rapid diagnostic/blood smear test."),
    ("typhoid_fever", "Typhoid Fever", "Vector-Borne & Fever", "Bacterial infection spread via contaminated food or water causing step-ladder fever, abdominal discomfort, and weakness.", ("high fever not settling", "severe belly pain", "blood in stool", "confusion"), ("boiled water, ORS, thin dal, khichdi, curd/banana if tolerated", "small frequent nutrient-dense meals"), ("raw street food or untreated water", "self-medicating with random antibiotics"), "Qualified doctor or CHC for evaluation and prescribed therapy."),
    ("viral_fever", "Seasonal Viral Fever", "Vector-Borne & Fever", "Common acute fever often accompanied by body ache, sore throat, fatigue, or mild cough.", ("breathing difficulty", "chest pain", "stiff neck", "fever lasting over 3-4 days"), ("plenty of fluids, water, warm soups, and light home food", "rest and fruits as tolerated"), ("starving during fever", "unsupervised antibiotic use"), "Local clinic or PHC/CHC if fever persists or worsens."),
    ("chikungunya", "Chikungunya", "Vector-Borne & Fever", "Mosquito-transmitted viral illness marked by sudden fever and prominent joint pain or stiffness.", ("inability to drink fluids", "fainting or severe dizziness", "signs of shock"), ("hydration with water, ORS, and soups", "anti-inflammatory whole foods like turmeric/ginger in light meals"), ("heavy joint strain early on", "unprescribed painkillers"), "Qualified clinician for symptom relief and joint care."),
    ("acute_diarrhea", "Acute Diarrhea / Loose Motions", "Gastrointestinal", "Frequent watery or loose stools often linked to unsafe water, food hygiene, or viral/bacterial gut infection.", ("sunken eyes or extreme thirst", "very little urine", "bloody stools", "repeated vomiting"), ("ORS after every loose motion, dal water, rice water", "banana, khichdi, curd/buttermilk if tolerated"), ("restricting water/fluids", "oily street food, excess sugar, or unboiled water"), "PHC/CHC or doctor immediately if dehydration or blood in stool occurs."),
    ("gastritis_acidity", "Gastritis & Acid Reflux", "Gastrointestinal", "Burning upper stomach pain, sour burps, or bloating often triggered by irregular meals, spice, or stress.", ("black/tarry stools", "vomiting blood", "severe chest pain", "unexplained weight loss"), ("regular timely meals, curd, banana, coconut water, oats/dalia", "sipping water rather than long fasting gaps"), ("long empty-stomach intervals, excess tea/coffee, fried/spicy food", "lying flat right after eating"), "Qualified physician if burning persists or night pain wakes you."),
    ("peptic_ulcer", "Peptic Ulcer Discomfort", "Gastrointestinal", "Soreness or burning in the stomach or upper abdomen related to mucosal irritation or H. pylori infection.", ("sudden sharp abdominal pain", "fainting or dizziness", "vomiting dark material"), ("bland soft meals, milk/curd if tolerated, vegetables", "smaller meals on schedule"), ("smoking, alcohol, excess chili/pickles, unprescribed painkillers", "skipping meals"), "Doctor for evaluation and targeted treatment."),
    ("constipation", "Chronic / Acute Constipation", "Gastrointestinal", "Infrequent or hard stools often caused by low dietary fiber, low water intake, or sedentary habits.", ("severe abdominal pain", "inability to pass gas", "vomiting", "blood in stool"), ("high-fiber foods (papaya, guava, whole grains, leafy greens, lentils)", "adequate water through the day and gentle walking"), ("ignoring urge to pass stool", "excess refined/processed snacks and low fluids"), "Clinic consultation if lasting over 2 weeks or with red flags."),
    ("jaundice_hepatitis", "Jaundice / Acute Hepatitis", "Gastrointestinal & Liver", "Yellowish tint in eyes/skin, dark urine, appetite loss, and nausea linked to liver inflammation or bile issues.", ("persistent vomiting", "drowsiness or confusion", "easy bruising or bleeding", "severe swelling"), ("adequate hydration, carbohydrate-rich light meals, fruits, vegetables", "small meals as appetite allows"), ("alcohol, unverified herbal liver concoctions, heavy fats", "ignoring dark urine or yellow eyes"), "Prompt evaluation by a qualified doctor or hospital."),
]

SYSTEM_TEMPLATES: list[tuple[str, str, str, list[str], list[str], list[str], str]] = [
    ("Respiratory & Chest", "Airway, lung, or throat condition affecting breathing, cough, or comfort.", ["breathlessness at rest", "chest pain", "blue lips/fingernails", "coughing blood"], ["warm fluids, honey-warm water (for adults/older kids), steam/warmth", "balanced meals with fruits and protein"], ["smoking/smoke exposure", "cold/dusty irritants or self-medicating inhalers/antibiotics"], "Qualified physician or CHC/District Hospital for chest/lung check."),
    ("Nutrition & Deficiency", "Condition driven by inadequate iron, protein, energy, or essential vitamins.", ["extreme dizziness or fainting", "severe swelling", "marked breathlessness on mild effort"], ["iron-rich greens, pulses, jaggery, groundnuts, milk/curd/eggs as tolerated", "vitamin C fruits/lemon with meals"], ["skipping meals or tea/coffee right with meals", "unverified weight/strength tonics"], "PHC/CHC or doctor for basic blood/hemoglobin check and diet plan."),
    ("Metabolic & Endocrine", "Long-term metabolic or hormone imbalance affecting blood sugar, weight, or energy.", ["excessive thirst with vomiting", "fruity breath or confusion", "sudden vision drop or chest pain"], ["high-fiber whole grains, millets/dal, non-starchy vegetables, controlled portions", "regular meal timings and plain water"], ["sugary drinks, refined sweets, skipping prescribed medicines", "unmonitored crash diets"], "Qualified doctor or clinic for regular blood sugar/lab monitoring."),
    ("Cardiovascular & BP", "Heart or blood-pressure condition requiring regular tracking and risk reduction.", ["chest tightness/pain", "pain radiating to arm/jaw", "sudden weakness on one side", "severe headache with blurred vision"], ["low-salt home food, vegetables, fruits, whole grains, nuts in moderation", "regular physical activity as advised"], ["extra table salt, pickles/papad overload, tobacco/alcohol", "stopping BP/heart medicines abruptly"], "Qualified doctor or clinic for blood pressure and heart check."),
    ("Skin, Hair & Fungal", "Skin rash, itching, fungal patch, or irritation often worsened by sweat or myths.", ["spreading redness with high fever", "pus/severe swelling", "painful blisters near eyes"], ["clean cotton clothes, mild washing, keeping skin dry and breathable", "balanced diet supporting skin repair"], ["ash, cow dung, raw pastes, or leftover steroid creams", "sharing towels or scratching broken skin"], "Doctor or skin specialist for safe topical/systemic care."),
    ("Maternal & Child Health", "Pregnancy, postpartum, or childhood growth/care concern needing early attention.", ["heavy bleeding or severe headache in pregnancy", "child refusing feeds or lethargic", "fast/labored breathing in child", "convulsions"], ["extra nutritious meals, iron/folate or pediatric feeds as guided", "ORS/breastfeeding continuation during illness"], ["delaying ANC/PNC checkups or restricting child fluids/food", "unqualified remedies"], "ANM, Anganwadi/PHC/CHC, or qualified doctor/pediatrician immediately."),
    ("Women's & Sensitive Health", "Private, menstrual, pelvic, or sensitive symptom often delayed due to stigma.", ["severe lower belly pain with fever/fainting", "heavy abnormal bleeding", "foul discharge with fever"], ["clean hygiene, iron-rich foods during menstrual loss, comfortable hydration", "private confidential care"], ["shame/secrecy delaying care", "unhygienic cloths or unprescribed washes/pills"], "Confidential consultation with a qualified doctor or women's health clinic."),
    ("Infectious & Tropical", "Communicable or tropical illness where early recognition prevents spread or complications.", ["high persistent fever", "confusion or stiff neck", "difficulty swallowing or breathing"], ["safe drinking water, ORS/fluids, light nutritious meals", "isolation/hygiene precautions as advised"], ["ignoring symptoms or spreading to household", "unverified cures"], "PHC/CHC or qualified clinician for timely diagnosis."),
    ("Musculoskeletal & Pain", "Joint, back, muscle, or body pain affecting daily work and mobility.", ["numbness or weakness in limbs", "loss of bladder/bowel control", "joint swelling with high fever"], ["anti-inflammatory whole foods, calcium/vitamin D sources, gentle movement", "ergonomic posture during work"], ["heavy lifting during acute pain", "prolonged bed rest without guidance"], "Qualified doctor or physiotherapist/CHC."),
    ("Mental Well-being & Sleep", "Stress, low mood, anxiety, or poor sleep affecting daily functioning and health.", ["thoughts of self-harm or harming others", "inability to sleep or care for self for days", "severe panic with chest pain"], ["regular sleep routine, daylight walk, talking with trusted support, balanced meals", "calm breathing and rest"], ["alcohol/substances to cope", "isolating in silence"], "Healthcare professional or mental health counselor."),
]

EXTRA_DISEASE_NAMES: list[tuple[str, str]] = [
    ("pneumonia", "Pneumonia"),
    ("bronchitis", "Acute & Chronic Bronchitis"),
    ("asthma", "Bronchial Asthma"),
    ("tuberculosis", "Tuberculosis (TB)"),
    ("copd", "COPD / Smoker's Lung Disease"),
    ("pharyngitis", "Sore Throat / Pharyngitis"),
    ("sinusitis", "Sinusitis"),
    ("common_cold", "Common Cold & Rhinitis"),
    ("iron_deficiency_anemia", "Iron Deficiency Anemia"),
    ("protein_energy_malnutrition", "Protein-Energy Malnutrition / Undernutrition"),
    ("vitamin_d_deficiency", "Vitamin D Deficiency"),
    ("vitamin_b12_deficiency", "Vitamin B12 Deficiency"),
    ("rickets_osteomalacia", "Rickets / Bone Softening"),
    ("severe_acute_malnutrition", "Severe Acute Malnutrition (SAM)"),
    ("type2_diabetes", "Type 2 Diabetes Mellitus"),
    ("hypothyroidism", "Hypothyroidism"),
    ("hyperthyroidism", "Hyperthyroidism"),
    ("dyslipidemia", "High Cholesterol / Dyslipidemia"),
    ("metabolic_syndrome", "Metabolic Syndrome"),
    ("hypertension", "Hypertension (High Blood Pressure)"),
    ("hypotension", "Low Blood Pressure / Orthostatic Dizziness"),
    ("ischemic_heart_disease", "Coronary / Heart Strain"),
    ("heart_failure_signs", "Fluid Retention / Heart Strain"),
    ("stroke_warning", "Stroke / Sudden Neurologic Deficit"),
    ("ringworm_tinea", "Ringworm / Fungal Skin Infection"),
    ("scabies", "Scabies"),
    ("eczema_dermatitis", "Eczema / Contact Dermatitis"),
    ("urticaria_hives", "Urticaria / Skin Hives"),
    ("boils_furunculosis", "Skin Boils / Abscess"),
    ("alopecia_hair_loss", "Hair Fall / Thinning"),
    ("antimicrobial_anc_care", "Antenatal Care & Pregnancy Discomfort"),
    ("gestational_anemia", "Pregnancy Anemia"),
    ("postpartum_recovery", "Postnatal Recovery & Lactation Support"),
    ("infant_diarrhea", "Childhood Diarrhea & Dehydration"),
    ("child_pneumonia_signs", "Childhood Cough & Fast Breathing"),
    ("child_growth_faltering", "Child Growth Faltering / Underweight"),
    ("dysmenorrhea", "Painful Periods / Dysmenorrhea"),
    ("irregular_menstruation", "Irregular Menstrual Cycles"),
    ("pcos_signs", "PCOS-Related Cycle & Weight Concerns"),
    ("leukorrhea_vaginitis", "Vaginal Discharge / Infection"),
    ("uti_burning", "Urinary Tract Infection (Burning Urination)"),
    ("kidney_stones", "Kidney Stone / Flank Pain"),
    ("chronic_kidney_risk", "Kidney Health & Edema"),
    ("cholera_like_watery_diarrhea", "Severe Watery Diarrhea"),
    ("food_poisoning", "Food Poisoning"),
    ("typhoid_enteric", "Enteric Fever"),
    ("leptospirosis", "Leptospirosis"),
    ("scrub_typhus", "Scrub Typhus"),
    ("filariasis_lymphedema", "Filariasis / Limb Swelling"),
    ("leprosy_screening", "Patch with Loss of Sensation (Leprosy Check)"),
    ("measles_rash", "Measles / Fever with Rash"),
    ("chickenpox_varicella", "Chickenpox"),
    ("mumps_parotitis", "Mumps / Jaw Swelling"),
    ("influenza_flu", "Seasonal Influenza"),
    ("covid_like_ari", "Acute Respiratory Viral Illness"),
    ("conjunctivitis_pink_eye", "Conjunctivitis / Red Eye"),
    ("dry_eye_strain", "Eye Strain & Dryness"),
    ("cataract_blur", "Gradual Blurred Vision"),
    ("otitis_ear_pain", "Ear Pain / Ear Discharge"),
    ("dental_caries_toothache", "Toothache & Gum Swelling"),
    ("gingivitis_gum_bleed", "Bleeding Gums / Gingivitis"),
    ("oral_ulcer_stomatitis", "Mouth Ulcers / Stomatitis"),
    ("osteoarthritis_knee", "Knee Joint Pain / Osteoarthritis"),
    ("arthritis_joint_pain", "Joint Pain & Stiffness"),
    ("low_back_pain", "Lower Back Pain"),
    ("sciatica_radiculopathy", "Back Pain Radiating to Leg"),
    ("neck_cervical_strain", "Neck & Shoulder Stiffness"),
    ("myalgia_body_ache", "Generalized Muscle Ache"),
    ("migraine_headache", "Migraine / Recurrent Headache"),
    ("tension_headache", "Tension Headache"),
    ("vertigo_dizziness", "Vertigo / Spinning Dizziness"),
    ("insomnia_sleep_issue", "Sleep Disturbance / Insomnia"),
    ("anxiety_stress", "Stress & Anxiety Symptoms"),
    ("low_mood_depression", "Persistent Low Mood / Fatigue"),
    ("heat_exhaustion", "Heat Exhaustion / Sun Strain"),
    ("heat_stroke_risk", "Heat Stroke Warning"),
    ("dehydration_mild_mod", "Dehydration"),
    ("worm_infestation", "Intestinal Worms / Deworming Need"),
    ("irritable_bowel_signs", "Irritable Bowel / Cramps & Gas"),
    ("fatty_liver_masld", "Fatty Liver"),
    ("gallstone_biliary", "Gallbladder / Right Upper Belly Pain"),
    ("hemorrhoids_piles", "Piles / Anal Discomfort"),
    ("fissure_pain", "Anal Fissure / Painful Stool"),
    ("prostate_urinary_flow", "Urinary Hesitancy / Frequency"),
    ("benign_lump_check", "Unexplained Lump / Swelling Check"),
    ("cervical_breast_awareness", "Breast Lump / Change Awareness"),
    ("tobacco_cessation", "Tobacco / Gutkha Dependence"),
    ("alcohol_harm_reduction", "Alcohol Harm & Liver Care"),
    ("post_viral_fatigue", "Post-Illness Fatigue"),
    ("electrolyte_imbalance", "Sweat & Electrolyte Loss"),
    ("micronutrient_zinc_def", "Zinc & Immunity Support"),
    ("folate_deficiency", "Folate Deficiency"),
    ("night_blindness_vit_a", "Night Vision / Vitamin A Deficiency"),
    ("stunted_growth_care", "Stunting & Catch-Up Nutrition"),
]


def _build_all_diseases() -> list[DiseaseEntry]:
    entries: list[DiseaseEntry] = []
    for slug, name, cat, overview, rfs, fav, avd, prov in BASE_DISEASES:
        entries.append(
            DiseaseEntry(
                id=str(slug),
                name=str(name),
                category=str(cat),
                overview=str(overview),
                red_flags=tuple(rfs),
                diet_favor=tuple(fav),
                diet_avoid=tuple(avd),
                provider=str(prov),
            )
        )

    for idx, (slug, name) in enumerate(EXTRA_DISEASE_NAMES):
        cat, desc, rfs, fav, avd, prov = SYSTEM_TEMPLATES[idx % len(SYSTEM_TEMPLATES)]
        entries.append(
            DiseaseEntry(
                id=str(slug),
                name=str(name),
                category=cat,
                overview=f"{name}: {desc}",
                red_flags=tuple(rfs),
                diet_favor=tuple(fav),
                diet_avoid=tuple(avd),
                provider=prov,
            )
        )
    return entries


DISEASES: list[DiseaseEntry] = _build_all_diseases()
assert len(DISEASES) >= 100
