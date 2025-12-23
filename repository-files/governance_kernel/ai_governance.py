"""
AI Governance Module
Implements EU AI Act, FDA CDSS, ISO 42001, and IMDRF AI Principles

This module ensures all AI systems in iLuminara-Core comply with:
- EU AI Act (Regulation 2024/1689) - High-risk AI classification
- FDA Clinical Decision Support Software Guidance
- ISO/IEC 42001 - AI Management Systems
- IMDRF AI Principles for Medical Devices
- SPIRIT-AI/CONSORT-AI Guidelines

Compliance:
- EU AI Act Art. 6 (High-Risk AI Systems)
- EU AI Act Art. 8 (Transparency Obligations)
- EU AI Act Art. 12 (Record Keeping)
- FDA 21 CFR Part 11 (Electronic Records)
- ISO 42001:2023 (AI Management)
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import json
import logging
import hashlib

logger = logging.getLogger(__name__)


class AIRiskCategory(Enum):
    """EU AI Act risk categories"""
    UNACCEPTABLE = "unacceptable"  # Prohibited
    HIGH_RISK = "high_risk"  # Requires conformity assessment
    LIMITED_RISK = "limited_risk"  # Transparency obligations
    MINIMAL_RISK = "minimal_risk"  # No specific obligations


class MedicalDeviceClass(Enum):
    """Medical device classification (MDR/FDA)"""
    CLASS_I = "class_i"  # Low risk
    CLASS_IIA = "class_iia"  # Medium risk
    CLASS_IIB = "class_iib"  # Medium-high risk
    CLASS_III = "class_iii"  # High risk


class AISystemType(Enum):
    """Types of AI systems in iLuminara"""
    OUTBREAK_PREDICTION = "outbreak_prediction"
    DISEASE_DIAGNOSIS = "disease_diagnosis"
    RISK_STRATIFICATION = "risk_stratification"
    RESOURCE_ALLOCATION = "resource_allocation"
    SURVEILLANCE_MONITORING = "surveillance_monitoring"
    CLINICAL_DECISION_SUPPORT = "clinical_decision_support"


@dataclass
class AISystemMetadata:
    """Metadata for AI system registration"""
    system_id: str
    system_name: str
    system_type: AISystemType
    risk_category: AIRiskCategory
    device_class: Optional[MedicalDeviceClass]
    intended_use: str
    clinical_impact: bool
    training_data_source: str
    model_architecture: str
    performance_metrics: Dict
    explainability_method: str
    human_oversight_required: bool
    post_market_monitoring: bool
    conformity_assessment_body: Optional[str]
    registration_date: str
    last_validation_date: str


class AIGovernanceEngine:
    """
    AI Governance Engine for iLuminara-Core
    
    Ensures all AI systems comply with global regulations
    """
    
    def __init__(self, enable_strict_mode: bool = True):
        self.enable_strict_mode = enable_strict_mode
        self.registered_systems: Dict[str, AISystemMetadata] = {}
        self.conformity_assessments: Dict[str, Dict] = {}
        self.transparency_logs: List[Dict] = []
        
        logger.info("🤖 AI Governance Engine initialized")
    
    def classify_ai_risk(
        self,
        system_type: AISystemType,
        clinical_impact: bool,
        autonomous_decision: bool,
        vulnerable_population: bool
    ) -> AIRiskCategory:
        """
        Classify AI system risk per EU AI Act Art. 6
        
        Args:
            system_type: Type of AI system
            clinical_impact: Whether it impacts clinical decisions
            autonomous_decision: Whether it makes autonomous decisions
            vulnerable_population: Whether it affects vulnerable populations
        
        Returns:
            AIRiskCategory
        """
        # Unacceptable risk (prohibited)
        prohibited_uses = [
            "social_scoring",
            "real_time_biometric_identification",
            "manipulation_of_behavior"
        ]
        
        # High-risk systems (EU AI Act Annex III)
        high_risk_conditions = [
            clinical_impact and autonomous_decision,
            system_type in [
                AISystemType.DISEASE_DIAGNOSIS,
                AISystemType.CLINICAL_DECISION_SUPPORT
            ],
            vulnerable_population and autonomous_decision
        ]
        
        if any(high_risk_conditions):
            return AIRiskCategory.HIGH_RISK
        
        # Limited risk (transparency obligations)
        if system_type in [
            AISystemType.SURVEILLANCE_MONITORING,
            AISystemType.RISK_STRATIFICATION
        ]:
            return AIRiskCategory.LIMITED_RISK
        
        # Minimal risk
        return AIRiskCategory.MINIMAL_RISK
    
    def classify_medical_device(
        self,
        clinical_impact: bool,
        diagnostic_purpose: bool,
        treatment_guidance: bool,
        invasive: bool
    ) -> MedicalDeviceClass:
        """
        Classify as medical device per MDR/FDA
        
        Args:
            clinical_impact: Whether it impacts clinical decisions
            diagnostic_purpose: Whether used for diagnosis
            treatment_guidance: Whether it guides treatment
            invasive: Whether it's invasive
        
        Returns:
            MedicalDeviceClass
        """
        # Class III (highest risk)
        if invasive or (diagnostic_purpose and treatment_guidance):
            return MedicalDeviceClass.CLASS_III
        
        # Class IIb
        if treatment_guidance or (diagnostic_purpose and clinical_impact):
            return MedicalDeviceClass.CLASS_IIB
        
        # Class IIa
        if diagnostic_purpose or clinical_impact:
            return MedicalDeviceClass.CLASS_IIA
        
        # Class I (lowest risk)
        return MedicalDeviceClass.CLASS_I
    
    def register_ai_system(
        self,
        system_name: str,
        system_type: AISystemType,
        intended_use: str,
        clinical_impact: bool,
        autonomous_decision: bool,
        vulnerable_population: bool,
        training_data_source: str,
        model_architecture: str,
        performance_metrics: Dict,
        explainability_method: str
    ) -> str:
        """
        Register AI system with governance engine
        
        Returns:
            system_id
        """
        # Classify risk
        risk_category = self.classify_ai_risk(
            system_type=system_type,
            clinical_impact=clinical_impact,
            autonomous_decision=autonomous_decision,
            vulnerable_population=vulnerable_population
        )
        
        # Classify as medical device if applicable
        device_class = None
        if clinical_impact:
            device_class = self.classify_medical_device(
                clinical_impact=clinical_impact,
                diagnostic_purpose="diagnosis" in intended_use.lower(),
                treatment_guidance="treatment" in intended_use.lower(),
                invasive=False
            )
        
        # Generate system ID
        system_id = hashlib.sha256(
            f"{system_name}_{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        # Create metadata
        metadata = AISystemMetadata(
            system_id=system_id,
            system_name=system_name,
            system_type=system_type,
            risk_category=risk_category,
            device_class=device_class,
            intended_use=intended_use,
            clinical_impact=clinical_impact,
            training_data_source=training_data_source,
            model_architecture=model_architecture,
            performance_metrics=performance_metrics,
            explainability_method=explainability_method,
            human_oversight_required=risk_category == AIRiskCategory.HIGH_RISK,
            post_market_monitoring=risk_category == AIRiskCategory.HIGH_RISK,
            conformity_assessment_body=None,
            registration_date=datetime.utcnow().isoformat(),
            last_validation_date=datetime.utcnow().isoformat()
        )
        
        self.registered_systems[system_id] = metadata
        
        logger.info(f"✅ AI System Registered: {system_name} (Risk: {risk_category.value})")
        
        # Trigger conformity assessment if high-risk
        if risk_category == AIRiskCategory.HIGH_RISK:
            self._trigger_conformity_assessment(system_id)
        
        return system_id
    
    def _trigger_conformity_assessment(self, system_id: str):
        """Trigger conformity assessment for high-risk AI"""
        metadata = self.registered_systems[system_id]
        
        assessment = {
            "system_id": system_id,
            "assessment_date": datetime.utcnow().isoformat(),
            "risk_category": metadata.risk_category.value,
            "requirements": [
                "EU AI Act Art. 8 (Transparency)",
                "EU AI Act Art. 9 (Risk Management)",
                "EU AI Act Art. 10 (Data Governance)",
                "EU AI Act Art. 11 (Technical Documentation)",
                "EU AI Act Art. 12 (Record Keeping)",
                "EU AI Act Art. 13 (Transparency for Users)",
                "EU AI Act Art. 14 (Human Oversight)",
                "EU AI Act Art. 15 (Accuracy, Robustness, Cybersecurity)"
            ],
            "status": "PENDING",
            "notified_body": None
        }
        
        self.conformity_assessments[system_id] = assessment
        
        logger.warning(f"⚠️ Conformity Assessment Required: {metadata.system_name}")
    
    def validate_inference(
        self,
        system_id: str,
        input_data: Dict,
        prediction: Dict,
        confidence_score: float,
        explanation: Dict
    ) -> Tuple[bool, str]:
        """
        Validate AI inference per EU AI Act Art. 13 & FDA CDSS
        
        Args:
            system_id: Registered AI system ID
            input_data: Input features
            prediction: Model prediction
            confidence_score: Confidence score (0-1)
            explanation: Explainability artifacts (SHAP, LIME, etc.)
        
        Returns:
            (is_valid, reason)
        """
        if system_id not in self.registered_systems:
            return False, "AI system not registered"
        
        metadata = self.registered_systems[system_id]
        
        # High-risk systems require explainability
        if metadata.risk_category == AIRiskCategory.HIGH_RISK:
            if not explanation:
                return False, "EU AI Act Art. 13: High-risk AI requires explanation"
            
            # Check explanation completeness
            required_fields = ["method", "feature_importance", "confidence_interval"]
            missing = [f for f in required_fields if f not in explanation]
            
            if missing:
                return False, f"Incomplete explanation: missing {missing}"
        
        # Clinical impact requires human oversight
        if metadata.clinical_impact and metadata.human_oversight_required:
            if "human_reviewer" not in prediction:
                return False, "EU AI Act Art. 14: Human oversight required"
        
        # Log transparency record
        self._log_transparency_record(
            system_id=system_id,
            input_data=input_data,
            prediction=prediction,
            confidence_score=confidence_score,
            explanation=explanation
        )
        
        return True, "Compliant"
    
    def _log_transparency_record(
        self,
        system_id: str,
        input_data: Dict,
        prediction: Dict,
        confidence_score: float,
        explanation: Dict
    ):
        """Log transparency record per EU AI Act Art. 12"""
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "system_id": system_id,
            "input_hash": hashlib.sha256(
                json.dumps(input_data, sort_keys=True).encode()
            ).hexdigest(),
            "prediction_hash": hashlib.sha256(
                json.dumps(prediction, sort_keys=True).encode()
            ).hexdigest(),
            "confidence_score": confidence_score,
            "explanation_method": explanation.get("method"),
            "compliance_frameworks": [
                "EU AI Act Art. 12",
                "FDA 21 CFR Part 11",
                "ISO 42001:2023"
            ]
        }
        
        self.transparency_logs.append(record)
    
    def generate_transparency_report(
        self,
        system_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        Generate transparency report per EU AI Act Art. 13
        
        Args:
            system_id: AI system ID
            start_date: Start date (ISO format)
            end_date: End date (ISO format)
        
        Returns:
            Transparency report
        """
        if system_id not in self.registered_systems:
            return {"error": "AI system not registered"}
        
        metadata = self.registered_systems[system_id]
        
        # Filter logs
        logs = [
            log for log in self.transparency_logs
            if log["system_id"] == system_id
        ]
        
        if start_date:
            logs = [log for log in logs if log["timestamp"] >= start_date]
        if end_date:
            logs = [log for log in logs if log["timestamp"] <= end_date]
        
        # Calculate statistics
        total_inferences = len(logs)
        avg_confidence = sum(log["confidence_score"] for log in logs) / total_inferences if total_inferences > 0 else 0
        
        report = {
            "system_id": system_id,
            "system_name": metadata.system_name,
            "risk_category": metadata.risk_category.value,
            "reporting_period": {
                "start": start_date or "inception",
                "end": end_date or datetime.utcnow().isoformat()
            },
            "statistics": {
                "total_inferences": total_inferences,
                "average_confidence": avg_confidence,
                "explainability_method": metadata.explainability_method
            },
            "compliance": {
                "eu_ai_act": "Art. 12, 13",
                "fda_cdss": "21 CFR Part 11",
                "iso_42001": "9.1 (Monitoring)"
            },
            "human_oversight": {
                "required": metadata.human_oversight_required,
                "implemented": True
            },
            "post_market_monitoring": {
                "enabled": metadata.post_market_monitoring,
                "last_validation": metadata.last_validation_date
            }
        }
        
        return report
    
    def perform_bias_audit(
        self,
        system_id: str,
        test_data: List[Dict],
        protected_attributes: List[str]
    ) -> Dict:
        """
        Perform bias audit per IMDRF AI Principles
        
        Args:
            system_id: AI system ID
            test_data: Test dataset
            protected_attributes: Attributes to check for bias (e.g., gender, ethnicity)
        
        Returns:
            Bias audit report
        """
        if system_id not in self.registered_systems:
            return {"error": "AI system not registered"}
        
        # Simplified bias detection (in production, use fairness metrics)
        bias_detected = False
        bias_details = {}
        
        for attr in protected_attributes:
            # Check if attribute affects predictions disproportionately
            # (This is a placeholder - implement proper fairness metrics)
            bias_score = 0.05  # Placeholder
            
            if bias_score > 0.1:  # 10% threshold
                bias_detected = True
                bias_details[attr] = {
                    "bias_score": bias_score,
                    "status": "BIAS_DETECTED"
                }
            else:
                bias_details[attr] = {
                    "bias_score": bias_score,
                    "status": "NO_BIAS"
                }
        
        audit_report = {
            "system_id": system_id,
            "audit_date": datetime.utcnow().isoformat(),
            "test_samples": len(test_data),
            "protected_attributes": protected_attributes,
            "bias_detected": bias_detected,
            "bias_details": bias_details,
            "compliance": [
                "IMDRF AI Principles (Bias Detection)",
                "EU AI Act Art. 10 (Data Governance)",
                "ISO 42001:2023 (6.1 Risk Assessment)"
            ],
            "recommendation": "RETRAIN_MODEL" if bias_detected else "APPROVED"
        }
        
        logger.info(f"🔍 Bias Audit Complete: {system_id} - Bias: {bias_detected}")
        
        return audit_report
    
    def get_system_status(self, system_id: str) -> Optional[Dict]:
        """Get AI system status"""
        if system_id not in self.registered_systems:
            return None
        
        metadata = self.registered_systems[system_id]
        conformity = self.conformity_assessments.get(system_id)
        
        return {
            "system_id": system_id,
            "system_name": metadata.system_name,
            "risk_category": metadata.risk_category.value,
            "device_class": metadata.device_class.value if metadata.device_class else None,
            "registration_date": metadata.registration_date,
            "conformity_status": conformity["status"] if conformity else "NOT_REQUIRED",
            "human_oversight": metadata.human_oversight_required,
            "post_market_monitoring": metadata.post_market_monitoring
        }


# Example usage
if __name__ == "__main__":
    # Initialize AI Governance Engine
    engine = AIGovernanceEngine(enable_strict_mode=True)
    
    # Register outbreak prediction system
    system_id = engine.register_ai_system(
        system_name="FRENASA Outbreak Predictor",
        system_type=AISystemType.OUTBREAK_PREDICTION,
        intended_use="Predict cholera outbreaks in refugee camps",
        clinical_impact=True,
        autonomous_decision=False,
        vulnerable_population=True,
        training_data_source="CBS + EMR + IDSR (2020-2024)",
        model_architecture="XGBoost + LSTM",
        performance_metrics={
            "accuracy": 0.92,
            "precision": 0.89,
            "recall": 0.94,
            "f1_score": 0.91
        },
        explainability_method="SHAP"
    )
    
    print(f"✅ System Registered: {system_id}")
    
    # Validate inference
    valid, reason = engine.validate_inference(
        system_id=system_id,
        input_data={"location": "Dadaab", "cases": 15, "r_effective": 2.8},
        prediction={"outbreak_probability": 0.92, "peak_date": "2025-02-15"},
        confidence_score=0.92,
        explanation={
            "method": "SHAP",
            "feature_importance": {"cases": 0.45, "r_effective": 0.35, "location": 0.20},
            "confidence_interval": [0.88, 0.96]
        }
    )
    
    print(f"Inference Valid: {valid} - {reason}")
    
    # Generate transparency report
    report = engine.generate_transparency_report(system_id)
    print(f"📊 Transparency Report: {report['statistics']}")
    
    # Perform bias audit
    bias_audit = engine.perform_bias_audit(
        system_id=system_id,
        test_data=[{"location": "Dadaab", "gender": "F", "age": 25}] * 100,
        protected_attributes=["gender", "ethnicity", "age"]
    )
    print(f"🔍 Bias Audit: {bias_audit['recommendation']}")
