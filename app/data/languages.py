"""All 22 Scheduled Languages of India plus major regional dialects & Hinglish/code-switch support."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IndianLanguage:
    code: str
    name: str
    native_name: str
    script: str
    bcp47_tts: str
    sample_phrase: str
    dialects: tuple[str, ...]


INDIAN_LANGUAGES: list[IndianLanguage] = [
    IndianLanguage("hi", "Hindi", "हिन्दी", "Devanagari", "hi-IN", "मुझे दो दिन से बुखार और कमजोरी है", ("Awadhi", "Bhojpuri", "Braj", "Bundeli", "Haryanvi", "Rajasthani", "Chhattisgarhi")),
    IndianLanguage("bn", "Bengali", "বাংলা", "Bengali", "bn-IN", "আমার দুই দিন ধরে জ্বর ও দুর্বলতা আছে", ("Rarh", "Bangla", "Sylheti")),
    IndianLanguage("mr", "Marathi", "मराठी", "Devanagari", "mr-IN", "मला दोन दिवसांपासून ताप आणि अशक्तपणा आहे", ("Puneri", "Nagpuri", "Konkani-Marathi", "Varhadi")),
    IndianLanguage("te", "Telugu", "తెలుగు", "Telugu", "te-IN", "నాకు రెండు రోజులుగా జ్వరం మరియు నీరసంగా ఉంది", ("Coastal Andhra", "Rayalaseema", "Telangana")),
    IndianLanguage("ta", "Tamil", "தமிழ்", "Tamil", "ta-IN", "எனக்கு இரண்டு நாட்களாக காய்ச்சல் மற்றும் சோர்வு உள்ளது", ("Kongu", "Madurai", "Chennai", "Tirunelveli")),
    IndianLanguage("gu", "Gujarati", "ગુજરાતી", "Gujarati", "gu-IN", "મને બે દિવસથી તાવ અને નબળાઈ છે", ("Kathiyawadi", "Surti", "Kachchhi", "Charotari")),
    IndianLanguage("ur", "Urdu", "اردو", "Perso-Arabic", "ur-IN", "مجھے دو دن سے بخار اور کمزوری ہے", ("Dakhini", "Lucknowi")),
    IndianLanguage("kn", "Kannada", "ಕನ್ನಡ", "Kannada", "kn-IN", "ನನಗೆ ಎರಡು ದಿನಗಳಿಂದ ಜ್ವರ ಮತ್ತು ನಿಶಕ್ತಿ ಇದೆ", ("Mysuru", "North Karnataka", "Coastal Kannada")),
    IndianLanguage("ml", "Malayalam", "മലയാളം", "Malayalam", "ml-IN", "എനിക്ക് രണ്ട് ദിവസമായി പനിയും ക്ഷീണവുമുണ്ട്", ("Travancore", "Kochi", "Malabar")),
    IndianLanguage("or", "Odia", "ଓଡ଼ିଆ", "Odia", "or-IN", "ମୋତେ ଦୁଇ ଦିନ ଧରି ଜ୍ୱର ଏବଂ ଦୁର୍ବଳତା ଅଛି", ("Cuttack", "Sambalpuri", "South Odia")),
    IndianLanguage("pa", "Punjabi", "ਪੰਜਾਬੀ", "Gurmukhi", "pa-IN", "ਮੈਨੂੰ ਦੋ ਦਿਨਾਂ ਤੋਂ ਬੁਖਾਰ ਅਤੇ ਕਮਜ਼ੋਰੀ ਹੈ", ("Majhi", "Malwai", "Doabi", "Powadhi")),
    IndianLanguage("as", "Assamese", "অসমীয়া", "Bengali-Assamese", "as-IN", "মোৰ দুদিন ধৰি জ্বৰ আৰু দুৰ্বলতা হৈছে", ("Upper Assamese", "Lower Assamese")),
    IndianLanguage("mai", "Maithili", "मैथिली", "Devanagari", "hi-IN", "हमरा दू दिन सँ जर आ कमजोरी अछि", ("Mithila")),
    IndianLanguage("sat", "Santali", "ᱥᱟᱱᱛᱟᱲᱤ", "Ol Chiki", "hi-IN", "ᱤᱧᱟᱜ ᱵᱟᱨ ᱢᱟᱦᱟ ᱠᱷᱚᱱ ᱵᱩᱠᱷᱟᱨ ᱟᱨ ᱠᱚᱢᱡᱳᱨᱤ ᱢᱮᱱᱟᱜᱼᱟ", ("Santhal Pargana", "Mayurbhanj")),
    IndianLanguage("ks", "Kashmiri", "کٲشُر", "Perso-Arabic / Devanagari", "hi-IN", "مےٚ چھِ دۄن دۄہن پؠٹھ بخار تہٕ کمزوری", ("Kashmir Valley")),
    IndianLanguage("ne", "Nepali", "नेपाली", "Devanagari", "hi-IN", "मलाई दुई दिनदेखि ज्वरो र कमजोरी छ", ("Darjeeling", "Sikkim")),
    IndianLanguage("sd", "Sindhi", "سنڌي", "Arabic / Devanagari", "hi-IN", "مون کي ٻن ڏينهن کان بخار ۽ ڪمزوري آهي", ("Kachchh", "Ulhasnagar")),
    IndianLanguage("kok", "Konkani", "कोंकणी", "Devanagari", "mr-IN", "म्हाका दोन दिसां सावन जोर आनी अशक्तपण आसा", ("Goan", "Mangalorean")),
    IndianLanguage("doi", "Dogri", "डोगरी", "Devanagari", "hi-IN", "मिगी दौं दिनें कोला बुखार ते कमजोरी ऐ", ("Jammu")),
    IndianLanguage("mni", "Manipuri", "ꯃꯤꯇꯩꯂꯣꯟ", "Meitei Mayek", "bn-IN", "ꯑꯩꯉꯣꯟꯗꯥ ꯅꯨꯃꯤꯠ ꯲ ꯑꯣꯏꯔꯦ ꯑꯁꯥꯕꯥ ꯑꯃꯁꯨꯡ ꯑꯅꯥꯕꯥ ꯂꯩꯔꯤ", ("Imphal Valley")),
    IndianLanguage("brx", "Bodo", "बड़ो", "Devanagari", "hi-IN", "आंनि साननैनिफ्राय फिसा गोबाव आरो गोहो गोमानाय जादों", ("Kokrajhar", "Udalguri")),
    IndianLanguage("sa", "Sanskrit", "संस्कृतम्", "Devanagari", "hi-IN", "मम द्वित्रयदिवसेभ्यः ज्वरः दौर्बल्यं च वर्तते", ("Classical / Spoken")),
]

SCRIPT_RANGES: list[tuple[int, int, str]] = [
    (0x0980, 0x09FF, "bn"),
    (0x0A80, 0x0AFF, "gu"),
    (0x0B00, 0x0B7F, "or"),
    (0x0B80, 0x0BFF, "ta"),
    (0x0C00, 0x0C7F, "te"),
    (0x0C80, 0x0CFF, "kn"),
    (0x0D00, 0x0D7F, "ml"),
    (0x0A00, 0x0A7F, "pa"),
    (0x1C50, 0x1C7F, "sat"),
    (0xABC0, 0xABFF, "mni"),
    (0x0900, 0x097F, "hi"),
]

LANGUAGE_BY_CODE: dict[str, IndianLanguage] = {lang.code: lang for lang in INDIAN_LANGUAGES}


def detect_indian_language(text: str, requested_code: str | None = None) -> IndianLanguage:
    if requested_code:
        normalized = requested_code.split("-")[0].lower()
        if normalized in LANGUAGE_BY_CODE:
            return LANGUAGE_BY_CODE[normalized]

    for ch in text:
        cp = ord(ch)
        for start, end, code in SCRIPT_RANGES:
            if start <= cp <= end:
                return LANGUAGE_BY_CODE[code]

    lowered = text.lower()
    if any(w in lowered for w in ["bukhar", "pet", "dast", "kamzori", "chakkar", "pani", "paani", "khansi", "gale"]):
        return LANGUAGE_BY_CODE["hi"]
    return LANGUAGE_BY_CODE["hi"]
