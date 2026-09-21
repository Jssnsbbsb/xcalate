from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import AskSerializer
from .services.groq_client import GroqClient          # 👈 CHANGED
from api.services.sarvam_client import SarvamClient
from api.services.exceptions import SarvamError


@api_view(["POST"])
@parser_classes([JSONParser])
def ask_companion(request):
    """
    POST /api/companion/ask/
    Body: {
      question: "Where can I see the sunset?",
      target_language: "hi-IN",
      region: "imphal",
      speaker: "anushka",
      include_audio: true
    }
    """
    serializer = AskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    d = serializer.validated_data

    # --- 1. Groq: get English answer ---
    try:
        ai = GroqClient()                              # 👈 CHANGED
        answer_en = ai.ask(
            question=d["question"],
            region=d.get("region") or None,
        )
    except Exception as e:
        return Response(
            {"error": "groq_error", "message": str(e), "code": "GROQ_ERROR"},  # 👈 CHANGED
            status=status.HTTP_502_BAD_GATEWAY,
        )

    # --- 2 & 3. Sarvam: translate + TTS ---
    answer_translated = answer_en
    audio_payload = None

    try:
        sarvam = SarvamClient()

        if d["target_language"] and not d["target_language"].startswith("en"):
            tr = sarvam.translate(
                text=answer_en,
                source_lang="en-IN",
                target_lang=d["target_language"],
            )
            answer_translated = tr.get("translated_text", answer_en)

        if d.get("include_audio", True):
            tts = sarvam.text_to_speech(
                text=answer_translated,
                target_lang=d["target_language"],
                speaker=d["speaker"],
            )
            audios = tts.get("audios") or []
            if audios:
                audio_payload = {
                    "format": "mp3",
                    "base64": audios[0],
                    "sample_rate": 22050,
                }

    except SarvamError as e:
        return Response({
            "question": d["question"],
            "answer_en": answer_en,
            "answer_translated": answer_translated,
            "target_language": d["target_language"],
            "audio": None,
            "warning": f"Translation/TTS failed: {e.message}",
        })

    return Response({
        "question": d["question"],
        "answer_en": answer_en,
        "answer_translated": answer_translated,
        "target_language": d["target_language"],
        "audio": audio_payload,
    })