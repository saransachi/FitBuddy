import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "FitBuddy - AI Fitness Plan Generator"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./fitbuddy.db"
    )

    GOOGLE_API_KEY = os.getenv(
        "GOOGLE_API_KEY",
        ""
    )

    WORKOUT_MODEL = os.getenv(
        "WORKOUT_MODEL",
        "gemini-2.5-flash"
    )

    NUTRITION_MODEL = os.getenv(
        "NUTRITION_MODEL",
        "gemini-2.5-flash"
    )

    ADMIN_KEY = os.getenv(
        "ADMIN_KEY",
        "fitbuddy-admin"
    )

    AI_ENABLED = os.getenv(
        "AI_ENABLED",
        "true"
    ).lower() == "true"


settings = Settings()
