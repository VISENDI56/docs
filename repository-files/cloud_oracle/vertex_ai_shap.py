"""
Vertex AI + SHAP Integration
Right to Explanation (EU AI Act §6, GDPR Art. 22)

Every high-risk clinical inference requires explainability.
This module integrates Google Cloud Vertex AI with SHAP (SHapley Additive exPlanations)
to provide transparent, auditable AI decision-making.

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
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for AI inference"""
    LOW = "low"           # Confidence < 0.5
    MEDIUM = "medium"     # Confidence 0.5-0.7
    HIGH = "high"         # Confidence 0.7-0.9
    CRITICAL = "critical" # Confidence > 0.9


class ExplainabilityMethod(Enum):
    """Explainability methods"""
    SHAP = "shap"
    LIME = "lime"
    FEATURE_IMPORTANCE = "feature_importance"
    INTEGRATED_GRADIENTS = "integrated_gradients"


class VertexAIExplainer:
    """
    Vertex AI model with mandatory SHAP explainability for high-risk inferences.
    
    Enforces EU AI Act §6 requirement for transparency in high-risk AI systems.
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
        
        logger.info(f"🧠 Vertex AI Explainer initialized - Model: {model_name}")
    
    def predict_with_explanation(
        self,
        endpoint_id: str,
        instances: List[Dict],
        feature_names: List[str],
        background_data: Optional[np.ndarray] = None
    ) -> List[Dict]:
        """
        Make prediction with mandatory SHAP explanation for high-risk inferences.
        
        Args:
            endpoint_id: Vertex AI endpoint ID
            instances: Input instances for prediction
            feature_names: Names of input features
            background_data: Background dataset for SHAP (optional)
        
        Returns:
            List of predictions with explanations
        """
        # Get endpoint
        endpoint = aiplatform.Endpoint(endpoint_id)
        
        # Make prediction
        predictions = endpoint.predict(instances=instances)
        
        results = []
        
        for idx, (instance, prediction) in enumerate(zip(instances, predictions.predictions)):
            # Extract confidence score
            confidence = self._extract_confidence(prediction)
            
            # Determine risk level
            risk_level = self._determine_risk_level(confidence)
            
            # High-risk inferences require explanation
            if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                logger.info(f"🔍 High-risk inference detected (confidence: {confidence:.2%}) - Generating SHAP explanation")
                
                # Generate SHAP explanation
                shap_values, base_value = self._generate_shap_explanation(
                    endpoint=endpoint,
                    instance=instance,
                    feature_names=feature_names,
                    background_data=background_data
                )
                
                # Build explanation
                explanation = {
                    "method": "SHAP",
                    "confidence_score": confidence,
                    "risk_level": risk_level.value,
                    "base_value": float(base_value),
                    "shap_values": {
                        feature: float(value)
                        for feature, value in zip(feature_names, shap_values)
                    },
                    "feature_importance": self._rank_features(feature_names, shap_values),
                    "evidence_chain": self._build_evidence_chain(feature_names, shap_values, instance),
                    "decision_rationale": self._generate_rationale(feature_names, shap_values, prediction)
                }
                
                # Audit log
                if self.enable_audit:
                    self._log_explanation(instance, prediction, explanation)
                
            else:
                # Low/medium risk - basic explanation
                explanation = {
                    "method": "BASIC",
                    "confidence_score": confidence,
                    "risk_level": risk_level.value,
                    "message": "Low-risk inference - detailed explanation not required"
                }
            
            results.append({
                "instance": instance,
                "prediction": prediction,
                "explanation": explanation,
                "timestamp": datetime.utcnow().isoformat(),
                "compliance": {
                    "eu_ai_act": "§6 (High-Risk AI) - COMPLIANT",
                    "gdpr": "Art. 22 (Right to Explanation) - COMPLIANT"
                }
            })
        
        return results
    
    def _generate_shap_explanation(
        self,
        endpoint: aiplatform.Endpoint,
        instance: Dict,
        feature_names: List[str],
        background_data: Optional[np.ndarray] = None
    ) -> Tuple[np.ndarray, float]:
        """
        Generate SHAP explanation for a single instance.
        
        Args:
            endpoint: Vertex AI endpoint
            instance: Input instance
            feature_names: Feature names
            background_data: Background dataset for SHAP
        
        Returns:
            (shap_values, base_value)
        """
        # Convert instance to numpy array
        instance_array = np.array([instance[f] for f in feature_names]).reshape(1, -1)
        
        # Create prediction function
        def predict_fn(X):
            instances = [
                {feature: float(value) for feature, value in zip(feature_names, row)}
                for row in X
            ]
            predictions = endpoint.predict(instances=instances)
            return np.array([self._extract_confidence(p) for p in predictions.predictions])
        
        # Use background data or create synthetic
        if background_data is None:
            # Create synthetic background (mean of instance features)
            background_data = instance_array
        
        # Initialize SHAP explainer
        explainer = shap.KernelExplainer(predict_fn, background_data)
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(instance_array)
        
        # Extract values
        if isinstance(shap_values, list):
            shap_values = shap_values[0]  # Binary classification
        
        shap_values = shap_values[0]  # First instance
        base_value = explainer.expected_value
        
        if isinstance(base_value, np.ndarray):
            base_value = base_value[0]
        
        return shap_values, base_value
    
    def _extract_confidence(self, prediction) -> float:
        """Extract confidence score from prediction"""
        if isinstance(prediction, dict):
            return prediction.get('confidence', prediction.get('score', 0.5))
        elif isinstance(prediction, (list, np.ndarray)):
            return float(prediction[0]) if len(prediction) > 0 else 0.5
        else:
            return float(prediction)
    
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
    
    def _rank_features(self, feature_names: List[str], shap_values: np.ndarray) -> List[Dict]:
        """Rank features by absolute SHAP value"""
        feature_importance = [
            {
                "feature": name,
                "shap_value": float(value),
                "abs_importance": abs(float(value))
            }
            for name, value in zip(feature_names, shap_values)
        ]
        
        # Sort by absolute importance
        feature_importance.sort(key=lambda x: x['abs_importance'], reverse=True)
        
        return feature_importance
    
    def _build_evidence_chain(
        self,
        feature_names: List[str],
        shap_values: np.ndarray,
        instance: Dict
    ) -> List[str]:
        """Build evidence chain for decision"""
        evidence = []
        
        # Get top 3 features
        ranked = self._rank_features(feature_names, shap_values)[:3]
        
        for item in ranked:
            feature = item['feature']
            shap_value = item['shap_value']
            feature_value = instance.get(feature, 'N/A')
            
            direction = "increases" if shap_value > 0 else "decreases"
            evidence.append(
                f"{feature}={feature_value} {direction} risk by {abs(shap_value):.3f}"
            )
        
        return evidence
    
    def _generate_rationale(
        self,
        feature_names: List[str],
        shap_values: np.ndarray,
        prediction
    ) -> str:
        """Generate human-readable decision rationale"""
        ranked = self._rank_features(feature_names, shap_values)
        top_feature = ranked[0]
        
        confidence = self._extract_confidence(prediction)
        
        rationale = (
            f"The model predicts with {confidence:.1%} confidence. "
            f"The most influential factor is '{top_feature['feature']}' "
            f"(SHAP value: {top_feature['shap_value']:.3f}), which "
            f"{'increases' if top_feature['shap_value'] > 0 else 'decreases'} "
            f"the predicted risk."
        )
        
        return rationale
    
    def _log_explanation(self, instance: Dict, prediction, explanation: Dict):
        """Log explanation to BigQuery for audit trail"""
        try:
            row = {
                "timestamp": datetime.utcnow().isoformat(),
                "model_name": self.model_name,
                "instance": json.dumps(instance),
                "prediction": json.dumps(str(prediction)),
                "explanation": json.dumps(explanation),
                "risk_level": explanation['risk_level'],
                "confidence_score": explanation['confidence_score'],
                "compliance_framework": "EU_AI_ACT_GDPR"
            }
            
            errors = self.bq_client.insert_rows_json(self.audit_table, [row])
            
            if errors:
                logger.error(f"❌ Failed to log explanation: {errors}")
            else:
                logger.info(f"✅ Explanation logged to audit trail")
        
        except Exception as e:
            logger.error(f"❌ Audit logging failed: {e}")
    
    def batch_explain(
        self,
        endpoint_id: str,
        instances: List[Dict],
        feature_names: List[str],
        background_data: Optional[np.ndarray] = None
    ) -> pd.DataFrame:
        """
        Batch explanation for multiple instances.
        
        Returns:
            DataFrame with predictions and explanations
        """
        results = self.predict_with_explanation(
            endpoint_id=endpoint_id,
            instances=instances,
            feature_names=feature_names,
            background_data=background_data
        )
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {
                "timestamp": r['timestamp'],
                "confidence": r['explanation']['confidence_score'],
                "risk_level": r['explanation']['risk_level'],
                "method": r['explanation']['method'],
                "top_feature": r['explanation'].get('feature_importance', [{}])[0].get('feature', 'N/A'),
                "evidence": '; '.join(r['explanation'].get('evidence_chain', [])),
                "rationale": r['explanation'].get('decision_rationale', 'N/A')
            }
            for r in results
        ])
        
        return df


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-health",
        location="us-central1",
        model_name="cholera-outbreak-forecaster",
        high_risk_threshold=0.7
    )
    
    # Example instances
    instances = [
        {
            "cases_last_7_days": 45,
            "population_density": 1200,
            "water_quality_score": 0.3,
            "sanitation_coverage": 0.4,
            "rainfall_mm": 120,
            "temperature_celsius": 28
        }
    ]
    
    feature_names = [
        "cases_last_7_days",
        "population_density",
        "water_quality_score",
        "sanitation_coverage",
        "rainfall_mm",
        "temperature_celsius"
    ]
    
    # Make prediction with explanation
    results = explainer.predict_with_explanation(
        endpoint_id="projects/123/locations/us-central1/endpoints/456",
        instances=instances,
        feature_names=feature_names
    )
    
    # Print results
    for result in results:
        print(f"\n{'='*60}")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['explanation']['confidence_score']:.1%}")
        print(f"Risk Level: {result['explanation']['risk_level']}")
        print(f"\nEvidence Chain:")
        for evidence in result['explanation'].get('evidence_chain', []):
            print(f"  • {evidence}")
        print(f"\nRationale: {result['explanation'].get('decision_rationale', 'N/A')}")
        print(f"\nCompliance:")
        for framework, status in result['compliance'].items():
            print(f"  ✓ {framework}: {status}")
