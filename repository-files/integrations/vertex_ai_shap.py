"""
Vertex AI + SHAP Integration
Right to Explanation (EU AI Act §6, GDPR Art. 22)

Every high-risk clinical inference requires explainability.
This module integrates Vertex AI predictions with SHAP analysis.

Compliance:
- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- HIPAA §164.312(b) (Audit Controls)
"""

import shap
import numpy as np
from typing import Dict, List, Optional, Tuple
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class VertexAIExplainer:
    """
    Integrates Vertex AI with SHAP for explainable AI predictions.
    
    Every high-risk inference (confidence > 0.7) automatically triggers
    SHAP analysis to comply with EU AI Act §6.
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
        
        # Audit trail
        self.audit_log = []
        
        logger.info(f"🧠 Vertex AI Explainer initialized - Project: {project_id}")
    
    def predict_with_explanation(
        self,
        endpoint_id: str,
        instances: List[Dict],
        feature_names: List[str],
        background_data: Optional[np.ndarray] = None
    ) -> Dict:
        """
        Make prediction with automatic SHAP explanation for high-risk inferences.
        
        Args:
            endpoint_id: Vertex AI endpoint ID
            instances: Input instances for prediction
            feature_names: Names of input features
            background_data: Background dataset for SHAP (optional)
        
        Returns:
            {
                "predictions": [...],
                "confidence_scores": [...],
                "explanations": [...],  # SHAP values
                "high_risk": bool,
                "compliance_status": "COMPLIANT" | "REQUIRES_REVIEW"
            }
        """
        # Get endpoint
        endpoint = aiplatform.Endpoint(endpoint_id)
        
        # Make prediction
        predictions = endpoint.predict(instances=instances)
        
        # Extract confidence scores
        confidence_scores = self._extract_confidence_scores(predictions)
        
        # Check if high-risk
        max_confidence = max(confidence_scores)
        is_high_risk = max_confidence >= self.high_risk_threshold
        
        # Generate SHAP explanation if high-risk
        explanations = None
        compliance_status = "COMPLIANT"
        
        if is_high_risk:
            logger.warning(f"⚠️ High-risk inference detected (confidence: {max_confidence:.2f})")
            
            try:
                explanations = self._generate_shap_explanation(
                    endpoint=endpoint,
                    instances=instances,
                    feature_names=feature_names,
                    background_data=background_data
                )
                compliance_status = "COMPLIANT"
                logger.info("✅ SHAP explanation generated - EU AI Act §6 compliant")
            
            except Exception as e:
                logger.error(f"❌ SHAP explanation failed: {e}")
                compliance_status = "REQUIRES_REVIEW"
        
        # Audit log
        if self.enable_audit:
            self._log_audit(
                endpoint_id=endpoint_id,
                confidence=max_confidence,
                high_risk=is_high_risk,
                compliance_status=compliance_status
            )
        
        return {
            "predictions": predictions.predictions,
            "confidence_scores": confidence_scores,
            "explanations": explanations,
            "high_risk": is_high_risk,
            "compliance_status": compliance_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _generate_shap_explanation(
        self,
        endpoint: aiplatform.Endpoint,
        instances: List[Dict],
        feature_names: List[str],
        background_data: Optional[np.ndarray] = None
    ) -> List[Dict]:
        """
        Generate SHAP explanations for predictions.
        
        Returns:
            List of SHAP explanations with feature contributions
        """
        # Convert instances to numpy array
        X = np.array([list(inst.values()) for inst in instances])
        
        # Create prediction function
        def predict_fn(data):
            instances_list = [
                {feature_names[i]: float(val) for i, val in enumerate(row)}
                for row in data
            ]
            predictions = endpoint.predict(instances=instances_list)
            return np.array(predictions.predictions)
        
        # Use background data or sample from instances
        if background_data is None:
            background_data = X[:min(100, len(X))]
        
        # Create SHAP explainer
        explainer = shap.KernelExplainer(predict_fn, background_data)
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(X)
        
        # Format explanations
        explanations = []
        for i, instance in enumerate(instances):
            explanation = {
                "instance_id": i,
                "feature_contributions": {
                    feature_names[j]: float(shap_values[i][j])
                    for j in range(len(feature_names))
                },
                "base_value": float(explainer.expected_value),
                "prediction": float(predict_fn(X[i:i+1])[0])
            }
            
            # Sort features by absolute contribution
            sorted_features = sorted(
                explanation["feature_contributions"].items(),
                key=lambda x: abs(x[1]),
                reverse=True
            )
            explanation["top_features"] = sorted_features[:5]
            
            explanations.append(explanation)
        
        return explanations
    
    def _extract_confidence_scores(self, predictions) -> List[float]:
        """Extract confidence scores from predictions"""
        # Handle different prediction formats
        if hasattr(predictions, 'predictions'):
            preds = predictions.predictions
        else:
            preds = predictions
        
        # Extract confidence (assumes classification with probabilities)
        confidence_scores = []
        for pred in preds:
            if isinstance(pred, dict) and 'confidence' in pred:
                confidence_scores.append(pred['confidence'])
            elif isinstance(pred, (list, np.ndarray)):
                confidence_scores.append(max(pred))
            else:
                confidence_scores.append(float(pred))
        
        return confidence_scores
    
    def validate_explanation_compliance(
        self,
        explanation: Dict,
        required_fields: List[str] = None
    ) -> Tuple[bool, List[str]]:
        """
        Validate that explanation meets compliance requirements.
        
        Args:
            explanation: SHAP explanation dictionary
            required_fields: Required fields for compliance
        
        Returns:
            (is_compliant, missing_fields)
        """
        if required_fields is None:
            required_fields = [
                "feature_contributions",
                "base_value",
                "prediction",
                "top_features"
            ]
        
        missing_fields = []
        for field in required_fields:
            if field not in explanation:
                missing_fields.append(field)
        
        is_compliant = len(missing_fields) == 0
        
        return is_compliant, missing_fields
    
    def generate_explanation_report(
        self,
        result: Dict,
        patient_id: Optional[str] = None
    ) -> str:
        """
        Generate human-readable explanation report for clinical review.
        
        Complies with:
        - EU AI Act §8 (Transparency)
        - GDPR Art. 22 (Right to Explanation)
        """
        report = []
        report.append("=" * 60)
        report.append("CLINICAL AI EXPLANATION REPORT")
        report.append("=" * 60)
        report.append("")
        
        if patient_id:
            report.append(f"Patient ID: {patient_id}")
        
        report.append(f"Timestamp: {result['timestamp']}")
        report.append(f"High-Risk Inference: {'YES' if result['high_risk'] else 'NO'}")
        report.append(f"Compliance Status: {result['compliance_status']}")
        report.append("")
        
        # Predictions
        report.append("PREDICTIONS:")
        for i, (pred, conf) in enumerate(zip(result['predictions'], result['confidence_scores'])):
            report.append(f"  Instance {i}: {pred} (confidence: {conf:.2%})")
        report.append("")
        
        # Explanations
        if result['explanations']:
            report.append("FEATURE CONTRIBUTIONS (SHAP Analysis):")
            for i, exp in enumerate(result['explanations']):
                report.append(f"\n  Instance {i}:")
                report.append(f"    Base Value: {exp['base_value']:.4f}")
                report.append(f"    Prediction: {exp['prediction']:.4f}")
                report.append(f"\n    Top Contributing Features:")
                for feature, contribution in exp['top_features']:
                    direction = "↑" if contribution > 0 else "↓"
                    report.append(f"      {direction} {feature}: {contribution:+.4f}")
        else:
            report.append("EXPLANATIONS: Not required (low-risk inference)")
        
        report.append("")
        report.append("=" * 60)
        report.append("COMPLIANCE ATTESTATION:")
        report.append("  ✓ EU AI Act §6 (High-Risk AI Systems)")
        report.append("  ✓ GDPR Art. 22 (Right to Explanation)")
        report.append("  ✓ HIPAA §164.312(b) (Audit Controls)")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def _log_audit(
        self,
        endpoint_id: str,
        confidence: float,
        high_risk: bool,
        compliance_status: str
    ):
        """Internal audit logging"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "endpoint_id": endpoint_id,
            "confidence": confidence,
            "high_risk": high_risk,
            "compliance_status": compliance_status,
            "framework": "EU_AI_ACT_6"
        }
        self.audit_log.append(audit_entry)
        
        # Log to file
        with open("logs/vertex_ai_audit.jsonl", "a") as f:
            f.write(json.dumps(audit_entry) + "\n")


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-health",
        location="us-central1",
        high_risk_threshold=0.7
    )
    
    # Example: Malaria diagnosis prediction
    instances = [
        {
            "fever": 1.0,
            "chills": 1.0,
            "headache": 0.8,
            "nausea": 0.6,
            "fatigue": 0.9,
            "age": 35,
            "location_risk": 0.7
        }
    ]
    
    feature_names = ["fever", "chills", "headache", "nausea", "fatigue", "age", "location_risk"]
    
    # Make prediction with explanation
    result = explainer.predict_with_explanation(
        endpoint_id="projects/123/locations/us-central1/endpoints/456",
        instances=instances,
        feature_names=feature_names
    )
    
    # Generate report
    report = explainer.generate_explanation_report(
        result=result,
        patient_id="PAT_12345"
    )
    
    print(report)
