"""
Chatbot Logic and Student Context Builder
Coordinates between AI service, knowledge base, and student data
"""

from sqlalchemy.orm import Session
from models import User, StudentProfile, StudentSkill, StudentProject, StudentCareerGoal, SkillAssessmentResult
from ai_service import ai_service


class StudentContextBuilder:
    """Builds personalized student context from database"""

    @staticmethod
    def build_context(user: User, db: Session) -> dict:
        """Build comprehensive student context for chatbot"""
        context = {
            "user_id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        }

        # Get student profile
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
        if profile:
            context["profile"] = {
                "university": profile.university,
                "branch": profile.branch,
                "year_of_study": profile.year_of_study,
                "cgpa": profile.cgpa_percentage,
            }

        # Get skills
        skills = db.query(StudentSkill).filter(StudentSkill.user_id == user.id).all()
        context["skills"] = [skill.skill_name for skill in skills]
        context["skills_with_proficiency"] = [
            {"name": skill.skill_name, "proficiency": skill.proficiency} for skill in skills
        ]

        # Get projects
        projects = db.query(StudentProject).filter(StudentProject.user_id == user.id).all()
        context["projects"] = [
            {
                "name": project.project_name,
                "description": project.description,
                "technologies": project.technologies_used,
            }
            for project in projects
        ]

        # Get career goals
        career_goal = db.query(StudentCareerGoal).filter(StudentCareerGoal.user_id == user.id).first()
        if career_goal:
            context["career_goal"] = career_goal.target_career
            context["preferred_role"] = career_goal.preferred_role
            context["career_interests"] = career_goal.career_interests
            context["short_term_goal"] = career_goal.short_term_goal
            context["long_term_goal"] = career_goal.long_term_goal

        # Get assessment results
        assessments = db.query(SkillAssessmentResult).filter(SkillAssessmentResult.user_id == user.id).all()
        context["assessment_results"] = {
            assessment.skill_name: {
                "score": assessment.score,
                "percentage": assessment.percentage,
                "level": assessment.level,
            }
            for assessment in assessments
        }

        # Calculate missing skills based on career goal and assessments
        context["missing_skills"] = StudentContextBuilder._calculate_missing_skills(
            context
        )

        # Build student summary
        context["summary"] = StudentContextBuilder._build_summary(context)

        return context

    @staticmethod
    def _calculate_missing_skills(context: dict) -> list[str]:
        """Calculate missing skills based on career goal"""
        career_skill_requirements = {
            "backend developer": ["FastAPI", "REST APIs", "Docker", "PostgreSQL"],
            "frontend developer": ["React", "TypeScript", "CSS", "Web APIs"],
            "full stack developer": ["Python", "JavaScript", "Databases", "Docker"],
            "data scientist": ["Python", "Machine Learning", "Statistics", "SQL"],
            "cyber security": ["Linux", "Networking", "Cryptography", "Security Tools"],
            "devops engineer": ["Docker", "Kubernetes", "AWS", "CI/CD"],
        }

        career_goal = (context.get("career_goal") or "").lower()
        required_skills = []

        for goal, skills in career_skill_requirements.items():
            if goal in career_goal:
                required_skills = skills
                break

        current_skills = [s.lower() for s in context.get("skills", [])]
        missing = [
            skill for skill in required_skills
            if not any(curr_skill in skill.lower() or skill.lower() in curr_skill for curr_skill in current_skills)
        ]

        return missing

    @staticmethod
    def _build_summary(context: dict) -> str:
        """Build a readable summary of student context"""
        summary_parts = []

        if context.get("full_name"):
            summary_parts.append(f"Student: {context['full_name']}")

        if context.get("career_goal"):
            summary_parts.append(f"Career Goal: {context['career_goal']}")

        if context.get("skills"):
            summary_parts.append(f"Skills: {', '.join(context['skills'])}")

        if context.get("missing_skills"):
            summary_parts.append(
                f"Missing Skills: {', '.join(context['missing_skills'][:3])}"
            )

        if context.get("assessment_results"):
            avg_level = StudentContextBuilder._calculate_average_level(
                context["assessment_results"]
            )
            summary_parts.append(f"Overall Level: {avg_level}")

        return " | ".join(summary_parts)

    @staticmethod
    def _calculate_average_level(assessment_results: dict) -> str:
        """Calculate average skill level"""
        if not assessment_results:
            return "Not Assessed"

        level_mapping = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Expert": 4}
        levels = []

        for result in assessment_results.values():
            level = result.get("level", "Beginner")
            levels.append(level_mapping.get(level, 1))

        if not levels:
            return "Not Assessed"

        avg = sum(levels) / len(levels)

        if avg < 1.5:
            return "Beginner"
        elif avg < 2.5:
            return "Intermediate"
        elif avg < 3.5:
            return "Advanced"
        else:
            return "Expert"


class ChatbotLogic:
    """Main chatbot logic coordinator"""

    @staticmethod
    async def process_message(
        user_message: str, user: User, db: Session
    ) -> dict:
        """Process a user message and generate response"""

        # Build student context
        student_context = StudentContextBuilder.build_context(user, db)

        # Call AI service with student context
        ai_response = await ai_service.chat(user_message, student_context)

        return {
            "response": ai_response["response"],
            "context_used": ai_response.get("context_used"),
        }

    @staticmethod
    def get_student_context_summary(user: User, db: Session) -> str:
        """Get a summary of student context for display"""
        context = StudentContextBuilder.build_context(user, db)
        return context.get("summary", "No profile information found. Please complete your profile.")
