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

  getLanguage() {
    return (this.languageSelect && this.languageSelect.value) || "en-IN";
  }

  setAutoSpeak(enabled) {
    this.autoSpeak = Boolean(enabled);
    if (!this.autoSpeak) {
      this.stopSpeaking();
    }
  }

  stopSpeaking() {
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
  }

  speak(text, langCode = null) {
    if (!this.autoSpeak || !text || !("speechSynthesis" in window)) {
      return;
    }
    this.stopSpeaking();
    const utterance = new SpeechSynthesisUtterance(text);
    utter.lang = langCode || this.getLanguage();
    window.speechSynthesis.speak(utter);
  }

  toggleListen() {
    if (!this.recognition) {
      this.onStatus(
        "Speech recognition is not supported in this browser. Type your message instead."
      );
      return;
    }

    if (this.isListening) {
      this.recognition.stop();
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
      this.onStatus(`Listening (${this.recognition.lang})...`);
    };

    this.recognition.onresult = (event) => {
      const transcript = event.results?.[0]?.[0]?.transcript?.trim() || "";
      this._setListening(false);
      if (transcript) {
        this.onTranscript(transcript);
      } else {
        this.onStatus("No speech detected. Please try again.");
      }
    };

    this.recognition.onerror = (event) => {
      this._setListening(false);
      const err = event?.error || "unknown";
      if (err === "not-allowed" || err === "service-not-allowed") {
        this.onStatus("Microphone permission blocked. Allow mic access or type your sentence.");
      } else {
        this.onStatus(`Voice input error (${err}). You can type your sentence instead.`);
      }
    };

    this.recognition.onend = () => {
      this._setListening(false);
    };
  }
}
