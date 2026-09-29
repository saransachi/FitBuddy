from google import genai

from ..config import settings


def generate_nutrition_tip_with_flash(
    goal: str
) -> str:

    if not settings.AI_ENABLED:
        return create_fallback_nutrition_tip(goal)

    if not settings.GOOGLE_API_KEY:
        return create_fallback_nutrition_tip(goal)

    client = genai.Client(
        api_key=settings.GOOGLE_API_KEY
    )

    prompt = f"""
You are FitBuddy, a fitness and wellness assistant.

Give one short, practical nutrition and recovery tip
for a person whose fitness goal is:

{goal}

Requirements:
- Keep the advice general and safe.
- Do not recommend extreme dieting.
- Do not provide medical diagnosis.
- Keep the response easy to understand.
- Mention hydration, balanced nutrition, or recovery
  when appropriate.
"""

    try:
        response = client.models.generate_content(
            model=settings.NUTRITION_MODEL,
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return create_fallback_nutrition_tip(goal)

    except Exception:
        return create_fallback_nutrition_tip(goal)


def create_fallback_nutrition_tip(
    goal: str
) -> str:

    return (
        f"For your goal of {goal}, focus on balanced meals, "
        "adequate hydration, regular sleep, and sufficient "
        "recovery between workouts."
    )