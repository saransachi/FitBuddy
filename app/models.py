from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Float,
        nullable=False
    )

    goal = Column(
        String(100),
        nullable=False
    )

    intensity = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class WorkoutPlan(Base):

    __tablename__ = "workout_plans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(100),
        nullable=False,
        index=True
    )

    original_plan = Column(
        Text,
        nullable=False
    )

    updated_plan = Column(
        Text,
        nullable=True
    )

    nutrition_tip = Column(
        Text,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )