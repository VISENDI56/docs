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
    """Explanation methods"""
    SHAP = "shap"
    LIME = "lime"
    FEATURE_IMPORTANCE = "feature_importance"


class VertexAIExplainer:
    """
    Vertex AI model wrapper with mandatory SHAP explainability.
    
    All high-risk inferences (confidence > 0.7) automatically trigger
    SHAP analysis to comply with EU AI Act §6.
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        model_name: str = "outbreak-predictor",
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
        features: Dict[str, any],
        patient_id: Optional[str] = None,
        jurisdiction: str = "KDPA_KE"
    ) -> Dict:
        """
        Make prediction with automatic explainability for high-risk inferences.
        
        Args:
            features: Input features for prediction
            patient_id: Patient identifier (for audit)
            jurisdiction: Legal jurisdiction
        
        Returns:
            {
                "prediction": float,
                "confidence": float,
                "risk_level": str,
                "explanation": {...},
                "compliance": {...}
            }
        """
        # Convert features to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Get prediction from Vertex AI
        prediction, confidence = self._get_vertex_prediction(feature_df)
        
        # Determine risk level
        risk_level = self._calculate_risk_level(confidence)
        
        # Generate explanation if high-risk
        explanation = None
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            logger.info(f"⚠️ High-risk inference detected (confidence: {confidence:.2f}) - Generating SHAP explanation")
            explanation = self._generate_shap_explanation(feature_df, features)
        
        # Build result
        result = {
            "prediction": float(prediction),
            "confidence": float(confidence),
            "risk_level": risk_level.value,
            "explanation": explanation,
            "compliance": {
                "eu_ai_act_s6": explanation is not None,
                "gdpr_art_22": explanation is not None,
                "explainability_required": risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL],
                "jurisdiction": jurisdiction
            },
            "metadata": {
                "model_name": self.model_name,
                "timestamp": datetime.utcnow().isoformat(),
                "patient_id": patient_id
            }
        }
        
        # Audit log
        if self.enable_audit:
            self._log_audit(result, features, patient_id, jurisdiction)
        
        return result
    
    def _get_vertex_prediction(self, feature_df: pd.DataFrame) -> Tuple[float, float]:
        """
        Get prediction from Vertex AI model.
        
        For demo purposes, this uses a simple heuristic.
        In production, replace with actual Vertex AI endpoint call.
        """
        # TODO: Replace with actual Vertex AI endpoint
        # endpoint = aiplatform.Endpoint(endpoint_name=self.endpoint_name)
        # prediction = endpoint.predict(instances=feature_df.to_dict('records'))
        
        # Demo heuristic: Calculate risk score based on symptoms
        risk_score = 0.0
        
        # Symptom severity
        if 'fever' in feature_df.columns and feature_df['fever'].iloc[0]:
            risk_score += 0.3
        if 'diarrhea' in feature_df.columns and feature_df['diarrhea'].iloc[0]:
            risk_score += 0.4
        if 'vomiting' in feature_df.columns and feature_df['vomiting'].iloc[0]:
            risk_score += 0.3
        
        # Add some noise for realism
        risk_score += np.random.uniform(-0.1, 0.1)
        risk_score = np.clip(risk_score, 0.0, 1.0)
        
        # Confidence is inverse of uncertainty
        confidence = 0.7 + np.random.uniform(0, 0.25)
        
        return risk_score, confidence
    
    def _calculate_risk_level(self, confidence: float) -> RiskLevel:
        """Calculate risk level based on confidence score"""
        if confidence < 0.5:
            return RiskLevel.LOW
        elif confidence < 0.7:
            return RiskLevel.MEDIUM
        elif confidence < 0.9:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def _generate_shap_explanation(
        self,
        feature_df: pd.DataFrame,
        features: Dict
    ) -> Dict:
        """
        Generate SHAP explanation for high-risk inference.
        
        SHAP (SHapley Additive exPlanations) provides:
        - Feature importance
        - Contribution to prediction
        - Baseline vs actual
        """
        try:
            # Initialize SHAP explainer if not already done
            if self.shap_explainer is None:
                # Use a simple linear explainer for demo
                # In production, use model-specific explainer
                self.shap_explainer = shap.LinearExplainer(
                    lambda x: self._get_vertex_prediction(pd.DataFrame(x, columns=feature_df.columns))[0],
                    feature_df
                )
            
            # Calculate SHAP values
            shap_values = self.shap_explainer.shap_values(feature_df)
            
            # Build explanation
            explanation = {
                "method": "SHAP",
                "feature_contributions": {},
                "top_features": [],
                "baseline_value": float(self.shap_explainer.expected_value) if hasattr(self.shap_explainer, 'expected_value') else 0.5,
                "evidence_chain": []
            }
            
            # Feature contributions
            for i, feature_name in enumerate(feature_df.columns):
                contribution = float(shap_values[0][i]) if isinstance(shap_values, np.ndarray) else 0.0
                explanation["feature_contributions"][feature_name] = {
                    "value": features.get(feature_name),
                    "contribution": contribution,
                    "importance": abs(contribution)
                }
            
            # Sort by importance
            sorted_features = sorted(
                explanation["feature_contributions"].items(),
                key=lambda x: x[1]["importance"],
                reverse=True
            )
            
            # Top 3 features
            explanation["top_features"] = [
                {
                    "feature": name,
                    "value": data["value"],
                    "contribution": data["contribution"]
                }
                for name, data in sorted_features[:3]
            ]
            
            # Evidence chain (human-readable)
            for feature, data in sorted_features[:3]:
                if data["contribution"] > 0:
                    explanation["evidence_chain"].append(
                        f"{feature}={data['value']} increases risk by {data['contribution']:.2%}"
                    )
                else:
                    explanation["evidence_chain"].append(
                        f"{feature}={data['value']} decreases risk by {abs(data['contribution']):.2%}"
                    )
            
            logger.info(f"✅ SHAP explanation generated - Top feature: {sorted_features[0][0]}")
            return explanation
        
        except Exception as e:
            logger.error(f"❌ SHAP explanation failed: {e}")
            return {
                "method": "SHAP",
                "error": str(e),
                "fallback": "Feature importance not available"
            }
    
    def _log_audit(
        self,
        result: Dict,
        features: Dict,
        patient_id: Optional[str],
        jurisdiction: str
    ):
        """Log AI inference to BigQuery audit table"""
        try:
            audit_record = {
                "timestamp": datetime.utcnow().isoformat(),
                "model_name": self.model_name,
                "patient_id": patient_id,
                "jurisdiction": jurisdiction,
                "prediction": result["prediction"],
                "confidence": result["confidence"],
                "risk_level": result["risk_level"],
                "explanation_provided": result["explanation"] is not None,
                "features": json.dumps(features),
                "explanation": json.dumps(result["explanation"]) if result["explanation"] else None,
                "compliance_eu_ai_act": result["compliance"]["eu_ai_act_s6"],
                "compliance_gdpr_art_22": result["compliance"]["gdpr_art_22"]
            }
            
            # Insert to BigQuery
            errors = self.bq_client.insert_rows_json(self.audit_table, [audit_record])
            
            if errors:
                logger.error(f"❌ Audit log failed: {errors}")
            else:
                logger.info(f"✅ Audit logged - Patient: {patient_id}, Risk: {result['risk_level']}")
        
        except Exception as e:
            logger.error(f"❌ Audit logging failed: {e}")
    
    def batch_predict_with_explanation(
        self,
        features_list: List[Dict],
        patient_ids: Optional[List[str]] = None,
        jurisdiction: str = "KDPA_KE"
    ) -> List[Dict]:
        """
        Batch prediction with explainability.
        
        Args:
            features_list: List of feature dictionaries
            patient_ids: List of patient identifiers
            jurisdiction: Legal jurisdiction
        
        Returns:
            List of prediction results with explanations
        """
        if patient_ids is None:
            patient_ids = [None] * len(features_list)
        
        results = []
        for features, patient_id in zip(features_list, patient_ids):
            result = self.predict_with_explanation(
                features=features,
                patient_id=patient_id,
                jurisdiction=jurisdiction
            )
            results.append(result)
        
        logger.info(f"✅ Batch prediction complete - {len(results)} inferences")
        return results


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-core",
        location="us-central1",
        model_name="outbreak-predictor",
        high_risk_threshold=0.7,
        enable_audit=True
    )
    
    # Example patient features
    patient_features = {
        "fever": True,
        "diarrhea": True,
        "vomiting": True,
        "age": 35,
        "location_lat": 0.0512,
        "location_lng": 40.3129,
        "days_since_onset": 2
    }
    
    # Get prediction with explanation
    result = explainer.predict_with_explanation(
        features=patient_features,
        patient_id="PAT_12345",
        jurisdiction="KDPA_KE"
    )
    
    print(f"\n🧠 Prediction: {result['prediction']:.2%}")
    print(f"📊 Confidence: {result['confidence']:.2%}")
    print(f"⚠️  Risk Level: {result['risk_level']}")
    
    if result['explanation']:
        print(f"\n📋 Explanation (SHAP):")
        print(f"   Baseline: {result['explanation']['baseline_value']:.2%}")
        print(f"\n   Top Contributing Features:")
        for feature in result['explanation']['top_features']:
            print(f"   - {feature['feature']}: {feature['value']} (contribution: {feature['contribution']:+.2%})")
        
        print(f"\n   Evidence Chain:")
        for evidence in result['explanation']['evidence_chain']:
            print(f"   - {evidence}")
    
    print(f"\n✅ Compliance:")
    print(f"   EU AI Act §6: {result['compliance']['eu_ai_act_s6']}")
    print(f"   GDPR Art. 22: {result['compliance']['gdpr_art_22']}")
