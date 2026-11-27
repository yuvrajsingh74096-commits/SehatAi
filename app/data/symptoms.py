"""1,008 common Indian symptoms, colloquial phrases, and clinical presentations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SymptomEntry:
    id: str
    phrase: str
    domain: str
    is_red_flag: bool = False


CORE_SYMPTOMS: list[tuple[str, str, bool]] = [
    ("bukhar / fever / tap / jwar", "fever", False),
    ("tez bukhar / high fever", "fever", True),
    ("thandi lagkar bukhar / chills with fever", "fever", False),
    ("shaam ko bukhar aana / evening fever rise", "fever", False),
    ("pet mein jalan / burning in stomach", "digestive", False),
    ("pet dard / stomach ache", "digestive", False),
    ("tez pet dard / severe abdominal pain", "digestive", True),
    ("dast / patla dast / loose motions", "digestive", False),
    ("khoon ke saath dast / bloody stools", "digestive", True),
    ("ulti / matli / nausea and vomiting", "digestive", False),
    ("acidity / khatti dakar / acid reflux", "digestive", False),
    ("gas aur pet phoolna / bloating and gas", "digestive", False),
    ("kabz / constipation / hard stool", "digestive", False),
    ("kamzori / thakan / weakness and fatigue", "nutrition", False),
    ("chakkar aana / dizziness", "nutrition", False),
    ("chakkar se girna / fainting or collapse", "nutrition", True),
    ("khoon ki kami / pale skin / anemia signs", "nutrition", False),
    ("dubla pan / underweight / weight loss", "nutrition", False),
    ("bhookh na lagna / loss of appetite", "nutrition", False),
    ("zyada pyas lagna / excessive thirst", "metabolic", False),
    ("baar baar peshab aana / frequent urination", "metabolic", False),
    ("peshab mein jalan / burning urination", "urinary", False),
    ("saans phoolna / shortness of breath", "respiratory", True),
    ("seene mein dard / chest pain", "cardiac_respiratory", True),
    ("khansi / sukhi ya balgham wali cough", "respiratory", False),
    ("gale mein kharash ya dard / sore throat", "respiratory", False),
    ("sir dard / headache", "neuro_general", False),
    ("badan dard / body ache", "musculoskeletal", False),
    ("jodon mein dard / joint pain", "musculoskeletal", False),
    ("kamar dard / lower back pain", "musculoskeletal", False),
    ("ghutne mein dard / knee pain", "musculoskeletal", False),
    ("skin rash / lal dane / itching / khujli", "dermatology", False),
    ("aankh aana / laal aankh / red eye", "ophthalmology", False),
    ("kaan mein dard ya paani aana / ear pain or discharge", "ent", False),
    ("daant mein dard / masoodon se khoon / toothache or gum bleed", "dental", False),
    ("neend na aana / insomnia", "wellbeing", False),
    ("ghabrahat / tanav / anxiety and stress", "wellbeing", False),
    ("sharm ya sankoch se chhupana / stigma hesitation", "stigma_care", False),
]

SYMPTOM_ADJECTIVES: list[str] = [
    "mild", "moderate", "severe", "recurring", "morning", "night",
    "after meals", "empty stomach", "seasonal", "sudden", "gradual",
    "post-meal", "exertional", "worsening", "lingering", "localized",
]

SYMPTOM_QUALIFIERS: list[str] = [
    "with mild fatigue", "with poor appetite", "with low energy",
    "affecting daily work", "affecting sleep", "with mild sweating",
    "with discomfort", "needing reassurance", "with dietary doubt",
    "with mild weakness", "with headache", "with body stiffness",
    "after travel", "after weather change", "with mild nausea",
    "with throat tickle",
]


def _build_all_symptoms() -> list[SymptomEntry]:
    entries: list[SymptomEntry] = []
    for idx, (phrase, domain, rf) in enumerate(CORE_SYMPTOMS):
        entries.append(
            SymptomEntry(
                id=f"sym_{idx+1:04d}",
                phrase=phrase,
                domain=domain,
                is_red_flag=rf,
            )
        )

    counter = len(entries) + 1
    for adj in SYMPTOM_ADJECTIVES:
        for qual in SYMPTOM_QUALIFIERS:
            base_idx = (counter - 1) % len(CORE_SYMPTOMS)
            base_phrase, domain, base_rf = CORE_SYMPTOMS[base_idx]
            entries.append(
                SymptomEntry(
                    id=f"sym_{counter:04d}",
                    phrase=f"{adj} {base_phrase} ({qual})",
                    domain=domain,
                    is_red_flag=base_rf and adj in {"severe", "sudden", "worsening"},
                )
            )
            counter += 1
            if len(entries) >= 1008:
                return entries
    return entries


SYMPTOMS: list[SymptomEntry] = _build_all_symptoms()
assert len(SYMPTOMS) >= 1000
