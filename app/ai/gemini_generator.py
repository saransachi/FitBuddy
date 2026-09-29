from google import genai

from ..config import settings


def fallback_plan(
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
) -> str:

    return f"""
FITBUDDY - 7 DAY FITNESS PLAN

Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}


DAY 1 - FULL BODY

Warm-up:
5-10 minutes of easy movement.

Workout:
- Bodyweight squats: 3 sets x 10 reps
- Incline push-ups: 3 sets x 8 reps
- Glute bridges: 3 sets x 12 reps
- Bird dogs: 3 sets x 8 each side

Cooldown:
5 minutes of gentle stretching.


DAY 2 - CARDIO

Warm-up:
5 minutes.

Workout:
- Brisk walking or cycling: 20-30 minutes
- Easy mobility: 5 minutes

Cooldown:
5 minutes.


DAY 3 - UPPER BODY

Warm-up:
5-10 minutes.

Workout:
- Incline push-ups: 3 x 8
- Resistance-band rows: 3 x 10
- Shoulder raises: 2 x 10
- Dead bug: 3 x 8 each side

Cooldown:
5 minutes.


DAY 4 - RECOVERY

- Easy walking: 15-20 minutes
- Gentle stretching
- Mobility exercises
- Focus on hydration and sleep


DAY 5 - LOWER BODY

Warm-up:
5-10 minutes.

Workout:
- Squats: 3 x 10
- Reverse lunges: 2 x 8 each side
- Glute bridges: 3 x 12
- Calf raises: 3 x 12

Cooldown:
5 minutes.


DAY 6 - CARDIO + CORE

Warm-up:
5 minutes.

Workout:
- Brisk walking/cycling: 20 minutes
- Plank: 3 x 15-30 seconds
- Dead bug: 3 x 8 each side

Cooldown:
5 minutes.


DAY 7 - REST

- Light walking if comfortable
- Gentle stretching
- Recovery
- Adequate sleep


SAFETY NOTE:

Start gradually, use proper technique,
rest when necessary, and stop if an exercise
causes pain or unusual symptoms.
"""


def generate_workout_gemini(
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
) -> str:

    if (
        not settings.AI_ENABLED
        or not settings.GOOGLE_API_KEY
    ):
        return fallback_plan(
            name,
            age,
            weight,
            goal,
            intensity
        )

    client = genai.Client(
        api_key=settings.GOOGLE_API_KEY
    )

    prompt = f"""
You are the workout-planning AI for FitBuddy.

Create a safe, beginner-friendly 7-day fitness plan.

User information:

Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

Requirements:

1. Create exactly seven days.
2. Include a warm-up.
3. Include the main workout.
4. Include sets, repetitions, or duration.
5. Include rest periods where appropriate.
6. Include cooldown or recovery.
7. Adapt the plan to the user's goal.
8. Adapt the plan to the selected intensity.
9. Do not diagnose medical conditions.
10. Do not make extreme weight-loss claims.
11. Do not recommend extreme dieting.
12. Keep the plan practical and age-appropriate.

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
            "Gemini workout error:",
            error
        )

    return fallback_plan(
        name,
        age,
        weight,
        goal,
        intensity
    )