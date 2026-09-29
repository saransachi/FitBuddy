from google import genai

from ..config import settings


def fallback_tip(goal: str) -> str:

    goal_lower = goal.lower()

    if "muscle" in goal_lower:

        return (
            "Nutrition tip: Include protein-rich foods "
            "in regular balanced meals. Stay hydrated "
            "and prioritize adequate sleep and recovery."
        )

    if (
        "weight" in goal_lower
        or "loss" in goal_lower
    ):

        return (
            "Nutrition tip: Focus on balanced meals "
            "with vegetables, whole grains, protein "
            "and healthy fats. Drink water regularly "
            "and avoid extreme dieting."
        )

    return (
        "Recovery tip: Stay hydrated, eat balanced "
        "meals, sleep adequately, and allow enough "
        "recovery between challenging workouts."
    )


def generate_nutrition_tip_with_flash(
    goal: str
) -> str:

    if (
        not settings.AI_ENABLED
        or not settings.GOOGLE_API_KEY
    ):
        return fallback_tip(goal)

    client = genai.Client(
        api_key=settings.GOOGLE_API_KEY
    )

    prompt = f"""
You are FitBuddy's nutrition and recovery assistant.

Fitness goal:
{goal}

Give ONE concise practical nutrition
or recovery tip.

Requirements:

- Maximum 100 words.
- Easy to understand.
- No extreme dieting.
- No medical diagnosis.
- Do not recommend restrictive eating.
- Mention hydration, balanced nutrition,
  protein or recovery when appropriate.
"""

    try:

        response = client.models.generate_content(
            model=settings.NUTRITION_MODEL,
            contents=prompt
        )

        text = getattr(
            response,
            "text",
            None
        )

        if text:
            return text.strip()

    except Exception as error:

        print(
            "Gemini nutrition error:",
            error
        )

    return fallback_tip(goal)