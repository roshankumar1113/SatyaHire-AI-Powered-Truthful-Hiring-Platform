"""
AI Service - Production Version
Handles AI-powered interview question generation and answer evaluation
"""
from openai import OpenAI
import json
import os
from typing import Dict, Optional
from app.ml.ai_client import AIClient


# Language code mapping for Whisper API
LANGUAGE_CODE_MAP = {
    "english": "en",
    "hindi": "hi",
    "tamil": "ta",
    "telugu": "te",
    "kannada": "kn",
    "malayalam": "ml",
    "marathi": "mr",
    "gujarati": "gu",
    "bengali": "bn",
    "punjabi": "pa",
    "urdu": "ur"
}


class AIService:
    """
    AI Service for multilingual interview management
    """
    
    def __init__(self):
        self.ai_client = AIClient()
        # Initialize OpenAI client if API key is available
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEYS", "").split(",")[0]
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
        else:
            self.openai_client = None
    
    def generate_or_evaluate(
        self,
        role: str,
        experience_level: str,
        language: str,
        previous_question: str = "",
        candidate_answer: str = "",
        question_number: int = 1,
        max_questions: int = 10
    ) -> Dict:
        """
        Generate interview question or evaluate answer
        
        Args:
            role: Job role
            experience_level: junior, mid, senior
            language: Interview language
            previous_question: Previous question text
            candidate_answer: Candidate's answer
            question_number: Current question number
            max_questions: Total questions
            
        Returns:
            Dictionary with question and optional evaluation
        """
        
        system_prompt = f"""You are SatyaHire AI, a professional multilingual interviewer.

Rules:
- Speak only in {language}.
- Keep professional tone.
- Return ONLY valid JSON.
- Never explain outside JSON.
- If you fail to generate valid JSON, regenerate response until JSON is valid."""

        user_prompt = f"""Interview Details:
Role: {role}
Experience Level: {experience_level}
Language: {language}
Current Question Number: {question_number}
Total Questions: {max_questions}

Previous Question: {previous_question if previous_question else "None"}

Candidate Answer: {candidate_answer if candidate_answer else "None"}

Instructions:

1. If candidate_answer is empty:
   - Generate a new interview question in {language}.
   - Adjust difficulty according to {experience_level}.

2. If candidate_answer exists:
   - Evaluate answer in {language}.
   - Give score 0-10.
   - Give strengths.
   - Give improvements.
   - Provide corrected answer.
   - Generate next question.

IMPORTANT:
- Everything must be in {language}.
- Be realistic like a real human interviewer.
- Do NOT repeat previous questions.

Return JSON format:

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

Note: If this is question {question_number} of {max_questions} and candidate_answer is provided, set interview_status to "COMPLETED". Otherwise "IN_PROGRESS"."""

        try:
            # Try OpenAI first if available
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    temperature=0.7,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                content = response.choices[0].message.content
            else:
                # Fallback to AIClient (supports multiple providers)
                content = self.ai_client.generate_text(
                    prompt=user_prompt,
                    system_prompt=system_prompt,
                    temperature=0.7,
                    max_tokens=1000
                )
            
            # Parse JSON response
            return self._parse_response(content)
            
        except Exception as e:
            raise Exception(f"AI service error: {str(e)}")
    
    def _parse_response(self, content: str) -> Dict:
        """
        Parse AI response and extract JSON
        
        Args:
            content: Raw AI response
            
        Returns:
            Parsed JSON dictionary
        """
        try:
            # Try to parse as JSON directly
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                json_text = content[json_start:json_end].strip()
                return json.loads(json_text)
            elif "```" in content:
                json_start = content.find("```") + 3
                json_end = content.find("```", json_start)
                json_text = content[json_start:json_end].strip()
                return json.loads(json_text)
            else:
                # Try to find JSON object in text
                start = content.find("{")
                end = content.rfind("}") + 1
                if start != -1 and end > start:
                    json_text = content[start:end]
                    return json.loads(json_text)
                else:
                    raise ValueError("No valid JSON found in AI response")
    
    def transcribe_audio(
        self,
        audio_file,
        language: str = "english"
    ) -> Dict:
        """
        Transcribe audio to text using Whisper API
        
        Args:
            audio_file: Audio file object
            language: Interview language
            
        Returns:
            Dictionary with transcript and metadata
        """
        if not self.openai_client:
            raise Exception("OpenAI API key not configured")
        
        # Get language code for Whisper
        language_code = LANGUAGE_CODE_MAP.get(language.lower(), "en")
        
        try:
            response = self.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language_code,
                response_format="verbose_json"
            )
            
            return {
                "transcript": response.text,
                "language": response.language,
                "duration": response.duration,
                "confidence": 0.95  # Whisper doesn't provide confidence, use default
            }
            
        except Exception as e:
            raise Exception(f"Audio transcription error: {str(e)}")
    
    def text_to_speech(
        self,
        text: str,
        language: str = "english",
        voice: str = "alloy"
    ) -> bytes:
        """
        Convert text to speech using OpenAI TTS
        
        Args:
            text: Text to convert
            language: Language of text
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            
        Returns:
            Audio bytes
        """
        if not self.openai_client:
            raise Exception("OpenAI API key not configured")
        
        try:
            response = self.openai_client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            
            return response.content
            
        except Exception as e:
            raise Exception(f"Text-to-speech error: {str(e)}")
    
    @staticmethod
    def get_language_code(language: str) -> str:
        """
        Get language code for Whisper API
        
        Args:
            language: Language name
            
        Returns:
            Language code
        """
        return LANGUAGE_CODE_MAP.get(language.lower(), "en")


# Singleton instance
ai_service = AIService()
