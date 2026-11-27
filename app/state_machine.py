"""Deterministic dialogue, triage, language, disease, symptom & nutrition engine for SehatAI."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.data.diseases import DISEASES, DiseaseEntry
from app.data.languages import INDIAN_LANGUAGES, detect_indian_language
from app.data.nutrition import NUTRITION_ITEMS
from app.data.symptoms import SYMPTOMS


RED_FLAG_KEYWORDS = [
    "chest pain",
    "seene mein dard",
    "breathing",
    "breathless",
    "sans phool",
    "saans phool",
    "bleeding",
    "khoon",
    "faint",
    "behosh",
    "unconscious",
    "stiff neck",
    "seizure",
    "fit",
    "severe dehydration",
    "chakkar se gir",
    "high fever",
    "tez bukhar",
]

MYTH_RULES = [
    {
        "triggers": ["pani kam", "paani kam", "stop water", "no water", "kam pina", "avoid water"],
        "myth": "Restricting water or fluids during loose motions, vomiting, or fever.",
        "correction": (
            "Cutting back on fluids speeds up dehydration. Sip clean water, ORS, or light broths "
            "regularly unless a doctor gives a specific fluid limit."
        ),
    },
    {
        "triggers": ["ash", "rakh", "cow dung", "gobar", "haldi paste on wound", "local healer", "quack"],
        "myth": "Using ash, cow dung, unsterile applications, or unqualified remedies for rashes, wounds, or disease.",
        "correction": (
            "Unsterile substances can introduce infection and delay proper care. Clean gently with safe "
            "water and consult a qualified medical professional."
        ),
    },
    {
        "triggers": ["starve", "no food", "bhukha", "avoid all food", "khana band", "kam khana"],
        "myth": "Skipping meals or starving during illness, weakness, or low weight.",
        "correction": (
            "Going without food worsens weakness and slows recovery. Small, nutrient-dense, easy-to-digest "
            "meals help the body heal and fight infection."
        ),
    },
]

CONFIDENCE_THRESHOLD = 0.65
MAX_CLARIFYING_TURNS = 3


@dataclass
class SessionState:
    """Bounded per-session state shared across turns."""

    session_id: str
    language: str = "hi"
    language_name: str = "Hindi"
    clarifying_turns_used: int = 0
    collected_slots: dict[str, Any] = field(default_factory=dict)
    confirmed_transcripts: list[str] = field(default_factory=list)
    unconfirmed_notes: list[str] = field(default_factory=list)
    red_flag_detected: bool = False
    completed_summary: dict[str, Any] | None = None


def check_red_flags(text: str) -> bool:
    lowered = text.lower()
    if any(term in lowered for term in RED_FLAG_KEYWORDS):
        return True
    for sym in SYMPTOMS:
        if sym.is_red_flag and any(tok.strip() and tok.strip() in lowered for tok in sym.phrase.split("/")):
            return True
    return False


def match_diseases(history_text: str) -> list[DiseaseEntry]:
    lowered = history_text.lower()
    scored: list[tuple[int, DiseaseEntry]] = []
    for d in DISEASES:
        score = 0
        for word in d.name.lower().replace("(", " ").replace(")", " ").split():
            if len(word) >= 4 and word in lowered:
                score += 2
        for word in d.overview.lower().split():
            if len(word) >= 5 and word in lowered:
                score += 1
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    if scored:
        return [d for _, d in scored[:3]]

    # Fallback matched to broad symptom categories
    if any(k in lowered for k in ["kamzori", "weak", "chakkar", "anemia", "khana", "nutrition", "dubla", "bhukha"]):
        return [d for d in DISEASES if d.id in ("iron_deficiency_anemia", "protein_energy_malnutrition", "vitamin_d_deficiency")][:2]
    if any(k in lowered for k in ["pet", "dast", "ulti", "acidity", "gas", "paani", "pani"]):
        return [d for d in DISEASES if d.id in ("acute_diarrhea", "gastritis_acidity", "dehydration_mild_mod")][:2]
    return [d for d in DISEASES if d.id in ("viral_fever", "iron_deficiency_anemia")][:2]


def match_symptoms(history_text: str) -> list[str]:
    lowered = history_text.lower()
    matched: list[str] = []
    for sym in SYMPTOMS[:120]:
        parts = [p.strip() for p in sym.phrase.split("/") if len(p.strip()) >= 3]
        if any(p in lowered for p in parts):
            matched.append(sym.phrase)
            if len(matched) >= 5:
                break
    return matched


def find_matching_myths(history_text: str) -> list[dict[str, str]]:
    lowered = history_text.lower()
    matched: list[dict[str, str]] = []
    for rule in MYTH_RULES:
        if any(trig in lowered for trig in rule["triggers"]):
            matched.append({"myth": rule["myth"], "correction": rule["correction"]})
    if not matched:
        matched.append(
            {
                "myth": "Ignoring early symptoms or nutritional gaps due to stigma, busy schedules, or home myths.",
                "correction": (
                    "Spotting early signs, maintaining balanced meals and hydration, and consulting a "
                    "qualified clinician early prevents worse outcomes."
                ),
            }
        )
    return matched


def update_slots(state: SessionState, text: str) -> None:
    matched_diseases = match_diseases(text)
    matched_syms = match_symptoms(text)
    if matched_diseases:
        state.collected_slots["possible_conditions"] = [d.name for d in matched_diseases]
    if matched_syms:
        state.collected_slots["matched_symptoms"] = matched_syms
    lowered = text.lower()
    if any(w in lowered for w in ["din", "day", "subah", "kal", "week", "hafta", "month", "mahina"]):
        state.collected_slots["duration_mentioned"] = True
    if any(w in lowered for w in ["chakkar", "dizzy", "kamzori", "weak", "tez", "severe", "badh"]):
        state.collected_slots["severity_mentioned"] = True


def build_four_part_summary(state: SessionState) -> dict[str, Any]:
    combined_text = " ".join(state.confirmed_transcripts)
    diseases = match_diseases(combined_text)
    myths = find_matching_myths(combined_text)
    primary = diseases[0]
    related_names = ", ".join(d.name for d in diseases)

    if state.red_flag_detected:
        urgent_check = (
            f"URGENT WARNING: Potential high-risk signs were mentioned (related areas: {related_names}). "
            "Please visit the nearest 24x7 clinic, CHC, or hospital emergency room immediately."
        )
        next_provider = "Immediate in-person care at a nearby CHC, District Hospital, or Emergency unit."
    else:
        urgent_check = (
            f"Focus Areas ({related_names}): {primary.overview} "
            f"Watch for warning signs: {', '.join(primary.red_flags)}. "
            "Seek urgent medical care right away if severe or worsening signs appear."
        )
        next_provider = primary.provider

    myth_lines = [f"{m['myth']} -> {m['correction']}" for m in myths]
    nutrition_highlights = [f"{n.item}: {n.benefit}" for n in NUTRITION_ITEMS[:3]]
    food_guidance = {
        "favor": list(primary.diet_favor) + nutrition_highlights[:1],
        "avoid": list(primary.diet_avoid),
    }

    visit_summary = {
        "confirmed_points": state.confirmed_transcripts[-4:],
        "unconfirmed_notes": state.unconfirmed_notes,
        "recommended_provider": next_provider,
        "disclaimer": (
            f"SehatAI ({state.language_name}) informational voice guide only—not a medical diagnosis "
            "or prescription. Always consult a qualified healthcare professional."
        ),
    }

    return {
        "urgent_check": urgent_check,
        "myth_and_care": myth_lines,
        "food_and_steps": food_guidance,
        "visit_summary": visit_summary,
    }


def process_voice_turn(
    state: SessionState,
    transcript: str,
    confidence: float,
    noise_level: str,
    requested_language: str | None = None,
) -> dict[str, Any]:
    """Execute one deterministic voice turn according to SehatAI rules."""
    cleaned = transcript.strip()
    lang_info = detect_indian_language(cleaned, requested_language or state.language)
    state.language = lang_info.code
    state.language_name = lang_info.name

    # 1. Handle high background noise explicitly
    if noise_level == "high":
        state.unconfirmed_notes.append(f"High background noise during turn: '{cleaned or '[unclear]'}'")
        return {
            "action": "noise_prompt",
            "spoken_response": (
                "Aas-paas ka shor kaafi zyada hai, isliye awaaz saaf nahi aa rahi. "
                "Kripya thodi shaant jagah par jaayein ya phone ko muh ke paas laakar dobara bolein."
            ),
            "ui_banner": "High background noise detected — move to a quieter spot and tap Speak.",
            "session": _serialize_state(state),
        }

    # 2. Handle low speech recognition confidence or empty utterance
    if not cleaned or confidence < CONFIDENCE_THRESHOLD:
        state.unconfirmed_notes.append(f"Low-confidence audio ({confidence:.2f}): '{cleaned}'")
        return {
            "action": "confirm_prompt",
            "spoken_response": (
                f"Mujhe poori baat saaf sunai nahi di. Kya aapne kaha: '{cleaned or 'kuch takleef hai'}'? "
                "Kripya sirf woh chhota hissa dobara bolein."
            ),
            "ui_banner": f"Low recognition confidence ({confidence:.2f}) — please confirm or repeat briefly.",
            "choices": [
                "Bukhar, pet ya dast ki takleef hai",
                "Kamzori, chakkar ya nutrition/khane ki salah chahiye",
                "Gale, khansi, rash ya koi private/sensitive baat hai",
            ],
            "session": _serialize_state(state),
        }

    # 3. Record confirmed transcript and check red flags first
    state.confirmed_transcripts.append(cleaned)
    update_slots(state, cleaned)
    if check_red_flags(cleaned):
        state.red_flag_detected = True

    # 4. Ask at most one focused question per turn up to MAX_CLARIFYING_TURNS
    if not state.red_flag_detected and state.clarifying_turns_used < MAX_CLARIFYING_TURNS:
        state.clarifying_turns_used += 1
        if state.clarifying_turns_used == 1:
            follow_up = (
                "Maine aapki baat sun li. Yeh takleef kab se shuru hui hai, "
                "aur kya aapko bukhar, kamzori, ulti, dast, ya koi aur lakshan bhi hai?"
            )
        elif state.clarifying_turns_used == 2:
            follow_up = (
                "Samajh gaya. Kya yeh din-ba-din badh rahi hai, aur aapka rozana ka "
                "khana-peena kaisa chal raha hai—kya kisi myth ya gharelu nuskhe ki baat bhi hai?"
            )
        else:
            follow_up = (
                "Ek aakhiri baat: kya aap kisi sharam, sankoch, ya chinta ki wajah se "
                "doctor ko dikhane mein rukawat mehsoos kar rahe hain?"
            )

        return {
            "action": "clarify",
            "spoken_response": follow_up,
            "ui_banner": f"Clarifying question {state.clarifying_turns_used} of {MAX_CLARIFYING_TURNS} ({lang_info.name})",
            "session": _serialize_state(state),
        }

    # 5. Produce the four-part care summary
    summary = build_four_part_summary(state)
    state.completed_summary = summary
    spoken_recap = (
        f"{summary['urgent_check']} "
        f"Misconception check: {summary['myth_and_care'][0]} "
        f"Next step: {summary['visit_summary']['recommended_provider']} "
        f"{summary['visit_summary']['disclaimer']}"
    )

    return {
        "action": "summary",
        "spoken_response": spoken_recap,
        "ui_banner": f"Care guidance ready ({lang_info.name}) — review or replay audio summary.",
        "summary": summary,
        "session": _serialize_state(state),
    }


def _serialize_state(state: SessionState) -> dict[str, Any]:
    return {
        "session_id": state.session_id,
        "language": state.language,
        "language_name": state.language_name,
        "clarifying_turns_used": state.clarifying_turns_used,
        "max_clarifying_turns": MAX_CLARIFYING_TURNS,
        "collected_slots": state.collected_slots,
        "confirmed_turns_count": len(state.confirmed_transcripts),
        "unconfirmed_notes_count": len(state.unconfirmed_notes),
        "red_flag_detected": state.red_flag_detected,
    }


def get_knowledge_counts() -> dict[str, int]:
    return {
        "scheduled_indian_languages": len(INDIAN_LANGUAGES),
        "diseases": len(DISEASES),
        "symptoms": len(SYMPTOMS),
        "nutrition_entries": len(NUTRITION_ITEMS),
    }
