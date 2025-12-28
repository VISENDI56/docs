"""
Knowledge Mesh - Sovereign AI Tutors
Offline AI education system aligned with Kenyan Competency-Based Curriculum (CBC)

Democratizes high-quality education without internet costs.
Teacher-to-student ratio: 1:100 → 1:1 (AI-augmented)

Compliance:
- Kenya Competency-Based Curriculum (CBC) 2017
- UNESCO Education 2030 Framework
- UNHCR Education Strategy 2030
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import random

logger = logging.getLogger(__name__)


class SubjectArea(Enum):
    """CBC Subject Areas"""
    MATHEMATICS = "mathematics"
    ENGLISH = "english"
    KISWAHILI = "kiswahili"
    SCIENCE = "science"
    SOCIAL_STUDIES = "social_studies"
    RELIGIOUS_EDUCATION = "religious_education"
    CREATIVE_ARTS = "creative_arts"
    PHYSICAL_EDUCATION = "physical_education"
    LIFE_SKILLS = "life_skills"


class GradeLevel(Enum):
    """CBC Grade Levels"""
    GRADE_1 = 1
    GRADE_2 = 2
    GRADE_3 = 3
    GRADE_4 = 4
    GRADE_5 = 5
    GRADE_6 = 6
    GRADE_7 = 7
    GRADE_8 = 8
    GRADE_9 = 9


class LanguageMode(Enum):
    """Language delivery modes"""
    ENGLISH = "english"
    KISWAHILI = "kiswahili"
    SOMALI = "somali"
    MIXED_ENGLISH_SOMALI = "mixed_english_somali"
    MIXED_KISWAHILI_SOMALI = "mixed_kiswahili_somali"


@dataclass
class LessonPlan:
    """Structured lesson plan"""
    title: str
    subject: SubjectArea
    grade_level: GradeLevel
    language: LanguageMode
    duration_minutes: int
    learning_outcomes: List[str]
    activities: List[Dict]
    assessment: Dict
    resources: List[str]
    differentiation: Dict  # For different learning abilities


@dataclass
class StudentProfile:
    """Individual student learning profile"""
    student_id: str
    name: str
    grade_level: GradeLevel
    language_preference: LanguageMode
    learning_pace: str  # "fast", "average", "slow"
    strengths: List[SubjectArea]
    areas_for_improvement: List[SubjectArea]
    attendance_rate: float
    last_assessment_scores: Dict[SubjectArea, float]


class SovereignTutor:
    """
    Offline AI Tutor (NIM) aligned with Kenyan CBC Curriculum.
    Runs on Ghost-Mesh for refugee education.
    
    Features:
    - Personalized learning paths
    - Multi-language support (English, Kiswahili, Somali)
    - Offline operation on edge devices
    - CBC-aligned assessments
    - Cultural sensitivity
    """
    
    def __init__(
        self,
        model_path: str = "./models/llama3-cbc-tutor",
        enable_offline_mode: bool = True,
        default_language: LanguageMode = LanguageMode.MIXED_ENGLISH_SOMALI
    ):
        self.model_path = model_path
        self.enable_offline_mode = enable_offline_mode
        self.default_language = default_language
        
        # Load CBC curriculum standards
        self.curriculum_standards = self._load_cbc_standards()
        
        # Student profiles
        self.students: Dict[str, StudentProfile] = {}
        
        logger.info("📚 Sovereign Tutor initialized")
        logger.info(f"   Model: {model_path}")
        logger.info(f"   Offline Mode: {enable_offline_mode}")
        logger.info(f"   Default Language: {default_language.value}")
    
    def generate_lesson(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel,
        language: Optional[LanguageMode] = None,
        student_profile: Optional[StudentProfile] = None
    ) -> LessonPlan:
        """
        Generate a personalized lesson plan aligned with CBC.
        
        Args:
            subject: Subject area
            grade_level: Grade level
            language: Language mode (defaults to tutor's default)
            student_profile: Optional student profile for personalization
        
        Returns:
            Complete lesson plan
        """
        language = language or self.default_language
        
        logger.info(f"📖 [Edu-NIM] Generating {subject.value} lesson for Grade {grade_level.value}")
        logger.info(f"   Language: {language.value}")
        
        # Get CBC learning outcomes for this grade/subject
        learning_outcomes = self._get_learning_outcomes(subject, grade_level)
        
        # Generate activities
        activities = self._generate_activities(
            subject, grade_level, language, student_profile
        )
        
        # Generate assessment
        assessment = self._generate_assessment(subject, grade_level, language)
        
        # Get resources
        resources = self._get_resources(subject, grade_level)
        
        # Differentiation strategies
        differentiation = self._generate_differentiation(student_profile)
        
        lesson = LessonPlan(
            title=self._generate_lesson_title(subject, grade_level),
            subject=subject,
            grade_level=grade_level,
            language=language,
            duration_minutes=40,  # Standard CBC lesson duration
            learning_outcomes=learning_outcomes,
            activities=activities,
            assessment=assessment,
            resources=resources,
            differentiation=differentiation
        )
        
        logger.info(f"✅ Lesson generated: {lesson.title}")
        logger.info(f"   Outcomes: {len(learning_outcomes)}")
        logger.info(f"   Activities: {len(activities)}")
        
        return lesson
    
    def personalize_learning_path(
        self,
        student: StudentProfile,
        target_subjects: Optional[List[SubjectArea]] = None
    ) -> List[LessonPlan]:
        """
        Generate a personalized learning path for a student.
        
        Args:
            student: Student profile
            target_subjects: Subjects to focus on (defaults to areas for improvement)
        
        Returns:
            List of personalized lesson plans
        """
        logger.info(f"🎯 Personalizing learning path for {student.name}")
        
        # Determine focus areas
        if target_subjects is None:
            target_subjects = student.areas_for_improvement
        
        learning_path = []
        
        for subject in target_subjects:
            # Generate lesson at appropriate difficulty
            lesson = self.generate_lesson(
                subject=subject,
                grade_level=student.grade_level,
                language=student.language_preference,
                student_profile=student
            )
            learning_path.append(lesson)
        
        logger.info(f"✅ Learning path created: {len(learning_path)} lessons")
        
        return learning_path
    
    def assess_student(
        self,
        student: StudentProfile,
        subject: SubjectArea,
        responses: Dict[str, str]
    ) -> Dict:
        """
        Assess student responses and provide feedback.
        
        Args:
            student: Student profile
            subject: Subject being assessed
            responses: Student's responses to assessment questions
        
        Returns:
            Assessment results with feedback
        """
        logger.info(f"📝 Assessing {student.name} - {subject.value}")
        
        # In production, use actual NIM model for assessment
        # For now, simulate scoring
        
        total_questions = len(responses)
        correct_answers = random.randint(int(total_questions * 0.6), total_questions)
        score = (correct_answers / total_questions) * 100
        
        # Generate feedback
        feedback = self._generate_feedback(score, subject, student)
        
        # Update student profile
        student.last_assessment_scores[subject] = score
        
        result = {
            "student_id": student.student_id,
            "subject": subject.value,
            "score": score,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "feedback": feedback,
            "next_steps": self._recommend_next_steps(score, subject, student)
        }
        
        logger.info(f"✅ Assessment complete - Score: {score:.1f}%")
        
        return result
    
    def translate_content(
        self,
        content: str,
        source_language: LanguageMode,
        target_language: LanguageMode
    ) -> str:
        """
        Translate educational content between languages.
        
        Preserves cultural context and educational terminology.
        """
        logger.info(f"🌐 Translating: {source_language.value} → {target_language.value}")
        
        # In production, use actual translation model
        # For now, return with language tag
        translated = f"[{target_language.value.upper()}] {content}"
        
        return translated
    
    def _load_cbc_standards(self) -> Dict:
        """Load CBC curriculum standards"""
        # In production, load from actual CBC documents
        return {
            "mathematics": {
                "grade_1": ["Number sense 1-100", "Basic addition", "Basic subtraction"],
                "grade_4": ["Multiplication tables", "Division", "Fractions"],
                "grade_7": ["Algebra basics", "Geometry", "Data handling"]
            },
            "science": {
                "grade_1": ["Living things", "Non-living things", "Weather"],
                "grade_4": ["Plants", "Animals", "Matter"],
                "grade_7": ["Cells", "Energy", "Forces"]
            }
        }
    
    def _get_learning_outcomes(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel
    ) -> List[str]:
        """Get CBC learning outcomes for subject/grade"""
        
        # Sample learning outcomes
        outcomes_map = {
            (SubjectArea.MATHEMATICS, GradeLevel.GRADE_4): [
                "Multiply numbers up to 1000",
                "Solve word problems involving multiplication",
                "Understand the relationship between multiplication and division"
            ],
            (SubjectArea.SCIENCE, GradeLevel.GRADE_4): [
                "Identify parts of a plant and their functions",
                "Explain the process of photosynthesis",
                "Classify plants based on characteristics"
            ],
            (SubjectArea.ENGLISH, GradeLevel.GRADE_4): [
                "Read and comprehend grade-level texts",
                "Write coherent paragraphs with topic sentences",
                "Use correct grammar and punctuation"
            ]
        }
        
        key = (subject, grade_level)
        return outcomes_map.get(key, ["General learning outcome for this grade/subject"])
    
    def _generate_activities(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel,
        language: LanguageMode,
        student_profile: Optional[StudentProfile]
    ) -> List[Dict]:
        """Generate engaging learning activities"""
        
        activities = []
        
        if subject == SubjectArea.MATHEMATICS:
            activities = [
                {
                    "type": "interactive",
                    "title": "Multiplication Practice",
                    "description": "Use local objects (stones, sticks) to demonstrate multiplication",
                    "duration_minutes": 15
                },
                {
                    "type": "group_work",
                    "title": "Word Problem Challenge",
                    "description": "Solve real-world problems from camp life",
                    "duration_minutes": 15
                },
                {
                    "type": "individual",
                    "title": "Practice Worksheet",
                    "description": "Complete 10 multiplication problems",
                    "duration_minutes": 10
                }
            ]
        elif subject == SubjectArea.SCIENCE:
            activities = [
                {
                    "type": "observation",
                    "title": "Plant Exploration",
                    "description": "Observe local plants and identify parts",
                    "duration_minutes": 15
                },
                {
                    "type": "experiment",
                    "title": "Photosynthesis Demo",
                    "description": "Simple experiment with leaves and sunlight",
                    "duration_minutes": 15
                },
                {
                    "type": "discussion",
                    "title": "Plant Classification",
                    "description": "Group discussion on plant types",
                    "duration_minutes": 10
                }
            ]
        else:
            activities = [
                {
                    "type": "interactive",
                    "title": "Engaging Activity",
                    "description": "Interactive learning activity",
                    "duration_minutes": 20
                },
                {
                    "type": "practice",
                    "title": "Practice Exercise",
                    "description": "Reinforce learning through practice",
                    "duration_minutes": 20
                }
            ]
        
        return activities
    
    def _generate_assessment(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel,
        language: LanguageMode
    ) -> Dict:
        """Generate CBC-aligned assessment"""
        
        return {
            "type": "formative",
            "questions": [
                {
                    "id": 1,
                    "question": "Sample question 1",
                    "type": "multiple_choice",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "B"
                },
                {
                    "id": 2,
                    "question": "Sample question 2",
                    "type": "short_answer",
                    "expected_answer": "Sample answer"
                }
            ],
            "rubric": {
                "excellent": "90-100%",
                "good": "75-89%",
                "satisfactory": "60-74%",
                "needs_improvement": "<60%"
            }
        }
    
    def _get_resources(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel
    ) -> List[str]:
        """Get required resources for lesson"""
        
        common_resources = [
            "Chalkboard/whiteboard",
            "Chalk/markers",
            "Student notebooks",
            "Pencils"
        ]
        
        subject_resources = {
            SubjectArea.MATHEMATICS: ["Counting objects", "Number charts"],
            SubjectArea.SCIENCE: ["Local plant samples", "Magnifying glass"],
            SubjectArea.ENGLISH: ["Reading books", "Picture cards"]
        }
        
        return common_resources + subject_resources.get(subject, [])
    
    def _generate_differentiation(
        self,
        student_profile: Optional[StudentProfile]
    ) -> Dict:
        """Generate differentiation strategies"""
        
        if not student_profile:
            return {
                "fast_learners": "Extension activities with advanced problems",
                "average_learners": "Standard activities as planned",
                "slow_learners": "Additional support with visual aids and peer tutoring"
            }
        
        if student_profile.learning_pace == "fast":
            return {
                "strategy": "Challenge with advanced content",
                "activities": ["Peer tutoring", "Independent research"]
            }
        elif student_profile.learning_pace == "slow":
            return {
                "strategy": "Additional support and scaffolding",
                "activities": ["One-on-one support", "Visual aids", "Repetition"]
            }
        else:
            return {
                "strategy": "Standard pacing with optional extensions",
                "activities": ["Group work", "Practice exercises"]
            }
    
    def _generate_lesson_title(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel
    ) -> str:
        """Generate engaging lesson title"""
        
        titles = {
            SubjectArea.MATHEMATICS: f"Grade {grade_level.value} Mathematics: Exploring Numbers",
            SubjectArea.SCIENCE: f"Grade {grade_level.value} Science: Discovering Nature",
            SubjectArea.ENGLISH: f"Grade {grade_level.value} English: Language Adventures"
        }
        
        return titles.get(subject, f"Grade {grade_level.value} {subject.value.title()}")
    
    def _generate_feedback(
        self,
        score: float,
        subject: SubjectArea,
        student: StudentProfile
    ) -> str:
        """Generate personalized feedback"""
        
        if score >= 90:
            return f"Excellent work, {student.name}! You have mastered this {subject.value} topic."
        elif score >= 75:
            return f"Good job, {student.name}! You're making great progress in {subject.value}."
        elif score >= 60:
            return f"Well done, {student.name}. Keep practicing {subject.value} to improve further."
        else:
            return f"Keep trying, {student.name}. Let's work together on {subject.value}."
    
    def _recommend_next_steps(
        self,
        score: float,
        subject: SubjectArea,
        student: StudentProfile
    ) -> List[str]:
        """Recommend next learning steps"""
        
        if score >= 90:
            return [
                "Move to next topic",
                "Try advanced challenges",
                "Help peers who need support"
            ]
        elif score >= 75:
            return [
                "Review challenging areas",
                "Practice with additional exercises",
                "Prepare for next topic"
            ]
        else:
            return [
                "Review lesson materials",
                "Get additional support from teacher",
                "Practice with peer tutor",
                "Retake assessment when ready"
            ]


# Example usage
if __name__ == "__main__":
    # Initialize tutor
    tutor = SovereignTutor(
        enable_offline_mode=True,
        default_language=LanguageMode.MIXED_ENGLISH_SOMALI
    )
    
    # Create student profile
    student = StudentProfile(
        student_id="STU_001",
        name="Amina Hassan",
        grade_level=GradeLevel.GRADE_4,
        language_preference=LanguageMode.MIXED_ENGLISH_SOMALI,
        learning_pace="average",
        strengths=[SubjectArea.ENGLISH],
        areas_for_improvement=[SubjectArea.MATHEMATICS, SubjectArea.SCIENCE],
        attendance_rate=0.95,
        last_assessment_scores={}
    )
    
    # Generate personalized lesson
    lesson = tutor.generate_lesson(
        subject=SubjectArea.MATHEMATICS,
        grade_level=GradeLevel.GRADE_4,
        student_profile=student
    )
    
    print("\n" + "="*60)
    print("LESSON PLAN")
    print("="*60)
    print(f"Title: {lesson.title}")
    print(f"Subject: {lesson.subject.value}")
    print(f"Grade: {lesson.grade_level.value}")
    print(f"Language: {lesson.language.value}")
    print(f"Duration: {lesson.duration_minutes} minutes")
    print(f"\nLearning Outcomes:")
    for outcome in lesson.learning_outcomes:
        print(f"  • {outcome}")
    print(f"\nActivities:")
    for activity in lesson.activities:
        print(f"  • {activity['title']} ({activity['duration_minutes']} min)")
    
    # Generate learning path
    learning_path = tutor.personalize_learning_path(student)
    print(f"\n✅ Personalized learning path: {len(learning_path)} lessons")
