"""
Vertex AI + SHAP Integration
Right to Explanation (EU AI Act §6, GDPR Art. 22)

Every high-risk clinical inference requires explainability.
This module integrates Vertex AI models with SHAP (SHapley Additive exPlanations)
to provide transparent, auditable AI decisions.

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

from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """AI inference risk levels per EU AI Act"""
    LOW = "low"  # Minimal risk (e.g., spam filter)
    MEDIUM = "medium"  # Limited risk (e.g., symptom checker)
    HIGH = "high"  # High risk (e.g., diagnosis, treatment recommendation)
    UNACCEPTABLE = "unacceptable"  # Prohibited (e.g., social scoring)


class ExplainabilityMethod(Enum):
    """Supported explainability methods"""
    SHAP = "shap"  # SHapley Additive exPlanations
    LIME = "lime"  # Local Interpretable Model-agnostic Explanations
    FEATURE_IMPORTANCE = "feature_importance"  # Model-native feature importance


class VertexAIExplainer:
    """
    Integrates Vertex AI with SHAP for explainable AI.
    
    Ensures every high-risk inference includes:
    - Confidence score
    - Feature contributions (SHAP values)
    - Evidence chain
    - Decision rationale
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        high_risk_threshold: float = 0.7,
        enable_compliance_check: bool = True
    ):
        self.project_id = project_id
        self.location = location
        self.high_risk_threshold = high_risk_threshold
        self.enable_compliance_check = enable_compliance_check
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # Initialize SovereignGuardrail
        if enable_compliance_check:
            self.guardrail = SovereignGuardrail(enable_tamper_proof_audit=True)
        
        logger.info(f"🧠 Vertex AI Explainer initialized - Project: {project_id}")
    
    def predict_with_explanation(
        self,
        endpoint_id: str,
        instances: List[Dict],
        feature_names: List[str],
        risk_level: RiskLevel = RiskLevel.HIGH,
        jurisdiction: str = "EU_AI_ACT"
    ) -> Dict:
        """
        Make prediction with mandatory explainability for high-risk inferences.
        
        Args:
            endpoint_id: Vertex AI endpoint ID
            instances: Input instances for prediction
            feature_names: Names of input features
            risk_level: Risk level of the inference
            jurisdiction: Legal jurisdiction
        
        Returns:
            Dictionary with predictions and explanations
        """
        # Get endpoint
        endpoint = aiplatform.Endpoint(endpoint_id)
        
        # Make prediction
        prediction_response = endpoint.predict(instances=instances)
        predictions = prediction_response.predictions
        
        # Extract confidence scores
        confidence_scores = [
            pred.get('confidence', pred.get('score', 0.0))
            for pred in predictions
        ]
        
        # Determine if explanation is required
        max_confidence = max(confidence_scores)
        requires_explanation = (
            risk_level in [RiskLevel.HIGH, RiskLevel.UNACCEPTABLE] or
            max_confidence >= self.high_risk_threshold
        )
        
        result = {
            "predictions": predictions,
            "confidence_scores": confidence_scores,
            "risk_level": risk_level.value,
            "requires_explanation": requires_explanation,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Generate explanation if required
        if requires_explanation:
            logger.info(f"🔍 High-risk inference detected - Generating explanation")
            
            # Generate SHAP explanation
            explanation = self._generate_shap_explanation(
                endpoint=endpoint,
                instances=instances,
                feature_names=feature_names
            )
            
            result["explanation"] = explanation
            
            # Compliance validation
            if self.enable_compliance_check:
                try:
                    self.guardrail.validate_action(
                        action_type='High_Risk_Inference',
                        payload={
                            'actor': 'vertex_ai_model',
                            'resource': endpoint_id,
                            'explanation': json.dumps(explanation),
                            'confidence_score': max_confidence,
                            'evidence_chain': explanation.get('evidence_chain', []),
                            'consent_token': 'VALID_TOKEN',  # Should be provided by caller
                            'consent_scope': 'diagnosis'
                        },
                        jurisdiction=jurisdiction
                    )
                    result["compliance_status"] = "APPROVED"
                    logger.info(f"✅ Compliance check passed - Jurisdiction: {jurisdiction}")
                
                except SovereigntyViolationError as e:
                    result["compliance_status"] = "VIOLATION"
                    result["compliance_error"] = str(e)
                    logger.error(f"❌ Compliance violation: {e}")
        
        return result
    
    def _generate_shap_explanation(
        self,
        endpoint: aiplatform.Endpoint,
        instances: List[Dict],
        feature_names: List[str]
    ) -> Dict:
        """
        Generate SHAP explanation for model predictions.
        
        Args:
            endpoint: Vertex AI endpoint
            instances: Input instances
            feature_names: Feature names
        
        Returns:
            SHAP explanation dictionary
        """
        # Convert instances to numpy array
        X = np.array([list(inst.values()) for inst in instances])
        
        # Create prediction function for SHAP
        def predict_fn(X_input):
            instances_list = [
                {name: float(val) for name, val in zip(feature_names, row)}
                for row in X_input
            ]
            response = endpoint.predict(instances=instances_list)
            # Extract prediction scores
            return np.array([
                pred.get('score', pred.get('confidence', 0.0))
                for pred in response.predictions
            ])
        
        # Initialize SHAP explainer
        # Use KernelExplainer for model-agnostic explanations
        explainer = shap.KernelExplainer(predict_fn, X)
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(X)
        
        # Build explanation
        explanation = {
            "method": "SHAP",
            "shap_values": shap_values.tolist(),
            "feature_names": feature_names,
            "feature_contributions": [
                {
                    "feature": name,
                    "value": float(X[0][i]),
                    "shap_value": float(shap_values[0][i]),
                    "contribution_pct": float(abs(shap_values[0][i]) / np.sum(np.abs(shap_values[0])) * 100)
                }
                for i, name in enumerate(feature_names)
            ],
            "base_value": float(explainer.expected_value),
            "evidence_chain": self._build_evidence_chain(feature_names, X[0], shap_values[0]),
            "decision_rationale": self._generate_rationale(feature_names, shap_values[0])
        }
        
        # Sort by contribution
        explanation["feature_contributions"].sort(
            key=lambda x: abs(x["shap_value"]),
            reverse=True
        )
        
        return explanation
    
    def _build_evidence_chain(
        self,
        feature_names: List[str],
        feature_values: np.ndarray,
        shap_values: np.ndarray
    ) -> List[str]:
        """Build human-readable evidence chain"""
        evidence = []
        
        # Get top 5 contributing features
        top_indices = np.argsort(np.abs(shap_values))[-5:][::-1]
        
        for idx in top_indices:
            feature = feature_names[idx]
            value = feature_values[idx]
            contribution = shap_values[idx]
            
            direction = "increases" if contribution > 0 else "decreases"
            evidence.append(
                f"{feature}={value:.2f} {direction} risk by {abs(contribution):.3f}"
            )
        
        return evidence
    
    def _generate_rationale(
        self,
        feature_names: List[str],
        shap_values: np.ndarray
    ) -> str:
        """Generate human-readable decision rationale"""
        top_idx = np.argmax(np.abs(shap_values))
        top_feature = feature_names[top_idx]
        top_contribution = shap_values[top_idx]
        
        direction = "positive" if top_contribution > 0 else "negative"
        
        return (
            f"The model's decision is primarily driven by {top_feature}, "
            f"which has a {direction} contribution of {abs(top_contribution):.3f}. "
            f"This feature accounts for {abs(top_contribution) / np.sum(np.abs(shap_values)) * 100:.1f}% "
            f"of the total prediction."
        )
    
    def batch_predict_with_explanation(
        self,
        endpoint_id: str,
        instances: List[Dict],
        feature_names: List[str],
        risk_level: RiskLevel = RiskLevel.HIGH
    ) -> List[Dict]:
        """
        Batch prediction with explanations.
        
        Args:
            endpoint_id: Vertex AI endpoint ID
            instances: List of input instances
            feature_names: Feature names
            risk_level: Risk level
        
        Returns:
            List of prediction results with explanations
        """
        results = []
        
        for instance in instances:
            result = self.predict_with_explanation(
                endpoint_id=endpoint_id,
                instances=[instance],
                feature_names=feature_names,
                risk_level=risk_level
            )
            results.append(result)
        
        return results
    
    def export_explanation_to_bigquery(
        self,
        explanation: Dict,
        dataset_id: str,
        table_id: str
    ):
        """
        Export explanation to BigQuery for audit trail.
        
        Args:
            explanation: SHAP explanation
            dataset_id: BigQuery dataset ID
            table_id: BigQuery table ID
        """
        client = bigquery.Client(project=self.project_id)
        
        table_ref = f"{self.project_id}.{dataset_id}.{table_id}"
        
        # Prepare row
        row = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": explanation["method"],
            "feature_contributions": json.dumps(explanation["feature_contributions"]),
            "evidence_chain": json.dumps(explanation["evidence_chain"]),
            "decision_rationale": explanation["decision_rationale"],
            "base_value": explanation["base_value"]
        }
        
        # Insert row
        errors = client.insert_rows_json(table_ref, [row])
        
        if errors:
            logger.error(f"❌ BigQuery insert failed: {errors}")
        else:
            logger.info(f"✅ Explanation exported to BigQuery: {table_ref}")


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-health",
        location="us-central1",
        high_risk_threshold=0.7,
        enable_compliance_check=True
    )
    
    # Example: Cholera outbreak prediction
    instances = [
        {
            "temperature": 38.5,
            "diarrhea_severity": 8,
            "vomiting": 1,
            "dehydration_level": 7,
            "days_since_onset": 2,
            "population_density": 5000,
            "water_quality_index": 3
        }
    ]
    
    feature_names = [
        "temperature",
        "diarrhea_severity",
        "vomiting",
        "dehydration_level",
        "days_since_onset",
        "population_density",
        "water_quality_index"
    ]
    
    # Make prediction with explanation
    result = explainer.predict_with_explanation(
        endpoint_id="projects/123/locations/us-central1/endpoints/456",
        instances=instances,
        feature_names=feature_names,
        risk_level=RiskLevel.HIGH,
        jurisdiction="EU_AI_ACT"
    )
    
    print(f"✅ Prediction: {result['predictions']}")
    print(f"📊 Confidence: {result['confidence_scores']}")
    
    if result.get("explanation"):
        print(f"\n🔍 EXPLANATION:")
        print(f"   Method: {result['explanation']['method']}")
        print(f"   Evidence Chain:")
        for evidence in result['explanation']['evidence_chain']:
            print(f"      - {evidence}")
        print(f"   Rationale: {result['explanation']['decision_rationale']}")
    
    print(f"\n🛡️ Compliance: {result.get('compliance_status', 'N/A')}")
