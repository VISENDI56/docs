"""
Vertex AI + SHAP Explainability Integration
Right to Explanation (EU AI Act §6, GDPR Art. 22)

Every high-risk clinical inference requires explainability.
"""

import shap
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
from google.cloud import aiplatform
from google.cloud.aiplatform import explain

logger = logging.getLogger(__name__)


@dataclass
class ExplanationResult:
    """Structured explanation for high-risk inference"""
    prediction: float
    confidence_score: float
    shap_values: Dict[str, float]
    feature_importance: Dict[str, float]
    evidence_chain: List[str]
    decision_rationale: str
    compliance_status: str
    timestamp: str


class VertexAIExplainability:
    """
    Integrates Vertex AI models with SHAP explainability.
    
    Compliance:
    - EU AI Act §6 (High-Risk AI Systems)
    - GDPR Art. 22 (Right to Explanation)
    - ISO 27001 A.18.1.4 (Privacy and Protection)
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        high_risk_threshold: float = 0.7
    ):
        self.project_id = project_id
        self.location = location
        self.high_risk_threshold = high_risk_threshold
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        logger.info(f"🧠 Vertex AI Explainability initialized - Project: {project_id}")
    
    def explain_prediction(
        self,
        model_endpoint: str,
        input_features: Dict[str, any],
        feature_names: List[str],
        background_data: Optional[np.ndarray] = None
    ) -> ExplanationResult:
        """
        Generate SHAP explanation for a prediction.
        
        Args:
            model_endpoint: Vertex AI model endpoint
            input_features: Input features for prediction
            feature_names: Names of features
            background_data: Background dataset for SHAP (optional)
        
        Returns:
            ExplanationResult with complete explanation
        """
        # Get prediction from Vertex AI
        endpoint = aiplatform.Endpoint(model_endpoint)
        
        # Prepare input
        instances = [input_features]
        
        # Get prediction with explanation
        prediction_response = endpoint.predict(instances=instances)
        
        prediction = prediction_response.predictions[0]
        confidence_score = float(prediction) if isinstance(prediction, (int, float)) else float(prediction[0])
        
        # Check if high-risk (requires explanation)
        is_high_risk = confidence_score >= self.high_risk_threshold
        
        if is_high_risk:
            logger.warning(f"⚠️ HIGH-RISK INFERENCE detected - Confidence: {confidence_score:.2%}")
        
        # Generate SHAP explanation
        shap_values, feature_importance = self._generate_shap_explanation(
            model_endpoint=model_endpoint,
            input_features=input_features,
            feature_names=feature_names,
            background_data=background_data
        )
        
        # Build evidence chain
        evidence_chain = self._build_evidence_chain(
            shap_values=shap_values,
            feature_names=feature_names,
            input_features=input_features
        )
        
        # Generate decision rationale
        decision_rationale = self._generate_rationale(
            prediction=confidence_score,
            shap_values=shap_values,
            feature_names=feature_names
        )
        
        # Compliance check
        compliance_status = self._check_compliance(
            confidence_score=confidence_score,
            has_explanation=True,
            evidence_chain=evidence_chain
        )
        
        result = ExplanationResult(
            prediction=confidence_score,
            confidence_score=confidence_score,
            shap_values=shap_values,
            feature_importance=feature_importance,
            evidence_chain=evidence_chain,
            decision_rationale=decision_rationale,
            compliance_status=compliance_status,
            timestamp=datetime.utcnow().isoformat()
        )
        
        logger.info(f"✅ Explanation generated - Compliance: {compliance_status}")
        
        return result
    
    def _generate_shap_explanation(
        self,
        model_endpoint: str,
        input_features: Dict[str, any],
        feature_names: List[str],
        background_data: Optional[np.ndarray] = None
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """Generate SHAP values for the prediction"""
        
        # Convert input to numpy array
        input_array = np.array([list(input_features.values())])
        
        # Create SHAP explainer
        if background_data is None:
            # Use input as background (for demo purposes)
            background_data = input_array
        
        # Define prediction function for SHAP
        def predict_fn(X):
            endpoint = aiplatform.Endpoint(model_endpoint)
            predictions = []
            for row in X:
                features = {name: val for name, val in zip(feature_names, row)}
                pred = endpoint.predict(instances=[features])
                predictions.append(pred.predictions[0])
            return np.array(predictions)
        
        # Create SHAP explainer (using KernelExplainer for model-agnostic explanation)
        explainer = shap.KernelExplainer(predict_fn, background_data)
        
        # Calculate SHAP values
        shap_values_array = explainer.shap_values(input_array)
        
        # Convert to dictionary
        shap_values = {
            name: float(val) 
            for name, val in zip(feature_names, shap_values_array[0])
        }
        
        # Calculate feature importance (absolute SHAP values)
        feature_importance = {
            name: abs(val) 
            for name, val in shap_values.items()
        }
        
        # Sort by importance
        feature_importance = dict(
            sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        )
        
        return shap_values, feature_importance
    
    def _build_evidence_chain(
        self,
        shap_values: Dict[str, float],
        feature_names: List[str],
        input_features: Dict[str, any]
    ) -> List[str]:
        """Build evidence chain from SHAP values"""
        
        evidence = []
        
        # Sort features by absolute SHAP value
        sorted_features = sorted(
            shap_values.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Top 5 most important features
        for feature, shap_val in sorted_features[:5]:
            direction = "increases" if shap_val > 0 else "decreases"
            feature_value = input_features.get(feature, "N/A")
            
            evidence.append(
                f"{feature}={feature_value} {direction} risk by {abs(shap_val):.3f}"
            )
        
        return evidence
    
    def _generate_rationale(
        self,
        prediction: float,
        shap_values: Dict[str, float],
        feature_names: List[str]
    ) -> str:
        """Generate human-readable decision rationale"""
        
        # Find most influential features
        sorted_features = sorted(
            shap_values.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        top_feature, top_shap = sorted_features[0]
        
        risk_level = "HIGH" if prediction >= 0.7 else "MODERATE" if prediction >= 0.4 else "LOW"
        
        rationale = (
            f"Risk assessment: {risk_level} ({prediction:.1%} confidence). "
            f"Primary factor: {top_feature} (SHAP: {top_shap:.3f}). "
            f"Decision based on {len(feature_names)} clinical features with "
            f"explainable AI (SHAP) analysis."
        )
        
        return rationale
    
    def _check_compliance(
        self,
        confidence_score: float,
        has_explanation: bool,
        evidence_chain: List[str]
    ) -> str:
        """Check compliance with EU AI Act and GDPR"""
        
        is_high_risk = confidence_score >= self.high_risk_threshold
        
        if is_high_risk:
            if has_explanation and len(evidence_chain) > 0:
                return "COMPLIANT (EU AI Act §6, GDPR Art. 22)"
            else:
                return "NON-COMPLIANT (Missing explanation for high-risk inference)"
        else:
            return "COMPLIANT (Low-risk inference)"
    
    def validate_explanation_quality(
        self,
        explanation: ExplanationResult,
        min_evidence_items: int = 3
    ) -> bool:
        """
        Validate that explanation meets quality standards.
        
        Requirements:
        - Confidence score present
        - SHAP values calculated
        - Evidence chain with minimum items
        - Decision rationale provided
        """
        
        checks = {
            "confidence_score": explanation.confidence_score is not None,
            "shap_values": len(explanation.shap_values) > 0,
            "evidence_chain": len(explanation.evidence_chain) >= min_evidence_items,
            "decision_rationale": len(explanation.decision_rationale) > 0,
            "compliance_status": "COMPLIANT" in explanation.compliance_status
        }
        
        all_passed = all(checks.values())
        
        if not all_passed:
            failed_checks = [k for k, v in checks.items() if not v]
            logger.error(f"❌ Explanation quality check failed: {failed_checks}")
        
        return all_passed


class OutbreakRiskExplainer(VertexAIExplainability):
    """
    Specialized explainer for outbreak risk predictions.
    """
    
    def explain_outbreak_risk(
        self,
        model_endpoint: str,
        location: Dict[str, float],
        symptoms: List[str],
        environmental_factors: Dict[str, float],
        historical_data: Optional[np.ndarray] = None
    ) -> ExplanationResult:
        """
        Explain outbreak risk prediction.
        
        Args:
            model_endpoint: Vertex AI model endpoint
            location: {"lat": float, "lng": float}
            symptoms: List of reported symptoms
            environmental_factors: Temperature, rainfall, etc.
            historical_data: Historical outbreak data for SHAP background
        
        Returns:
            ExplanationResult with outbreak-specific explanation
        """
        
        # Prepare features
        input_features = {
            "latitude": location["lat"],
            "longitude": location["lng"],
            "symptom_count": len(symptoms),
            **environmental_factors
        }
        
        feature_names = list(input_features.keys())
        
        # Generate explanation
        explanation = self.explain_prediction(
            model_endpoint=model_endpoint,
            input_features=input_features,
            feature_names=feature_names,
            background_data=historical_data
        )
        
        # Add outbreak-specific context
        explanation.decision_rationale += (
            f" Symptoms reported: {', '.join(symptoms)}. "
            f"Location: ({location['lat']:.4f}, {location['lng']:.4f})."
        )
        
        return explanation


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = OutbreakRiskExplainer(
        project_id="iluminara-health",
        location="us-central1",
        high_risk_threshold=0.7
    )
    
    # Explain outbreak risk
    explanation = explainer.explain_outbreak_risk(
        model_endpoint="projects/123/locations/us-central1/endpoints/456",
        location={"lat": 0.4221, "lng": 40.2255},
        symptoms=["diarrhea", "vomiting", "dehydration"],
        environmental_factors={
            "temperature": 32.5,
            "rainfall": 15.2,
            "population_density": 850
        }
    )
    
    print(f"🎯 Prediction: {explanation.prediction:.1%}")
    print(f"📊 Compliance: {explanation.compliance_status}")
    print(f"🔍 Evidence Chain:")
    for evidence in explanation.evidence_chain:
        print(f"   - {evidence}")
    print(f"💡 Rationale: {explanation.decision_rationale}")
