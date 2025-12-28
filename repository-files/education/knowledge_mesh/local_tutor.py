"""
Knowledge Mesh - Sovereign AI Tutors
Offline-first education platform using local LLMs (NIMs) for refugee education

Compliance:
- Kenya Competency-Based Curriculum (CBC)
- UNESCO Education 2030 Framework
- UNHCR Education Strategy 2030
- Right to Education (Universal Declaration of Human Rights Art. 26)
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class SubjectArea(Enum):
    """CBC Subject Areas"""
    MATHEMATICS = "mathematics"
    ENGLISH = "english"
    KISWAHILI = "kiswahili"
    SCIENCE = "science"
    SOCIAL_STUDIES = "social_studies"
    CREATIVE_ARTS = "creative_arts"
    PHYSICAL_EDUCATION = "physical_education"
    LIFE_SKILLS = "life_skills"


class GradeLevel(Enum):
    """Kenya CBC Grade Levels"""
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
    lesson_id: str
    subject: SubjectArea
    grade_level: GradeLevel
    title: str
    learning_objectives: List[str]
    content: str
    activities: List[Dict]
    assessment: Dict
    language: LanguageMode
    duration_minutes: int
    resources_required: List[str]


@dataclass
class StudentProfile:
    """Student learning profile"""
    student_id: str
    name: str
    grade_level: GradeLevel
    preferred_language: LanguageMode
    learning_pace: str  # "fast", "moderate", "slow"
    strengths: List[SubjectArea]
    areas_for_improvement: List[SubjectArea]
    attendance_rate: float
    last_assessment_scores: Dict[SubjectArea, float]


class SovereignTutor:
    """
    Offline AI Tutor (NIM) aligned with Kenyan CBC Curriculum.
    Runs on Ghost-Mesh for refugee education.
    
    Use Case: Democratize high-quality education in camps with 1:100 teacher ratios
    """
    
    def __init__(
        self,
        model_path: str = "./models/llama3-cbc-tuned",
        offline_mode: bool = True,
        language_default: LanguageMode = LanguageMode.MIXED_ENGLISH_SOMALI
    ):
        self.model_path = model_path
        self.offline_mode = offline_mode
        self.language_default = language_default
        
        # CBC Curriculum database (simplified)
        self.curriculum_db = self._load_cbc_curriculum()
        
        # Student profiles
        self.students: Dict[str, StudentProfile] = {}
        
        logger.info(f"📚 Sovereign Tutor initialized")
        logger.info(f"   Model: {model_path}")
        logger.info(f"   Offline Mode: {offline_mode}")
        logger.info(f"   Default Language: {language_default.value}")
    
    def generate_lesson(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel,
        language: Optional[LanguageMode] = None,
        personalized_for: Optional[str] = None
    ) -> LessonPlan:
        """
        Generate a personalized lesson plan aligned with CBC.
        
        Args:
            subject: Subject area
            grade_level: Grade level (1-9)
            language: Language mode (defaults to instance default)
            personalized_for: Student ID for personalization
        
        Returns:
            Complete lesson plan
        """
        language = language or self.language_default
        
        logger.info(f"📖 [Edu-NIM] Generating {subject.value} lesson for Grade {grade_level.value}...")
        logger.info(f"   Language: {language.value}")
        
        # Get curriculum objectives
        objectives = self._get_curriculum_objectives(subject, grade_level)
        
        # Personalize if student profile exists
        if personalized_for and personalized_for in self.students:
            student = self.students[personalized_for]
            objectives = self._personalize_objectives(objectives, student)
            logger.info(f"   Personalized for: {student.name}")
        
        # Generate lesson content
        lesson_content = self._generate_lesson_content(
            subject, grade_level, objectives, language
        )
        
        # Generate activities
        activities = self._generate_activities(subject, grade_level, language)
        
        # Generate assessment
        assessment = self._generate_assessment(subject, grade_level, objectives)
        
        lesson_plan = LessonPlan(
            lesson_id=f"{subject.value}_{grade_level.value}_{datetime.now().strftime('%Y%m%d')}",
            subject=subject,
            grade_level=grade_level,
            title=self._generate_lesson_title(subject, grade_level),
            learning_objectives=objectives,
            content=lesson_content,
            activities=activities,
            assessment=assessment,
            language=language,
            duration_minutes=40,  # Standard CBC lesson duration
            resources_required=self._get_required_resources(subject)
        )
        
        logger.info(f"✅ Lesson generated: {lesson_plan.title}")
        return lesson_plan
    
    def _load_cbc_curriculum(self) -> Dict:
        """Load CBC curriculum standards"""
        # Simplified curriculum database
        return {
            SubjectArea.MATHEMATICS: {
                GradeLevel.GRADE_4: [
                    "Understand place value up to 10,000",
                    "Perform addition and subtraction with regrouping",
                    "Identify and classify 2D and 3D shapes",
                    "Measure length, mass, and capacity"
                ],
                GradeLevel.GRADE_7: [
                    "Solve linear equations and inequalities",
                    "Calculate area and perimeter of complex shapes",
                    "Understand ratios, proportions, and percentages",
                    "Analyze and interpret data using graphs"
                ]
            },
            SubjectArea.SCIENCE: {
                GradeLevel.GRADE_4: [
                    "Understand photosynthesis and plant growth",
                    "Identify states of matter and their properties",
                    "Explore simple machines and their uses",
                    "Understand the water cycle"
                ],
                GradeLevel.GRADE_7: [
                    "Understand cell structure and function",
                    "Explore chemical reactions and equations",
                    "Study forces, motion, and energy",
                    "Understand ecosystems and biodiversity"
                ]
            },
            SubjectArea.ENGLISH: {
                GradeLevel.GRADE_4: [
                    "Read and comprehend grade-level texts",
                    "Write descriptive and narrative paragraphs",
                    "Use correct grammar and punctuation",
                    "Expand vocabulary through context clues"
                ],
                GradeLevel.GRADE_7: [
                    "Analyze literary texts and themes",
                    "Write persuasive and expository essays",
                    "Use advanced grammar structures",
                    "Deliver oral presentations effectively"
                ]
            }
        }
    
    def _get_curriculum_objectives(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel
    ) -> List[str]:
        """Get CBC learning objectives for subject and grade"""
        try:
            return self.curriculum_db[subject][grade_level]
        except KeyError:
            # Default objectives if not in database
            return [
                f"Understand key concepts in {subject.value}",
                f"Apply knowledge to solve problems",
                f"Demonstrate mastery through assessment"
            ]
    
    def _personalize_objectives(
        self,
        objectives: List[str],
        student: StudentProfile
    ) -> List[str]:
        """Personalize objectives based on student profile"""
        # Adjust difficulty based on learning pace
        if student.learning_pace == "fast":
            objectives.append("Explore advanced concepts and extensions")
        elif student.learning_pace == "slow":
            objectives.insert(0, "Review prerequisite concepts")
        
        return objectives
    
    def _generate_lesson_content(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel,
        objectives: List[str],
        language: LanguageMode
    ) -> str:
        """Generate lesson content"""
        # Example: Photosynthesis lesson for Grade 4 Science
        if subject == SubjectArea.SCIENCE and grade_level == GradeLevel.GRADE_4:
            if language == LanguageMode.MIXED_ENGLISH_SOMALI:
                return """
# Photosynthesis (Sawir-soo-saarka)

## Introduction
Plants (dhirta) make their own food using sunlight (iftiinka qorraxda), water (biyaha), and air (hawada).

## The Process
1. **Sunlight** - Plants capture energy from the sun
   - Somali: Dhirtu waxay qabtaan tamarta qorraxda
2. **Water** - Roots absorb water from soil
   - Somali: Xididadu waxay nuugaan biyaha ciidda
3. **Carbon Dioxide** - Leaves take in CO2 from air
   - Somali: Caleemaha waxay qaataan kaarboon-dayookside hawada
4. **Oxygen** - Plants release oxygen we breathe
   - Somali: Dhirtu waxay sii daayaan oksijiin aan neefsanno

## Why It Matters
Without photosynthesis, there would be no food or oxygen on Earth!
                """
        
        # Generic content template
        return f"""
# {subject.value.title()} - Grade {grade_level.value}

## Learning Objectives
{chr(10).join(f'- {obj}' for obj in objectives)}

## Main Content
[Lesson content would be generated by the LLM based on CBC standards]

## Key Concepts
- Concept 1
- Concept 2
- Concept 3

## Practice Examples
[Examples aligned with learning objectives]
        """
    
    def _generate_activities(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel,
        language: LanguageMode
    ) -> List[Dict]:
        """Generate interactive activities"""
        activities = []
        
        if subject == SubjectArea.SCIENCE:
            activities.append({
                "type": "hands_on_experiment",
                "title": "Observe Photosynthesis",
                "description": "Place a plant in sunlight and observe changes over 3 days",
                "duration_minutes": 15,
                "materials": ["plant", "water", "sunlight", "notebook"]
            })
        
        elif subject == SubjectArea.MATHEMATICS:
            activities.append({
                "type": "problem_solving",
                "title": "Real-World Math Problems",
                "description": "Solve problems related to market shopping and budgeting",
                "duration_minutes": 20,
                "materials": ["paper", "pencil", "calculator"]
            })
        
        elif subject == SubjectArea.ENGLISH:
            activities.append({
                "type": "creative_writing",
                "title": "Write a Story",
                "description": "Write a short story about your community",
                "duration_minutes": 25,
                "materials": ["paper", "pencil"]
            })
        
        # Group discussion activity (universal)
        activities.append({
            "type": "group_discussion",
            "title": "Share and Learn",
            "description": "Discuss key concepts with classmates",
            "duration_minutes": 10,
            "materials": []
        })
        
        return activities
    
    def _generate_assessment(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel,
        objectives: List[str]
    ) -> Dict:
        """Generate assessment aligned with objectives"""
        return {
            "type": "formative_assessment",
            "questions": [
                {
                    "question": f"Explain the main concept of today's lesson",
                    "type": "open_ended",
                    "points": 5
                },
                {
                    "question": f"Apply what you learned to solve this problem",
                    "type": "problem_solving",
                    "points": 10
                },
                {
                    "question": f"What questions do you still have?",
                    "type": "reflection",
                    "points": 5
                }
            ],
            "total_points": 20,
            "passing_score": 14,
            "feedback_enabled": True
        }
    
    def _generate_lesson_title(
        self,
        subject: SubjectArea,
        grade_level: GradeLevel
    ) -> str:
        """Generate engaging lesson title"""
        titles = {
            SubjectArea.SCIENCE: "Exploring the Wonders of Science",
            SubjectArea.MATHEMATICS: "Math in Our Daily Lives",
            SubjectArea.ENGLISH: "The Power of Words",
            SubjectArea.SOCIAL_STUDIES: "Understanding Our World"
        }
        return titles.get(subject, f"{subject.value.title()} Lesson")
    
    def _get_required_resources(self, subject: SubjectArea) -> List[str]:
        """Get required teaching resources"""
        common_resources = ["chalkboard", "chalk", "notebooks", "pencils"]
        
        subject_specific = {
            SubjectArea.SCIENCE: ["science kit", "specimens", "magnifying glass"],
            SubjectArea.MATHEMATICS: ["ruler", "protractor", "calculator"],
            SubjectArea.CREATIVE_ARTS: ["art supplies", "musical instruments"],
            SubjectArea.PHYSICAL_EDUCATION: ["sports equipment", "open space"]
        }
        
        return common_resources + subject_specific.get(subject, [])
    
    def register_student(self, student: StudentProfile):
        """Register a student for personalized learning"""
        self.students[student.student_id] = student
        logger.info(f"👤 Student registered: {student.name} (Grade {student.grade_level.value})")
    
    def track_progress(
        self,
        student_id: str,
        subject: SubjectArea,
        assessment_score: float
    ):
        """Track student progress"""
        if student_id in self.students:
            student = self.students[student_id]
            student.last_assessment_scores[subject] = assessment_score
            logger.info(f"📊 Progress tracked: {student.name} - {subject.value}: {assessment_score}%")
    
    def generate_progress_report(self, student_id: str) -> Dict:
        """Generate student progress report"""
        if student_id not in self.students:
            return {"error": "Student not found"}
        
        student = self.students[student_id]
        
        return {
            "student_name": student.name,
            "grade_level": student.grade_level.value,
            "attendance_rate": f"{student.attendance_rate:.1%}",
            "assessment_scores": {
                subject.value: f"{score:.1f}%"
                for subject, score in student.last_assessment_scores.items()
            },
            "strengths": [s.value for s in student.strengths],
            "areas_for_improvement": [s.value for s in student.areas_for_improvement],
            "recommendations": self._generate_recommendations(student)
        }
    
    def _generate_recommendations(self, student: StudentProfile) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Check attendance
        if student.attendance_rate < 0.8:
            recommendations.append("⚠️ Improve attendance to enhance learning outcomes")
        
        # Check assessment scores
        for subject, score in student.last_assessment_scores.items():
            if score < 50:
                recommendations.append(
                    f"📚 Focus on {subject.value} - consider additional tutoring"
                )
            elif score > 85:
                recommendations.append(
                    f"⭐ Excellent work in {subject.value} - explore advanced topics"
                )
        
        return recommendations


# Example usage
if __name__ == "__main__":
    # Initialize Sovereign Tutor
    tutor = SovereignTutor(
        offline_mode=True,
        language_default=LanguageMode.MIXED_ENGLISH_SOMALI
    )
    
    # Generate a Science lesson for Grade 4
    lesson = tutor.generate_lesson(
        subject=SubjectArea.SCIENCE,
        grade_level=GradeLevel.GRADE_4,
        language=LanguageMode.MIXED_ENGLISH_SOMALI
    )
    
    print(f"\n📖 Lesson Plan Generated:")
    print(f"   Title: {lesson.title}")
    print(f"   Subject: {lesson.subject.value}")
    print(f"   Grade: {lesson.grade_level.value}")
    print(f"   Language: {lesson.language.value}")
    print(f"   Duration: {lesson.duration_minutes} minutes")
    print(f"\n📋 Learning Objectives:")
    for obj in lesson.learning_objectives:
        print(f"   - {obj}")
    print(f"\n🎯 Activities: {len(lesson.activities)}")
    print(f"✅ Assessment: {lesson.assessment['total_points']} points")
    
    # Register a student
    student = StudentProfile(
        student_id="STU_001",
        name="Amina Hassan",
        grade_level=GradeLevel.GRADE_4,
        preferred_language=LanguageMode.MIXED_ENGLISH_SOMALI,
        learning_pace="moderate",
        strengths=[SubjectArea.ENGLISH, SubjectArea.CREATIVE_ARTS],
        areas_for_improvement=[SubjectArea.MATHEMATICS],
        attendance_rate=0.92,
        last_assessment_scores={
            SubjectArea.SCIENCE: 78.0,
            SubjectArea.MATHEMATICS: 65.0,
            SubjectArea.ENGLISH: 88.0
        }
    )
    
    tutor.register_student(student)
    
    # Generate progress report
    report = tutor.generate_progress_report("STU_001")
    print(f"\n📊 Progress Report:")
    print(json.dumps(report, indent=2))
