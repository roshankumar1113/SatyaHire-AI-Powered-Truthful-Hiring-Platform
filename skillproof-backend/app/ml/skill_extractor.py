"""
Advanced Skill Extraction Module
Extracts skills from resumes with high accuracy using NLP
"""

import re
from typing import List, Dict, Set
import spacy
from collections import Counter

class SkillExtractor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            self.nlp = None
        
        # Comprehensive skill taxonomy
        self.skill_database = self._load_skill_database()
        
    def _load_skill_database(self) -> Dict[str, List[str]]:
        """Load comprehensive skill taxonomy"""
        return {
            "programming_languages": [
                "python", "java", "javascript", "typescript", "c++", "c#", "ruby",
                "php", "swift", "kotlin", "go", "rust", "scala", "r", "matlab",
                "perl", "shell", "bash", "powershell", "sql", "html", "css"
            ],
            "frameworks": [
                "react", "angular", "vue", "svelte", "next.js", "nuxt", "gatsby",
                "django", "flask", "fastapi", "express", "nest.js", "spring boot",
                "laravel", "rails", "asp.net", "tensorflow", "pytorch", "keras",
                "scikit-learn", "pandas", "numpy", "opencv"
            ],
            "databases": [
                "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
                "cassandra", "dynamodb", "oracle", "sql server", "sqlite",
                "mariadb", "neo4j", "couchdb", "firebase"
            ],
            "cloud_platforms": [
                "aws", "azure", "gcp", "google cloud", "heroku", "digitalocean",
                "linode", "cloudflare", "vercel", "netlify"
            ],
            "devops": [
                "docker", "kubernetes", "jenkins", "gitlab ci", "github actions",
                "terraform", "ansible", "chef", "puppet", "circleci", "travis ci",
                "nginx", "apache", "linux", "unix"
            ],
            "ai_ml": [
                "machine learning", "deep learning", "nlp", "computer vision",
                "neural networks", "cnn", "rnn", "lstm", "transformer", "bert",
                "gpt", "reinforcement learning", "data science", "statistics"
            ],
            "tools": [
                "git", "github", "gitlab", "bitbucket", "jira", "confluence",
                "slack", "trello", "asana", "figma", "sketch", "adobe xd",
                "postman", "swagger", "vs code", "intellij", "pycharm"
            ],
            "methodologies": [
                "agile", "scrum", "kanban", "waterfall", "devops", "ci/cd",
                "tdd", "bdd", "microservices", "rest api", "graphql", "soap"
            ],
            "soft_skills": [
                "leadership", "communication", "teamwork", "problem solving",
                "critical thinking", "time management", "project management",
                "mentoring", "presentation", "negotiation"
            ]
        }
    
    def extract_skills(self, text: str) -> Dict[str, any]:
        """
        Extract skills from text with categorization and confidence scores
        
        Returns:
            Dict with skills, categories, confidence scores
        """
        text_lower = text.lower()
        
        # Extract skills by category
        categorized_skills = {}
        all_skills = []
        
        for category, skills in self.skill_database.items():
            found_skills = []
            for skill in skills:
                # Use word boundaries for accurate matching
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill.title())
                    all_skills.append({
                        "name": skill.title(),
                        "category": category.replace("_", " ").title(),
                        "confidence": self._calculate_confidence(skill, text_lower)
                    })
            
            if found_skills:
                categorized_skills[category] = found_skills
        
        # Extract using NLP if available
        if self.nlp:
            nlp_skills = self._extract_with_nlp(text)
            all_skills.extend(nlp_skills)
        
        # Remove duplicates and sort by confidence
        unique_skills = self._deduplicate_skills(all_skills)
        
        return {
            "skills": unique_skills,
            "categorized_skills": categorized_skills,
            "total_count": len(unique_skills),
            "top_skills": unique_skills[:10],
            "skill_summary": self._generate_summary(categorized_skills)
        }
    
    def _calculate_confidence(self, skill: str, text: str) -> float:
        """Calculate confidence score based on frequency and context"""
        # Count occurrences
        count = len(re.findall(r'\b' + re.escape(skill) + r'\b', text))
        
        # Base confidence on frequency
        if count >= 3:
            confidence = 0.95
        elif count == 2:
            confidence = 0.85
        else:
            confidence = 0.75
        
        # Boost confidence if in skills section
        if re.search(r'skills?.*' + re.escape(skill), text, re.IGNORECASE):
            confidence = min(confidence + 0.1, 1.0)
        
        return round(confidence, 2)
    
    def _extract_with_nlp(self, text: str) -> List[Dict]:
        """Extract skills using spaCy NER"""
        doc = self.nlp(text)
        nlp_skills = []
        
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                # Check if it's a known technology
                if self._is_technology(ent.text):
                    nlp_skills.append({
                        "name": ent.text,
                        "category": "Technology",
                        "confidence": 0.70
                    })
        
        return nlp_skills
    
    def _is_technology(self, text: str) -> bool:
        """Check if text is a technology/tool"""
        tech_indicators = ['js', 'py', 'api', 'db', 'sql', 'ml', 'ai']
        text_lower = text.lower()
        
        # Check against all skills
        for skills in self.skill_database.values():
            if text_lower in skills:
                return True
        
        # Check for tech indicators
        return any(indicator in text_lower for indicator in tech_indicators)
    
    def _deduplicate_skills(self, skills: List[Dict]) -> List[Dict]:
        """Remove duplicate skills and keep highest confidence"""
        skill_map = {}
        
        for skill in skills:
            name = skill['name'].lower()
            if name not in skill_map or skill['confidence'] > skill_map[name]['confidence']:
                skill_map[name] = skill
        
        # Sort by confidence
        return sorted(skill_map.values(), key=lambda x: x['confidence'], reverse=True)
    
    def _generate_summary(self, categorized_skills: Dict) -> str:
        """Generate human-readable summary"""
        if not categorized_skills:
            return "No skills detected"
        
        summaries = []
        for category, skills in categorized_skills.items():
            category_name = category.replace("_", " ").title()
            summaries.append(f"{category_name}: {len(skills)} skills")
        
        return " | ".join(summaries)
    
    def match_skills(self, candidate_skills: List[str], required_skills: List[str]) -> Dict:
        """
        Match candidate skills against required skills
        
        Returns:
            Match score, matched skills, missing skills
        """
        candidate_set = set(s.lower() for s in candidate_skills)
        required_set = set(s.lower() for s in required_skills)
        
        matched = candidate_set.intersection(required_set)
        missing = required_set - candidate_set
        extra = candidate_set - required_set
        
        # Calculate match score
        if not required_set:
            match_score = 0
        else:
            match_score = (len(matched) / len(required_set)) * 100
        
        return {
            "match_score": round(match_score, 2),
            "matched_skills": list(matched),
            "missing_skills": list(missing),
            "additional_skills": list(extra),
            "matched_count": len(matched),
            "required_count": len(required_set),
            "recommendation": self._get_recommendation(match_score)
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Get hiring recommendation based on match score"""
        if score >= 80:
            return "Excellent match - Highly recommended"
        elif score >= 60:
            return "Good match - Recommended"
        elif score >= 40:
            return "Moderate match - Consider with training"
        else:
            return "Low match - Not recommended"
    
    def extract_experience_level(self, text: str) -> Dict:
        """Extract years of experience and seniority level"""
        # Patterns for experience
        patterns = [
            r'(\d+)\+?\s*years?\s*of\s*experience',
            r'experience\s*:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*experience',
            r'(\d+)\+?\s*years?\s*in'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(m) for m in matches])
        
        avg_years = max(years) if years else 0
        
        # Determine seniority level
        if avg_years >= 8:
            level = "Senior"
        elif avg_years >= 5:
            level = "Mid-Level"
        elif avg_years >= 2:
            level = "Junior"
        elif avg_years >= 1:
            level = "Entry-Level"
        else:
            level = "Fresher"
        
        return {
            "years_of_experience": avg_years,
            "seniority_level": level,
            "experience_range": f"{avg_years}-{avg_years+2} years"
        }
    
    def analyze_skill_proficiency(self, text: str, skill: str) -> Dict:
        """Analyze proficiency level for a specific skill"""
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        # Proficiency indicators
        expert_keywords = ['expert', 'advanced', 'proficient', 'mastery', 'specialist']
        intermediate_keywords = ['intermediate', 'working knowledge', 'familiar', 'experience with']
        beginner_keywords = ['basic', 'beginner', 'learning', 'exposure to']
        
        # Find skill context
        skill_pattern = r'.{0,50}' + re.escape(skill_lower) + r'.{0,50}'
        contexts = re.findall(skill_pattern, text_lower)
        
        if not contexts:
            return {"proficiency": "Unknown", "confidence": 0.0}
        
        context = ' '.join(contexts)
        
        # Determine proficiency
        if any(keyword in context for keyword in expert_keywords):
            return {"proficiency": "Expert", "confidence": 0.90}
        elif any(keyword in context for keyword in intermediate_keywords):
            return {"proficiency": "Intermediate", "confidence": 0.80}
        elif any(keyword in context for keyword in beginner_keywords):
            return {"proficiency": "Beginner", "confidence": 0.70}
        else:
            # Default based on frequency
            count = len(re.findall(r'\b' + re.escape(skill_lower) + r'\b', text_lower))
            if count >= 3:
                return {"proficiency": "Intermediate", "confidence": 0.75}
            else:
                return {"proficiency": "Beginner", "confidence": 0.65}
