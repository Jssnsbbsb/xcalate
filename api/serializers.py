from rest_framework import serializers


class TextTranslateSerializer(serializers.Serializer):
    input = serializers.CharField(max_length=2000)
    source_language = serializers.CharField(default="auto", required=False)
    target_language = serializers.CharField(default="hi-IN")


class TTSSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)
    target_language = serializers.CharField(default="hi-IN")
    speaker = serializers.CharField(default="anushka", required=False)
    pace = serializers.FloatField(default=1.0, min_value=0.5, max_value=2.0, required=False)
    codec = serializers.ChoiceField(
        choices=["mp3", "wav", "aac", "opus", "flac"],
        default="mp3",
        required=False,
    )


class VoiceTranslateSerializer(serializers.Serializer):
    audio = serializers.FileField()
    target_language = serializers.CharField(default="en-IN")
    source_language = serializers.CharField(default="unknown", required=False)
    speaker = serializers.CharField(default="anushka", required=False)
    stt_mode = serializers.ChoiceField(
        choices=["transcribe", "translate", "verbatim", "translit", "codemix"],
        default="transcribe",
        required=False,
    )