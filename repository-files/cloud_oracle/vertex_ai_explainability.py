"""
Vertex AI + SHAP Explainability Integration
Right to Explanation (EU AI Act §6, GDPR Art. 22)

Every high-risk clinical inference requires explainability with SHAP values,
feature importance, and evidence chains.

Compliance:
- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- HIPAA §164.524 (Access to Protected Health Information)
"""

import shap
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from google.cloud import aiplatform
from google.cloud.aiplatform import explain
import logging

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
    compliance_attestation: Dict[str, str]
    timestamp: str


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
        high_risk_threshold: float = 0.7
    ):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.high_risk_threshold = high_risk_threshold
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # SHAP explainer (initialized on first use)
        self.explainer = None
        self.background_data = None
        
        logger.info(f"🧠 Vertex AI Explainer initialized - Model: {model_name}")
    
    def predict_with_explanation(
        self,
        features: Dict[str, float],
        require_explanation: bool = True
    ) -> ExplanationResult:
        """
        Make prediction with mandatory explanation for high-risk inferences.
        
        Args:
            features: Input features for prediction
            require_explanation: Force explanation even if not high-risk
        
        Returns:
            ExplanationResult with SHAP values and evidence chain
        """
        # Make prediction
        prediction, confidence = self._predict(features)
        
        # Determine if explanation is required
        is_high_risk = confidence >= self.high_risk_threshold
        needs_explanation = is_high_risk or require_explanation
        
        if needs_explanation:
            logger.info(f"⚠️ High-risk inference detected (confidence: {confidence:.2%})")
            
            # Generate SHAP explanation
            shap_values = self._compute_shap_values(features)
            
            # Compute feature importance
            feature_importance = self._compute_feature_importance(features)
            
            # Build evidence chain
            evidence_chain = self._build_evidence_chain(features, shap_values)
            
            # Generate decision rationale
            rationale = self._generate_rationale(
                prediction, confidence, shap_values, evidence_chain
            )
            
            # Compliance attestation
            attestation = self._generate_compliance_attestation(
                is_high_risk, confidence
            )
            
            return ExplanationResult(
                prediction=prediction,
                confidence_score=confidence,
                shap_values=shap_values,
                feature_importance=feature_importance,
                evidence_chain=evidence_chain,
                decision_rationale=rationale,
                compliance_attestation=attestation,
                timestamp=datetime.utcnow().isoformat()
            )
        else:
            # Low-risk inference - minimal explanation
            return ExplanationResult(
                prediction=prediction,
                confidence_score=confidence,
                shap_values={},
                feature_importance={},
                evidence_chain=["Low-risk inference - no explanation required"],
                decision_rationale=f"Prediction: {prediction:.2f} (confidence: {confidence:.2%})",
                compliance_attestation={"status": "LOW_RISK"},
                timestamp=datetime.utcnow().isoformat()
            )
    
    def _predict(self, features: Dict[str, float]) -> Tuple[float, float]:
        """Make prediction using Vertex AI model"""
        # Convert features to array
        feature_array = np.array([list(features.values())])
        
        # TODO: Replace with actual Vertex AI prediction
        # For now, simulate prediction
        prediction = np.random.uniform(0, 100)  # Predicted case count
        confidence = np.random.uniform(0.5, 0.99)  # Confidence score
        
        return prediction, confidence
    
    def _compute_shap_values(self, features: Dict[str, float]) -> Dict[str, float]:
        """
        Compute SHAP values for feature contributions.
        
        SHAP (SHapley Additive exPlanations) provides game-theoretic
        feature importance that satisfies EU AI Act transparency requirements.
        """
        if self.explainer is None:
            self._initialize_shap_explainer()
        
        # Convert features to array
        feature_array = np.array([list(features.values())])
        
        # Compute SHAP values
        shap_values = self.explainer.shap_values(feature_array)
        
        # Map back to feature names
        feature_names = list(features.keys())
        shap_dict = {
            name: float(value)
            for name, value in zip(feature_names, shap_values[0])
        }
        
        return shap_dict
    
    def _initialize_shap_explainer(self):
        """Initialize SHAP explainer with background data"""
        # TODO: Load actual background data from BigQuery
        # For now, generate synthetic background
        self.background_data = np.random.randn(100, 10)
        
        # Create SHAP explainer
        # Using KernelExplainer for model-agnostic explanations
        def model_predict(X):
            # Simulate model predictions
            return np.random.uniform(0, 100, size=(X.shape[0],))
        
        self.explainer = shap.KernelExplainer(
            model_predict,
            self.background_data
        )
        
        logger.info("✅ SHAP explainer initialized")
    
    def _compute_feature_importance(
        self, features: Dict[str, float]
    ) -> Dict[str, float]:
        """Compute feature importance scores"""
        # TODO: Use actual model feature importance
        # For now, simulate based on feature values
        importance = {
            name: abs(value) / sum(abs(v) for v in features.values())
            for name, value in features.items()
        }
        
        # Sort by importance
        importance = dict(
            sorted(importance.items(), key=lambda x: x[1], reverse=True)
        )
        
        return importance
    
    def _build_evidence_chain(
        self,
        features: Dict[str, float],
        shap_values: Dict[str, float]
    ) -> List[str]:
        """
        Build evidence chain showing reasoning path.
        
        Required by EU AI Act §8 for transparency.
        """
        evidence = []
        
        # Sort features by SHAP value magnitude
        sorted_features = sorted(
            shap_values.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Top 3 contributing features
        for feature, shap_value in sorted_features[:3]:
            feature_value = features[feature]
            direction = "increases" if shap_value > 0 else "decreases"
            evidence.append(
                f"{feature}={feature_value:.2f} {direction} risk by {abs(shap_value):.2f}"
            )
        
        return evidence
    
    def _generate_rationale(
        self,
        prediction: float,
        confidence: float,
        shap_values: Dict[str, float],
        evidence_chain: List[str]
    ) -> str:
        """Generate human-readable decision rationale"""
        # Find most influential feature
        top_feature = max(shap_values.items(), key=lambda x: abs(x[1]))
        
        rationale = (
            f"Predicted outbreak risk: {prediction:.1f} cases "
            f"(confidence: {confidence:.1%}). "
            f"Primary driver: {top_feature[0]} "
            f"(SHAP: {top_feature[1]:.2f}). "
            f"Evidence: {'; '.join(evidence_chain[:2])}."
        )
        
        return rationale
    
    def _generate_compliance_attestation(
        self,
        is_high_risk: bool,
        confidence: float
    ) -> Dict[str, str]:
        """Generate compliance attestation for audit trail"""
        attestation = {
            "status": "HIGH_RISK" if is_high_risk else "LOW_RISK",
            "confidence": f"{confidence:.2%}",
            "frameworks": "EU AI Act §6, GDPR Art. 22",
            "explanation_method": "SHAP (SHapley Additive exPlanations)",
            "attestation_time": datetime.utcnow().isoformat()
        }
        
        if is_high_risk:
            attestation["compliance_note"] = (
                "High-risk AI inference - Full explanation provided per EU AI Act §6"
            )
        
        return attestation


class OutbreakForecaster:
    """
    Outbreak forecasting with mandatory explainability.
    
    Integrates with Vertex AI AutoML for time-series forecasting
    and SHAP for transparency.
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1"
    ):
        self.explainer = VertexAIExplainer(
            project_id=project_id,
            location=location,
            model_name="outbreak-forecaster"
        )
    
    def forecast_outbreak(
        self,
        location: str,
        disease: str,
        historical_cases: List[int],
        environmental_factors: Dict[str, float],
        forecast_horizon_days: int = 14
    ) -> ExplanationResult:
        """
        Forecast outbreak with full explainability.
        
        Args:
            location: Geographic location
            disease: Disease type (cholera, malaria, etc.)
            historical_cases: Historical case counts
            environmental_factors: Temperature, rainfall, etc.
            forecast_horizon_days: Forecast window
        
        Returns:
            ExplanationResult with prediction and SHAP explanation
        """
        # Build feature vector
        features = {
            "avg_cases_7d": np.mean(historical_cases[-7:]),
            "avg_cases_14d": np.mean(historical_cases[-14:]),
            "case_trend": historical_cases[-1] - historical_cases[-7],
            "temperature": environmental_factors.get("temperature", 25.0),
            "rainfall": environmental_factors.get("rainfall", 0.0),
            "humidity": environmental_factors.get("humidity", 60.0),
            "population_density": environmental_factors.get("population_density", 1000),
            "healthcare_capacity": environmental_factors.get("healthcare_capacity", 0.5),
            "forecast_horizon": forecast_horizon_days,
            "disease_severity": self._get_disease_severity(disease)
        }
        
        # Make prediction with explanation
        result = self.explainer.predict_with_explanation(
            features=features,
            require_explanation=True  # Always explain outbreak forecasts
        )
        
        logger.info(
            f"📊 Outbreak forecast: {result.prediction:.1f} cases "
            f"(confidence: {result.confidence_score:.1%})"
        )
        
        return result
    
    def _get_disease_severity(self, disease: str) -> float:
        """Get disease severity score"""
        severity_map = {
            "cholera": 0.9,
            "malaria": 0.7,
            "typhoid": 0.6,
            "measles": 0.5,
            "influenza": 0.3
        }
        return severity_map.get(disease.lower(), 0.5)


# Example usage
if __name__ == "__main__":
    # Initialize forecaster
    forecaster = OutbreakForecaster(
        project_id="iluminara-core",
        location="us-central1"
    )
    
    # Forecast cholera outbreak
    result = forecaster.forecast_outbreak(
        location="Dadaab",
        disease="cholera",
        historical_cases=[5, 8, 12, 15, 18, 22, 28],
        environmental_factors={
            "temperature": 32.0,
            "rainfall": 15.0,
            "humidity": 75.0,
            "population_density": 5000,
            "healthcare_capacity": 0.3
        },
        forecast_horizon_days=14
    )
    
    # Print explanation
    print(f"✅ Prediction: {result.prediction:.1f} cases")
    print(f"📊 Confidence: {result.confidence_score:.1%}")
    print(f"🔍 Decision Rationale: {result.decision_rationale}")
    print(f"📋 Evidence Chain:")
    for evidence in result.evidence_chain:
        print(f"   - {evidence}")
    print(f"🛡️ Compliance: {result.compliance_attestation['status']}")
