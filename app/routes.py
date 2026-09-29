from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import User
from .models import WorkoutPlan

from .ai.gemini_generator import generate_workout_gemini
from .ai.gemini_flash_generator import generate_nutrition_tip_with_flash
from .ai.updated_plan import update_workout_plan


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


# =========================================
# Home Page
# =========================================

@router.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# =========================================
# Generate Workout Plan
# =========================================

@router.post("/generate-workout")
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db)
):

    intensity = intensity.strip().lower()

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user is None:

        user = User(
            user_id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

        db.add(user)

    else:

        user.name = name
        user.age = age
        user.weight = weight
        user.goal = goal
        user.intensity = intensity

    db.commit()

    workout_plan = generate_workout_gemini(
        name=name,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    nutrition_tip = generate_nutrition_tip_with_flash(
        goal=goal
    )

    existing_plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.user_id == user_id
        )
        .first()
    )

    if existing_plan is None:

        plan = WorkoutPlan(
            user_id=user_id,
            original_plan=workout_plan,
            updated_plan=None,
            nutrition_tip=nutrition_tip,
            feedback=None
        )

        db.add(plan)

    else:

        existing_plan.original_plan = workout_plan
        existing_plan.updated_plan = None
        existing_plan.nutrition_tip = nutrition_tip
        existing_plan.feedback = None

    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "user_id": user_id
        }
    )


# =========================================
# Submit Feedback
# =========================================

@router.post("/submit-feedback")
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    plan = (
        db.query(WorkoutPlan)
        .filter(
            WorkoutPlan.user_id == user_id
        )
        .first()
    )

    if plan is None:

        raise HTTPException(
            status_code=404,
            detail="Workout plan not found"
        )

    current_plan = (
        plan.updated_plan
        if plan.updated_plan
        else plan.original_plan
    )

    updated_plan = update_workout_plan(
        original_plan=current_plan,
        feedback=feedback
    )

    plan.updated_plan = updated_plan
    plan.feedback = feedback

    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "user": user,
            "plan": updated_plan,
            "nutrition_tip": plan.nutrition_tip,
            "user_id": user_id,
            "feedback_submitted": True
        }
    )


# =========================================
# View All Users - Admin
# =========================================

@router.get("/view-all-users")
def view_all_users(
    request: Request,
    admin_key: str = "",
    db: Session = Depends(get_db)
):

    if admin_key != settings.ADMIN_KEY:

        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={
                "request": request,
                "users": [],
                "error": "Invalid admin key"
            },
            status_code=403
        )

    users = (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )

    plans = (
        db.query(WorkoutPlan)
        .order_by(WorkoutPlan.created_at.desc())
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "request": request,
            "users": users,
            "plans": plans,
            "admin_key": admin_key
        }
    )


# =========================================
# Delete User - Admin
# =========================================

@router.post("/delete-user/{user_id}")
def delete_user(
    user_id: str,
    admin_key: str = Form(...),
    db: Session = Depends(get_db)
):

    if admin_key != settings.ADMIN_KEY:

        raise HTTPException(
            status_code=403,
            detail="Invalid admin key"
        )

    user = (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )

    if user:

        db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).delete()

        db.delete(user)

        db.commit()

    return RedirectResponse(
        url=f"/view-all-users?admin_key={admin_key}",
        status_code=303
    )