from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("languages/", views.languages, name="languages"),
    path("voices/", views.voices, name="voices"),
    path("voice/translate/", views.voice_translate, name="voice-translate"),
    path("text/translate/", views.text_translate, name="text-translate"),
    path("text/tts/", views.text_tts, name="text-tts"),
]