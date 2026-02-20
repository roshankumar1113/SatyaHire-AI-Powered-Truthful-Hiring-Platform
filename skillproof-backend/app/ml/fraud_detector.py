import numpy as np
from typing import Dict, List
from sklearn.ensemble import IsolationForest, RandomForestClassifier
import joblib

class FraudDetector:
    def __init__(self):
        # Initialize models (in production, load pre-trained models)
        self.anomaly_detector = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        
    def extract_features(self, submission_data: Dict) -> np.ndarray:
        """Extract features from submission data"""
        features = []
        
        # Time-based features
        avg_time_per_question = submission_data.get('avg_time_per_question', 0)
        total_time = submission_data.get('total_time_seconds', 0)
        features.extend([avg_time_per_question, total_time])
        
        # Behavioral features
        tab_switches = submission_data.get('tab_switches', 0)
        copy_paste_events = submission_data.get('copy_paste_events', 0)
        features.extend([tab_switches, copy_paste_events])
        
        # Answer pattern features
        answer_change_count = submission_data.get('answer_changes', 0)
        questions_answered = submission_data.get('questions_answered', 0)
        features.extend([answer_change_count, questions_answered])
        
        # Time variance (how consistent is timing)
        time_variance = np.var(submission_data.get('question_times', [0]))
        features.append(time_variance)
        
        # Rapid answer rate (answers < 10 seconds)
        rapid_answers = sum(1 for t in submission_data.get('question_times', []) if t < 10)
        features.append(rapid_answers)
        
        return np.array(features).reshape(1, -1)
    
    def detect_anomalies(self, features: np.ndarray) -> float:
        """Detect anomalies using Isolation Forest"""
        # Returns -1 for anomalies, 1 for normal
        prediction = self.anomaly_detector.predict(features)
        
        # Get anomaly score (lower = more anomalous)
        score = self.anomaly_detector.score_samples(features)[0]
        
        # Convert to 0-100 scale (higher = more suspicious)
        fraud_score = max(0, min(100, (1 - score) * 50))
        
        return fraud_score
    
    def analyze_time_patterns(self, question_times: List[float]) -> Dict:
        """Analyze timing patterns for anomalies"""
        if not question_times:
            return {"suspicious": False, "reason": "No data"}
        
        times = np.array(question_times)
        mean_time = np.mean(times)
        std_time = np.std(times)
        
        # Check for suspiciously fast answers
        very_fast = sum(1 for t in times if t < 5)
        fast_ratio = very_fast / len(times)
        
        # Check for suspiciously consistent timing
        if std_time < 2 and len(times) > 5:
            return {
                "suspicious": True,
                "reason": "Timing too consistent (possible bot)",
                "severity": "high"
            }
        
        # Check for too many fast answers
        if fast_ratio > 0.5:
            return {
                "suspicious": True,
                "reason": "Too many rapid answers",
                "severity": "medium"
            }
        
        return {"suspicious": False}
    
    def analyze_behavioral_patterns(self, submission_data: Dict) -> Dict:
        """Analyze behavioral patterns"""
        flags = []
        
        # Tab switching analysis
        tab_switches = submission_data.get('tab_switches', 0)
        if tab_switches > 10:
            flags.append({
                "type": "excessive_tab_switching",
                "count": tab_switches,
                "severity": "high"
            })
        
        # Copy-paste analysis
        copy_paste = submission_data.get('copy_paste_events', 0)
        if copy_paste > 5:
            flags.append({
                "type": "excessive_copy_paste",
                "count": copy_paste,
                "severity": "medium"
            })
        
        # Answer pattern analysis
        answer_changes = submission_data.get('answer_changes', 0)
        if answer_changes > 20:
            flags.append({
                "type": "excessive_answer_changes",
                "count": answer_changes,
                "severity": "low"
            })
        
        return {
            "flags": flags,
            "total_flags": len(flags)
        }
    
    def calculate_fraud_score(self, submission_data: Dict) -> Dict:
        """Calculate overall fraud score"""
        # Extract features
        features = self.extract_features(submission_data)
        
        # Get anomaly score
        anomaly_score = self.detect_anomalies(features)
        
        # Analyze patterns
        time_analysis = self.analyze_time_patterns(
            submission_data.get('question_times', [])
        )
        behavioral_analysis = self.analyze_behavioral_patterns(submission_data)
        
        # Calculate weighted fraud score
        base_score = anomaly_score
        
        # Add penalties
        if time_analysis.get('suspicious'):
            base_score += 20
        
        base_score += behavioral_analysis['total_flags'] * 10
        
        # Cap at 100
        final_score = min(100, base_score)
        
        # Determine risk level
        if final_score < 30:
            risk_level = "low"
        elif final_score < 60:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return {
            "fraud_score": round(final_score, 2),
            "risk_level": risk_level,
            "time_analysis": time_analysis,
            "behavioral_flags": behavioral_analysis['flags'],
            "explanation": self._generate_explanation(
                final_score, time_analysis, behavioral_analysis
            )
        }
    
    def _generate_explanation(
        self, score: float, time_analysis: Dict, behavioral_analysis: Dict
    ) -> str:
        """Generate human-readable explanation"""
        if score < 30:
            return "No significant fraud indicators detected. Normal test behavior."
        
        reasons = []
        if time_analysis.get('suspicious'):
            reasons.append(time_analysis['reason'])
        
        for flag in behavioral_analysis['flags']:
            reasons.append(f"{flag['type'].replace('_', ' ').title()}: {flag['count']}")
        
        return "Fraud indicators: " + "; ".join(reasons)
