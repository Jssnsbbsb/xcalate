from rest_framework import serializers


class AskSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    target_language = serializers.CharField(default="hi-IN", required=False)
    region = serializers.CharField(required=False, allow_blank=True)
    speaker = serializers.CharField(default="anushka", required=False)
    include_audio = serializers.BooleanField(default=True, required=False)