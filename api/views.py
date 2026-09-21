from django.shortcuts import render

# Create your views here.
import time
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .services.sarvam_client import (
    SarvamClient,
    SUPPORTED_LANGUAGES,
    SUPPORTED_VOICES,
)
from .services.exceptions import SarvamError
from .serializers import (
    TextTranslateSerializer,
    TTSSerializer,
    VoiceTranslateSerializer,
)


# ---------- Health ----------
@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "message": "API is live 🚀"})


# ---------- Meta ----------
@api_view(["GET"])
def languages(request):
    return Response({
        "languages": [
            {"code": code, "name": name}
            for code, name in SUPPORTED_LANGUAGES.items()
        ]
    })


@api_view(["GET"])
def voices(request):
    return Response({"voices": SUPPORTED_VOICES})


# ---------- Voice Translation (main) ----------
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def voice_translate(request):
    serializer = VoiceTranslateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    audio = data["audio"]

    # Basic validation
    if audio.size > 25 * 1024 * 1024:
        return Response(
            {"error": "audio_too_large", "message": "Max 25 MB", "code": "AUDIO_TOO_LONG"},
            status=400,
        )

    started = time.time()
    try:
        client = SarvamClient()
        result = client.voice_translate_pipeline(
            audio_file=audio,
            target_lang=data["target_language"],
            source_lang=data["source_language"],
            speaker=data["speaker"],
        )
    except SarvamError as e:
        return Response(
            {"error": e.code.lower(), "message": e.message, "code": e.code},
            status=e.status,
        )

    return Response({
        "request_id": f"vt_{int(started)}",
        "transcript": result["transcript"],
        "translated_text": result["translated_text"],
        "source_language_detected": result["source_language_detected"],
        "target_language": result["target_language"],
        "audio": {
            "format": "mp3",
            "sample_rate": 22050,
            "base64": result["audio_base64"],
        },
        "processing_time_ms": int((time.time() - started) * 1000),
    })


# ---------- Text Translation ----------
@api_view(["POST"])
@parser_classes([JSONParser])
def text_translate(request):
    serializer = TextTranslateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    d = serializer.validated_data

    try:
        client = SarvamClient()
        result = client.translate(
            text=d["input"],
            source_lang=d["source_language"],
            target_lang=d["target_language"],
        )
    except SarvamError as e:
        return Response(
            {"error": e.code.lower(), "message": e.message, "code": e.code},
            status=e.status,
        )

    return Response({
        "translated_text": result.get("translated_text", ""),
        "source_language_detected": result.get("source_language_code", d["source_language"]),
        "target_language": d["target_language"],
    })


# ---------- TTS ----------
@api_view(["POST"])
@parser_classes([JSONParser])
def text_tts(request):
    serializer = TTSSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    d = serializer.validated_data

    try:
        client = SarvamClient()
        result = client.text_to_speech(
            text=d["text"],
            target_lang=d["target_language"],
            speaker=d["speaker"],
            pace=d["pace"],
        )
    except SarvamError as e:
        return Response(
            {"error": e.code.lower(), "message": e.message, "code": e.code},
            status=e.status,
        )

    audios = result.get("audios") or []
    return Response({
        "request_id": result.get("request_id", ""),
        "audio": {
            "format": d["codec"],
            "base64": audios[0] if audios else None,
            "sample_rate": 22050,
        },
    })
@api_view(["POST"])
@parser_classes([JSONParser])
def text_translate_to_manipuri(request):
    """
    Translates text from a source language (auto-detected) into Manipuri.
    Perfect for tourist use cases.
    """
    source_text = request.data.get("text")
    if not source_text:
        return Response(
            {"error": "missing_text", "message": "Field 'text' is required"},
            status=400,
        )

    try:
        client = SarvamClient()
        # Use source_lang='auto' for automatic detection of English, French, etc.
        result = client.translate(
            text=source_text,
            source_lang="auto",
            target_lang="mni-IN"  # Always Manipuri
        )
    except SarvamError as e:
        return Response({"error": e.code, "message": e.message}, status=e.status)

    return Response({
        "original_text": source_text,
        "manipuri_text": result.get("translated_text", ""),
        "source_language_detected": result.get("source_language_code", "unknown"),
        "target_language": "mni-IN"
    })