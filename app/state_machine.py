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
    {"code": "en-IN", "label": "English"},
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

SUPPORTED_CODES = {item["code"] for item in INDIAN_LANGUAGES}


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


def detect_language(text: str, fallback: str = "en-IN") -> str:
    if not text:
        return fallback if fallback in SUPPORTED_CODES else "en-IN"

    if re.search(r"[\u0980-\u09FF]", text):
        return "bn-IN"
    if re.search(r"[\u0B80-\u0BFF]", text):
        return "ta-IN"
    if re.search(r"[\u0C00-\u0C7F]", text):
        return "te-IN"
    if re.search(r"[\u0A80-\u0AFF]", text):
        return "gu-IN"
    if re.search(r"[\u0C80-\u0CFF]", text):
        return "kn-IN"
    if re.search(r"[\u0D00-\u0D7F]", text):
        return "ml-IN"
    if re.search(r"[\u0A00-\u0A7F]", text):
        return "pa-IN"
    if re.search(r"[\u0900-\u097F]", text):
        if re.search(r"\b(namaskar|kasa ahes|kashi ahes|tap|dok dukhi|pot dukhi)\b", text.lower()):
            return "mr-IN"
        return "hi-IN"

    lowered = text.lower()
    if fallback == "en-IN":
        if re.search(r"\b(namaste|namaskar|bukhar|khansi|sir dard|pet dard|kya hal|kaise ho|kaisi ho)\b", lowered):
            return "hi-IN"
        if re.search(r"\b(sat sri akal|kiddan|ki haal)\b", lowered):
            return "pa-IN"

    return fallback if fallback in SUPPORTED_CODES else "en-IN"


GREETING_PATTERNS = [
    r"^(hi|hello|hey|helo|hlo|good morning|good afternoon|good evening|greetings)\b[\s!.,?]*$",
    r"^(namaste|namaskar|pranam|sat sri akal|vanakkam|nomoshkar|kem cho|kasa kay)\b[\s!.,?]*$",
    r"^(नमस्ते|नमस्कार|प्रणाम|हेलो|हाय|सत श्री अकाल|নমস্কার|வணக்கம்|నమస్కారం|નમસ્તે|ನಮಸ್ಕಾರ|നമസ്കാരം)\b[\s!.,?]*$",
]

GREETING_REPLIES: dict[str, str] = {
    "en-IN": "Hello, how are you and how can I help you today?",
    "hi-IN": "नमस्ते, आप कैसे हैं और आज मैं आपकी क्या मदद कर सकता हूँ?",
    "bn-IN": "নমস্কার, আপনি কেমন আছেন এবং আজ আমি আপনাকে কীভাবে সাহায্য করতে পারি?",
    "ta-IN": "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள், இன்று நான் உங்களுக்கு எப்படி உதவ முடியும்?",
    "te-IN": "నమస్కారం, మీరు ఎలా ఉన్నారు మరియు ఈరోజు నేను మీకు ఎలా సహాయం చేయగలను?",
    "mr-IN": "नमस्कार, तुम्ही कसे आहात आणि आज मी तुम्हाला कशी मदत करू शकतो?",
    "gu-IN": "નમસ્તે, તમે કેમ છો અને આજે હું તમને કેવી રીતે મદદ કરી શકું?",
    "kn-IN": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ ಮತ್ತು ಇಂದು ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ?",
    "ml-IN": "നമസ്കാരം, നിങ്ങൾക്ക് എങ്ങനെയുണ്ട്, ഇന്ന് എനിക്ക് നിങ്ങളെ എങ്ങനെ സഹായിക്കാനാകും?",
    "pa-IN": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ ਅਤੇ ਅੱਜ ਮੈਂ ਤੁਹਾਡੀ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?",
}

EMPTY_INPUT_REPLIES: dict[str, str] = {
    "en-IN": "I didn't hear a sentence. Please tap the microphone or type what you want to ask.",
    "hi-IN": "मुझे कोई वाक्य सुनाई नहीं दिया। कृपया माइक दबाएँ या अपना सवाल लिखें।",
    "bn-IN": "আমি কোনো বাক্য শুনতে পাইনি। অনুগ্রহ করে মাইক চাপুন অথবা আপনার কথা লিখুন।",
    "ta-IN": "எனக்கு எந்த வாக்கியமும் கேட்கவில்லை. மைக்கை அழுத்தவும் அல்லது உங்கள் கேள்வியை தட்டச்சு செய்யவும்.",
    "te-IN": "నాకు ఎటువంటి వాక్యం వినిపించలేదు. దయచేసి మైక్ నొక్కండి లేదా మీ ప్రశ్నను టైప్ చేయండి.",
    "mr-IN": "मला कोणतेही वाक्य ऐकू आले नाही. कृपया माइक दाबा किंवा तुमचा प्रश्न लिहा.",
    "gu-IN": "મને કોઈ વાક્ય સંભળાયું નથી. કૃપા કરીને માઇક દબાવો અથવા તમારો પ્રશ્ન લખો.",
    "kn-IN": "ನನಗೆ ಯಾವುದೇ ವಾಕ್ಯ ಕೇಳಿಸಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮೈಕ್ ಒತ್ತಿ ಅಥವಾ ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ.",
    "ml-IN": "എനിക്ക് ഒരു വാക്യവും കേൾക്കാൻ കഴിഞ്ഞില്ല. ദയവായി മൈക്ക് അമർത്തുക അല്ലെങ്കിൽ നിങ്ങളുടെ ചോദ്യം ടൈപ്പ് ചെയ്യുക.",
    "pa-IN": "ਮੈਨੂੰ ਕੋਈ ਵਾਕ ਸੁਣਾਈ ਨਹੀਂ ਦਿੱਤਾ। ਕਿਰਪਾ ਕਰਕੇ ਮਾਈਕ ਦਬਾਓ ਜਾਂ ਆਪਣਾ ਸਵਾਲ ਲਿਖੋ।",
}

PATIENT_DETAILS_PROMPT: dict[str, str] = {
    "en-IN": "To give more relevant guidance for these symptoms, please share your age, gender, and any co-morbidities (such as diabetes, high blood pressure, asthma, or thyroid/heart/kidney conditions).",
    "hi-IN": "इन लक्षणों के लिए अधिक उपयुक्त जानकारी देने के लिए कृपया अपनी उम्र, लिंग और कोई पुरानी बीमारी या सह-रुग्णता (जैसे शुगर, हाई बीपी, दमा, या दिल/गुर्दे/थायरॉयड की समस्या) बताएँ।",
    "bn-IN": "এই উপসর্গগুলোর জন্য আরও সঠিক তথ্য দিতে অনুগ্রহ করে আপনার বয়স, লিঙ্গ এবং আগে থেকে কোনো রোগ (যেমন ডায়াবেটিস, উচ্চ রক্তচাপ, হাঁপানি বা কিডনি/হার্টের সমস্যা) থাকলে তা জানান।",
    "ta-IN": "இந்த அறிகுறிகளுக்கு மேலும் பொருத்தமான ஆலோசனை வழங்க உங்கள் வயது, பாலினம் மற்றும் ஏற்கனவே உள்ள உடல்நலப் பிரச்சனைகள் (சர்க்கரை நோய், உயர் ரத்த அழுத்தம், ஆஸ்துமா போன்றவை) இருந்தால் கூறவும்.",
    "te-IN": "ఈ లక్షణాలకు మరింత తగిన సూచనలు ఇవ్వడానికి దయచేసి మీ వయస్సు, లింగం మరియు ముందే ఉన్న ఆరోగ్య సమస్యలు (మధుమేహం, అధిక రక్తపోటు, ఆస్తమా మొదలైనవి) ఉంటే తెలపండి.",
    "mr-IN": "या लक्षणांसाठी अधिक योग्य माहिती देण्यासाठी कृपया तुमचे वय, लिंग आणि आधीपासून काही आजार (जसे मधुमेह, उच्च रक्तदाब, दमा किंवा हृदय/मूत्रपिंडाचे आजार) असल्यास सांगा.",
    "gu-IN": "આ લક્ષણો માટે વધુ યોગ્ય માર્ગદર્શન આપવા માટે કૃપા કરીને તમારી ઉંમર, લિંગ અને અગાઉથી કોઈ બીમારી (જેમ કે ડાયાબિટીસ, બ્લડ પ્રેશર, અસ્થમા વગેરે) હોય તો જણાવો.",
    "kn-IN": "ಈ ಲಕ್ಷಣಗಳಿಗೆ ಹೆಚ್ಚು ಸೂಕ್ತವಾದ ಮಾಹಿತಿ ನೀಡಲು ದಯವಿಟ್ಟು ನಿಮ್ಮ ವಯಸ್ಸು, ಲಿಂಗ ಮತ್ತು ಮೊದಲೇ ಇರುವ ಆರೋಗ್ಯ ಸಮಸ್ಯೆಗಳು (ಮಧುಮೇಹ, ಅಧಿಕ ರಕ್ತದೊತ್ತಡ, ಅಸ್ತಮಾ ಇತ್ಯಾದಿ) ಇದ್ದರೆ ತಿಳಿಸಿ.",
    "ml-IN": "ഈ ലക്ഷണങ്ങൾക്ക് കൂടുതൽ അനുയോജ്യമായ വിവരങ്ങൾ നൽകാൻ ദയവായി നിങ്ങളുടെ പ്രായം, ലിംഗഭേദം, നിലവിലുള്ള മറ്റ് രോഗങ്ങൾ (പ്രമേഹം, രക്താതിമർദ്ദം, ആസ്ത്മ തുടങ്ങിയവ) എന്നിവ പറയുക.",
    "pa-IN": "ਇਹਨਾਂ ਲੱਛਣਾਂ ਲਈ ਵਧੇਰੇ ਢੁਕਵੀਂ ਜਾਣਕਾਰੀ ਦੇਣ ਲਈ ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਉਮਰ, ਲਿੰਗ ਅਤੇ ਪਹਿਲਾਂ ਤੋਂ ਕੋਈ ਬਿਮਾਰੀ (ਜਿਵੇਂ ਸ਼ੂਗਰ, ਬਲੱਡ ਪ੍ਰੈਸ਼ਰ, ਦਮਾ ਆਦਿ) ਹੋਵੇ ਤਾਂ ਦੱਸੋ।",
}

URGENT_NOTICE: dict[str, str] = {
    "en-IN": "Urgent alert: Please seek immediate emergency medical care right away for severe warning signs such as chest pain, trouble breathing, fainting, severe bleeding, or sudden neurological symptoms.",
    "hi-IN": "तत्काल चेतावनी: सीने में दर्द, साँस लेने में तकलीफ़, बेहोशी, अधिक रक्तस्राव या अचानक कमज़ोरी/सुन्नपन जैसे गंभीर लक्षण होने पर तुरंत नजदीकी आपातकालीन चिकित्सा सहायता लें।",
    "bn-IN": "জরুরি সতর্কতা: বুকে ব্যথা, শ্বাসকষ্ট, অজ্ঞান হয়ে যাওয়া, অতিরিক্ত রক্তপাত বা হঠাৎ দুর্বলতার মতো গুরুতর লক্ষণ থাকলে অবিলম্বে জরুরি চিকিৎসা নিন।",
    "ta-IN": "அவசர எச்சரிக்கை: நெஞ்சு வலி, மூச்சுத்திணறல், மயக்கம், அதிக ரத்தப்போக்கு போன்ற தீவிர அறிகுறிகள் இருந்தால் உடனடியாக அவசர மருத்துவ உதவியை நாடுங்கள்.",
    "te-IN": "అత్యవసర హెచ్చరిక: ఛాతీ నొప్పి, శ్వాస తీసుకోవడంలో ఇబ్బంది, స్పృహ తప్పడం, తీవ్ర రక్తస్రావం వంటి లక్షణాలు ఉంటే వెంటనే అత్యవసర వైద్య సహాయం తీసుకోండి.",
    "mr-IN": "तातडीचा इशारा: छातीत दुखणे, श्वास घेण्यास त्रास, बेशुद्ध पडणे किंवा तीव्र रक्तस्त्राव यांसारखी लक्षणे असल्यास त्वरित आपत्कालीन वैद्यकीय मदत घ्या.",
    "gu-IN": "તાત્કાલિક ચેતવણી: છાતીમાં દુખાવો, શ્વાસ લેવામાં તકલીફ, બેભાન થવું અથવા વધુ પડતું રક્તસ્રાવ જેવા લક્ષણો હોય તો તરત જ કટોકટીની તબીબી મદદ લો.",
    "kn-IN": "ತುರ್ತು ಎಚ್ಚರಿಕೆ: ಎದೆ ನೋವು, ಉಸಿರಾಟದ ತೊಂದರೆ, ಮೂರ್ಛೆ ಅಥವಾ ತೀವ್ರ ರಕ್ತಸ್ರಾವದಂತಹ ಲಕ್ಷಣಗಳಿದ್ದರೆ ತಕ್ಷಣ ತುರ್ತು ವೈದ್ಯಕೀಯ ನೆರವು ಪಡೆಯಿರಿ.",
    "ml-IN": "അടിയന്തര മുന്നറിയിപ്പ്: നെഞ്ചുവേദന, ശ്വാസതടസ്സം, ബോധക്ഷയം, കനത്ത രക്തസ്രാവം തുടങ്ങിയ ലക്ഷണങ്ങളുണ്ടെങ്കിൽ ഉടൻ അടിയന്തര വൈദ്യസഹായം തേടുക.",
    "pa-IN": "ਤੁਰੰਤ ਚੇਤਾਵਨੀ: ਛਾਤੀ ਵਿੱਚ ਦਰਦ, ਸਾਹ ਲੈਣ ਵਿੱਚ ਤਕਲੀਫ਼, ਬੇਹੋਸ਼ੀ ਜਾਂ ਜ਼ਿਆਦਾ ਖੂਨ ਵਹਿਣ ਵਰਗੇ ਲੱਛਣ ਹੋਣ 'ਤੇ ਤੁਰੰਤ ਐਮਰਜੈਂਸੀ ਡਾਕਟਰੀ ਮਦਦ ਲਓ।",
}

GENERAL_FALLBACK: dict[str, str] = {
    "en-IN": "I have received your message. Please share the exact symptoms or health topic you are asking about so I can guide you clearly.",
    "hi-IN": "मुझे आपका संदेश मिल गया है। कृपया अपने लक्षण या स्वास्थ्य विषय के बारे में स्पष्ट रूप से बताएँ ताकि मैं सही जानकारी दे सकूँ।",
    "bn-IN": "আমি আপনার বার্তা পেয়েছি। অনুগ্রহ করে আপনার উপসর্গ বা স্বাস্থ্য সংক্রান্ত বিষয় পরিষ্কারভাবে বলুন।",
    "ta-IN": "உங்கள் செய்தி எனக்குக் கிடைத்தது. தெளிவான வழிகாட்டுதலுக்கு உங்கள் அறிகுறிகள் அல்லது உடல்நலக் கேள்வியைக் கூறுங்கள்.",
    "te-IN": "మీ సందేశం నాకు అందింది. స్పష్టమైన సమాచారం కోసం మీ లక్షణాలు లేదా ఆరోగ్య సమస్యను వివరంగా చెప్పండి.",
    "mr-IN": "मला तुमचा संदेश मिळाला आहे. योग्य मार्गदर्शनासाठी तुमची लक्षणे किंवा आरोग्य विषयक प्रश्न स्पष्टपणे सांगा.",
    "gu-IN": "મને તમારો સંદેશ મળ્યો છે. યોગ્ય માર્ગદર્શન માટે તમારા લક્ષણો અથવા સ્વાસ્થ્ય વિશે સ્પષ્ટ જણાવો.",
    "kn-IN": "ನಿಮ್ಮ ಸಂದೇಶ ನನಗೆ ತಲುಪಿದೆ. ಸರಿಯಾದ ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ನಿಮ್ಮ ಲಕ್ಷಣಗಳು ಅಥವಾ ಆರೋಗ್ಯ ಸಮಸ್ಯೆಯನ್ನು ಸ್ಪಷ್ಟವಾಗಿ ತಿಳಿಸಿ.",
    "ml-IN": "നിങ്ങളുടെ സന്ദേശം എനിക്ക് ലഭിച്ചു. വ്യക്തമായ മാർഗ്ഗനിർദ്ദേശത്തിനായി ലക്ഷണങ്ങളോ ആരോഗ്യ പ്രശ്നമോ വ്യക്തമാക്കുക.",
    "pa-IN": "ਮੈਨੂੰ ਤੁਹਾਡਾ ਸੁਨੇਹਾ ਮਿਲ ਗਿਆ ਹੈ। ਸਹੀ ਜਾਣਕਾਰੀ ਲਈ ਆਪਣੇ ਲੱਛਣ ਜਾਂ ਸਿਹਤ ਸਬੰਧੀ ਸਵਾਲ ਸਪੱਸ਼ਟ ਦੱਸੋ।",
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
    r"(सीने में दर्द|सांस लेने में तकलीफ|साँस लेने में तकलीफ़|बेहोश|बेहोशी)",
]

TOPIC_RULES: list[tuple[str, bool, list[str], dict[str, str]]] = [
    (
        "fever",
        True,
        [r"\bfever\b", r"\btemperature\b", r"\bbukhar\b", r"\bchills\b", r"\bbody ache\b", r"(बुखार|तेज़ बुखार|ठंड लगना|शरीर में दर्द|ज्वर)"],
        {
            "en-IN": "For fever and body ache, rest well, drink plenty of water or oral fluids, and monitor your temperature regularly.",
            "hi-IN": "बुखार और शरीर दर्द के लिए आराम करें, पर्याप्त पानी या तरल पदार्थ पिएँ और नियमित रूप से तापमान जाँचते रहें।",
            "bn-IN": "জ্বর ও শরীর ব্যথার জন্য বিশ্রাম নিন, পর্যাপ্ত পানি বা তরল খাবার খান এবং নিয়মিত তাপমাত্রা পরীক্ষা করুন।",
            "ta-IN": "காய்ச்சல் மற்றும் உடல் வலிக்கு நன்கு ஓய்வெடுங்கள், போதுமான தண்ணீர் அல்லது திரவங்களைக் குடியுங்கள், வெப்பநிலையைக் கவனியுங்கள்.",
            "te-IN": "జ్వరం మరియు ఒళ్లు నొప్పులకు విశ్రాంతి తీసుకోండి, తగినంత నీరు లేదా ద్రవాలు తాగండి మరియు ఉష్ణోగ్రతను గమనించండి.",
            "mr-IN": "ताप आणि अंगदुखीसाठी पुरेशी विश्रांती घ्या, भरपूर पाणी किंवा द्रव पदार्थ प्या आणि शरीराचे तापमान तपासा.",
            "gu-IN": "તાવ અને શરીરના દુખાવા માટે આરામ કરો, પૂરતું પાણી અથવા પ્રવાહી લો અને તાપમાન નિયમિત તપાસો.",
            "kn-IN": "ಜ್ವರ ಮತ್ತು ಮೈಕೈ ನೋವಿಗೆ ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ, ಸಾಕಷ್ಟು ನೀರು ಅಥವಾ ದ್ರವ ಸೇವಿಸಿ ಮತ್ತು ತಾಪಮಾನವನ್ನು ಗಮನಿಸಿ.",
            "ml-IN": "പനിക്കും ശരീരവേദനയ്ക്കും നന്നായി വിശ്രമിക്കുക, ധാരാളം വെള്ളം അല്ലെങ്കിൽ ദ്രാവകങ്ങൾ കുടിക്കുക, താപനില പരിശോധിക്കുക.",
            "pa-IN": "ਬੁਖਾਰ ਅਤੇ ਸਰੀਰ ਦਰਦ ਲਈ ਆਰਾਮ ਕਰੋ, ਕਾਫ਼ੀ ਪਾਣੀ ਜਾਂ ਤਰਲ ਪੀਓ ਅਤੇ ਤਾਪਮਾਨ ਦੀ ਜਾਂਚ ਕਰਦੇ ਰਹੋ।",
        },
    ),
    (
        "cough_cold",
        True,
        [r"\bcough\b", r"\bcold\b", r"\bsore throat\b", r"\bkhansi\b", r"\bthroat\b", r"(खांसी|खाँसी|जुकाम|गले में खराश|गला दर्द)"],
        {
            "en-IN": "For cough, cold, or sore throat, take warm fluids, warm salt-water gargles, and rest your voice.",
            "hi-IN": "खांसी, जुकाम या गले की खराश के लिए गुनगुने तरल पदार्थ लें, गुनगुने नमक पानी से गरारे करें और आराम करें।",
            "bn-IN": "কাশি, সর্দি বা গলা ব্যথার জন্য হালকা গরম পানীয় খান, উষ্ণ লবণ পানিতে গার্গল করুন এবং বিশ্রাম নিন।",
            "ta-IN": "இருமல், சளி அல்லது தொண்டை வலிக்கு வெதுவெதுப்பான பானங்கள் குடியுங்கள், வெந்நீரில் உப்பு கலந்து வாய் கொப்பளியுங்கள்.",
            "te-IN": "దగ్గు, జలుబు లేదా గొంతు నొప్పికి గోరువెచ్చని ద్రవాలు తీసుకోండి, గోరువెచ్చని ఉప్పునీటితో పుక్కిలించండి మరియు విశ్రాంతి తీసుకోండి.",
            "mr-IN": "खोकला, सर्दी किंवा घसा खवखवत असल्यास कोमट पेये घ्या, कोमट मिठाच्या पाण्याने गुळण्या करा आणि विश्रांती घ्या.",
            "gu-IN": "ઉધરસ, શરદી અથવા ગળાના દુખાવા માટે હુંફાળું પ્રવાહી લો, હુંફાળા મીઠાના પાણીથી કોગળા કરો અને આરામ કરો.",
            "kn-IN": "ಕೆಮ್ಮು, ಶೀತ ಅಥವಾ ಗಂಟಲು ನೋವಿಗೆ ಉಗುರುಬೆಚ್ಚಗಿನ ದ್ರವ ಸೇವಿಸಿ, ಉಪ್ಪು ನೀರಿನಿಂದ ಬಾಯಿ ಮುಕ್ಕಳಿಸಿ ಮತ್ತು ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ.",
            "ml-IN": "ചുമ, ജലദോഷം അല്ലെങ്കിൽ തൊണ്ടവേദന എന്നിവയ്ക്ക് ഇളംചൂടുള്ള പാനീയങ്ങൾ കുടിക്കുക, ഉപ്പുവെള്ളത്തിൽ കവിൾ കൊള്ളുക.",
            "pa-IN": "ਖੰਘ, ਜ਼ੁਕਾਮ ਜਾਂ ਗਲੇ ਦੀ ਖਰਾਸ਼ ਲਈ ਕੋਸੇ ਤਰਲ ਪਦਾਰਥ ਲਓ, ਕੋਸੇ ਲੂਣ ਵਾਲੇ ਪਾਣੀ ਨਾਲ ਗਰਾਰੇ ਕਰੋ ਅਤੇ ਆਰਾਮ ਕਰੋ।",
        },
    ),
    (
        "headache_dizzy",
        True,
        [r"\bheadache\b", r"\bmigraine\b", r"\bdizzy\b", r"\bdizziness\b", r"\bsir dard\b", r"(सिरदर्द|सिर में दर्द|चक्कर|माइग्रेन)"],
        {
            "en-IN": "For headache or dizziness, rest in a calm spot, drink water, avoid skipping meals, and sit or lie down safely.",
            "hi-IN": "सिरदर्द या चक्कर आने पर शांत जगह पर आराम करें, पानी पिएँ, समय पर भोजन करें और सुरक्षित रूप से बैठें या लेटें।",
            "bn-IN": "মাথাব্যথা বা মাথা ঘোরার জন্য শান্ত স্থানে বিশ্রাম নিন, পানি খান, সময়মতো খাবার খান এবং নিরাপদে বসুন বা শুয়ে পড়ুন।",
            "ta-IN": "தலைவலி அல்லது தலைச்சுற்றலுக்கு அமைதியான இடத்தில் ஓய்வெடுங்கள், தண்ணீர் குடியுங்கள், உணவைத் தவிர்க்க வேண்டாம்.",
            "te-IN": "తలనొప్పి లేదా తలతిరగడం ఉంటే ప్రశాంతంగా విశ్రాంతి తీసుకోండి, నీరు తాగండి, సమయానికి భోజనం చేయండి.",
            "mr-IN": "डोकेदुखी किंवा चक्कर येत असल्यास शांत ठिकाणी विश्रांती घ्या, पाणी प्या, वेळेवर जेवण करा आणि सुरक्षित बसा किंवा झोपा.",
            "gu-IN": "માથાનો દુખાવો અથવા ચક્કર આવે તો શાંત જગ્યાએ આરામ કરો, પાણી પીવો અને સમયસર ખોરાક લો.",
            "kn-IN": "ತಲೆನೋವು ಅಥವಾ ತಲೆತಿರುಗುವಿಕೆ ಇದ್ದರೆ ಶಾಂತ ಸ್ಥಳದಲ್ಲಿ ವಿಶ್ರಾಂತಿ ಪಡೆಯಿರಿ, ನೀರು ಕುಡಿಯಿರಿ, ಸಮಯಕ್ಕೆ ಸರಿಯಾಗಿ ಆಹಾರ ಸೇವಿಸಿ.",
            "ml-IN": "തലവേദനയോ തലകറക്കമോ ഉണ്ടെങ്കിൽ ശാന്തമായി വിശ്രമിക്കുക, വെള്ളം കുടിക്കുക, സമയത്തിന് ഭക്ഷണം കഴിക്കുക.",
            "pa-IN": "ਸਿਰ ਦਰਦ ਜਾਂ ਚੱਕਰ ਆਉਣ 'ਤੇ ਸ਼ਾਂਤ ਥਾਂ 'ਤੇ ਆਰਾਮ ਕਰੋ, ਪਾਣੀ ਪੀਓ ਅਤੇ ਸਮੇਂ ਸਿਰ ਖਾਣਾ ਖਾਓ।",
        },
    ),
    (
        "stomach",
        True,
        [r"\bstomach\b", r"\bacidity\b", r"\bgas\b", r"\bnausea\b", r"\bvomit\b", r"\bvomiting\b", r"\bdiarrhea\b", r"\bpet dard\b", r"(पेट दर्द|पेट में दर्द|एसिडिटी|गैस|उल्टी|दस्त)"],
        {
            "en-IN": "For stomach discomfort, acidity, or loose motions, choose light meals and sip water or oral rehydration fluids gradually.",
            "hi-IN": "पेट की परेशानी, एसिडिटी या दस्त में हल्का भोजन करें और थोड़ा-थोड़ा करके पानी या ओआरएस लेते रहें।",
            "bn-IN": "পেটের অস্বস্তি, অ্যাসিডিটি বা ডায়রিয়ায় হালকা খাবার খান এবং অল্প অল্প করে পানি বা ওআরএস পান করুন।",
            "ta-IN": "வயிற்று அசௌகரியம், அமிலத்தன்மை அல்லது வயிற்றுப்போக்குக்கு எளிதில் செரிக்கும் உணவை உண்டு சிறிது சிறிதாக நீர் அருந்துங்கள்.",
            "te-IN": "కడుపు నొప్పి, ఎసిడిటీ లేదా విరేచనాలకు తేలికపాటి ఆహారం తీసుకోండి మరియు కొద్దికొద్దిగా నీరు లేదా ఓఆర్ఎస్ తాగండి.",
            "mr-IN": "पोटदुखी, आम्लपित्त किंवा जुलाब असल्यास हलका आहार घ्या आणि थोडेथोडे पाणी किंवा ओआरएस प्या.",
            "gu-IN": "પેટની તકલીફ, એસિડિટી અથવા ઝાડામાં હળવો ખોરાક લો અને થોડું થોડું પાણી અથવા ઓઆરએસ પીવો.",
            "kn-IN": "ಹೊಟ್ಟೆ ನೋವು, ಆಮ್ಲೀಯತೆ ಅಥವಾ ಭೇದಿಗೆ ಹಗುರವಾದ ಆಹಾರ ಸೇವಿಸಿ ಮತ್ತು ಸ್ವಲ್ಪ ಸ್ವಲ್ಪವಾಗಿ ನೀರು ಅಥವಾ ಓಆರ್‌ಎಸ್ ಕುಡಿಯಿರಿ.",
            "ml-IN": "വയറുവേദന, അസിഡിറ്റി അല്ലെങ്കിൽ വയറിളക്കം എന്നിവയ്ക്ക് ലഘുവായ ഭക്ഷണം കഴിക്കുകയും കുറച്ചുകുറച്ചായി വെള്ളം കുടിക്കുകയും ചെയ്യുക.",
            "pa-IN": "ਪੇਟ ਦਰਦ, ਐਸੀਡਿਟੀ ਜਾਂ ਦਸਤ ਵਿੱਚ ਹਲਕਾ ਭੋਜਨ ਖਾਓ ਅਤੇ ਥੋੜ੍ਹਾ-ਥੋੜ੍ਹਾ ਪਾਣੀ ਜਾਂ ਓਆਰਐਸ ਪੀਂਦੇ ਰਹੋ।",
        },
    ),
    (
        "nutrition",
        False,
        [r"\bdiet\b", r"\bnutrition\b", r"\bfood\b", r"\bmeal\b", r"\bprotein\b", r"\biron\b", r"\bvitamin\b", r"(आहार|पोषण|खाना|भोजन|प्रोटीन|आयरन|विटामिन)"],
        {
            "en-IN": "For daily nutrition, include whole grains, lentils or pulses, seasonal vegetables, adequate protein, and clean drinking water.",
            "hi-IN": "रोज़ाना के पोषण के लिए साबुत अनाज, दालें, मौसमी सब्ज़ियाँ, पर्याप्त प्रोटीन और स्वच्छ पानी शामिल करें।",
            "bn-IN": "দৈনন্দিন পুষ্টির জন্য গোটা শস্য, ডাল, মরশুমি শাকসবজি, পর্যাপ্ত প্রোটিন এবং নিরাপদ পানি রাখুন।",
            "ta-IN": "தினசரி ஊட்டச்சத்திற்கு முழு தானியங்கள், பருப்பு வகைகள், பருவகால காய்கறிகள், புரதம் மற்றும் சுத்தமான தண்ணீர் சேர்த்துக்கொள்ளுங்கள்.",
            "te-IN": "రోజువారీ పోషకాహారం కోసం తృణధాన్యాలు, పప్పులు, సీజనల్ కూరగాయలు, తగినంత ప్రోటీన్ మరియు శుభ్రమైన నీరు తీసుకోండి.",
            "mr-IN": "दैनंदिन पोषणासाठी संपूर्ण धान्य, डाळी, हंगामी भाज्या, पुरेसे प्रथिने आणि स्वच्छ पाणी यांचा समावेश करा.",
            "gu-IN": "દૈનિક પોષણ માટે આખા અનાજ, કઠોળ, મોસમી શાકભાજી, પૂરતું પ્રોટીન અને સ્વચ્છ પાણી લો.",
            "kn-IN": "ದೈನಂದಿನ ಪೋಷಣೆಗಾಗಿ ಧಾನ್ಯಗಳು, ಬೇಳೆಕಾಳುಗಳು, ಋತುಮಾನದ ತರಕಾರಿಗಳು, ಪ್ರೋಟೀನ್ ಮತ್ತು ಶುದ್ಧ ನೀರನ್ನು ಸೇವಿಸಿ.",
            "ml-IN": "ദൈനംദിന പോഷകാഹാരത്തിനായി ധാന്യങ്ങൾ, പയർവർഗ്ഗങ്ങൾ, പച്ചക്കറികൾ, പ്രോട്ടീൻ, ശുദ്ധജലം എന്നിവ ഉൾപ്പെടുത്തുക.",
            "pa-IN": "ਰੋਜ਼ਾਨਾ ਪੋਸ਼ਣ ਲਈ ਸਾਬਤ ਅਨਾਜ, ਦਾਲਾਂ, ਮੌਸਮੀ ਸਬਜ਼ੀਆਂ, ਲੋੜੀਂਦਾ ਪ੍ਰੋਟੀਨ ਅਤੇ ਸਾਫ਼ ਪਾਣੀ ਲਓ।",
        },
    ),
]


def _is_greeting(text: str) -> bool:
    cleaned = text.strip().lower()
    return any(re.match(pat, cleaned, flags=re.IGNORECASE) for pat in GREETING_PATTERNS)


def process_voice_turn(
    state: SessionState,
    transcript: str,
    language: str | None = None,
) -> dict[str, Any]:
    raw_text = " ".join((transcript or "").strip().split())
    preferred = language if language in SUPPORTED_CODES else state.language
    lang = detect_language(raw_text, fallback=preferred) if raw_text else preferred
    state.language = lang
    key_info = get_key_status()

    if not raw_text:
        reply = EMPTY_INPUT_REPLIES.get(lang, EMPTY_INPUT_REPLIES["en-IN"])
        return {
            "language": lang,
            "input_text": "",
            "detected_topics": [],
            "urgent": False,
            "reply": reply,
            "keys": key_info,
            "key_status": key_info,
            "history": state.history[-12:],
        }

    if _is_greeting(raw_text):
        reply = GREETING_REPLIES.get(lang, GREETING_REPLIES["en-IN"])
        state.history.append({"role": "user", "text": raw_text, "language": lang})
        state.history.append({"role": "assistant", "text": reply, "language": lang})
        return {
            "language": lang,
            "input_text": raw_text,
            "detected_topics": ["greeting"],
            "urgent": False,
            "reply": reply,
            "keys": key_info,
            "key_status": key_info,
            "history": state.history[-12:],
        }

    lowered = raw_text.lower()
    urgent = any(re.search(pat, lowered) for pat in RED_FLAG_PATTERNS)

    matched_topics: list[str] = []
    any_symptom = False
    parts: list[str] = []

    if urgent:
        parts.append(URGENT_NOTICE.get(lang, URGENT_NOTICE["en-IN"]))

    for topic_key, is_symptom, patterns, lang_map in TOPIC_RULES:
        if any(re.search(pat, lowered) for pat in patterns):
            matched_topics.append(topic_key)
            if is_symptom:
                any_symptom = True
            parts.append(lang_map.get(lang, lang_map["en-IN"]))

    if not parts:
        parts.append(GENERAL_FALLBACK.get(lang, GENERAL_FALLBACK["en-IN"]))

    if any_symptom or urgent:
        parts.append(PATIENT_DETAILS_PROMPT.get(lang, PATIENT_DETAILS_PROMPT["en-IN"]))

    reply = " ".join(parts)
    if matched_topics:
        state.last_topics = matched_topics

    state.history.append({"role": "user", "text": raw_text, "language": lang})
    state.history.append({"role": "assistant", "text": reply, "language": lang})

    return {
        "language": lang,
        "input_text": raw_text,
        "detected_topics": matched_topics,
        "urgent": urgent,
        "reply": reply,
        "keys": key_info,
        "key_status": key_info,
        "history": state.history[-12:],
    }
