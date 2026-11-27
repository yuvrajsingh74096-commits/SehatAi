from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

try:
    from app.data.symptoms import SYMPTOMS
except Exception:
    SYMPTOMS = []

try:
    from app.data.nutrition import NUTRITION_ITEMS
except Exception:
    NUTRITION_ITEMS = []


INDIAN_LANGUAGES: list[dict[str, str]] = [
    {"code": "en-IN", "label": "English (India)"},
    {"code": "hi-IN", "label": "हिन्दी (Hindi)"},
    {"code": "bn-IN", "label": "বাংলা (Bengali)"},
    {"code": "ta-IN", "label": "தமிழ் (Tamil)"},
    {"code": "te-IN", "label": "తెలుగు (Telugu)"},
    {"code": "mr-IN", "label": "मराठी (Marathi)"},
    {"code": "gu-IN", "label": "ગુજરાતી (Gujarati)"},
    {"code": "kn-IN", "label": "ಕನ್ನಡ (Kannada)"},
    {"code": "ml-IN", "label": "മലയാളം (Malayalam)"},
    {"code": "pa-IN", "label": "ਪੰਜਾਬੀ (Punjabi)"},
]


@dataclass
class SessionState:
    language: str = "en-IN"
    history: list[dict[str, str]] = field(default_factory=list)
    last_topics: list[str] = field(default_factory=list)


def get_knowledge_counts() -> dict[str, int]:
    return {
        "symptoms": len(SYMPTOMS),
        "nutrition": len(NUTRITION_ITEMS),
        "languages": len(INDIAN_LANGUAGES),
    }


def get_key_status() -> dict[str, Any]:
    return {
        "offline_engine_ready": True,
        "openai_key_set": False,
        "google_key_set": False,
        "status_message": "Key not set — running local sentence-aware mode",
    }


RED_FLAG_PATTERNS = [
    r"\bchest pain\b",
    r"\bshortness of breath\b",
    r"\bdifficulty breathing\b",
    r"\bcan'?t breathe\b",
    r"\bunconscious\b",
    r"\bfainting\b",
    r"\bseizure\b",
    r"\bsevere bleeding\b",
    r"\bstroke\b",
    r"\bsuicid",
]

TOPIC_RULES: list[tuple[str, list[str], str, str]] = [
    (
        "Fever & Infection",
        ["fever", "temperature", "bukhar", "chills", "shivering", "body ache", "body pain"],
        "Track your temperature every 4–6 hours, stay well hydrated with water, ORS, or clear broths, and rest. Avoid self-medicating with unprescribed antibiotics.",
        "Seek prompt medical evaluation if fever is high (above 102°F / 38.9°C), lasts more than 3 days, or comes with rash, confusion, or stiff neck.",
    ),
    (
        "Cough, Cold & Throat",
        ["cough", "cold", "sore throat", "khansi", "congestion", "sneezing", "runny nose", "phlegm"],
        "Warm fluids, steam inhalation, saline gargles, and rest can soothe throat irritation and airway dryness.",
        "Get checked by a doctor if breathing becomes labored, chest tightness appears, or cough persists beyond 2–3 weeks.",
    ),
    (
        "Headache & Dizziness",
        ["headache", "migraine", "sir dard", "dizzy", "dizziness", "lightheaded", "vertigo"],
        "Sit or lie down quietly, drink water, check if you skipped meals or sleep, and limit bright screen strain.",
        "Seek urgent care if a headache starts suddenly and severely, follows a head injury, or occurs with vision changes, weakness, or vomiting.",
    ),
    (
        "Stomach & Digestion",
        ["stomach", "abdomen", "acidity", "gas", "nausea", "vomit", "vomiting", "diarrhea", "loose motion", "pet dard", "constipation"],
        "Favor light, easily digestible meals (like khichdi, banana, rice, curd if tolerated) and sip oral rehydration fluids steadily, especially with loose stools or vomiting.",
        "Consult a clinician promptly for severe sharp abdominal pain, persistent vomiting, blood in stool/vomit, or signs of dehydration.",
    ),
    (
        "Nutrition & Diet",
        ["diet", "nutrition", "food", "eat", "eating", "protein", "iron", "vitamin", "calorie", "meal", "thali", "weight", "anaemia", "anemia"],
        "Build balanced meals around whole grains, pulses/legumes, colorful seasonal vegetables, adequate protein, and clean water; pair iron-rich foods with vitamin C sources.",
        "A doctor or registered dietitian can tailor targets if you manage diabetes, kidney/liver conditions, pregnancy, or significant weight changes.",
    ),
    (
        "Sleep & Fatigue",
        ["tired", "fatigue", "exhausted", "sleep", "insomnia", "weakness", "low energy", "neend"],
        "Keep a consistent sleep-wake schedule, reduce caffeine and screens before bed, and check hydration and regular meal timing.",
        "Discuss persistent fatigue lasting over two weeks with a physician to check basic blood parameters and sleep quality.",
    ),
]


def _extract_clauses(text: str) -> list[str]:
    parts = [p.strip() for p in re.split(r"[.!?\n;]+", text) if p.strip()]
    return parts if parts else [text.strip()]


def process_voice_turn(
    state: SessionState,
    transcript: str,
    language: str | None = None,
) -> dict[str, Any]:
    if language:
        state.language = language

    cleaned = " ".join((transcript or "").strip().split())
    key_info = get_key_status()

    if not cleaned:
        return {
            "language": state.language,
            "input_text": "",
            "detected_topics": [],
            "urgent": False,
            "reply": "I didn't catch a sentence yet. Please speak or type what you are experiencing or ask a health or nutrition question.",
            "follow_up": "You can say something like: 'I have had a mild fever and sore throat since yesterday.'",
            "keys": key_info,
            "key_status": key_info,
            "history": state.history[-10:],
        }

    lowered = cleaned.lower()
    urgent = any(re.search(pat, lowered) for pat in RED_FLAG_PATTERNS)

    matched_topics: list[tuple[str, str, str]] = []
    for topic_name, keywords, guidance, watch_for in TOPIC_RULES:
        if any(re.search(r"\b" + re.escape(kw) + r"\b", lowered) for kw in keywords):
            matched_topics.append((topic_name, guidance, watch_for))

    clauses = _extract_clauses(cleaned)
    topic_names = [t[0] for t in matched_topics]
    if topic_names:
        state.last_topics = topic_names

    response_parts: list[str] = []

    if urgent:
        response_parts.append(
            "Urgent warning: Your message mentions symptoms that can signal a serious condition. "
            "Please seek immediate in-person medical care or emergency services right away rather than waiting."
        )

    if matched_topics:
        summary_focus = ", ".join(topic_names)
        if len(clauses) > 1:
            response_parts.append(
                f"Based on what you shared across {len(clauses)} points regarding {summary_focus}:"
            )
        else:
            response_parts.append(
                f"Based on your statement about {summary_focus}:"
            )

        for topic_name, guidance, watch_for in matched_topics:
            response_parts.append(f"• {topic_name}: {guidance} Watch for: {watch_for}")
    else:
        short_quote = cleaned if len(cleaned) <= 140 else cleaned[:137] + "..."
        response_parts.append(
            f'I processed your input: "{short_quote}". Because this does not match a specific symptom or diet keyword in my local rules yet, '
            "share any specific symptoms (such as fever, pain, cough, digestion, or sleep) or diet goals, along with how long it has been happening."
        )

    reply_text = "\n".join(response_parts)

    state.history.append({"role": "user", "text": cleaned, "language": state.language})
    state.history.append({"role": "assistant", "text": reply_text, "language": state.language})

    return {
        "language": state.language,
        "input_text": cleaned,
        "detected_topics": topic_names,
        "urgent": urgent,
        "reply": reply_text,
        "follow_up": "Would you like to add symptom duration, severity, or ask about food and hydration for this?",
        "keys": key_info,
        "key_status": key_info,
        "history": state.history[-10:],
    }
