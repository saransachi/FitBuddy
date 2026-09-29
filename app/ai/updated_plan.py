from google import genai

from ..config import settings


def fallback_updated_plan(
    original_plan: str,
    feedback: str
) -> str:

    return f"""
UPDATED FITBUDDY PLAN

The following feedback was received:

{feedback}


UPDATED PLAN

Keep the original plan as the starting point
and make reasonable adjustments based on the
feedback.

DAY 1
- Light warm-up
- Comfortable full-body exercises
- Cooldown and recovery


DAY 2
- Moderate walking or another comfortable
  cardio activity
- Gentle mobility


DAY 3
- Upper-body exercises
- Core exercises
- Cooldown


DAY 4
- Recovery day
- Gentle walking
- Stretching
- Adequate rest


DAY 5
- Lower-body exercises
- Comfortable repetitions
- Cooldown


DAY 6
- Light cardio
- Core exercises
- Recovery


DAY 7
- Rest and recovery


SAFETY NOTE:

Make gradual changes, use proper technique,
and stop an exercise if it causes pain or
unusual symptoms.
"""


def update_workout_plan(
    original_plan: str,
    feedback: str
) -> str:

    if (
        not settings.AI_ENABLED
        or not settings.GOOGLE_API_KEY
    ):
        return fallback_updated_plan(
            original_plan,
            feedback
        )

    client = genai.Client(
        api_key=settings.GOOGLE_API_KEY
    )

    prompt = f"""
You are FitBuddy's fitness-plan update assistant.

The user already has this 7-day plan:

---------------- ORIGINAL PLAN ----------------

{original_plan}

---------------- USER FEEDBACK ----------------

{feedback}

-------------------------------------------------

Create an updated 7-day fitness plan based on
the user's feedback.

Requirements:

1. Keep exactly seven days.
2. Make reasonable changes based on the feedback.
3. Keep the plan practical.
4. Include warm-up.
5. Include workout.
6. Include duration, sets, or repetitions.
7. Include cooldown or recovery.
8. Do not diagnose medical conditions.
9. Do not recommend extreme dieting.
10. Do not make extreme weight-loss claims.
11. If the feedback suggests pain or injury,
    recommend appropriate rest and professional
    medical guidance rather than pushing through it.

Use this structure:

DAY 1
Focus:
Warm-up:
Workout:
Cooldown:

DAY 2
Focus:
Warm-up:
Workout:
Cooldown:

Continue through DAY 7.

End with a short safety note.
"""

    try:

        response = client.models.generate_content(
            model=settings.WORKOUT_MODEL,
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
            "Gemini updated-plan error:",
            error
        )

    return fallback_updated_plan(
        original_plan,
        feedback
    )