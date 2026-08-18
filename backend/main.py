from sqlalchemy import func
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from auth import authenticate_user, create_access_token, get_password_hash
from database import Base, engine, ensure_student_profile_columns, ensure_student_projects_user_id, ensure_student_skills_user_id
from dependencies import get_current_user, get_db
from models import SkillAssessmentResult, StudentCareerGoal, StudentProfile, StudentProject, StudentSkill, User, Chat, ChatMessage
from schemas import (
    LoginRequest,
    RegisterRequest,
    StudentProfileCreate,
    StudentProfileResponse,
    StudentProfileUpdate,
    ChatMessageRequest,
    ChatResponse,
    ChatListResponse,
    ChatbotResponse,
)
from learning_planner import (
    build_adaptive_recommendations,
    build_course_recommendations,
    build_learning_plan,
    build_learning_progress,
    build_learning_roadmap,
    get_missing_skills,
)
from skill_intelligence import (
    build_recommendations,
    build_skill_gap,
    evaluate_assessment,
    get_questions_for_skill,
    normalize_skill_name,
)
from chatbot_logic import ChatbotLogic, StudentContextBuilder

Base.metadata.create_all(bind=engine)
ensure_student_profile_columns()
ensure_student_skills_user_id()
ensure_student_projects_user_id()

app = FastAPI(
    title="AI-Powered Student Support API",
    version="1.0.0",
    description="Authentication and student profile backend for the student support platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


def normalize_email(email: str | None) -> str | None:
    if email is None:
        return None
    cleaned = email.strip()
    if not cleaned:
        return None
    return cleaned.lower()


def get_or_create_student_profile(db: Session, current_user: User) -> StudentProfile:
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if profile:
        return profile

    profile = StudentProfile(
        user_id=current_user.id,
        full_name=current_user.full_name,
        email=current_user.email,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def validate_email_for_user(db: Session, current_user: User, email: str | None):
    normalized_email = normalize_email(email)
    if not normalized_email:
        existing_email = normalize_email(getattr(current_user, "email", None))
        if existing_email:
            return existing_email
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required.",
        )

    try:
        from pydantic import EmailStr, TypeAdapter, ValidationError

        TypeAdapter(EmailStr).validate_python(normalized_email)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please enter a valid email address.",
        )

    existing_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_user and existing_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered to another user.",
        )

    return normalized_email


@app.get("/")
def health_check():
    return {"message": "Authentication backend is running"}


@app.post("/register")
@app.post("/api/register")
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    user = User(
        full_name=payload.full_name.strip(),
        email=email,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        },
    }
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

# Ensure you have your database session dependency and models imported
# Example endpoint implementation:

@app.get("/api/student/profile")
def get_student_profile(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_email = current_user.email if hasattr(current_user, "email") else current_user.get("sub")
    db_user = db.query(User).filter(User.email == user_email).first() if hasattr(User, "email") else current_user

    return {
        "full_name": getattr(db_user, "full_name", "Student"),
        "email": getattr(db_user, "email", user_email),
        "profile": getattr(db_user, "profile", None),
        "skills": [],
        "projects": [],
        "certifications": [],
        "career_goal": None
    }

@app.post("/api/student/profile")
def update_student_profile(payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return {"message": "Profile updated successfully"}

@app.post("/login")
@app.post("/api/login")
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email.strip().lower(), payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        },
    }


@app.get("/me")
@app.get("/api/me")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat(),
    }


@app.get("/profile")
@app.get("/api/profile")
def get_student_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    career_goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()

    serialized_skills = [
        {
            "id": skill.id,
            "skill_name": skill.skill_name,
            "proficiency": skill.proficiency,
        }
        for skill in db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    ]

    serialized_projects = [
        {
            "id": project.id,
            "project_name": project.project_name,
            "description": project.description,
            "technologies_used": project.technologies_used,
            "skills_used": project.skills_used,
            "student_role": project.student_role,
            "project_duration": project.project_duration,
            "project_link": project.project_link,
        }
        for project in db.query(StudentProject).filter(StudentProject.user_id == current_user.id).all()
    ]

    result = {
        "id": profile.id if profile else None,
        "user_id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
        "phone_number": profile.phone_number if profile else None,
        "university": profile.university if profile else None,
        "branch": profile.branch if profile else None,
        "year_of_study": profile.year_of_study if profile else None,
        "current_semester": profile.current_semester if profile else None,
        "cgpa_percentage": profile.cgpa_percentage if profile else None,
        "skills": serialized_skills,
        "projects": serialized_projects,
        "career_goal": {
            "target_career": career_goal.target_career if career_goal else None,
            "preferred_role": career_goal.preferred_role if career_goal else None,
            "preferred_industry": career_goal.preferred_industry if career_goal else None,
            "career_interests": career_goal.career_interests if career_goal else None,
            "short_term_goal": career_goal.short_term_goal if career_goal else None,
            "long_term_goal": career_goal.long_term_goal if career_goal else None,
        } if career_goal else None,
    }
    return result


@app.post("/profile", response_model=StudentProfileResponse)
@app.post("/api/profile", response_model=StudentProfileResponse)
def create_student_profile(
    payload: StudentProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student profile already exists. Use PUT /profile to update it.",
        )

    profile = StudentProfile(user_id=current_user.id)
    data = payload.model_dump(exclude_unset=True)

    if "full_name" in data and data["full_name"] is not None:
        full_name = str(data["full_name"]).strip()
        if not full_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name cannot be empty.",
            )
        profile.full_name = full_name
        current_user.full_name = full_name

    if "email" in data and data["email"] is not None:
        email = validate_email_for_user(db, current_user, str(data["email"]))
        profile.email = email
        current_user.email = email

    for field, value in data.items():
        if field in {"full_name", "email"}:
            continue
        if value is not None:
            setattr(profile, field, value)

    db.add(profile)
    db.commit()
    db.refresh(profile)
    db.refresh(current_user)
    return profile


@app.put("/profile", response_model=StudentProfileResponse)
@app.put("/api/profile", response_model=StudentProfileResponse)
def update_student_profile(
    payload: StudentProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    data = payload.model_dump(exclude_unset=True)

    if "full_name" in data and data["full_name"] is not None:
        full_name = str(data["full_name"]).strip()
        if not full_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name cannot be empty.",
            )
        profile.full_name = full_name
        current_user.full_name = full_name

    if "email" in data and data["email"] is not None:
        email = validate_email_for_user(db, current_user, str(data["email"]))
        profile.email = email
        current_user.email = email

    for field, value in data.items():
        if field in {"full_name", "email"}:
            continue
        if value is not None:
            setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    db.refresh(current_user)
    return profile


@app.post("/api/student/skills")
@app.post("/profile/skills")
@app.post("/api/profile/skills")
def create_skill(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill_name = str(payload.get("skill_name", "")).strip()
    if not skill_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill name is required.")

    try:
        student_profile = get_or_create_student_profile(db, current_user)

        existing = db.query(StudentSkill).filter(
            StudentSkill.user_id == current_user.id,
            StudentSkill.profile_id == student_profile.id,
            StudentSkill.skill_name.ilike(skill_name),
        ).first()
        if existing:
            return {"id": existing.id, "skill_name": existing.skill_name, "proficiency": existing.proficiency}

        skill = StudentSkill(
            user_id=current_user.id,
            profile_id=student_profile.id,
            skill_name=skill_name,
            proficiency=str(payload.get("proficiency") or "Intermediate"),
        )
        db.add(skill)
        db.commit()
        db.refresh(skill)
        return {"id": skill.id, "skill_name": skill.skill_name, "proficiency": skill.proficiency}
    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Skill save failed: {exc}") from exc


@app.get("/api/student/skills")
@app.get("/profile/skills")
@app.get("/api/profile/skills")
def list_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return [
        {"id": skill.id, "skill_name": skill.skill_name, "proficiency": skill.proficiency}
        for skill in db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    ]


@app.put("/api/student/skills/{skill_id}")
@app.put("/api/profile/skills/{skill_id}")
def update_skill(
    skill_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.query(StudentSkill).filter(StudentSkill.id == skill_id, StudentSkill.user_id == current_user.id).first()
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found.")

    skill_name = str(payload.get("skill_name", "")).strip()
    if not skill_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill name is required.")

    student_profile = get_or_create_student_profile(db, current_user)
    duplicate = (
        db.query(StudentSkill)
        .filter(
            StudentSkill.user_id == current_user.id,
            StudentSkill.profile_id == student_profile.id,
            StudentSkill.skill_name.ilike(skill_name),
            StudentSkill.id != skill_id,
        )
        .first()
    )
    if duplicate:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill already exists.")

    skill.skill_name = skill_name
    skill.proficiency = str(payload.get("proficiency") or skill.proficiency or "Intermediate")
    db.commit()
    db.refresh(skill)
    return {"id": skill.id, "skill_name": skill.skill_name, "proficiency": skill.proficiency}


@app.delete("/api/student/skills/{skill_id}")
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.query(StudentSkill).filter(StudentSkill.id == skill_id, StudentSkill.user_id == current_user.id).first()
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found.")
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted successfully."}


@app.post("/api/student/projects")
def create_project(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project_name = str(payload.get("project_name", "")).strip()
    if not project_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Project name is required.")

    student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student_profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student profile not found.")

    project = StudentProject(
        user_id=current_user.id,
        profile_id=student_profile.id,
        title=project_name,
        project_name=project_name,
        description=str(payload.get("description") or ""),
        technologies_used=str(payload.get("technologies_used") or ""),
        skills_used=str(payload.get("skills_used") or ""),
        student_role=str(payload.get("student_role") or ""),
        project_duration=str(payload.get("project_duration") or ""),
        project_link=str(payload.get("project_link") or ""),
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {
        "id": project.id,
        "project_name": project.project_name,
        "description": project.description,
        "technologies_used": project.technologies_used,
        "skills_used": project.skills_used,
        "student_role": project.student_role,
        "project_duration": project.project_duration,
        "project_link": project.project_link,
    }


@app.get("/api/student/projects")
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return [
        {
            "id": project.id,
            "project_name": project.project_name,
            "description": project.description,
            "technologies_used": project.technologies_used,
            "skills_used": project.skills_used,
            "student_role": project.student_role,
            "project_duration": project.project_duration,
            "project_link": project.project_link,
        }
        for project in db.query(StudentProject).filter(StudentProject.user_id == current_user.id).all()
    ]


@app.delete("/api/student/projects/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = db.query(StudentProject).filter(StudentProject.id == project_id, StudentProject.user_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully."}


@app.get("/api/student/career-goal")
def get_career_goal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    if not goal:
        return {}
    return {
        "target_career": goal.target_career,
        "preferred_role": goal.preferred_role,
        "preferred_industry": goal.preferred_industry,
        "career_interests": goal.career_interests,
        "short_term_goal": goal.short_term_goal,
        "long_term_goal": goal.long_term_goal,
    }


@app.post("/api/student/career-goal")
def save_career_goal(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    if not goal:
        goal = StudentCareerGoal(user_id=current_user.id)
        db.add(goal)

    goal.target_career = str(payload.get("target_career") or "").strip()
    goal.preferred_role = str(payload.get("preferred_role") or "").strip()
    goal.preferred_industry = str(payload.get("preferred_industry") or "").strip()
    goal.career_interests = str(payload.get("career_interests") or "").strip()
    goal.short_term_goal = str(payload.get("short_term_goal") or "").strip()
    goal.long_term_goal = str(payload.get("long_term_goal") or "").strip()

    db.commit()
    db.refresh(goal)
    return {
        "target_career": goal.target_career,
        "preferred_role": goal.preferred_role,
        "preferred_industry": goal.preferred_industry,
        "career_interests": goal.career_interests,
        "short_term_goal": goal.short_term_goal,
        "long_term_goal": goal.long_term_goal,
    }


@app.get("/api/student/skill-gap")
def get_skill_gap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()

    current_skill_names = [normalize_skill_name(skill.skill_name) for skill in skills]
    career_name = goal.target_career if goal else (profile.full_name if profile and profile.full_name else None)
    preferred_role = goal.preferred_role if goal else None

    if not current_skill_names:
        return {
            "has_skills": False,
            "has_career_goal": bool(goal),
            "message": "No skills added yet. Add your skills in Student Profile to generate your skill analysis.",
            "overall_match": 0,
            "strong_skills": [],
            "developing_skills": [],
            "missing_skills": [],
            "required_skills": [],
            "career_name": career_name or "Career Goal",
        }

    if not goal:
        return {
            "has_skills": True,
            "has_career_goal": False,
            "message": "Set your career goal to generate a personalized skill-gap analysis.",
            "overall_match": 0,
            "strong_skills": [],
            "developing_skills": current_skill_names,
            "missing_skills": [],
            "required_skills": [],
            "career_name": "Career Goal",
        }

    result = build_skill_gap(current_skill_names, career_name, preferred_role)
    result["has_skills"] = True
    result["has_career_goal"] = True
    return result


@app.get("/api/student/assessment/skills")
def list_available_assessment_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    names = sorted({normalize_skill_name(skill.skill_name) for skill in skills if normalize_skill_name(skill.skill_name)})
    if not names:
        return {"skills": [], "message": "No skills added yet. Add your skills in Student Profile to generate assessments."}
    return {"skills": names}


@app.get("/api/student/assessment/questions")
def get_assessment_questions(
    skill_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not skill_name or not skill_name.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill name is required.")
    questions = get_questions_for_skill(skill_name)
    return {"skill_name": skill_name, "questions": questions}


@app.post("/api/student/assessment/submit")
def submit_assessment(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill_name = normalize_skill_name(str(payload.get("skill_name") or ""))
    if not skill_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Skill name is required.")

    answers = payload.get("answers") or []
    if not isinstance(answers, list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assessment answers must be a list.")

    result = evaluate_assessment(skill_name, answers)

    assessment = SkillAssessmentResult(
        user_id=current_user.id,
        skill_name=result["skill_name"],
        score=result["score"],
        total_questions=result["total_questions"],
        percentage=result["percentage"],
        level=result["level"],
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return {
        "id": assessment.id,
        "skill_name": assessment.skill_name,
        "score": assessment.score,
        "total_questions": assessment.total_questions,
        "percentage": assessment.percentage,
        "level": assessment.level,
    }


@app.get("/api/student/assessment-results")
def list_assessment_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(SkillAssessmentResult)
        .filter(SkillAssessmentResult.user_id == current_user.id)
        .order_by(SkillAssessmentResult.created_at.desc())
        .all()
    )
    latest_by_skill: dict[str, dict] = {}
    for item in results:
        latest_by_skill.setdefault(item.skill_name, {
            "skill_name": item.skill_name,
            "score": item.score,
            "total_questions": item.total_questions,
            "percentage": item.percentage,
            "level": item.level,
        })
    return {"results": list(latest_by_skill.values())}


@app.get("/api/student/skill-dashboard")
def get_skill_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    current_skill_names = [normalize_skill_name(skill.skill_name) for skill in skills]
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    profile_data = {
        "current_skills": current_skill_names,
        "career_name": goal.target_career if goal else None,
        "preferred_role": goal.preferred_role if goal else None,
    }
    gap = build_skill_gap(profile_data["current_skills"], profile_data["career_name"], profile_data["preferred_role"])
    assessment_results = (
        db.query(SkillAssessmentResult)
        .filter(SkillAssessmentResult.user_id == current_user.id)
        .order_by(SkillAssessmentResult.created_at.desc())
        .all()
    )
    latest_results = {}
    for item in assessment_results:
        latest_results.setdefault(item.skill_name, item)

    return {
        "overall_skill_score": gap.get("overall_match", 0),
        "strong_skills": gap.get("strong_skills", []),
        "developing_skills": gap.get("developing_skills", []),
        "missing_skills": gap.get("missing_skills", []),
        "assessment_results": [
            {
                "skill_name": item.skill_name,
                "percentage": item.percentage,
                "level": item.level,
            }
            for item in latest_results.values()
        ],
        "career_name": profile_data["career_name"] or "Career Goal",
    }


@app.get("/api/student/recommendations")
def get_skill_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    current_skill_names = [normalize_skill_name(skill.skill_name) for skill in skills]
    recommendations = build_recommendations(
        current_skill_names,
        goal.target_career if goal else None,
        goal.preferred_role if goal else None,
    )
    return {"recommendations": recommendations}


@app.get("/api/student/course-recommendations")
def get_course_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    current_skill_names = [normalize_skill_name(skill.skill_name) for skill in skills]
    career_name = goal.target_career if goal else None
    preferred_role = goal.preferred_role if goal else None
    missing_skills = get_missing_skills(current_skill_names, career_name, preferred_role)
    recommendations = build_course_recommendations(
        current_skill_names,
        career_name,
        preferred_role,
        missing_skills,
    )
    return {
        "career_name": career_name or "Career Goal",
        "missing_skills": missing_skills,
        "recommendations": recommendations,
    }


@app.get("/api/student/learning-roadmap")
def get_learning_roadmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    assessment_results = (
        db.query(SkillAssessmentResult)
        .filter(SkillAssessmentResult.user_id == current_user.id)
        .order_by(SkillAssessmentResult.created_at.desc())
        .all()
    )
    current_skill_names = [normalize_skill_name(skill.skill_name) for skill in skills]
    roadmap = build_learning_roadmap(
        current_skill_names,
        [
            {"skill_name": result.skill_name, "percentage": result.percentage}
            for result in assessment_results
        ],
        goal.target_career if goal else None,
        goal.preferred_role if goal else None,
    )
    return {"roadmap": roadmap}


@app.get("/api/student/learning-progress")
def get_learning_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    assessment_results = (
        db.query(SkillAssessmentResult)
        .filter(SkillAssessmentResult.user_id == current_user.id)
        .order_by(SkillAssessmentResult.created_at.desc())
        .all()
    )
    current_skill_names = [normalize_skill_name(skill.skill_name) for skill in skills]
    career_name = goal.target_career if goal else None
    preferred_role = goal.preferred_role if goal else None
    missing_skills = get_missing_skills(current_skill_names, career_name, preferred_role)
    course_recommendations = build_course_recommendations(
        current_skill_names,
        career_name,
        preferred_role,
        missing_skills,
    )
    progress = build_learning_progress(
        current_skill_names,
        missing_skills,
        course_recommendations,
        [
            {"skill_name": result.skill_name, "percentage": result.percentage}
            for result in assessment_results
        ],
        career_name,
    )
    progress["career_name"] = career_name or "Career Goal"
    return progress


@app.post("/api/student/learning-plan")
def generate_learning_plan(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    current_skill_names = [normalize_skill_name(skill.skill_name) for skill in skills]
    career_name = goal.target_career if goal else None
    preferred_role = goal.preferred_role if goal else None
    missing_skills = get_missing_skills(current_skill_names, career_name, preferred_role)
    daily_study_time = str(payload.get("daily_study_time") or "1 hour")
    learning_preference = str(payload.get("learning_preference") or "Mixed")
    plan = build_learning_plan(
        daily_study_time,
        learning_preference,
        missing_skills,
        current_skill_names,
        career_name,
    )
    adaptive = build_adaptive_recommendations(
        current_skill_names,
        missing_skills,
        [
            {"skill_name": result.skill_name, "percentage": result.percentage}
            for result in db.query(SkillAssessmentResult)
            .filter(SkillAssessmentResult.user_id == current_user.id)
            .order_by(SkillAssessmentResult.created_at.desc())
            .all()
        ],
        career_name,
    )
    return {
        "plan": plan,
        "adaptive_recommendations": adaptive,
        "missing_skills": missing_skills,
    }


@app.get("/api/student/adaptive-recommendations")
def get_adaptive_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skills = db.query(StudentSkill).filter(StudentSkill.user_id == current_user.id).all()
    goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == current_user.id).first()
    current_skill_names = [normalize_skill_name(skill.skill_name) for skill in skills]
    missing_skills = get_missing_skills(
        current_skill_names,
        goal.target_career if goal else None,
        goal.preferred_role if goal else None,
    )
    assessment_results = [
        {"skill_name": result.skill_name, "percentage": result.percentage}
        for result in db.query(SkillAssessmentResult)
        .filter(SkillAssessmentResult.user_id == current_user.id)
        .order_by(SkillAssessmentResult.created_at.desc())
        .all()
    ]
    return {
        "recommendations": build_adaptive_recommendations(
            current_skill_names,
            missing_skills,
            assessment_results,
            goal.target_career if goal else None,
        )
    }


# ==================== CHATBOT ENDPOINTS ====================


@app.get("/api/chat/context")
def get_chat_context(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the student's context for the chatbot"""
    context = StudentContextBuilder.build_context(current_user, db)
    return {
        "summary": context.get("summary"),
        "career_goal": context.get("career_goal"),
        "skills": context.get("skills"),
        "missing_skills": context.get("missing_skills"),
        "level": StudentContextBuilder._calculate_average_level(
            context.get("assessment_results", {})
        ),
    }


@app.post("/api/chat/new")
def create_new_chat(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new chat conversation"""
    chat = Chat(
        user_id=current_user.id,
        title="New Conversation"
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return {
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at.isoformat(),
        "updated_at": chat.updated_at.isoformat(),
    }


@app.get("/api/chat/list")
def list_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all chat conversations for current user"""
    chats = (
        db.query(Chat)
        .filter(Chat.user_id == current_user.id)
        .order_by(Chat.updated_at.desc())
        .all()
    )
    return {
        "chats": [
            {
                "id": chat.id,
                "title": chat.title,
                "created_at": chat.created_at.isoformat(),
                "updated_at": chat.updated_at.isoformat(),
            }
            for chat in chats
        ]
    }


@app.get("/api/chat/{chat_id}")
def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific chat conversation with all messages"""
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found."
        )

    messages = db.query(ChatMessage).filter(
        ChatMessage.chat_id == chat_id
    ).order_by(ChatMessage.created_at.asc()).all()

    return {
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at.isoformat(),
        "updated_at": chat.updated_at.isoformat(),
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in messages
        ]
    }


@app.post("/api/chat/{chat_id}/message")
async def send_chat_message(
    chat_id: int,
    payload: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Send a message and get AI response"""
    # Verify chat exists and belongs to user
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found."
        )

    user_message = payload.content.strip()
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty."
        )

    # Save user message
    user_msg = ChatMessage(
        chat_id=chat_id,
        user_id=current_user.id,
        role="user",
        content=user_message
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # Generate AI response using chatbot logic
    try:
        response_data = await ChatbotLogic.process_message(
            user_message, current_user, db
        )
        ai_response_text = response_data.get("response", "I couldn't generate a response. Please try again.")
    except Exception as e:
        ai_response_text = f"An error occurred while processing your message. Please try again."

    # Save AI response
    ai_msg = ChatMessage(
        chat_id=chat_id,
        user_id=current_user.id,
        role="assistant",
        content=ai_response_text
    )
    db.add(ai_msg)
    chat.updated_at = func.now()
    db.commit()
    db.refresh(ai_msg)

    # Update chat title if it's the first message
    if db.query(ChatMessage).filter(ChatMessage.chat_id == chat_id).count() == 2:
        chat.title = user_message[:50] + ("..." if len(user_message) > 50 else "")
        db.commit()

    return {
        "user_message": {
            "id": user_msg.id,
            "role": "user",
            "content": user_msg.content,
            "created_at": user_msg.created_at.isoformat(),
        },
        "ai_response": {
            "id": ai_msg.id,
            "role": "assistant",
            "content": ai_msg.content,
            "created_at": ai_msg.created_at.isoformat(),
        }
    }


@app.delete("/api/chat/{chat_id}")
def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a chat conversation"""
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found."
        )

    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully."}


@app.delete("/api/chat/{chat_id}/clear")
def clear_chat_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Clear all messages in a chat"""
    chat = db.query(Chat).filter(
        Chat.id == chat_id,
        Chat.user_id == current_user.id
    ).first()

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found."
        )

    messages = db.query(ChatMessage).filter(
        ChatMessage.chat_id == chat_id
    ).all()

    for message in messages:
        db.delete(message)

    chat.updated_at = func.now()
    db.commit()
    return {"message": "Chat cleared successfully."}
