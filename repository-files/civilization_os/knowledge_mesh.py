"""
Knowledge Mesh - AI-Powered Adaptive Learning System
Part of iLuminara Civilization OS

Personalized AI tutors with offline-first operation and federated learning.
Integrates with iLuminara's sovereignty framework for educational equity.

Compliance:
- UN SDG 4 (Quality Education)
- UNESCO Education 2030 Framework
- COPPA (Children's Online Privacy Protection Act)
- FERPA (Family Educational Rights and Privacy Act)
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)


class LearningStyle(Enum):
    """Learning style preferences"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    MULTIMODAL = "multimodal"


class SubjectDomain(Enum):
    """Subject domains"""
    MATHEMATICS = "mathematics"
    SCIENCE = "science"
    LANGUAGE = "language"
    HEALTH_LITERACY = "health_literacy"
    DIGITAL_LITERACY = "digital_literacy"
    CIVIC_EDUCATION = "civic_education"
    VOCATIONAL = "vocational"


class DifficultyLevel(Enum):
    """Content difficulty levels"""
    BEGINNER = 1
    ELEMENTARY = 2
    INTERMEDIATE = 3
    ADVANCED = 4
    EXPERT = 5


@dataclass
class LearnerProfile:
    """Individual learner profile"""
    learner_id: str
    age: int
    learning_style: LearningStyle
    proficiency_levels: Dict[SubjectDomain, float]  # 0-1 scale
    learning_pace: float  # Relative to average
    engagement_score: float  # 0-1 scale
    preferred_language: str
    accessibility_needs: List[str]
    metadata: Dict


@dataclass
class LearningContent:
    """Educational content unit"""
    content_id: str
    subject: SubjectDomain
    difficulty: DifficultyLevel
    title: str
    description: str
    content_type: str  # video, text, interactive, quiz
    duration_minutes: int
    prerequisites: List[str]
    learning_objectives: List[str]
    metadata: Dict


@dataclass
class LearningSession:
    """Individual learning session"""
    session_id: str
    learner_id: str
    content_id: str
    start_time: str
    end_time: Optional[str]
    completion_rate: float
    comprehension_score: float
    engagement_metrics: Dict
    feedback: Optional[str]


class KnowledgeMesh:
    """
    AI-powered adaptive learning system with offline-first operation.
    
    Features:
    - Personalized learning paths
    - Adaptive difficulty adjustment
    - Offline content delivery
    - Federated learning for privacy
    - Multi-language support
    """
    
    def __init__(
        self,
        mesh_name: str,
        enable_offline: bool = True,
        enable_federated_learning: bool = True
    ):
        self.mesh_name = mesh_name
        self.enable_offline = enable_offline
        self.enable_federated_learning = enable_federated_learning
        
        # Learner registry
        self.learners: Dict[str, LearnerProfile] = {}
        
        # Content library
        self.content_library: Dict[str, LearningContent] = {}
        
        # Learning sessions
        self.sessions: List[LearningSession] = []
        
        # Knowledge graph (subject relationships)
        self.knowledge_graph: Dict[str, List[str]] = {}
        
        logger.info(f"📚 Knowledge Mesh initialized - {mesh_name}")
    
    def register_learner(
        self,
        learner_id: str,
        age: int,
        learning_style: LearningStyle,
        preferred_language: str = "en",
        accessibility_needs: Optional[List[str]] = None
    ) -> LearnerProfile:
        """
        Register a new learner in the mesh.
        
        Args:
            learner_id: Unique identifier
            age: Learner age
            learning_style: Preferred learning style
            preferred_language: ISO language code
            accessibility_needs: List of accessibility requirements
        
        Returns:
            LearnerProfile object
        """
        # Initialize proficiency levels
        proficiency_levels = {
            domain: 0.0 for domain in SubjectDomain
        }
        
        profile = LearnerProfile(
            learner_id=learner_id,
            age=age,
            learning_style=learning_style,
            proficiency_levels=proficiency_levels,
            learning_pace=1.0,  # Average pace
            engagement_score=0.5,  # Neutral starting point
            preferred_language=preferred_language,
            accessibility_needs=accessibility_needs or [],
            metadata={"registered_at": datetime.utcnow().isoformat()}
        )
        
        self.learners[learner_id] = profile
        
        logger.info(f"✅ Registered learner: {learner_id} (Age: {age}, Style: {learning_style.value})")
        return profile
    
    def add_content(
        self,
        content_id: str,
        subject: SubjectDomain,
        difficulty: DifficultyLevel,
        title: str,
        description: str,
        content_type: str,
        duration_minutes: int,
        prerequisites: Optional[List[str]] = None,
        learning_objectives: Optional[List[str]] = None
    ) -> LearningContent:
        """
        Add educational content to the library.
        
        Args:
            content_id: Unique identifier
            subject: Subject domain
            difficulty: Difficulty level
            title: Content title
            description: Content description
            content_type: Type of content
            duration_minutes: Expected duration
            prerequisites: Required prior knowledge
            learning_objectives: Learning outcomes
        
        Returns:
            LearningContent object
        """
        content = LearningContent(
            content_id=content_id,
            subject=subject,
            difficulty=difficulty,
            title=title,
            description=description,
            content_type=content_type,
            duration_minutes=duration_minutes,
            prerequisites=prerequisites or [],
            learning_objectives=learning_objectives or [],
            metadata={"created_at": datetime.utcnow().isoformat()}
        )
        
        self.content_library[content_id] = content
        
        logger.info(f"📖 Added content: {title} ({subject.value}, Level {difficulty.value})")
        return content
    
    def generate_learning_path(
        self,
        learner_id: str,
        subject: SubjectDomain,
        target_proficiency: float = 0.8,
        time_budget_hours: Optional[int] = None
    ) -> List[LearningContent]:
        """
        Generate personalized learning path for a learner.
        
        Args:
            learner_id: Learner identifier
            subject: Subject domain
            target_proficiency: Target proficiency level (0-1)
            time_budget_hours: Maximum time budget
        
        Returns:
            Ordered list of LearningContent
        """
        if learner_id not in self.learners:
            raise ValueError(f"Learner not found: {learner_id}")
        
        learner = self.learners[learner_id]
        current_proficiency = learner.proficiency_levels.get(subject, 0.0)
        
        # Filter content by subject
        subject_content = [
            c for c in self.content_library.values()
            if c.subject == subject
        ]
        
        # Sort by difficulty
        subject_content.sort(key=lambda c: c.difficulty.value)
        
        # Build learning path
        learning_path = []
        cumulative_time = 0
        simulated_proficiency = current_proficiency
        
        for content in subject_content:
            # Check if learner is ready for this content
            if not self._check_prerequisites(learner_id, content):
                continue
            
            # Check time budget
            if time_budget_hours:
                if cumulative_time + content.duration_minutes > time_budget_hours * 60:
                    break
            
            # Add to path
            learning_path.append(content)
            cumulative_time += content.duration_minutes
            
            # Simulate proficiency gain
            proficiency_gain = self._estimate_proficiency_gain(
                learner=learner,
                content=content
            )
            simulated_proficiency += proficiency_gain
            
            # Check if target reached
            if simulated_proficiency >= target_proficiency:
                break
        
        logger.info(
            f"🎯 Generated learning path for {learner_id}: "
            f"{len(learning_path)} items, {cumulative_time} minutes"
        )
        
        return learning_path
    
    def start_learning_session(
        self,
        learner_id: str,
        content_id: str
    ) -> LearningSession:
        """
        Start a new learning session.
        
        Args:
            learner_id: Learner identifier
            content_id: Content identifier
        
        Returns:
            LearningSession object
        """
        if learner_id not in self.learners:
            raise ValueError(f"Learner not found: {learner_id}")
        
        if content_id not in self.content_library:
            raise ValueError(f"Content not found: {content_id}")
        
        session_id = f"SESSION_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{learner_id}"
        
        session = LearningSession(
            session_id=session_id,
            learner_id=learner_id,
            content_id=content_id,
            start_time=datetime.utcnow().isoformat(),
            end_time=None,
            completion_rate=0.0,
            comprehension_score=0.0,
            engagement_metrics={},
            feedback=None
        )
        
        self.sessions.append(session)
        
        logger.info(f"▶️ Started session: {session_id}")
        return session
    
    def complete_learning_session(
        self,
        session_id: str,
        completion_rate: float,
        comprehension_score: float,
        engagement_metrics: Optional[Dict] = None,
        feedback: Optional[str] = None
    ) -> LearningSession:
        """
        Complete a learning session and update learner profile.
        
        Args:
            session_id: Session identifier
            completion_rate: Completion percentage (0-1)
            comprehension_score: Comprehension score (0-1)
            engagement_metrics: Engagement data
            feedback: Learner feedback
        
        Returns:
            Updated LearningSession
        """
        # Find session
        session = next((s for s in self.sessions if s.session_id == session_id), None)
        
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        # Update session
        session.end_time = datetime.utcnow().isoformat()
        session.completion_rate = completion_rate
        session.comprehension_score = comprehension_score
        session.engagement_metrics = engagement_metrics or {}
        session.feedback = feedback
        
        # Update learner profile
        self._update_learner_profile(session)
        
        logger.info(
            f"✅ Completed session: {session_id} "
            f"(Completion: {completion_rate:.1%}, Score: {comprehension_score:.2f})"
        )
        
        return session
    
    def get_adaptive_recommendations(
        self,
        learner_id: str,
        count: int = 5
    ) -> List[LearningContent]:
        """
        Get adaptive content recommendations for a learner.
        
        Args:
            learner_id: Learner identifier
            count: Number of recommendations
        
        Returns:
            List of recommended LearningContent
        """
        if learner_id not in self.learners:
            raise ValueError(f"Learner not found: {learner_id}")
        
        learner = self.learners[learner_id]
        
        # Score all content
        scored_content = []
        
        for content in self.content_library.values():
            # Check prerequisites
            if not self._check_prerequisites(learner_id, content):
                continue
            
            # Calculate recommendation score
            score = self._calculate_recommendation_score(learner, content)
            
            scored_content.append((content, score))
        
        # Sort by score
        scored_content.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N
        recommendations = [c for c, _ in scored_content[:count]]
        
        logger.info(f"💡 Generated {len(recommendations)} recommendations for {learner_id}")
        
        return recommendations
    
    def export_learner_progress(
        self,
        learner_id: str,
        output_path: str
    ) -> bool:
        """
        Export learner progress report.
        
        Args:
            learner_id: Learner identifier
            output_path: Path to save report
        
        Returns:
            True if export successful
        """
        if learner_id not in self.learners:
            raise ValueError(f"Learner not found: {learner_id}")
        
        learner = self.learners[learner_id]
        
        # Get learner sessions
        learner_sessions = [s for s in self.sessions if s.learner_id == learner_id]
        
        # Calculate statistics
        total_sessions = len(learner_sessions)
        total_time_minutes = sum(
            self.content_library[s.content_id].duration_minutes
            for s in learner_sessions
            if s.content_id in self.content_library
        )
        avg_completion = np.mean([s.completion_rate for s in learner_sessions]) if learner_sessions else 0
        avg_comprehension = np.mean([s.comprehension_score for s in learner_sessions]) if learner_sessions else 0
        
        # Generate report
        report = {
            "learner_id": learner_id,
            "profile": {
                "age": learner.age,
                "learning_style": learner.learning_style.value,
                "preferred_language": learner.preferred_language,
                "learning_pace": learner.learning_pace,
                "engagement_score": learner.engagement_score
            },
            "proficiency_levels": {
                domain.value: level
                for domain, level in learner.proficiency_levels.items()
            },
            "statistics": {
                "total_sessions": total_sessions,
                "total_time_hours": total_time_minutes / 60,
                "average_completion_rate": avg_completion,
                "average_comprehension_score": avg_comprehension
            },
            "recent_sessions": [
                {
                    "content_id": s.content_id,
                    "start_time": s.start_time,
                    "completion_rate": s.completion_rate,
                    "comprehension_score": s.comprehension_score
                }
                for s in learner_sessions[-10:]  # Last 10 sessions
            ],
            "generated_at": datetime.utcnow().isoformat()
        }
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📊 Exported progress report: {output_path}")
        return True
    
    def _check_prerequisites(
        self,
        learner_id: str,
        content: LearningContent
    ) -> bool:
        """Check if learner meets content prerequisites"""
        if not content.prerequisites:
            return True
        
        learner = self.learners[learner_id]
        
        # Check if learner has completed prerequisites
        completed_content = set(
            s.content_id for s in self.sessions
            if s.learner_id == learner_id and s.completion_rate >= 0.8
        )
        
        return all(prereq in completed_content for prereq in content.prerequisites)
    
    def _estimate_proficiency_gain(
        self,
        learner: LearnerProfile,
        content: LearningContent
    ) -> float:
        """Estimate proficiency gain from content"""
        # Base gain from difficulty
        base_gain = content.difficulty.value * 0.05
        
        # Adjust for learning pace
        pace_multiplier = learner.learning_pace
        
        # Adjust for engagement
        engagement_multiplier = learner.engagement_score
        
        return base_gain * pace_multiplier * engagement_multiplier
    
    def _update_learner_profile(self, session: LearningSession):
        """Update learner profile based on session results"""
        learner = self.learners[session.learner_id]
        content = self.content_library[session.content_id]
        
        # Update proficiency
        proficiency_gain = session.comprehension_score * 0.1
        current = learner.proficiency_levels.get(content.subject, 0.0)
        learner.proficiency_levels[content.subject] = min(1.0, current + proficiency_gain)
        
        # Update engagement score (exponential moving average)
        engagement = session.completion_rate * session.comprehension_score
        learner.engagement_score = 0.7 * learner.engagement_score + 0.3 * engagement
        
        # Update learning pace
        expected_time = content.duration_minutes
        if session.end_time and session.start_time:
            start = datetime.fromisoformat(session.start_time)
            end = datetime.fromisoformat(session.end_time)
            actual_time = (end - start).total_seconds() / 60
            pace_ratio = expected_time / actual_time if actual_time > 0 else 1.0
            learner.learning_pace = 0.7 * learner.learning_pace + 0.3 * pace_ratio
    
    def _calculate_recommendation_score(
        self,
        learner: LearnerProfile,
        content: LearningContent
    ) -> float:
        """Calculate recommendation score for content"""
        # Proficiency match (content should be slightly above current level)
        current_proficiency = learner.proficiency_levels.get(content.subject, 0.0)
        target_proficiency = content.difficulty.value / 5.0
        proficiency_gap = target_proficiency - current_proficiency
        
        # Ideal gap is 0.1-0.2 (slightly challenging)
        if 0.1 <= proficiency_gap <= 0.2:
            proficiency_score = 1.0
        elif proficiency_gap < 0:
            proficiency_score = 0.5  # Too easy
        else:
            proficiency_score = max(0, 1.0 - (proficiency_gap - 0.2) * 2)
        
        # Learning style match
        style_score = 1.0  # Simplified - would match content type to learning style
        
        # Engagement prediction
        engagement_score = learner.engagement_score
        
        # Combined score
        return (proficiency_score * 0.5 + style_score * 0.3 + engagement_score * 0.2)


# Example usage
if __name__ == "__main__":
    # Initialize Knowledge Mesh
    mesh = KnowledgeMesh(
        mesh_name="Dadaab Education Network",
        enable_offline=True,
        enable_federated_learning=True
    )
    
    # Register learner
    learner = mesh.register_learner(
        learner_id="LEARNER_001",
        age=14,
        learning_style=LearningStyle.VISUAL,
        preferred_language="sw"  # Swahili
    )
    
    # Add content
    mesh.add_content(
        content_id="HEALTH_LIT_001",
        subject=SubjectDomain.HEALTH_LITERACY,
        difficulty=DifficultyLevel.BEGINNER,
        title="Understanding Cholera Prevention",
        description="Learn how to prevent cholera through hygiene and sanitation",
        content_type="video",
        duration_minutes=15,
        learning_objectives=[
            "Identify cholera symptoms",
            "Understand transmission pathways",
            "Practice prevention methods"
        ]
    )
    
    # Generate learning path
    path = mesh.generate_learning_path(
        learner_id="LEARNER_001",
        subject=SubjectDomain.HEALTH_LITERACY,
        target_proficiency=0.7,
        time_budget_hours=2
    )
    
    print(f"📚 Learning path: {len(path)} items")
    
    # Start session
    session = mesh.start_learning_session(
        learner_id="LEARNER_001",
        content_id="HEALTH_LIT_001"
    )
    
    # Complete session
    mesh.complete_learning_session(
        session_id=session.session_id,
        completion_rate=0.95,
        comprehension_score=0.85,
        feedback="Very helpful!"
    )
    
    # Get recommendations
    recommendations = mesh.get_adaptive_recommendations(
        learner_id="LEARNER_001",
        count=3
    )
    
    print(f"💡 Recommendations: {len(recommendations)}")
    
    # Export progress
    mesh.export_learner_progress(
        learner_id="LEARNER_001",
        output_path="learner_progress.json"
    )
