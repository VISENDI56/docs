"""
Vertex AI + SHAP Integration
Right to Explanation (EU AI Act §6, GDPR Art. 22)

Every high-risk clinical inference requires explainability.
This module integrates Vertex AI AutoML with SHAP (SHapley Additive exPlanations)
to provide transparent, auditable AI decisions.

Compliance:
- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- HIPAA §164.312(b) (Audit Controls)
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


class VertexAIExplainer:
    """
    Vertex AI model with SHAP explainability for high-risk clinical inferences.
    
    Ensures compliance with EU AI Act §6 by providing:
    - Feature importance
    - SHAP values
    - Decision rationale
    - Confidence scores
    - Evidence chain
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
        self.explainer = None
        
        logger.info(f"✅ Vertex AI Explainer initialized - Model: {model_name}")
    
    def predict_with_explanation(
        self,
        features: Dict[str, float],
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Make prediction with full explainability.
        
        Args:
            features: Input features for prediction
            context: Additional context (patient_id, location, etc.)
        
        Returns:
            {
                "prediction": float,
                "confidence": float,
                "risk_level": str,
                "explanation": {
                    "shap_values": List[float],
                    "feature_importance": Dict[str, float],
                    "decision_rationale": str,
                    "evidence_chain": List[str]
                },
                "compliance": {
                    "requires_explanation": bool,
                    "frameworks": List[str]
                }
            }
        """
        # Convert features to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Get prediction from Vertex AI
        prediction, confidence = self._get_vertex_prediction(feature_df)
        
        # Determine risk level
        risk_level = self._calculate_risk_level(confidence)
        
        # Check if explanation is required
        requires_explanation = confidence >= self.high_risk_threshold
        
        # Generate explanation
        explanation = None
        if requires_explanation:
            explanation = self._generate_shap_explanation(feature_df, features)
        
        # Build result
        result = {
            "prediction": float(prediction),
            "confidence": float(confidence),
            "risk_level": risk_level.value,
            "explanation": explanation,
            "compliance": {
                "requires_explanation": requires_explanation,
                "frameworks": self._get_applicable_frameworks(risk_level),
                "high_risk_threshold": self.high_risk_threshold
            },
            "timestamp": datetime.utcnow().isoformat(),
            "context": context or {}
        }
        
        # Audit log
        if self.enable_audit:
            self._log_inference(result, context)
        
        logger.info(
            f"🔮 Prediction: {prediction:.3f}, "
            f"Confidence: {confidence:.3f}, "
            f"Risk: {risk_level.value}, "
            f"Explanation: {'Required' if requires_explanation else 'Not Required'}"
        )
        
        return result
    
    def _get_vertex_prediction(
        self,
        feature_df: pd.DataFrame
    ) -> Tuple[float, float]:
        """
        Get prediction from Vertex AI model.
        
        For demo purposes, this uses a simple heuristic.
        In production, replace with actual Vertex AI endpoint call.
        """
        # TODO: Replace with actual Vertex AI endpoint
        # endpoint = aiplatform.Endpoint(endpoint_name=self.endpoint_name)
        # prediction = endpoint.predict(instances=feature_df.to_dict('records'))
        
        # Demo heuristic: weighted sum of features
        weights = {
            'fever': 0.3,
            'cough': 0.2,
            'diarrhea': 0.4,
            'vomiting': 0.3,
            'fatigue': 0.1,
            'headache': 0.15,
            'body_aches': 0.1
        }
        
        prediction = 0.0
        for feature, value in feature_df.iloc[0].items():
            if feature in weights:
                prediction += weights[feature] * value
        
        # Normalize to [0, 1]
        prediction = min(max(prediction, 0.0), 1.0)
        
        # Confidence is prediction with some noise
        confidence = min(prediction + np.random.uniform(0.05, 0.15), 1.0)
        
        return prediction, confidence
    
    def _generate_shap_explanation(
        self,
        feature_df: pd.DataFrame,
        features: Dict[str, float]
    ) -> Dict:
        """
        Generate SHAP explanation for high-risk inference.
        
        Returns:
            {
                "shap_values": List[float],
                "feature_importance": Dict[str, float],
                "decision_rationale": str,
                "evidence_chain": List[str]
            }
        """
        # Initialize SHAP explainer if not already done
        if self.explainer is None:
            # For demo, use a simple linear explainer
            # In production, use TreeExplainer or DeepExplainer based on model type
            self.explainer = shap.LinearExplainer(
                self._dummy_model,
                feature_df
            )
        
        # Calculate SHAP values
        shap_values = self.explainer.shap_values(feature_df)
        
        # Convert to feature importance
        feature_importance = {}
        for i, feature_name in enumerate(feature_df.columns):
            feature_importance[feature_name] = float(abs(shap_values[0][i]))
        
        # Sort by importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Generate decision rationale
        top_features = sorted_features[:3]
        rationale = self._generate_rationale(top_features, features)
        
        # Build evidence chain
        evidence_chain = [
            f"{feature}: {features[feature]:.2f} (importance: {importance:.3f})"
            for feature, importance in top_features
        ]
        
        return {
            "shap_values": [float(v) for v in shap_values[0]],
            "feature_importance": feature_importance,
            "decision_rationale": rationale,
            "evidence_chain": evidence_chain,
            "top_features": [f[0] for f in top_features]
        }
    
    def _dummy_model(self, X):
        """Dummy model for SHAP explainer (demo purposes)"""
        weights = np.array([0.3, 0.2, 0.4, 0.3, 0.1, 0.15, 0.1])
        return np.dot(X, weights[:X.shape[1]])
    
    def _generate_rationale(
        self,
        top_features: List[Tuple[str, float]],
        features: Dict[str, float]
    ) -> str:
        """Generate human-readable decision rationale"""
        rationale_parts = []
        
        for feature, importance in top_features:
            value = features[feature]
            
            if value > 0.7:
                severity = "severe"
            elif value > 0.4:
                severity = "moderate"
            else:
                severity = "mild"
            
            rationale_parts.append(
                f"{severity} {feature.replace('_', ' ')} "
                f"(contribution: {importance:.1%})"
            )
        
        rationale = (
            f"High-risk prediction based on: "
            f"{', '.join(rationale_parts)}. "
            f"Clinical review recommended."
        )
        
        return rationale
    
    def _calculate_risk_level(self, confidence: float) -> RiskLevel:
        """Calculate risk level based on confidence score"""
        if confidence >= 0.9:
            return RiskLevel.CRITICAL
        elif confidence >= 0.7:
            return RiskLevel.HIGH
        elif confidence >= 0.5:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _get_applicable_frameworks(self, risk_level: RiskLevel) -> List[str]:
        """Get applicable legal frameworks based on risk level"""
        frameworks = []
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            frameworks.extend([
                "EU AI Act §6 (High-Risk AI Systems)",
                "GDPR Art. 22 (Right to Explanation)",
                "HIPAA §164.312(b) (Audit Controls)"
            ])
        
        if risk_level == RiskLevel.CRITICAL:
            frameworks.append("ISO 27001 A.18.1.4 (Privacy and Protection of PII)")
        
        return frameworks
    
    def _log_inference(self, result: Dict, context: Optional[Dict]):
        """Log inference to BigQuery for audit trail"""
        try:
            row = {
                "timestamp": result["timestamp"],
                "model_name": self.model_name,
                "prediction": result["prediction"],
                "confidence": result["confidence"],
                "risk_level": result["risk_level"],
                "requires_explanation": result["compliance"]["requires_explanation"],
                "explanation": json.dumps(result["explanation"]) if result["explanation"] else None,
                "context": json.dumps(context) if context else None,
                "frameworks": json.dumps(result["compliance"]["frameworks"])
            }
            
            errors = self.bq_client.insert_rows_json(self.audit_table, [row])
            
            if errors:
                logger.error(f"❌ Audit log failed: {errors}")
            else:
                logger.debug(f"✅ Audit log written")
        
        except Exception as e:
            logger.error(f"❌ Audit log exception: {e}")
    
    def batch_predict_with_explanation(
        self,
        features_list: List[Dict[str, float]],
        contexts: Optional[List[Dict]] = None
    ) -> List[Dict]:
        """
        Batch prediction with explanations.
        
        Args:
            features_list: List of feature dictionaries
            contexts: Optional list of context dictionaries
        
        Returns:
            List of prediction results with explanations
        """
        results = []
        
        for i, features in enumerate(features_list):
            context = contexts[i] if contexts else None
            result = self.predict_with_explanation(features, context)
            results.append(result)
        
        logger.info(f"✅ Batch prediction complete - {len(results)} inferences")
        
        return results


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-core",
        location="us-central1",
        high_risk_threshold=0.7,
        enable_audit=True
    )
    
    # Example features: patient symptoms
    features = {
        "fever": 0.9,
        "cough": 0.3,
        "diarrhea": 0.8,
        "vomiting": 0.7,
        "fatigue": 0.6,
        "headache": 0.4,
        "body_aches": 0.5
    }
    
    # Context
    context = {
        "patient_id": "PAT_12345",
        "location": "Dadaab",
        "jurisdiction": "KDPA_KE",
        "data_type": "PHI"
    }
    
    # Get prediction with explanation
    result = explainer.predict_with_explanation(features, context)
    
    print("\n" + "="*60)
    print("VERTEX AI + SHAP EXPLANATION")
    print("="*60)
    print(f"\n📊 Prediction: {result['prediction']:.3f}")
    print(f"🎯 Confidence: {result['confidence']:.3f}")
    print(f"⚠️  Risk Level: {result['risk_level'].upper()}")
    
    if result['explanation']:
        print(f"\n🔍 EXPLANATION REQUIRED (High-Risk Inference)")
        print(f"\n📋 Decision Rationale:")
        print(f"   {result['explanation']['decision_rationale']}")
        
        print(f"\n🔗 Evidence Chain:")
        for evidence in result['explanation']['evidence_chain']:
            print(f"   • {evidence}")
        
        print(f"\n📊 Feature Importance:")
        for feature, importance in sorted(
            result['explanation']['feature_importance'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            print(f"   • {feature}: {importance:.3f}")
    
    print(f"\n✅ Compliance Frameworks:")
    for framework in result['compliance']['frameworks']:
        print(f"   • {framework}")
    
    print("\n" + "="*60)
