from __future__ import annotations

from typing import Any

CAREER_BASE_TOPICS = {
    "backend developer": ["Python", "SQL", "FastAPI", "REST API", "Docker", "Backend Project"],
    "full stack developer": ["JavaScript", "React", "SQL", "REST API", "Git", "Full Stack Project"],
    "data analyst": ["SQL", "Python", "Statistics", "Power BI", "Data Visualization", "Dashboard Project"],
    "cyber security": ["Networking", "Linux", "Python", "Web Security", "Cryptography", "Security Lab"],
    "software engineer": ["Python", "JavaScript", "Data Structures", "Git", "Algorithms", "Coding Practice"],
    "frontend developer": ["HTML/CSS", "JavaScript", "React", "UI/UX", "Responsive Design", "Portfolio Project"],
    "cloud engineer": ["Linux", "Python", "Docker", "Cloud", "Networking", "Deployment Project"],
}

COURSE_CATALOG = {
    "FastAPI": {
        "course_name": "FastAPI Fundamentals",
        "difficulty": "Beginner",
        "estimated_time": "3-4 hours",
        "why": "FastAPI is a key backend skill for many modern internship and job roles.",
    },
    "REST API": {
        "course_name": "REST API Development",
        "difficulty": "Intermediate",
        "estimated_time": "4-5 hours",
        "why": "REST APIs are central to backend development and data-driven application work.",
    },
    "Docker": {
        "course_name": "Docker Fundamentals",
        "difficulty": "Beginner",
        "estimated_time": "2-3 hours",
        "why": "Docker helps you package and deploy projects consistently in real-world workflows.",
    },
    "SQL": {
        "course_name": "SQL Queries & Data Modeling",
        "difficulty": "Beginner",
        "estimated_time": "3 hours",
        "why": "Strong SQL skills support backend work, analytics, and project development.",
    },
    "Python": {
        "course_name": "Python Fundamentals",
        "difficulty": "Beginner",
        "estimated_time": "4 hours",
        "why": "Python is the foundation for automation, backend work, and scripting tasks.",
    },
    "JavaScript": {
        "course_name": "Modern JavaScript Essentials",
        "difficulty": "Beginner",
        "estimated_time": "4 hours",
        "why": "JavaScript is core for frontend work and many modern full-stack roles.",
    },
    "React": {
        "course_name": "React Essentials",
        "difficulty": "Intermediate",
        "estimated_time": "5 hours",
        "why": "React is a common requirement for frontend and full-stack development paths.",
    },
    "HTML/CSS": {
        "course_name": "HTML & CSS Fundamentals",
        "difficulty": "Beginner",
        "estimated_time": "3 hours",
        "why": "Strong UI fundamentals improve frontend confidence and project quality.",
    },
    "Networking": {
        "course_name": "Networking Fundamentals",
        "difficulty": "Beginner",
        "estimated_time": "3 hours",
        "why": "Networking is essential for infrastructure, cybersecurity, and cloud roles.",
    },
    "Linux": {
        "course_name": "Linux Essentials",
        "difficulty": "Beginner",
        "estimated_time": "3 hours",
        "why": "Linux is commonly used in backend, security, cloud, and server environments.",
    },
    "Ethical Hacking": {
        "course_name": "Ethical Hacking Fundamentals",
        "difficulty": "Intermediate",
        "estimated_time": "4 hours",
        "why": "This complements cybersecurity and vulnerability analysis skills.",
    },
    "Web Security": {
        "course_name": "Web Security Basics",
        "difficulty": "Intermediate",
        "estimated_time": "4 hours",
        "why": "Security fundamentals are critical for protecting apps and APIs.",
    },
    "Cryptography": {
        "course_name": "Cryptography Essentials",
        "difficulty": "Intermediate",
        "estimated_time": "4 hours",
        "why": "Cryptography is important in secure application and cyber defense work.",
    },
    "Git": {
        "course_name": "Git & GitHub Essentials",
        "difficulty": "Beginner",
        "estimated_time": "2 hours",
        "why": "Version control is expected in almost every software project workflow.",
    },
    "Data Structures": {
        "course_name": "Data Structures Practice",
        "difficulty": "Intermediate",
        "estimated_time": "4 hours",
        "why": "Strong algorithmic thinking improves interview readiness and engineering quality.",
    },
    "Algorithms": {
        "course_name": "Algorithms Fundamentals",
        "difficulty": "Intermediate",
        "estimated_time": "5 hours",
        "why": "This helps with technical problem solving and software engineering tasks.",
    },
    "Cloud": {
        "course_name": "Cloud Foundations",
        "difficulty": "Intermediate",
        "estimated_time": "4 hours",
        "why": "Cloud concepts are increasingly important for scalable application projects.",
    },
    "Power BI": {
        "course_name": "Power BI Essentials",
        "difficulty": "Beginner",
        "estimated_time": "3 hours",
        "why": "Business intelligence tooling supports data analysis and reporting tasks.",
    },
    "Data Visualization": {
        "course_name": "Data Visualization Basics",
        "difficulty": "Beginner",
        "estimated_time": "3 hours",
        "why": "Clear data storytelling helps communicate analysis outcomes effectively.",
    },
}


def normalize_skill_name(value: str | None) -> str:
    if value is None:
        return ""
    cleaned = str(value).strip()
    return " ".join(cleaned.split())


def pretty_skill(value: str) -> str:
    cleaned = normalize_skill_name(value)
    return cleaned or "Skill"


def get_career_topics(career_name: str | None, preferred_role: str | None) -> list[str]:
    combined = " ".join(filter(None, [career_name, preferred_role])).strip().lower()
    for key, topics in CAREER_BASE_TOPICS.items():
        if key in combined or combined in key:
            return topics
    for key, topics in CAREER_BASE_TOPICS.items():
        if any(word in combined for word in key.split()):
            return topics
    return ["Python", "Git", "Project Practice"]


def get_missing_skills(current_skills: list[str], career_name: str | None, preferred_role: str | None) -> list[str]:
    desired = get_career_topics(career_name, preferred_role)
    present = {normalize_skill_name(skill).lower() for skill in current_skills if normalize_skill_name(skill)}
    missing = []
    for skill in desired:
        if normalize_skill_name(skill).lower() not in present:
            missing.append(skill)
    return missing


def build_course_recommendations(
    current_skills: list[str],
    career_name: str | None,
    preferred_role: str | None,
    missing_skills: list[str] | None = None,
) -> list[dict[str, str]]:
    missing = missing_skills or get_missing_skills(current_skills, career_name, preferred_role)
    if not missing:
        return [
            {
                "course_name": "Project-Based Review",
                "skill": "Portfolio Practice",
                "difficulty": "Intermediate",
                "priority": "Low",
                "why": "You already match most of the core requirements for your current target role.",
                "estimated_time": "2-3 hours",
            }
        ]

    recommendations: list[dict[str, str]] = []
    for idx, skill in enumerate(missing[:5]):
        ref = COURSE_CATALOG.get(skill, {
            "course_name": f"{skill} Fundamentals",
            "difficulty": "Beginner",
            "estimated_time": "3 hours",
            "why": f"This topic is highly relevant to your {career_name or 'target career'} path.",
        })
        priority = "High" if idx < 2 else "Medium"
        recommendations.append({
            "course_name": ref["course_name"],
            "skill": skill,
            "difficulty": ref["difficulty"],
            "priority": priority,
            "why": ref["why"],
            "estimated_time": ref["estimated_time"],
        })
    return recommendations


def build_learning_roadmap(
    current_skills: list[str],
    assessment_results: list[dict[str, Any]] | None,
    career_name: str | None,
    preferred_role: str | None,
) -> list[dict[str, str]]:
    topics = get_career_topics(career_name, preferred_role)
    assessment_lookup = {normalize_skill_name(item.get("skill_name")) for item in (assessment_results or []) if item.get("skill_name")}

    roadmap = []
    for index, topic in enumerate(topics[:6], start=1):
        skill_key = normalize_skill_name(topic).lower()
        if any(normalize_skill_name(skill).lower() == skill_key for skill in current_skills):
            status = "Completed"
        elif skill_key in {normalize_skill_name(skill).lower() for skill in assessment_lookup}:
            status = "In Progress"
        else:
            status = "Not Started"

        roadmap.append({
            "step": f"Step {index}",
            "skill": topic,
            "description": f"Focus on {topic} for your {career_name or 'career'} growth path.",
            "difficulty": "Beginner" if index < 3 else "Intermediate",
            "estimated_time": "1-2 hours" if index < 3 else "2-4 hours",
            "status": status,
        })
    return roadmap


def build_learning_plan(
    daily_study_time: str,
    learning_preference: str,
    missing_skills: list[str],
    current_skills: list[str],
    career_name: str | None,
) -> dict[str, Any]:
    topics = missing_skills[:5] if missing_skills else get_career_topics(career_name, None)[:5]
    time_minutes = {
        "30 minutes": 30,
        "1 hour": 60,
        "2 hours": 120,
        "3+ hours": 180,
    }.get(daily_study_time, 60)

    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    weekly_plan = []
    for i, day in enumerate(days):
        topic = topics[i % len(topics)] if topics else "Review"
        practice_mode = "theory" if learning_preference == "Theory" else "practice"
        project_mode = "project work" if learning_preference == "Projects" else "guided practice"
        if learning_preference == "Mixed":
            session_line = f"{min(45, max(20, time_minutes // 2))} minutes theory | {max(15, time_minutes - min(45, max(20, time_minutes // 2)))} minutes practice"
        elif learning_preference == "Practice":
            session_line = f"{time_minutes} minutes practice"
        elif learning_preference == "Projects":
            session_line = f"{time_minutes} minutes {project_mode}"
        else:
            session_line = f"{time_minutes} minutes theory"

        weekly_plan.append({
            "day": day,
            "focus": topic,
            "details": session_line,
        })
    return {
        "daily_study_time": daily_study_time,
        "learning_preference": learning_preference,
        "weekly_plan": weekly_plan,
    }


def build_learning_progress(
    current_skills: list[str],
    missing_skills: list[str],
    course_recommendations: list[dict[str, str]],
    assessment_results: list[dict[str, Any]] | None,
    career_name: str | None,
) -> dict[str, Any]:
    topics = get_career_topics(career_name, None)
    completed_count = sum(1 for topic in topics if normalize_skill_name(topic).lower() in {normalize_skill_name(skill).lower() for skill in current_skills})
    total_skills = max(len(topics), 1)
    overall = round((completed_count / total_skills) * 100)
    courses_completed = min(len(assessment_results or []), max(0, len(course_recommendations) - 1))
    total_courses = max(len(course_recommendations), 1)

    return {
        "overall_learning_progress": overall,
        "skills_completed": f"{completed_count} / {total_skills}",
        "courses_completed": f"{courses_completed} / {total_courses}",
        "roadmap_progress": f"{completed_count} / {total_skills}",
        "missing_skills": missing_skills,
    }


def build_adaptive_recommendations(
    current_skills: list[str],
    missing_skills: list[str],
    assessment_results: list[dict[str, Any]] | None,
    career_name: str | None,
) -> list[dict[str, str]]:
    average_score = 0
    if assessment_results:
        average_score = round(sum(item.get("percentage", 0) for item in assessment_results) / len(assessment_results))

    high_priority = missing_skills[:3]
    if average_score < 60:
        foundation = ["Python", "Git", "SQL"]
        high_priority = [*foundation, *missing_skills[:2]]

    recommendations = []
    for index, skill in enumerate(high_priority[:5]):
        priority = "High" if index < 2 else "Medium"
        if average_score >= 80 and index >= 2:
            priority = "Low"
        recommendations.append({
            "skill": skill,
            "priority": priority,
            "why": f"This is a targeted next step for your {career_name or 'career'} progress and closes a current knowledge gap.",
        })
    return recommendations
