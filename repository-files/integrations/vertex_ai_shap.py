"""
Vertex AI + SHAP Integration
Right to Explanation (EU AI Act §6, GDPR Art. 22)

Every high-risk clinical inference requires explainability.
This module integrates Vertex AI models with SHAP (SHapley Additive exPlanations)
to provide transparent, auditable AI decisions.

Compliance:
- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- HIPAA §164.312(b) (Audit Controls)
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
    """AI inference risk levels"""
    LOW = "low"           # Confidence < 0.5
    MEDIUM = "medium"     # Confidence 0.5-0.7
    HIGH = "high"         # Confidence 0.7-0.9
    CRITICAL = "critical" # Confidence > 0.9


class ExplainabilityMethod(Enum):
    """Supported explainability methods"""
    SHAP = "shap"
    LIME = "lime"
    FEATURE_IMPORTANCE = "feature_importance"


class VertexAIExplainer:
    """
    Integrates Vertex AI with SHAP for explainable AI.
    
    Ensures every high-risk inference includes:
    - Confidence score
    - SHAP values (feature contributions)
    - Evidence chain
    - Decision rationale
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        high_risk_threshold: float = 0.7,
        enable_audit: bool = True
    ):
        self.project_id = project_id
        self.location = location
        self.high_risk_threshold = high_risk_threshold
        self.enable_audit = enable_audit
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # Initialize BigQuery for audit logging
        if enable_audit:
            self.bq_client = bigquery.Client(project=project_id)
            self.audit_table = f"{project_id}.iluminara_audit.ai_explanations"
        
        logger.info(f"✅ Vertex AI Explainer initialized - Project: {project_id}")
    
    def predict_with_explanation(
        self,
        endpoint_id: str,
        instances: List[Dict],
        feature_names: List[str],
        patient_id: Optional[str] = None,
        jurisdiction: str = "GDPR_EU"
    ) -> Dict:
        """
        Make prediction with automatic SHAP explanation for high-risk inferences.
        
        Args:
            endpoint_id: Vertex AI endpoint ID
            instances: Input instances for prediction
            feature_names: Names of input features
            patient_id: Patient identifier (for audit)
            jurisdiction: Legal jurisdiction
        
        Returns:
            {
                "prediction": prediction_value,
                "confidence": confidence_score,
                "risk_level": "high" | "medium" | "low",
                "explanation": {
                    "shap_values": [...],
                    "feature_contributions": {...},
                    "evidence_chain": [...],
                    "decision_rationale": "..."
                },
                "compliance": {
                    "requires_explanation": True/False,
                    "frameworks": ["EU AI Act §6", "GDPR Art. 22"]
                }
            }
        """
        # Get endpoint
        endpoint = aiplatform.Endpoint(endpoint_id)
        
        # Make prediction
        predictions = endpoint.predict(instances=instances)
        
        # Extract prediction and confidence
        prediction = predictions.predictions[0]
        confidence = float(prediction.get("confidence", 0.0))
        
        # Determine risk level
        risk_level = self._determine_risk_level(confidence)
        
        # Check if explanation is required
        requires_explanation = confidence >= self.high_risk_threshold
        
        result = {
            "prediction": prediction,
            "confidence": confidence,
            "risk_level": risk_level.value,
            "timestamp": datetime.utcnow().isoformat(),
            "patient_id": patient_id,
            "jurisdiction": jurisdiction
        }
        
        # Generate explanation for high-risk inferences
        if requires_explanation:
            logger.info(f"🔍 High-risk inference detected (confidence: {confidence:.2%}) - Generating SHAP explanation")
            
            explanation = self._generate_shap_explanation(
                endpoint=endpoint,
                instances=instances,
                feature_names=feature_names,
                prediction=prediction
            )
            
            result["explanation"] = explanation
            result["compliance"] = {
                "requires_explanation": True,
                "frameworks": ["EU AI Act §6", "GDPR Art. 22"],
                "explanation_method": "SHAP",
                "explainability_score": self._calculate_explainability_score(explanation)
            }
        else:
            result["compliance"] = {
                "requires_explanation": False,
                "frameworks": [],
                "reason": f"Confidence {confidence:.2%} below threshold {self.high_risk_threshold:.2%}"
            }
        
        # Audit log
        if self.enable_audit:
            self._log_audit(result)
        
        return result
    
    def _generate_shap_explanation(
        self,
        endpoint: aiplatform.Endpoint,
        instances: List[Dict],
        feature_names: List[str],
        prediction: Dict
    ) -> Dict:
        """
        Generate SHAP explanation for a prediction.
        
        Returns:
            {
                "shap_values": [...],
                "feature_contributions": {...},
                "evidence_chain": [...],
                "decision_rationale": "..."
            }
        """
        # Convert instances to numpy array
        X = np.array([list(inst.values()) for inst in instances])
        
        # Create prediction function wrapper
        def predict_fn(X):
            instances_list = [
                {feature_names[i]: float(X[j, i]) for i in range(len(feature_names))}
                for j in range(X.shape[0])
            ]
            predictions = endpoint.predict(instances=instances_list)
            return np.array([p.get("confidence", 0.0) for p in predictions.predictions])
        
        # Initialize SHAP explainer
        explainer = shap.KernelExplainer(predict_fn, X)
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(X)
        
        # Get feature contributions
        feature_contributions = {
            feature_names[i]: float(shap_values[0][i])
            for i in range(len(feature_names))
        }
        
        # Sort by absolute contribution
        sorted_contributions = sorted(
            feature_contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Build evidence chain (top 5 features)
        evidence_chain = [
            {
                "feature": feature,
                "contribution": contribution,
                "impact": "positive" if contribution > 0 else "negative"
            }
            for feature, contribution in sorted_contributions[:5]
        ]
        
        # Generate decision rationale
        top_feature = sorted_contributions[0]
        decision_rationale = self._generate_rationale(
            prediction=prediction,
            top_feature=top_feature,
            evidence_chain=evidence_chain
        )
        
        return {
            "shap_values": shap_values.tolist(),
            "feature_contributions": feature_contributions,
            "evidence_chain": evidence_chain,
            "decision_rationale": decision_rationale,
            "base_value": float(explainer.expected_value),
            "method": "SHAP (Kernel Explainer)"
        }
    
    def _generate_rationale(
        self,
        prediction: Dict,
        top_feature: Tuple[str, float],
        evidence_chain: List[Dict]
    ) -> str:
        """Generate human-readable decision rationale"""
        feature_name, contribution = top_feature
        
        rationale = f"The model predicts {prediction.get('label', 'outcome')} with "
        rationale += f"{prediction.get('confidence', 0.0):.1%} confidence. "
        rationale += f"The primary factor is '{feature_name}' (contribution: {contribution:.3f}). "
        
        if len(evidence_chain) > 1:
            rationale += "Additional contributing factors: "
            rationale += ", ".join([
                f"'{e['feature']}' ({e['contribution']:.3f})"
                for e in evidence_chain[1:3]
            ])
        
        return rationale
    
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
    
    def _calculate_explainability_score(self, explanation: Dict) -> float:
        """
        Calculate explainability score (0-1).
        
        Higher score = more explainable decision
        """
        # Check if all required fields are present
        required_fields = ["shap_values", "feature_contributions", "evidence_chain", "decision_rationale"]
        completeness = sum(1 for field in required_fields if field in explanation) / len(required_fields)
        
        # Check evidence chain quality
        evidence_quality = min(len(explanation.get("evidence_chain", [])) / 5.0, 1.0)
        
        # Check feature contribution diversity (not dominated by single feature)
        contributions = list(explanation.get("feature_contributions", {}).values())
        if contributions:
            max_contribution = max(abs(c) for c in contributions)
            total_contribution = sum(abs(c) for c in contributions)
            diversity = 1.0 - (max_contribution / total_contribution if total_contribution > 0 else 0)
        else:
            diversity = 0.0
        
        # Weighted average
        score = (completeness * 0.4) + (evidence_quality * 0.3) + (diversity * 0.3)
        
        return round(score, 3)
    
    def _log_audit(self, result: Dict):
        """Log AI explanation to BigQuery for audit trail"""
        try:
            audit_record = {
                "timestamp": result["timestamp"],
                "patient_id": result.get("patient_id"),
                "jurisdiction": result["jurisdiction"],
                "confidence": result["confidence"],
                "risk_level": result["risk_level"],
                "requires_explanation": result["compliance"]["requires_explanation"],
                "explanation_method": result["compliance"].get("explanation_method"),
                "explainability_score": result["compliance"].get("explainability_score"),
                "frameworks": json.dumps(result["compliance"]["frameworks"]),
                "prediction": json.dumps(result["prediction"]),
                "explanation": json.dumps(result.get("explanation", {}))
            }
            
            # Insert into BigQuery
            errors = self.bq_client.insert_rows_json(self.audit_table, [audit_record])
            
            if errors:
                logger.error(f"❌ Audit log failed: {errors}")
            else:
                logger.info(f"✅ Audit logged - Patient: {result.get('patient_id')}")
        
        except Exception as e:
            logger.error(f"❌ Audit logging error: {e}")
    
    def batch_explain(
        self,
        endpoint_id: str,
        instances: List[Dict],
        feature_names: List[str],
        jurisdiction: str = "GDPR_EU"
    ) -> List[Dict]:
        """
        Batch prediction with explanations.
        
        Optimized for processing multiple instances efficiently.
        """
        results = []
        
        for i, instance in enumerate(instances):
            patient_id = instance.get("patient_id", f"BATCH_{i}")
            
            result = self.predict_with_explanation(
                endpoint_id=endpoint_id,
                instances=[instance],
                feature_names=feature_names,
                patient_id=patient_id,
                jurisdiction=jurisdiction
            )
            
            results.append(result)
        
        logger.info(f"✅ Batch explanation complete - {len(results)} instances processed")
        
        return results


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-health",
        location="us-central1",
        high_risk_threshold=0.7,
        enable_audit=True
    )
    
    # Example: Cholera outbreak prediction
    instances = [{
        "fever": 1,
        "diarrhea": 1,
        "vomiting": 1,
        "dehydration": 1,
        "location_risk": 0.8,
        "recent_cases": 15,
        "water_quality": 0.3
    }]
    
    feature_names = [
        "fever", "diarrhea", "vomiting", "dehydration",
        "location_risk", "recent_cases", "water_quality"
    ]
    
    # Make prediction with explanation
    result = explainer.predict_with_explanation(
        endpoint_id="projects/123/locations/us-central1/endpoints/456",
        instances=instances,
        feature_names=feature_names,
        patient_id="PAT_12345",
        jurisdiction="KDPA_KE"
    )
    
    print(f"✅ Prediction: {result['prediction']}")
    print(f"📊 Confidence: {result['confidence']:.2%}")
    print(f"⚠️  Risk Level: {result['risk_level']}")
    
    if result['compliance']['requires_explanation']:
        print(f"🔍 Explanation required: {result['compliance']['frameworks']}")
        print(f"📝 Rationale: {result['explanation']['decision_rationale']}")
        print(f"📈 Explainability Score: {result['compliance']['explainability_score']}")
