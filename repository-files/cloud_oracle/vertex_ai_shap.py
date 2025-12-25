"""
Vertex AI + SHAP Integration
Right to Explanation for High-Risk Clinical Inferences

Compliance:
- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- HIPAA §164.524 (Right of Access)
- ISO 27001 A.18.1.4 (Privacy and Protection of PII)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum

import numpy as np
import pandas as pd
import shap
from google.cloud import aiplatform
from google.cloud import bigquery

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for AI inferences"""
    LOW = "low"           # Confidence < 0.5
    MEDIUM = "medium"     # Confidence 0.5-0.7
    HIGH = "high"         # Confidence 0.7-0.9
    CRITICAL = "critical" # Confidence > 0.9


class ExplanationMethod(Enum):
    """Explanation methods for model interpretability"""
    SHAP = "shap"
    LIME = "lime"
    FEATURE_IMPORTANCE = "feature_importance"
    INTEGRATED_GRADIENTS = "integrated_gradients"


class VertexAIExplainer:
    """
    Vertex AI model wrapper with SHAP explainability.
    
    Every high-risk clinical inference requires explanation to comply with:
    - EU AI Act §6 (High-Risk AI)
    - GDPR Art. 22 (Right to Explanation)
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        model_name: str = "outbreak-forecaster",
        high_risk_threshold: float = 0.7,
        enable_audit: bool = True
    ):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.high_risk_threshold = high_risk_threshold
        self.enable_audit = enable_audit
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # Initialize BigQuery for audit logging
        if enable_audit:
            self.bq_client = bigquery.Client(project=project_id)
            self.audit_table = f"{project_id}.iluminara_audit.ai_explanations"
        
        # SHAP explainer (initialized on first use)
        self.shap_explainer = None
        
        logger.info(f"🧠 Vertex AI Explainer initialized - Model: {model_name}")
    
    def predict_with_explanation(
        self,
        features: Dict[str, float],
        patient_id: str,
        jurisdiction: str = "GDPR_EU",
        require_explanation: bool = True
    ) -> Dict:
        """
        Make prediction with automatic explanation for high-risk inferences.
        
        Args:
            features: Input features for prediction
            patient_id: Patient identifier
            jurisdiction: Legal jurisdiction (GDPR_EU, KDPA_KE, etc.)
            require_explanation: Force explanation regardless of risk level
        
        Returns:
            Prediction with explanation and compliance metadata
        """
        # Convert features to array
        feature_array = np.array([list(features.values())])
        feature_names = list(features.keys())
        
        # Make prediction (mock for demonstration)
        prediction, confidence = self._predict(feature_array)
        
        # Determine risk level
        risk_level = self._determine_risk_level(confidence)
        
        # Check if explanation is required
        needs_explanation = (
            require_explanation or 
            confidence >= self.high_risk_threshold or
            risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
        )
        
        result = {
            "prediction": prediction,
            "confidence_score": float(confidence),
            "risk_level": risk_level.value,
            "patient_id": patient_id,
            "jurisdiction": jurisdiction,
            "timestamp": datetime.utcnow().isoformat(),
            "model_name": self.model_name,
            "features": features,
            "explanation_required": needs_explanation
        }
        
        # Generate explanation if required
        if needs_explanation:
            explanation = self._generate_shap_explanation(
                feature_array, 
                feature_names,
                prediction
            )
            result["explanation"] = explanation
            
            # Compliance check
            result["compliance"] = self._validate_compliance(
                explanation, 
                jurisdiction
            )
            
            logger.info(
                f"🔍 High-risk inference - Patient: {patient_id}, "
                f"Confidence: {confidence:.2%}, Explanation: GENERATED"
            )
        else:
            result["explanation"] = None
            result["compliance"] = {"status": "not_required"}
            
            logger.info(
                f"✅ Low-risk inference - Patient: {patient_id}, "
                f"Confidence: {confidence:.2%}, Explanation: NOT REQUIRED"
            )
        
        # Audit log
        if self.enable_audit:
            self._log_audit(result)
        
        return result
    
    def _predict(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Make prediction using Vertex AI model.
        
        In production, this would call the actual Vertex AI endpoint.
        For demonstration, we simulate a prediction.
        """
        # Mock prediction (replace with actual Vertex AI call)
        # Example: endpoint.predict(instances=features.tolist())
        
        # Simulate outbreak risk prediction
        risk_score = np.random.uniform(0.3, 0.95)
        
        if risk_score > 0.8:
            prediction = "HIGH_RISK_OUTBREAK"
        elif risk_score > 0.5:
            prediction = "MODERATE_RISK"
        else:
            prediction = "LOW_RISK"
        
        return prediction, risk_score
    
    def _generate_shap_explanation(
        self,
        features: np.ndarray,
        feature_names: List[str],
        prediction: str
    ) -> Dict:
        """
        Generate SHAP explanation for model prediction.
        
        SHAP (SHapley Additive exPlanations) provides:
        - Feature importance
        - Contribution to prediction
        - Baseline comparison
        """
        # Initialize SHAP explainer if not already done
        if self.shap_explainer is None:
            # In production, use actual model
            # self.shap_explainer = shap.Explainer(model)
            
            # Mock explainer for demonstration
            self.shap_explainer = self._create_mock_explainer()
        
        # Calculate SHAP values
        shap_values = self.shap_explainer(features)
        
        # Extract feature contributions
        feature_contributions = {}
        for i, name in enumerate(feature_names):
            feature_contributions[name] = {
                "value": float(features[0][i]),
                "shap_value": float(shap_values.values[0][i]),
                "contribution_pct": float(
                    abs(shap_values.values[0][i]) / 
                    np.sum(np.abs(shap_values.values[0])) * 100
                )
            }
        
        # Sort by contribution
        sorted_features = sorted(
            feature_contributions.items(),
            key=lambda x: abs(x[1]["shap_value"]),
            reverse=True
        )
        
        # Generate explanation
        explanation = {
            "method": ExplanationMethod.SHAP.value,
            "feature_contributions": dict(sorted_features),
            "top_3_features": [f[0] for f in sorted_features[:3]],
            "baseline_value": float(shap_values.base_values[0]),
            "prediction_value": float(
                shap_values.base_values[0] + 
                np.sum(shap_values.values[0])
            ),
            "evidence_chain": self._build_evidence_chain(sorted_features),
            "human_readable": self._generate_human_explanation(
                sorted_features, 
                prediction
            )
        }
        
        return explanation
    
    def _build_evidence_chain(
        self, 
        sorted_features: List[Tuple[str, Dict]]
    ) -> List[str]:
        """Build evidence chain for clinical decision"""
        evidence = []
        
        for feature_name, contribution in sorted_features[:5]:
            if contribution["shap_value"] > 0:
                evidence.append(
                    f"{feature_name} (value: {contribution['value']:.2f}) "
                    f"increases risk by {contribution['contribution_pct']:.1f}%"
                )
            else:
                evidence.append(
                    f"{feature_name} (value: {contribution['value']:.2f}) "
                    f"decreases risk by {contribution['contribution_pct']:.1f}%"
                )
        
        return evidence
    
    def _generate_human_explanation(
        self,
        sorted_features: List[Tuple[str, Dict]],
        prediction: str
    ) -> str:
        """Generate human-readable explanation"""
        top_feature = sorted_features[0]
        
        explanation = (
            f"The model predicts {prediction} primarily based on "
            f"{top_feature[0]} (contributing {top_feature[1]['contribution_pct']:.1f}% "
            f"to the decision). "
        )
        
        if len(sorted_features) > 1:
            second_feature = sorted_features[1]
            explanation += (
                f"The second most important factor is {second_feature[0]} "
                f"({second_feature[1]['contribution_pct']:.1f}% contribution). "
            )
        
        return explanation
    
    def _validate_compliance(
        self, 
        explanation: Dict, 
        jurisdiction: str
    ) -> Dict:
        """
        Validate explanation meets compliance requirements.
        
        Different jurisdictions have different requirements:
        - EU AI Act: High-risk AI requires explanation
        - GDPR Art. 22: Right to explanation for automated decisions
        - HIPAA: Right of access to health information
        """
        compliance = {
            "status": "compliant",
            "jurisdiction": jurisdiction,
            "requirements_met": [],
            "violations": []
        }
        
        # Check EU AI Act §6 requirements
        if jurisdiction in ["GDPR_EU", "EU_AI_ACT"]:
            if explanation["method"] in [ExplanationMethod.SHAP.value]:
                compliance["requirements_met"].append("EU AI Act §6 (Explainability)")
            else:
                compliance["violations"].append("EU AI Act §6 - Insufficient explanation")
                compliance["status"] = "non_compliant"
            
            if "evidence_chain" in explanation:
                compliance["requirements_met"].append("GDPR Art. 22 (Right to Explanation)")
            else:
                compliance["violations"].append("GDPR Art. 22 - Missing evidence chain")
                compliance["status"] = "non_compliant"
        
        # Check HIPAA requirements
        if jurisdiction == "HIPAA_US":
            if "human_readable" in explanation:
                compliance["requirements_met"].append("HIPAA §164.524 (Right of Access)")
            else:
                compliance["violations"].append("HIPAA §164.524 - Missing human explanation")
                compliance["status"] = "non_compliant"
        
        return compliance
    
    def _determine_risk_level(self, confidence: float) -> RiskLevel:
        """Determine risk level based on confidence score"""
        if confidence >= 0.9:
            return RiskLevel.CRITICAL
        elif confidence >= 0.7:
            return RiskLevel.HIGH
        elif confidence >= 0.5:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _create_mock_explainer(self):
        """Create mock SHAP explainer for demonstration"""
        # In production, this would be: shap.Explainer(actual_model)
        
        class MockExplainer:
            def __call__(self, features):
                # Generate mock SHAP values
                shap_values = np.random.randn(*features.shape) * 0.1
                
                class MockExplanation:
                    def __init__(self, values, base_values):
                        self.values = values
                        self.base_values = base_values
                
                return MockExplanation(shap_values, np.array([0.5]))
        
        return MockExplainer()
    
    def _log_audit(self, result: Dict):
        """Log inference to BigQuery audit table"""
        try:
            # Prepare audit record
            audit_record = {
                "timestamp": result["timestamp"],
                "patient_id": result["patient_id"],
                "model_name": result["model_name"],
                "prediction": result["prediction"],
                "confidence_score": result["confidence_score"],
                "risk_level": result["risk_level"],
                "explanation_required": result["explanation_required"],
                "jurisdiction": result["jurisdiction"],
                "compliance_status": result.get("compliance", {}).get("status"),
                "features": json.dumps(result["features"]),
                "explanation": json.dumps(result.get("explanation"))
            }
            
            # Insert to BigQuery
            errors = self.bq_client.insert_rows_json(
                self.audit_table, 
                [audit_record]
            )
            
            if errors:
                logger.error(f"❌ Audit log failed: {errors}")
            else:
                logger.debug(f"✅ Audit logged - Patient: {result['patient_id']}")
        
        except Exception as e:
            logger.error(f"❌ Audit logging error: {e}")


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-core",
        location="us-central1",
        model_name="outbreak-forecaster",
        high_risk_threshold=0.7
    )
    
    # Make prediction with explanation
    features = {
        "fever_cases": 45,
        "diarrhea_cases": 32,
        "population_density": 1200,
        "water_quality_index": 0.3,
        "sanitation_score": 0.4,
        "rainfall_mm": 120,
        "temperature_celsius": 28
    }
    
    result = explainer.predict_with_explanation(
        features=features,
        patient_id="PAT_12345",
        jurisdiction="GDPR_EU"
    )
    
    print(json.dumps(result, indent=2))
    
    # Output includes:
    # - Prediction
    # - Confidence score
    # - Risk level
    # - SHAP explanation
    # - Feature contributions
    # - Evidence chain
    # - Human-readable explanation
    # - Compliance validation
