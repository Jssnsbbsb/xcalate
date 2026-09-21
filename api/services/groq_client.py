from groq import Groq
from django.conf import settings
from places.models import Place


SYSTEM_PROMPT = """You are "Manipur Travel Companion" — a friendly, knowledgeable local guide
for tourists visiting Manipur, India. You help with:

- Places to visit (monuments, nature, temples, markets)
- Local food and restaurants
- Cultural etiquette and customs
- Best time to visit spots
- Travel tips within Manipur

Rules:
- Keep answers SHORT (2-4 sentences max) — they will be spoken aloud.
- Be warm, personal, and helpful. Speak like a local friend.
- If the user asks about something outside Manipur tourism, gently redirect.
- Use the CONTEXT below when relevant. Don't invent facts.
- Answer in English. Translation happens separately.
"""


class GroqClient:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set in environment")
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def _build_context(self, region=None, limit=15):
        """Pull relevant places from DB to ground the AI."""
        qs = Place.objects.all()
        if region:
            qs = qs.filter(region=region)
        qs = qs.order_by("-is_featured", "-rating")[:limit]

        lines = []
        for p in qs:
            lines.append(
                f"- {p.name} ({p.category}, {p.region}): {p.short_description}"
            )
        return "\n".join(lines) if lines else "No places in database yet."

    def ask(self, question, region=None):
        """
        Ask a question → returns English answer text.
        """
        context = self._build_context(region=region)

        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"""CONTEXT (curated Manipur data):
{context}

USER QUESTION:
{question}

Answer as the Manipur Travel Companion.""",
                    },
                ],
                model=self.model,
                temperature=0.6,
                max_tokens=300,
            )
            text = (completion.choices[0].message.content or "").strip()
            return text or "Sorry, I couldn't find an answer to that."
        except Exception as e:
            raise RuntimeError(f"Groq error: {e}")