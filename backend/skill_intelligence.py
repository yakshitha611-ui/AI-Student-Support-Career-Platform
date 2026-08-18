from __future__ import annotations

from typing import Any

CAREER_SKILL_REQUIREMENTS = {
    "backend developer": [
        "Python",
        "SQL",
        "Git",
        "FastAPI",
        "REST API",
        "Docker",
        "JavaScript",
    ],
    "full stack developer": [
        "JavaScript",
        "React",
        "Node.js",
        "SQL",
        "Git",
        "REST API",
        "HTML/CSS",
    ],
    "data analyst": [
        "SQL",
        "Python",
        "Excel",
        "Statistics",
        "Power BI",
        "Data Visualization",
    ],
    "cyber security": [
        "Networking",
        "Linux",
        "Python",
        "Ethical Hacking",
        "Web Security",
        "Cryptography",
    ],
    "software engineer": [
        "Python",
        "JavaScript",
        "Data Structures",
        "Git",
        "SQL",
        "Algorithms",
    ],
    "frontend developer": [
        "HTML/CSS",
        "JavaScript",
        "React",
        "Git",
        "UI/UX",
        "Responsive Design",
    ],
    "cloud engineer": [
        "Linux",
        "Python",
        "Git",
        "Docker",
        "Cloud",
        "Networking",
    ],
}

INTERNSHIP_HINTS = {
    "Python": ["Python", "FastAPI", "REST API", "SQL"],
    "SQL": ["SQL", "Python", "Data Analysis"],
    "JavaScript": ["JavaScript", "React", "HTML/CSS"],
    "React": ["React", "JavaScript", "HTML/CSS"],
    "Git": ["Git", "GitHub", "Version Control"],
    "Docker": ["Docker", "Cloud", "Linux"],
    "Networking": ["Networking", "Linux", "Cyber Security"],
    "Cyber Security": ["Cyber Security", "Networking", "Linux", "Web Security"],
}

QUESTION_BANK: dict[str, list[dict[str, Any]]] = {
    "Python": [
        {
            "id": "py-1",
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "define", "fun"],
            "correct_answer": "def",
            "difficulty": "Beginner",
            "skill": "Python",
        },
        {
            "id": "py-2",
            "question": "What is the output of len([1, 2, 3])?",
            "options": ["1", "2", "3", "4"],
            "correct_answer": "3",
            "difficulty": "Beginner",
            "skill": "Python",
        },
        {
            "id": "py-3",
            "question": "Which collection keeps key-value pairs in Python?",
            "options": ["Tuple", "List", "Dictionary", "Set"],
            "correct_answer": "Dictionary",
            "difficulty": "Intermediate",
            "skill": "Python",
        },
        {
            "id": "py-4",
            "question": "Which statement correctly creates a list comprehension?",
            "options": ["[x for x in range(5)]", "{x for x in range(5)}", "(x for x in range(5))", "list(range(5))"],
            "correct_answer": "[x for x in range(5)]",
            "difficulty": "Intermediate",
            "skill": "Python",
        },
    ],
    "SQL": [
        {
            "id": "sql-1",
            "question": "Which SQL command is used to fetch rows from a table?",
            "options": ["INSERT", "SELECT", "UPDATE", "DELETE"],
            "correct_answer": "SELECT",
            "difficulty": "Beginner",
            "skill": "SQL",
        },
        {
            "id": "sql-2",
            "question": "Which clause filters rows in SQL?",
            "options": ["ORDER BY", "GROUP BY", "WHERE", "HAVING"],
            "correct_answer": "WHERE",
            "difficulty": "Beginner",
            "skill": "SQL",
        },
        {
            "id": "sql-3",
            "question": "Which SQL command changes existing data?",
            "options": ["UPDATE", "INSERT", "ALTER", "DROP"],
            "correct_answer": "UPDATE",
            "difficulty": "Intermediate",
            "skill": "SQL",
        },
    ],
    "Java": [
        {
            "id": "java-1",
            "question": "Which keyword is used to define a class in Java?",
            "options": ["class", "function", "struct", "type"],
            "correct_answer": "class",
            "difficulty": "Beginner",
            "skill": "Java",
        },
        {
            "id": "java-2",
            "question": "Which keyword is used to create an object instance in Java?",
            "options": ["new", "create", "instance", "init"],
            "correct_answer": "new",
            "difficulty": "Beginner",
            "skill": "Java",
        },
        {
            "id": "java-3",
            "question": "Which Java access modifier allows access only within the same class?",
            "options": ["public", "private", "protected", "default"],
            "correct_answer": "private",
            "difficulty": "Intermediate",
            "skill": "Java",
        },
    ],
    "JavaScript": [
        {
            "id": "js-1",
            "question": "Which keyword is used to declare a variable in modern JavaScript?",
            "options": ["var", "let", "const", "Both let and const"],
            "correct_answer": "Both let and const",
            "difficulty": "Beginner",
            "skill": "JavaScript",
        },
        {
            "id": "js-2",
            "question": "Which method adds an item to the end of an array?",
            "options": ["push()", "pop()", "slice()", "map()"],
            "correct_answer": "push()",
            "difficulty": "Beginner",
            "skill": "JavaScript",
        },
        {
            "id": "js-3",
            "question": "Which symbol is used for strict equality in JavaScript?",
            "options": ["==", "=", "===", "!=="],
            "correct_answer": "===",
            "difficulty": "Intermediate",
            "skill": "JavaScript",
        },
    ],
    "HTML/CSS": [
        {
            "id": "html-1",
            "question": "Which tag is used to create a hyperlink in HTML?",
            "options": ["<link>", "<a>", "<href>", "<url>"],
            "correct_answer": "<a>",
            "difficulty": "Beginner",
            "skill": "HTML/CSS",
        },
        {
            "id": "html-2",
            "question": "Which CSS property controls text size?",
            "options": ["font-size", "text-size", "size", "font"],
            "correct_answer": "font-size",
            "difficulty": "Beginner",
            "skill": "HTML/CSS",
        },
        {
            "id": "html-3",
            "question": "Which CSS property changes the background color?",
            "options": ["color", "background-color", "bg-color", "text-color"],
            "correct_answer": "background-color",
            "difficulty": "Intermediate",
            "skill": "HTML/CSS",
        },
    ],
    "Data Structures": [
        {
            "id": "ds-1",
            "question": "Which data structure follows FIFO order?",
            "options": ["Stack", "Queue", "Tree", "Graph"],
            "correct_answer": "Queue",
            "difficulty": "Intermediate",
            "skill": "Data Structures",
        },
        {
            "id": "ds-2",
            "question": "Which data structure uses LIFO order?",
            "options": ["Queue", "Stack", "HashMap", "LinkedList"],
            "correct_answer": "Stack",
            "difficulty": "Intermediate",
            "skill": "Data Structures",
        },
        {
            "id": "ds-3",
            "question": "Which operation is used to add an item to the top of a stack?",
            "options": ["push", "pop", "enqueue", "dequeue"],
            "correct_answer": "push",
            "difficulty": "Intermediate",
            "skill": "Data Structures",
        },
    ],
    "Cyber Security": [
        {
            "id": "cyber-1",
            "question": "Which of these is a common method used to protect data in transit?",
            "options": ["Encryption", "Compression", "Caching", "Logging"],
            "correct_answer": "Encryption",
            "difficulty": "Intermediate",
            "skill": "Cyber Security",
        },
        {
            "id": "cyber-2",
            "question": "What does CIA stand for in cybersecurity?",
            "options": ["Confidentiality, Integrity, Availability", "Control, Integrity, Access", "Central, Input, Audit", "Confidentiality, Input, Analysis"],
            "correct_answer": "Confidentiality, Integrity, Availability",
            "difficulty": "Intermediate",
            "skill": "Cyber Security",
        },
        {
            "id": "cyber-3",
            "question": "Which practice helps prevent unauthorized access to systems?",
            "options": ["Authentication", "Caching", "Formatting", "Rendering"],
            "correct_answer": "Authentication",
            "difficulty": "Beginner",
            "skill": "Cyber Security",
        },
    ],
    "Networking": [
        {
            "id": "net-1",
            "question": "Which protocol is used to map domain names to IP addresses?",
            "options": ["DNS", "HTTP", "FTP", "SMTP"],
            "correct_answer": "DNS",
            "difficulty": "Beginner",
            "skill": "Networking",
        },
        {
            "id": "net-2",
            "question": "Which device connects multiple computers in a local network?",
            "options": ["Router", "Switch", "Monitor", "Keyboard"],
            "correct_answer": "Switch",
            "difficulty": "Beginner",
            "skill": "Networking",
        },
        {
            "id": "net-3",
            "question": "Which layer of the OSI model is responsible for routing?",
            "options": ["Application", "Transport", "Network", "Data Link"],
            "correct_answer": "Network",
            "difficulty": "Intermediate",
            "skill": "Networking",
        },
    ],
    "Git": [
        {
            "id": "git-1",
            "question": "Which command is used to create a local copy of a repository?",
            "options": ["git clone", "git commit", "git push", "git status"],
            "correct_answer": "git clone",
            "difficulty": "Beginner",
            "skill": "Git",
        },
        {
            "id": "git-2",
            "question": "Which command saves your current changes to the local repository?",
            "options": ["git add", "git commit", "git pull", "git branch"],
            "correct_answer": "git commit",
            "difficulty": "Beginner",
            "skill": "Git",
        },
        {
            "id": "git-3",
            "question": "Which command shows the status of modified files?",
            "options": ["git log", "git status", "git fetch", "git merge"],
            "correct_answer": "git status",
            "difficulty": "Intermediate",
            "skill": "Git",
        },
    ],
    "React": [
        {
            "id": "react-1",
            "question": "What is React primarily used for?",
            "options": ["Database management", "UI development", "Server setup", "Testing only"],
            "correct_answer": "UI development",
            "difficulty": "Beginner",
            "skill": "React",
        },
        {
            "id": "react-2",
            "question": "Which file typically contains the root component in a React app?",
            "options": ["index.js", "script.js", "main.css", "package.json"],
            "correct_answer": "index.js",
            "difficulty": "Intermediate",
            "skill": "React",
        },
        {
            "id": "react-3",
            "question": "What hook manages state in a function component?",
            "options": ["useState", "useEffect", "useMemo", "useContext"],
            "correct_answer": "useState",
            "difficulty": "Intermediate",
            "skill": "React",
        },
    ],
}


def normalize_skill_name(value: str | None) -> str:
    if value is None:
        return ""
    cleaned = str(value).strip()
    if not cleaned:
        return ""
    return " ".join(cleaned.split())


def friendly_skill_key(skill_name: str) -> str:
    normalized = normalize_skill_name(skill_name).lower()
    aliases = {
        "rest api": "REST API",
        "rest-api": "REST API",
        "fastapi": "FastAPI",
        "html/css": "HTML/CSS",
        "html css": "HTML/CSS",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "data structures and algorithms": "Data Structures",
        "data structures": "Data Structures",
        "cybersecurity": "Cyber Security",
        "cyber security": "Cyber Security",
        "git/github": "Git",
        "github": "Git",
    }
    return aliases.get(normalized, normalized.title())


def infer_career_requirements(career_name: str | None, preferred_role: str | None) -> list[str]:
    combined = " ".join(filter(None, [career_name, preferred_role])).strip().lower()
    if not combined:
        return []
    for key, skills in CAREER_SKILL_REQUIREMENTS.items():
        if key in combined or combined in key:
            return skills
    for key, skills in CAREER_SKILL_REQUIREMENTS.items():
        if any(term in combined for term in key.split()):
            return skills
    return []


def build_skill_gap(current_skills: list[str], career_name: str | None, preferred_role: str | None) -> dict[str, Any]:
    required_skills = infer_career_requirements(career_name, preferred_role)
    user_skill_set = {friendly_skill_key(skill) for skill in current_skills if normalize_skill_name(skill)}

    if not required_skills:
        return {
            "has_career_goal": bool(career_name or preferred_role),
            "overall_match": 0,
            "strong_skills": [],
            "developing_skills": sorted(user_skill_set),
            "missing_skills": [],
            "required_skills": [],
            "career_name": career_name or preferred_role or "Career Goal",
            "message": "Set your career goal to generate a personalized skill-gap analysis.",
        }

    strong = []
    missing = []
    for skill in required_skills:
        clean_skill = friendly_skill_key(skill)
        if clean_skill in user_skill_set:
            strong.append(clean_skill)
        else:
            missing.append(clean_skill)

    developing = sorted({friendly_skill_key(skill) for skill in current_skills if friendly_skill_key(skill) not in strong and friendly_skill_key(skill) not in missing})

    required_count = max(len(required_skills), 1)
    overall_match = round((len(strong) / required_count) * 100)

    return {
        "has_career_goal": True,
        "overall_match": overall_match,
        "strong_skills": strong,
        "developing_skills": developing,
        "missing_skills": missing,
        "required_skills": required_skills,
        "career_name": career_name or preferred_role or "Career Goal",
        "message": "Skill analysis generated from your saved profile and career goal.",
    }


def build_recommendations(current_skills: list[str], career_name: str | None, preferred_role: str | None) -> list[dict[str, str]]:
    gap_result = build_skill_gap(current_skills, career_name, preferred_role)
    missing = gap_result["missing_skills"]
    if not missing:
        return [
            {
                "skill": "Keep refining your current strengths",
                "priority": "Low",
                "why": "You already match the main requirements for your current career target.",
            }
        ]

    recommendations: list[dict[str, str]] = []
    for skill in missing:
        priority = "High" if skill in gap_result["required_skills"] else "Medium"
        why = f"This is important for {gap_result['career_name']} and helps close a current skill gap in your profile."
        if skill in INTERNSHIP_HINTS:
            why = f"This is often required by relevant internships and helps strengthen your {gap_result['career_name']} profile."
        recommendations.append({
            "skill": skill,
            "priority": priority,
            "why": why,
        })

    return recommendations[:5]


def get_questions_for_skill(skill_name: str) -> list[dict[str, Any]]:
    normalized = friendly_skill_key(skill_name)
    questions = QUESTION_BANK.get(normalized, [])
    if questions:
        return questions
    fallback = [
        {
            "id": f"generic-{normalized.lower().replace(' ', '-')}-1",
            "question": f"Which answer best reflects a strong understanding of {normalized}?",
            "options": ["Practice regularly", "Ignore it", "Avoid learning", "Delete the skill"],
            "correct_answer": "Practice regularly",
            "difficulty": "Beginner",
            "skill": normalized,
        }
    ]
    return fallback


def calculate_assessment_level(percentage: int) -> str:
    if percentage >= 80:
        return "Strong"
    if percentage >= 60:
        return "Good / Developing"
    if percentage >= 40:
        return "Needs Improvement"
    return "Beginner"


def evaluate_assessment(skill_name: str, answers: list[dict[str, Any]]) -> dict[str, Any]:
    questions = get_questions_for_skill(skill_name)
    by_id = {question["id"]: question for question in questions}
    score = 0
    total = len(questions)

    for answer in answers:
        question_id = answer.get("question_id")
        selected_value = answer.get("selected_option")
        question = by_id.get(question_id)
        if not question:
            continue
        if selected_value == question["correct_answer"]:
            score += 1

    percentage = round((score / total) * 100) if total else 0
    return {
        "skill_name": friendly_skill_key(skill_name),
        "score": score,
        "total_questions": total,
        "percentage": percentage,
        "level": calculate_assessment_level(percentage),
    }
