import requests
from django.conf import settings
from .exceptions import (
    SarvamError,
    SarvamAuthError,
    SarvamRateLimitError,
    SarvamTimeoutError,
    UnsupportedLanguageError,
)


# Supported languages (Sarvam AI — 22 scheduled Indian languages + English)
SUPPORTED_LANGUAGES = {
    "hi-IN": "Hindi",
    "bn-IN": "Bengali",
    "ta-IN": "Tamil",
    "te-IN": "Telugu",
    "kn-IN": "Kannada",
    "ml-IN": "Malayalam",
    "mr-IN": "Marathi",
    "gu-IN": "Gujarati",
    "pa-IN": "Punjabi",
    "or-IN": "Odia",
    "en-IN": "English (India)",
    "as-IN": "Assamese",
    "ur-IN": "Urdu",
    "ne-IN": "Nepali",
    "kok-IN": "Konkani",
    "ks-IN": "Kashmiri",
    "sd-IN": "Sindhi",
    "sa-IN": "Sanskrit",
    "sat-IN": "Santali",
    "mni-IN": "Manipuri",       # 👈 YOUR KEY LANGUAGE
    "brx-IN": "Bodo",
    "mai-IN": "Maithili",
    "doi-IN": "Dogri",
}

# Supported TTS voices (Bulbul v2)
SUPPORTED_VOICES = [
    {"id": "anushka", "name": "Anushka", "gender": "female", "language": "hi-IN"},
    {"id": "abhilash", "name": "Abhilash", "gender": "male", "language": "hi-IN"},
    {"id": "manisha", "name": "Manisha", "gender": "female", "language": "hi-IN"},
    {"id": "vidya", "name": "Vidya", "gender": "female", "language": "hi-IN"},
    {"id": "arya", "name": "Arya", "gender": "female", "language": "hi-IN"},
    {"id": "karun", "name": "Karun", "gender": "male", "language": "hi-IN"},
    {"id": "hitesh", "name": "Hitesh", "gender": "male", "language": "hi-IN"},
]


class SarvamClient:
    """Thin wrapper around Sarvam AI HTTP API."""

    def __init__(self):
        self.api_key = settings.SARVAM_API_KEY
        self.base_url = settings.SARVAM_BASE_URL
        if not self.api_key:
            raise SarvamError(
                "SARVAM_API_KEY is not set in environment",
                code="MISSING_API_KEY",
                status=500,
            )

    def _headers(self, json_content=False):
        h = {"api-subscription-key": self.api_key}
        if json_content:
            h["Content-Type"] = "application/json"
        return h

    def _handle(self, r):
        if r.status_code == 401:
            raise SarvamAuthError()
        if r.status_code == 429:
            raise SarvamRateLimitError()
        if r.status_code >= 500:
            raise SarvamError(f"Sarvam server error: {r.text}", status=502)
        if not r.ok:
            raise SarvamError(
                f"Sarvam error ({r.status_code}): {r.text}",
                code="SARVAM_ERROR",
                status=400,
            )
        return r.json()

    # ---------- Language Detection ----------
    def detect_language(self, text):
        """
        Detect language of input text via /text-lid.
        Returns a BCP-47 code like 'en-IN', 'hi-IN', 'mni-IN'.
        Falls back to 'en-IN' if detection fails.

        Note: sarvam-translate:v1 requires an explicit source language,
        so we detect first when caller passes 'auto'.
        """
        try:
            r = requests.post(
                f"{self.base_url}/text-lid",
                headers=self._headers(json_content=True),
                json={"input": text},
                timeout=15,
            )
        except requests.Timeout:
            return "en-IN"

        if not r.ok:
            # Don't crash the whole translate call over detection failure
            return "en-IN"

        data = r.json()
        return data.get("language_code") or "en-IN"

    # ---------- Text Translation ----------
    def translate(self, text, source_lang="auto", target_lang="hi-IN"):
        """
        Translate text between any of the 22 supported languages.
        Uses sarvam-translate:v1 (includes Manipuri).

        If source_lang == "auto", first call /text-lid to detect,
        because sarvam-translate:v1 doesn't natively support "auto".
        """
        if target_lang not in SUPPORTED_LANGUAGES:
            raise UnsupportedLanguageError(target_lang)

        # Handle auto-detection manually
        if source_lang == "auto" or not source_lang:
            source_lang = self.detect_language(text)

        # If detection returned something unsupported, default to English
        if source_lang not in SUPPORTED_LANGUAGES:
            source_lang = "en-IN"

        payload = {
            "input": text,
            "source_language_code": source_lang,
            "target_language_code": target_lang,
            "model": "sarvam-translate:v1",
        }

        try:
            r = requests.post(
                f"{self.base_url}/translate",
                headers=self._headers(json_content=True),
                json=payload,
                timeout=30,
            )
        except requests.Timeout:
            raise SarvamTimeoutError()

        result = self._handle(r)
        # Attach detected source language to the response for the frontend
        result["detected_source_language"] = source_lang
        return result

    # ---------- Text-to-Speech ----------
    def text_to_speech(
        self,
        text,
        target_lang="hi-IN",
        speaker="anushka",
        pace=1.0,
        codec="mp3",
        sample_rate=22050,
    ):
        payload = {
            "inputs": [text],
            "target_language_code": target_lang,
            "speaker": speaker,
            "pace": pace,
            "speech_sample_rate": sample_rate,
            "enable_preprocessing": True,
            "model": "bulbul:v2",
        }
        try:
            r = requests.post(
                f"{self.base_url}/text-to-speech",
                headers=self._headers(json_content=True),
                json=payload,
                timeout=60,
            )
        except requests.Timeout:
            raise SarvamTimeoutError()
        return self._handle(r)

    # ---------- Speech-to-Text ----------
    def speech_to_text(self, audio_file, language_code="unknown", mode="transcribe"):
        """
        Transcribe or translate an audio file.
        mode: transcribe | translate | verbatim | translit | codemix
        """
        files = {
            "file": (
                getattr(audio_file, "name", "audio.wav"),
                audio_file.read(),
                getattr(audio_file, "content_type", "audio/wav"),
            )
        }
        data = {"model": "saaras:v3", "mode": mode}
        if language_code and language_code != "unknown":
            data["language_code"] = language_code

        try:
            r = requests.post(
                f"{self.base_url}/speech-to-text",
                headers=self._headers(),
                files=files,
                data=data,
                timeout=90,
            )
        except requests.Timeout:
            raise SarvamTimeoutError()
        return self._handle(r)

    # ---------- High-level: full voice translation pipeline ----------
    def voice_translate_pipeline(
        self,
        audio_file,
        target_lang="en-IN",
        source_lang="unknown",
        speaker="anushka",
    ):
        """
        1. STT (transcribe in source language)
        2. Translate to target
        3. TTS in target language
        """
        # Step 1: transcribe
        stt = self.speech_to_text(audio_file, language_code=source_lang, mode="transcribe")
        transcript = stt.get("transcript", "")
        detected_lang = stt.get("language_code", source_lang)

        if not transcript.strip():
            return {
                "transcript": "",
                "translated_text": "",
                "source_language_detected": detected_lang,
                "target_language": target_lang,
                "audio_base64": None,
            }

        # Step 2: translate
        tr = self.translate(transcript, source_lang=detected_lang, target_lang=target_lang)
        translated = tr.get("translated_text", "")

        # Step 3: TTS
        audio_b64 = None
        if translated.strip():
            tts = self.text_to_speech(translated, target_lang=target_lang, speaker=speaker)
            audios = tts.get("audios") or []
            if audios:
                audio_b64 = audios[0]

        return {
            "transcript": transcript,
            "translated_text": translated,
            "source_language_detected": detected_lang,
            "target_language": target_lang,
            "audio_base64": audio_b64,
        }