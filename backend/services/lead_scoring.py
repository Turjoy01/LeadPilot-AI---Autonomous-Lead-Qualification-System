from typing import Dict, Any
from backend.models.lead import LeadFields, LeadGrade, ScoreHistory
from datetime import datetime


class LeadScoringEngine:
    """Lead scoring engine based on signals"""
    
    def __init__(self, hot_threshold: int = 70, warm_threshold: int = 40):
        self.hot_threshold = hot_threshold
        self.warm_threshold = warm_threshold
    
    def calculate_score(self, fields: LeadFields, conversation_signals: Dict[str, Any] = None) -> tuple[int, LeadGrade]:
        """
        Calculate lead score (0-100) and grade based on extracted fields and conversation signals
        
        Scoring factors:
        - Contact info completeness (30 points)
        - Budget indication (25 points)
        - Timeline urgency (25 points)
        - Service clarity (10 points)
        - Engagement signals (10 points)
        """
        score = 0
        
        # Contact info completeness (30 points)
        if fields.name:
            score += 10
        if fields.email:
            score += 10
        if fields.phone:
            score += 10
        
        # Budget indication (25 points)
        if fields.budget:
            budget_lower = fields.budget.lower()
            if any(word in budget_lower for word in ["high", "premium", "enterprise", "unlimited"]):
                score += 25
            elif any(word in budget_lower for word in ["medium", "standard", "moderate"]):
                score += 15
            elif any(word in budget_lower for word in ["low", "small", "budget"]):
                score += 5
            else:
                # Has budget info but not categorized
                score += 10
        
        # Timeline urgency (25 points)
        if fields.timeline:
            timeline_lower = fields.timeline.lower()
            if any(word in timeline_lower for word in ["asap", "urgent", "immediately", "now", "today", "this week"]):
                score += 25
            elif any(word in timeline_lower for word in ["soon", "next week", "this month", "2 weeks"]):
                score += 20
            elif any(word in timeline_lower for word in ["next month", "1 month", "30 days"]):
                score += 15
            elif any(word in timeline_lower for word in ["quarter", "3 months", "few months"]):
                score += 10
            else:
                score += 5
        
        # Service clarity (10 points)
        if fields.service_interest:
            score += 10
        
        # Engagement signals from conversation (10 points)
        if conversation_signals:
            message_count = conversation_signals.get("message_count", 0)
            if message_count >= 5:
                score += 10
            elif message_count >= 3:
                score += 5
            
            # Bonus for specific intent keywords
            intent_keywords = conversation_signals.get("intent_keywords", [])
            if any(word in intent_keywords for word in ["pricing", "quote", "cost", "buy", "purchase", "demo"]):
                score += 5  # Bonus points
        
        # Cap at 100
        score = min(score, 100)
        
        # Determine grade
        if score >= self.hot_threshold:
            grade = LeadGrade.HOT
        elif score >= self.warm_threshold:
            grade = LeadGrade.WARM
        elif score > 0:
            grade = LeadGrade.COLD
        else:
            grade = LeadGrade.UNQUALIFIED
        
        return score, grade
    
    def create_score_history_entry(self, score: int, grade: LeadGrade, reason: str = None) -> ScoreHistory:
        """Create a score history entry"""
        return ScoreHistory(
            score=score,
            grade=grade,
            timestamp=datetime.utcnow(),
            reason=reason
        )
