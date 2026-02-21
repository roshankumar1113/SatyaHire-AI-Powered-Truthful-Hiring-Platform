"""
Multilingual AI Interviewer Service
Handles structured technical interviews in multiple Indian languages
"""
from typing import Dict, Optional, List
from pydantic import BaseModel
import json
from app.ml.ai_client import AIClient


# Supported Languages
SUPPORTED_LANGUAGES = [
    "english", "hindi", "tamil", "telugu",
    "kannada", "malayalam", "marathi",
    "gujarati", "bengali", "punjabi", "urdu"
]

# Language Display Names
LANGUAGE_NAMES = {
    "english": "English",
    "hindi": "हिंदी",
    "tamil": "தமிழ்",
    "telugu": "తెలుగు",
    "kannada": "ಕನ್ನಡ",
    "malayalam": "മലയാളം",
    "marathi": "मराठी",
    "gujarati": "ગુજરાતી",
    "bengali": "বাংলা",
    "punjabi": "ਪੰਜਾਬੀ",
    "urdu": "اردو"
}


class InterviewRequest(BaseModel):
    role: str
    experience_level: str  # junior, mid, senior
    language: str
    max_questions: int = 5
    question_number: int = 1
    previous_question: str = ""
    candidate_answer: str = ""


class EvaluationResponse(BaseModel):
    score: float
    strengths: str
    improvements: str
    corrected_answer: str


class InterviewResponse(BaseModel):
    question: str
    evaluation: Optional[EvaluationResponse] = None
    difficulty: str  # easy, medium, hard
    interview_status: str  # IN_PROGRESS, COMPLETED


class MultilingualInterviewer:
    """
    Multilingual AI Interviewer
    Conducts structured technical interviews in multiple languages
    """
    
    def __init__(self):
        self.ai_client = AIClient()
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for AI interviewer"""
        return """You are SatyaHire AI, a professional multilingual AI interviewer.

Your job:
- Conduct structured technical interviews.
- Speak ONLY in the selected interview language.
- Maintain professional and respectful tone.
- Do NOT mix languages unless technical terms require English.
- Keep answers clear and concise.
- Always return output in valid JSON format only.
- Never add explanations outside JSON.

If you fail to generate valid JSON, regenerate response until JSON is valid."""
    
    def _get_user_prompt(self, request: InterviewRequest) -> str:
        """Generate dynamic user prompt based on interview state"""
        
        prompt = f"""Interview Details:
- Role: {request.role}
- Experience Level: {request.experience_level}
- Interview Language: {request.language}
- Total Questions: {request.max_questions}
- Current Question Number: {request.question_number}

Previous Question: {request.previous_question if request.previous_question else "None"}

Candidate Answer: {request.candidate_answer if request.candidate_answer else "None"}

Your Tasks:

1. If candidate_answer is empty:
   → Generate a new interview question in {request.language}.
   → Adjust difficulty according to {request.experience_level}.
   → Return only the question.

2. If candidate_answer is provided:
   → Evaluate the answer in {request.language}.
   → Give a score from 0-10.
   → Mention strengths.
   → Mention improvements.
   → Provide corrected model answer.
   → Then generate next question.

IMPORTANT:
- Everything must be written in {request.language}.
- Keep evaluation structured.
- Be realistic like a real human interviewer.
- Do NOT repeat previous questions.
- Do NOT switch language.

Return strictly in this JSON format:

{{
  "question": "string",
  "evaluation": {{
    "score": number,
    "strengths": "string",
    "improvements": "string",
    "corrected_answer": "string"
  }},
  "difficulty": "easy | medium | hard",
  "interview_status": "IN_PROGRESS | COMPLETED"
}}

Note: If this is question {request.question_number} of {request.max_questions}, and candidate_answer is provided, set interview_status to "COMPLETED". Otherwise "IN_PROGRESS"."""
        
        return prompt
    
    def validate_language(self, language: str) -> bool:
        """Validate if language is supported"""
        return language.lower() in SUPPORTED_LANGUAGES
    
    def conduct_interview(self, request: InterviewRequest) -> InterviewResponse:
        """
        Conduct interview and return structured response
        
        Args:
            request: Interview request with role, language, and answer details
            
        Returns:
            InterviewResponse with question and optional evaluation
        """
        # Validate language
        if not self.validate_language(request.language):
            raise ValueError(f"Unsupported language: {request.language}. Supported: {', '.join(SUPPORTED_LANGUAGES)}")
        
        # Generate prompts
        system_prompt = self.system_prompt
        user_prompt = self._get_user_prompt(request)
        
        # Call AI
        try:
            response_text = self.ai_client.generate_text(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Parse JSON response
            response_data = self._parse_ai_response(response_text)
            
            # Create response object
            interview_response = InterviewResponse(
                question=response_data.get("question", ""),
                difficulty=response_data.get("difficulty", "medium"),
                interview_status=response_data.get("interview_status", "IN_PROGRESS")
            )
            
            # Add evaluation if present
            if "evaluation" in response_data and response_data["evaluation"]:
                eval_data = response_data["evaluation"]
                interview_response.evaluation = EvaluationResponse(
                    score=float(eval_data.get("score", 0)),
                    strengths=eval_data.get("strengths", ""),
                    improvements=eval_data.get("improvements", ""),
                    corrected_answer=eval_data.get("corrected_answer", "")
                )
            
            return interview_response
            
        except Exception as e:
            raise Exception(f"Failed to conduct interview: {str(e)}")
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """
        Parse AI response and extract JSON
        
        Args:
            response_text: Raw AI response
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            # Try to parse as JSON directly
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
                return json.loads(json_text)
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
                return json.loads(json_text)
            else:
                # Try to find JSON object in text
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                if start != -1 and end > start:
                    json_text = response_text[start:end]
                    return json.loads(json_text)
                else:
                    raise ValueError("No valid JSON found in response")
    
    def get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages with display names"""
        return [
            {
                "code": lang,
                "name": LANGUAGE_NAMES.get(lang, lang.capitalize()),
                "native_name": LANGUAGE_NAMES.get(lang, lang.capitalize())
            }
            for lang in SUPPORTED_LANGUAGES
        ]
    
    def generate_first_question(
        self,
        role: str,
        experience_level: str,
        language: str,
        max_questions: int = 5
    ) -> InterviewResponse:
        """
        Generate first interview question
        
        Args:
            role: Job role (e.g., "Python Developer")
            experience_level: junior, mid, senior
            language: Interview language
            max_questions: Total number of questions
            
        Returns:
            InterviewResponse with first question
        """
        request = InterviewRequest(
            role=role,
            experience_level=experience_level,
            language=language,
            max_questions=max_questions,
            question_number=1,
            previous_question="",
            candidate_answer=""
        )
        
        return self.conduct_interview(request)
    
    def evaluate_and_next_question(
        self,
        role: str,
        experience_level: str,
        language: str,
        max_questions: int,
        question_number: int,
        previous_question: str,
        candidate_answer: str
    ) -> InterviewResponse:
        """
        Evaluate answer and generate next question
        
        Args:
            role: Job role
            experience_level: junior, mid, senior
            language: Interview language
            max_questions: Total questions
            question_number: Current question number
            previous_question: Previous question text
            candidate_answer: Candidate's answer
            
        Returns:
            InterviewResponse with evaluation and next question
        """
        request = InterviewRequest(
            role=role,
            experience_level=experience_level,
            language=language,
            max_questions=max_questions,
            question_number=question_number,
            previous_question=previous_question,
            candidate_answer=candidate_answer
        )
        
        return self.conduct_interview(request)


# Singleton instance
multilingual_interviewer = MultilingualInterviewer()
