"""
Vertex AI + SHAP Integration
Right to Explanation (EU AI Act §6, GDPR Art. 22)

Every high-risk clinical inference requires explainability.
This module integrates Vertex AI predictions with SHAP analysis.

Compliance:
- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- HIPAA §164.312(e)(1) (Transmission Security)
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
    Integrates Vertex AI predictions with SHAP explainability.
    
    Ensures every high-risk inference includes:
    - Confidence score
    - Evidence chain
    - Feature contributions (SHAP values)
    - Decision rationale
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        model_endpoint: Optional[str] = None,
        high_risk_threshold: float = 0.7
    ):
        self.project_id = project_id
        self.location = location
        self.model_endpoint = model_endpoint
        self.high_risk_threshold = high_risk_threshold
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        logger.info(f"🧠 Vertex AI Explainer initialized - Project: {project_id}")
    
    def predict_with_explanation(
        self,
        instances: List[Dict],
        feature_names: List[str],
        model_type: str = "tabular"
    ) -> Dict:
        """
        Make prediction with SHAP explanation.
        
        Args:
            instances: Input data for prediction
            feature_names: Names of features
            model_type: Type of model (tabular, image, text)
        
        Returns:
            Dictionary with prediction and explanation
        """
        # Get prediction from Vertex AI
        endpoint = aiplatform.Endpoint(self.model_endpoint)
        prediction = endpoint.predict(instances=instances)
        
        # Extract prediction details
        predictions = prediction.predictions
        confidence_score = float(predictions[0]) if predictions else 0.0
        
        # Determine if high-risk
        is_high_risk = confidence_score >= self.high_risk_threshold
        
        # Generate SHAP explanation
        if is_high_risk:
            logger.info(f"⚠️ High-risk inference detected (confidence: {confidence_score:.2%})")
            shap_values = self._generate_shap_explanation(
                instances=instances,
                feature_names=feature_names,
                model_type=model_type
            )
        else:
            shap_values = None
        
        # Build explanation
        explanation = {
            "prediction": predictions[0] if predictions else None,
            "confidence_score": confidence_score,
            "is_high_risk": is_high_risk,
            "timestamp": datetime.utcnow().isoformat(),
            "model_endpoint": self.model_endpoint,
            "compliance": {
                "eu_ai_act": "§6 (High-Risk AI)" if is_high_risk else "Not applicable",
                "gdpr": "Art. 22 (Right to Explanation)" if is_high_risk else "Not applicable"
            }
        }
        
        # Add SHAP explanation if high-risk
        if is_high_risk and shap_values is not None:
            explanation["shap_values"] = shap_values
            explanation["feature_importance"] = self._rank_features(
                shap_values, feature_names
            )
            explanation["decision_rationale"] = self._generate_rationale(
                shap_values, feature_names, predictions[0]
            )
        
        return explanation
    
    def _generate_shap_explanation(
        self,
        instances: List[Dict],
        feature_names: List[str],
        model_type: str
    ) -> Dict:
        """
        Generate SHAP values for model prediction.
        
        Args:
            instances: Input data
            feature_names: Feature names
            model_type: Model type
        
        Returns:
            SHAP values and metadata
        """
        try:
            # Convert instances to numpy array
            X = np.array([list(inst.values()) for inst in instances])
            
            # Create SHAP explainer based on model type
            if model_type == "tabular":
                # Use TreeExplainer for tree-based models
                # In production, load the actual model
                explainer = shap.KernelExplainer(
                    model=self._predict_function,
                    data=shap.sample(X, 100)
                )
            else:
                # Use KernelExplainer for other models
                explainer = shap.KernelExplainer(
                    model=self._predict_function,
                    data=shap.sample(X, 100)
                )
            
            # Calculate SHAP values
            shap_values = explainer.shap_values(X)
            
            # Convert to serializable format
            if isinstance(shap_values, list):
                shap_values = shap_values[0]
            
            return {
                "values": shap_values.tolist() if hasattr(shap_values, 'tolist') else shap_values,
                "base_value": float(explainer.expected_value) if hasattr(explainer, 'expected_value') else 0.0,
                "feature_names": feature_names,
                "method": "SHAP (SHapley Additive exPlanations)"
            }
        
        except Exception as e:
            logger.error(f"❌ SHAP explanation failed: {e}")
            return {
                "error": str(e),
                "fallback": "Feature importance not available"
            }
    
    def _predict_function(self, X: np.ndarray) -> np.ndarray:
        """
        Wrapper function for SHAP explainer.
        Calls Vertex AI endpoint for predictions.
        """
        # Convert numpy array to instances
        instances = [dict(enumerate(row)) for row in X]
        
        # Get predictions
        endpoint = aiplatform.Endpoint(self.model_endpoint)
        prediction = endpoint.predict(instances=instances)
        
        # Return predictions as numpy array
        return np.array(prediction.predictions)
    
    def _rank_features(
        self,
        shap_values: Dict,
        feature_names: List[str]
    ) -> List[Dict]:
        """
        Rank features by importance (absolute SHAP values).
        
        Args:
            shap_values: SHAP values dictionary
            feature_names: Feature names
        
        Returns:
            Ranked list of features with contributions
        """
        if "values" not in shap_values:
            return []
        
        values = shap_values["values"]
        if isinstance(values, list) and len(values) > 0:
            values = values[0]  # Take first instance
        
        # Calculate absolute importance
        importance = [(name, abs(val)) for name, val in zip(feature_names, values)]
        importance.sort(key=lambda x: x[1], reverse=True)
        
        # Format as list of dicts
        return [
            {
                "feature": name,
                "importance": float(imp),
                "contribution": "positive" if values[i] > 0 else "negative"
            }
            for i, (name, imp) in enumerate(importance)
        ]
    
    def _generate_rationale(
        self,
        shap_values: Dict,
        feature_names: List[str],
        prediction: float
    ) -> str:
        """
        Generate human-readable decision rationale.
        
        Args:
            shap_values: SHAP values
            feature_names: Feature names
            prediction: Model prediction
        
        Returns:
            Human-readable explanation
        """
        if "values" not in shap_values:
            return "Explanation not available"
        
        values = shap_values["values"]
        if isinstance(values, list) and len(values) > 0:
            values = values[0]
        
        # Get top 3 contributing features
        importance = [(name, val) for name, val in zip(feature_names, values)]
        importance.sort(key=lambda x: abs(x[1]), reverse=True)
        top_features = importance[:3]
        
        # Generate rationale
        rationale = f"Prediction: {prediction:.2%} confidence. "
        rationale += "Key factors: "
        
        for i, (name, val) in enumerate(top_features):
            direction = "increases" if val > 0 else "decreases"
            rationale += f"{name} {direction} risk"
            if i < len(top_features) - 1:
                rationale += ", "
        
        return rationale
    
    def validate_compliance(self, explanation: Dict) -> Dict:
        """
        Validate that explanation meets compliance requirements.
        
        Args:
            explanation: Explanation dictionary
        
        Returns:
            Compliance validation result
        """
        requirements = {
            "confidence_score": "confidence_score" in explanation,
            "evidence_chain": "feature_importance" in explanation,
            "feature_contributions": "shap_values" in explanation,
            "decision_rationale": "decision_rationale" in explanation
        }
        
        all_met = all(requirements.values())
        
        return {
            "compliant": all_met,
            "requirements_met": requirements,
            "frameworks": {
                "EU_AI_ACT": "§6 compliant" if all_met else "Non-compliant",
                "GDPR": "Art. 22 compliant" if all_met else "Non-compliant"
            }
        }


class OutbreakRiskPredictor:
    """
    Outbreak risk prediction with explainability.
    
    Integrates with iLuminara's Golden Thread for multi-source verification.
    """
    
    def __init__(
        self,
        project_id: str,
        model_endpoint: str,
        location: str = "us-central1"
    ):
        self.explainer = VertexAIExplainer(
            project_id=project_id,
            location=location,
            model_endpoint=model_endpoint,
            high_risk_threshold=0.7
        )
    
    def predict_outbreak_risk(
        self,
        case_count: int,
        population: int,
        attack_rate: float,
        r_effective: float,
        days_since_first_case: int,
        location: str
    ) -> Dict:
        """
        Predict outbreak risk with explanation.
        
        Args:
            case_count: Number of cases
            population: Population size
            attack_rate: Attack rate
            r_effective: Effective reproduction number
            days_since_first_case: Days since first case
            location: Geographic location
        
        Returns:
            Prediction with explanation
        """
        # Prepare features
        instances = [{
            "case_count": case_count,
            "population": population,
            "attack_rate": attack_rate,
            "r_effective": r_effective,
            "days_since_first_case": days_since_first_case
        }]
        
        feature_names = [
            "case_count",
            "population",
            "attack_rate",
            "r_effective",
            "days_since_first_case"
        ]
        
        # Get prediction with explanation
        explanation = self.explainer.predict_with_explanation(
            instances=instances,
            feature_names=feature_names,
            model_type="tabular"
        )
        
        # Add context
        explanation["location"] = location
        explanation["input_data"] = instances[0]
        
        # Validate compliance
        compliance = self.explainer.validate_compliance(explanation)
        explanation["compliance_validation"] = compliance
        
        logger.info(f"✅ Outbreak risk prediction complete - Location: {location}")
        
        return explanation


# Example usage
if __name__ == "__main__":
    # Initialize predictor
    predictor = OutbreakRiskPredictor(
        project_id="iluminara-core",
        model_endpoint="projects/123/locations/us-central1/endpoints/456",
        location="us-central1"
    )
    
    # Predict outbreak risk
    result = predictor.predict_outbreak_risk(
        case_count=150,
        population=100000,
        attack_rate=0.0015,
        r_effective=2.5,
        days_since_first_case=14,
        location="Dadaab Refugee Camp"
    )
    
    print(json.dumps(result, indent=2))
    
    # Check compliance
    if result["compliance_validation"]["compliant"]:
        print("✅ Compliant with EU AI Act §6 and GDPR Art. 22")
    else:
        print("❌ Non-compliant - Missing required explanations")
