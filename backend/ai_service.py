"""
AI Service Abstraction for Chatbot
Supports multiple providers: Local/Demo, OpenAI, etc.
"""

from abc import ABC, abstractmethod
from typing import Optional
import random
import re


class AIProvider(ABC):
    """Abstract base class for AI providers"""

    @abstractmethod
    async def generate_response(
        self, user_message: str, conversation_context: dict
    ) -> dict:
        """Generate an AI response"""
        pass


class LocalAIProvider(AIProvider):
    """Local/Demo AI Provider - No external API required"""

    def __init__(self):
        self.context_cache = {}

    async def generate_response(
        self, user_message: str, conversation_context: dict
    ) -> dict:
        """Generate response using local logic and knowledge base"""
        from knowledge_base import kb

        # Detect intent and topic
        intent, topic = self._detect_intent_and_topic(user_message)

        # Build relevant context
        context_used = self._build_context(topic, conversation_context)

        # Search knowledge base for relevant documents
        relevant_docs = kb.search_by_keywords(
            [topic] + self._extract_keywords(user_message)
        )

        # Generate response based on intent and topic
        if intent == "career_guidance":
            response = self._handle_career_guidance(
                user_message, conversation_context, relevant_docs, context_used
            )
        elif intent == "learning_guidance":
            response = self._handle_learning_guidance(
                user_message, conversation_context, relevant_docs, context_used
            )
        elif intent == "skill_assessment":
            response = self._handle_skill_assessment(
                user_message, conversation_context, relevant_docs, context_used
            )
        elif intent == "concept_explanation":
            response = self._handle_concept_explanation(
                user_message, relevant_docs, context_used
            )
        elif intent == "project_ideas":
            response = self._handle_project_ideas(
                user_message, conversation_context, context_used
            )
        else:
            response = self._handle_general_question(
                user_message, relevant_docs, context_used
            )

        return {"response": response, "context_used": context_used}

    def _detect_intent_and_topic(self, message: str) -> tuple[str, str]:
        """Detect user intent and topic from message"""
        message_lower = message.lower()

        # Career guidance intents
        if any(
            word in message_lower
            for word in ["career", "role", "job", "internship", "position"]
        ):
            return "career_guidance", self._extract_topic(message_lower)

        # Learning guidance intents
        if any(
            word in message_lower
            for word in [
                "learn",
                "study",
                "understand",
                "explain",
                "how to",
                "tutorial",
            ]
        ):
            return "learning_guidance", self._extract_topic(message_lower)

        # Skill assessment
        if any(
            word in message_lower for word in ["skill", "assessment", "ready", "capable"]
        ):
            return "skill_assessment", self._extract_topic(message_lower)

        # Concept explanation
        if any(
            word in message_lower
            for word in [
                "what is",
                "explain",
                "define",
                "concept",
                "meaning",
                "difference",
            ]
        ):
            return "concept_explanation", self._extract_topic(message_lower)

        # Project ideas
        if any(word in message_lower for word in ["project", "build", "create"]):
            return "project_ideas", self._extract_topic(message_lower)

        return "general", self._extract_topic(message_lower)

    def _extract_topic(self, message: str) -> str:
        """Extract main topic from message"""
        topics_mapping = {
            "rest api": "REST API",
            "database": "database",
            "python": "Python",
            "backend": "backend",
            "security": "cybersecurity",
            "linux": "Linux",
            "docker": "Docker",
            "cloud": "cloud",
            "machine learning": "machine learning",
            "interview": "interview",
            "internship": "internship",
        }

        for keyword, topic in topics_mapping.items():
            if keyword in message.lower():
                return topic

        return "general"

    def _extract_keywords(self, message: str) -> list[str]:
        """Extract keywords from message"""
        keywords = []
        keyword_mapping = {
            "api": ["REST", "HTTP", "endpoint"],
            "database": ["SQL", "MongoDB", "NoSQL"],
            "python": ["Python", "FastAPI", "Django"],
            "security": ["encryption", "authentication", "password"],
            "linux": ["terminal", "bash", "command"],
            "docker": ["container", "deployment"],
            "cloud": ["AWS", "Azure", "GCP"],
            "interview": ["coding", "system design"],
            "internship": ["preparation", "application"],
        }

        for word, related_keywords in keyword_mapping.items():
            if word in message.lower():
                keywords.extend(related_keywords)

        return list(set(keywords))[:5]

    def _build_context(self, topic: str, conversation_context: dict) -> dict:
        """Build context for response generation"""
        return {
            "topic": topic,
            "career_goal": conversation_context.get("career_goal"),
            "current_skills": conversation_context.get("skills", []),
            "missing_skills": conversation_context.get("missing_skills", []),
            "assessment_results": conversation_context.get("assessment_results", {}),
        }

    def _handle_career_guidance(
        self, user_message: str, context: dict, docs: list, context_used: dict
    ) -> str:
        """Handle career guidance questions"""
        career_goal = context.get("career_goal")
        skills = context.get("skills", [])

        responses = []

        if "suitable" in user_message.lower() or "match" in user_message.lower():
            if career_goal:
                responses.append(
                    f"Based on your career goal of {career_goal} and your current skills in {', '.join(skills[:3])}, "
                    f"this appears to be a suitable path for you. "
                )
            else:
                responses.append(
                    "To recommend a suitable career, I'd need more information about your interests and skills. "
                    "Please complete your profile first. "
                )

        if "skills" in user_message.lower() and "need" in user_message.lower():
            if docs:
                first_doc = docs[0]
                relevant_skills = self._extract_skills_from_doc(first_doc.content)
                responses.append(
                    f"For a career in {context_used.get('topic')}, you should focus on: {', '.join(relevant_skills[:5])}. "
                )
            else:
                responses.append(
                    f"To excel in {context_used.get('topic')}, focus on building strong fundamentals and practical projects. "
                )

        if "ready" in user_message.lower():
            missing = context.get("missing_skills", [])
            if missing:
                responses.append(
                    f"You're making progress! You're still missing key skills like {missing[0]}. "
                    "I recommend focusing on these before applying. "
                )
            else:
                responses.append(
                    "Great! Your skills look solid. "
                    "I recommend now building 2-3 strong projects and practicing interview questions. "
                )

        if not responses:
            responses.append(
                f"Based on what I know about {context_used.get('topic')}, "
                "this is an excellent career path with growing demand and good opportunities. "
                "Would you like guidance on specific skills to develop or how to prepare? "
            )

        return " ".join(responses)

    def _handle_learning_guidance(
        self, user_message: str, context: dict, docs: list, context_used: dict
    ) -> str:
        """Handle learning guidance questions"""
        topic = context_used.get("topic")
        responses = []

        if "next" in user_message.lower():
            current_skills = context.get("skills", [])
            missing_skills = context.get("missing_skills", [])

            if missing_skills:
                responses.append(
                    f"Based on your current skills, you should focus on learning {missing_skills[0]}. "
                )
            else:
                responses.append(
                    f"You've built a solid foundation in {current_skills[0] if current_skills else 'the basics'}. "
                    "Consider exploring advanced topics or building more complex projects. "
                )

        if "explain" in user_message.lower() or "simple" in user_message.lower():
            if docs:
                content = docs[0].content.split("\n")[1:6]
                responses.append(f"Here's a simple explanation: {' '.join(content)}")
            else:
                responses.append(
                    f"I'd be happy to explain {topic}! "
                    "This is an important concept that forms the foundation of modern development. "
                    "Would you like me to focus on a specific aspect? "
                )

        if "practice" in user_message.lower():
            responses.append(
                "Great way to learn! I recommend: 1) Solve 10 problems on LeetCode/HackerRank, "
                "2) Build a small project, 3) Teach it to someone else. "
                "Which would you prefer to start with? "
            )

        if not responses:
            responses.append(
                f"Learning {topic} is a great choice! "
                "Start with understanding the fundamentals, then move to practical applications. "
                "Practice is key to mastering any skill. "
            )

        return " ".join(responses)

    def _handle_skill_assessment(
        self, user_message: str, context: dict, docs: list, context_used: dict
    ) -> str:
        """Handle skill assessment questions"""
        assessment_results = context.get("assessment_results", {})
        topic = context_used.get("topic")

        responses = []

        if "ready" in user_message.lower():
            if topic in assessment_results:
                level = assessment_results[topic].get("level", "Unknown")
                responses.append(
                    f"Your current level in {topic} is {level}. "
                    "To be ready for professional work, aim for an Advanced or Expert level. "
                )
            else:
                responses.append(
                    f"I don't have assessment results for {topic} yet. "
                    "Take the skill assessment to get a detailed evaluation. "
                )

        if "improve" in user_message.lower() or "better" in user_message.lower():
            responses.append(
                f"To improve your {topic} skills, I recommend: "
                f"1) Review the fundamentals, "
                f"2) Solve practice problems, "
                f"3) Build real projects, "
                f"4) Learn from experienced developers. "
            )

        if not responses:
            responses.append(
                f"Your skill assessment in {topic} helps identify your strengths and areas for improvement. "
                "Would you like to take an assessment or get personalized learning recommendations? "
            )

        return " ".join(responses)

    def _handle_concept_explanation(
        self, user_message: str, docs: list, context_used: dict
    ) -> str:
        """Handle concept explanation requests"""
        responses = []

        if docs:
            doc = docs[0]
            responses.append(
                f"**{doc.title}**\n\n" f"{doc.content[:500]}...\n\n" f"Would you like me to dive deeper into any specific aspect?"
            )
        else:
            responses.append(
                f"I'd love to explain more about {context_used.get('topic')}! "
                f"This is a fundamental concept in modern development. "
                f"Could you specify which aspect interests you most? "
            )

        return " ".join(responses)

    def _handle_project_ideas(
        self, user_message: str, context: dict, context_used: dict
    ) -> str:
        """Handle project idea requests"""
        skill_level = self._get_skill_level(context)
        responses = []

        project_ideas = {
            "beginner": [
                "Todo List App with FastAPI backend",
                "Simple REST API for a Blog",
                "Weather Dashboard (frontend/backend)",
                "Simple Chat Application",
                "Task Management System",
            ],
            "intermediate": [
                "E-commerce Platform Backend",
                "Real-time Notification System",
                "Content Management System",
                "Social Media Clone",
                "Analytics Dashboard",
            ],
            "advanced": [
                "Microservices Architecture",
                "Machine Learning-powered Recommendation Engine",
                "Real-time Collaborative Editor",
                "Distributed Task Queue System",
                "AI-powered Chatbot Platform",
            ],
        }

        ideas = project_ideas.get(skill_level, project_ideas["beginner"])

        responses.append(f"Great project ideas for your level:\n")
        for i, idea in enumerate(ideas[:3], 1):
            responses.append(f"{i}. {idea}")

        responses.append(
            "\n\nPick one that excites you and build it step-by-step. "
            "This will significantly boost your portfolio! "
        )

        return " ".join(responses)

    def _handle_general_question(
        self, user_message: str, docs: list, context_used: dict
    ) -> str:
        """Handle general questions"""
        responses = []

        if docs:
            doc = docs[0]
            responses.append(
                f"Regarding your question about {doc.title}:\n\n" f"{doc.content[:300]}...\n\n" f"Feel free to ask for more details!"
            )
        else:
            responses.append(
                "That's an interesting question! "
                "While I specialize in career guidance, skill development, and learning paths, "
                "I'm here to help you succeed. "
                "Could you rephrase your question or ask about a specific skill or career topic? "
            )

        return " ".join(responses)

    def _extract_skills_from_doc(self, content: str) -> list[str]:
        """Extract skills mentioned in a document"""
        skills = []
        keywords = [
            "Python",
            "Java",
            "JavaScript",
            "REST",
            "API",
            "Database",
            "Docker",
            "AWS",
            "Linux",
        ]

        for keyword in keywords:
            if keyword.lower() in content.lower():
                skills.append(keyword)

        return skills

    def _get_skill_level(self, context: dict) -> str:
        """Determine user's overall skill level"""
        skills_count = len(context.get("skills", []))
        assessment_results = context.get("assessment_results", {})

        if skills_count >= 5 and len(assessment_results) >= 3:
            return "advanced"
        elif skills_count >= 3:
            return "intermediate"
        else:
            return "beginner"


class AIService:
    """Main AI Service class"""

    def __init__(self, provider: AIProvider = None):
        self.provider = provider or LocalAIProvider()

    async def chat(self, user_message: str, conversation_context: dict) -> dict:
        """Generate a chat response"""
        response = await self.provider.generate_response(user_message, conversation_context)
        return response

    def set_provider(self, provider: AIProvider):
        """Set a different AI provider"""
        self.provider = provider


# Global AI service instance
ai_service = AIService(LocalAIProvider())