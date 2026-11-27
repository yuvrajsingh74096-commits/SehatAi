export class SehatMicrophone {
  constructor({
    micButton,
    languageSelect,
    onTranscript,
    onStatus,
    onListeningChange,
  }) {
    this.micButton = micButton;
    this.languageSelect = languageSelect;
    this.onTranscript = onTranscript || (() => {});
    this.onStatus = onStatus || (() => {});
    this.onListeningChange = onListeningChange || (() => {});

    this.autoSpeak = true;
    this.isListening = false;
    this.voices = [];
    this._activeUtterance = null;

    if ("speechSynthesis" in window) {
      this._loadVoices();
      window.speechSynthesis.onvoiceschanged = () => this._loadVoices();
    }

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition || null;

    this.recognition = SpeechRecognition ? new SpeechRecognition() : null;
    if (this.recognition) {
      this.recognition.interimResults = false;
      this.recognition.maxAlternatives = 1;
      this._bindRecognitionEvents();
    }

    if (this.micButton) {
      this.micButton.addEventListener("click", () => this.toggleListen());
    }
  }

  _loadVoices() {
    if (!("speechSynthesis" in window)) return;
    this.voices = window.speechSynthesis.getVoices() || [];
  }

  _pickVoice(langCode) {
    if (!this.voices || this.voices.length === 0) {
      this._loadVoices();
    }
    if (!this.voices || this.voices.length === 0) return null;

    const target = (langCode || "en-IN").toLowerCase();
    const prefix = target.split("-")[0];

    return (
      this.voices.find((v) => v.lang && v.lang.toLowerCase() === target) ||
      this.voices.find((v) => v.lang && v.lang.toLowerCase().startsWith(prefix + "-")) ||
      this.voices.find((v) => v.lang && v.lang.toLowerCase().startsWith(prefix)) ||
      null
    );
  }

  getLanguage() {
    return (this.languageSelect && this.languageSelect.value) || "en-IN";
  }

  setLanguage(langCode) {
    if (langCode && this.languageSelect) {
      this.languageSelect.value = langCode;
    }
  }

  setAutoSpeak(enabled) {
    this.autoSpeak = Boolean(enabled);
    if (!this.autoSpeak) {
      this.stopSpeaking();
    }
  }

  stopSpeaking() {
    if ("speechSynthesis" in window) {
      try {
        window.speechSynthesis.cancel();
      } catch (_) {}
    }
    this._activeUtterance = null;
  }

  speak(text, langCode = null) {
    if (!this.autoSpeak || !text) return;

    if (!("speechSynthesis" in window)) {
      this.onStatus("Voice output (speechSynthesis) is not supported in this browser.");
      return;
    }

    const chosenLang = langCode || this.getLanguage();
    this.setLanguage(chosenLang);

    const cleanText = String(text).trim();
    if (!cleanText) return;

    try {
      window.speechSynthesis.cancel();
      if (window.speechSynthesis.paused) {
        window.speechSynthesis.resume();
      }

      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.lang = chosenLang;

      const matchedVoice = this._pickVoice(chosenLang);
      if (matchedVoice) {
        utterance.voice = matchedVoice;
        utterance.lang = matchedVoice.lang;
      }

      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;

      utterance.onerror = (event) => {
        if (event && event.error !== "interrupted" && event.error !== "canceled") {
          this.onStatus(`Voice playback notice (${event.error}). Check device TTS voice settings.`);
        }
      };

      this._activeUtterance = utterance;
      window.speechSynthesis.speak(utterance);

      setTimeout(() => {
        if ("speechSynthesis" in window && window.speechSynthesis.paused) {
          window.speechSynthesis.resume();
        }
      }, 150);
    } catch (_) {
      this.onStatus("Could not play voice reply automatically.");
    }
  }

  toggleListen() {
    if (!this.recognition) {
      this.onStatus(
        "Speech recognition is not supported in this browser. Type your message instead."
      );
      return;
    }

    if (this.isListening) {
      try {
        this.recognition.stop();
      } catch (_) {}
      return;
    }

    this.stopSpeaking();
    this.recognition.lang = this.getLanguage();
    try {
      this.recognition.start();
    } catch (_) {
      this._setListening(false);
    }
  }

  _setListening(active) {
    this.isListening = active;
    if (this.micButton) {
      this.micButton.classList.toggle("listening", active);
      this.micButton.setAttribute("aria-pressed", String(active));
    }
    this.onListeningChange(active);
  }

  _bindRecognitionEvents() {
    this.recognition.onstart = () => {
      this._setListening(true);
      this.onStatus(`Listening (${this.recognition.lang})... Speak now.`);
    };

    this.recognition.onresult = (event) => {
      const transcript = event.results?.[0]?.[0]?.transcript?.trim() || "";
      this._setListening(false);
      if (transcript) {
        this.onStatus(`Heard: "${transcript}" — getting reply...`);
        this.onTranscript(transcript);
      } else {
        this.onStatus("No speech detected. Please try again.");
      }
    };

    this.recognition.onerror = (event) => {
      this._setListening(false);
      const err = event?.error || "unknown";
      if (err === "not-allowed" || err === "service-not-allowed") {
        this.onStatus("Microphone permission blocked. Allow mic access or type your message.");
      } else {
        this.onStatus(`Voice input error (${err}). Type your message instead.`);
      }
    };

    this.recognition.onend = () => {
      this._setListening(false);
    };
  }
}
