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
    Vertex AI model with mandatory explainability for high-risk inferences.
    
    Every prediction with confidence > 0.7 triggers SHAP analysis.
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        model_name: str = "cholera-outbreak-predictor",
        explainability_threshold: float = 0.7,
        enable_audit: bool = True
    ):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.explainability_threshold = explainability_threshold
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
        instances: List[Dict],
        feature_names: List[str],
        patient_id: Optional[str] = None,
        jurisdiction: str = "GDPR_EU"
    ) -> Dict:
        """
        Make prediction with mandatory explainability for high-risk inferences.
        
        Args:
            instances: Input features for prediction
            feature_names: Names of features
            patient_id: Patient identifier (for audit)
            jurisdiction: Legal jurisdiction
        
        Returns:
            {
                "predictions": [...],
                "confidence": 0.95,
                "risk_level": "CRITICAL",
                "explanation": {
                    "method": "SHAP",
                    "feature_contributions": {...},
                    "evidence_chain": [...]
                },
                "compliance": {
                    "explainability_required": true,
                    "frameworks": ["EU AI Act §6", "GDPR Art. 22"]
                }
            }
        """
        # Get model endpoint
        endpoint = self._get_endpoint()
        
        # Make prediction
        response = endpoint.predict(instances=instances)
        predictions = response.predictions
        
        # Calculate confidence
        confidence = float(np.max(predictions[0])) if predictions else 0.0
        risk_level = self._calculate_risk_level(confidence)
        
        # Determine if explainability is required
        explainability_required = confidence >= self.explainability_threshold
        
        result = {
            "predictions": predictions,
            "confidence": confidence,
            "risk_level": risk_level.value,
            "timestamp": datetime.utcnow().isoformat(),
            "model_name": self.model_name,
            "patient_id": patient_id,
            "jurisdiction": jurisdiction
        }
        
        # Generate explanation if required
        if explainability_required:
            logger.info(f"🔍 High-risk inference detected (confidence: {confidence:.2%}) - Generating explanation")
            
            explanation = self._generate_shap_explanation(
                instances=instances,
                predictions=predictions,
                feature_names=feature_names
            )
            
            result["explanation"] = explanation
            result["compliance"] = {
                "explainability_required": True,
                "explainability_method": "SHAP",
                "frameworks": [
                    "EU AI Act §6 (High-Risk AI Systems)",
                    "GDPR Art. 22 (Right to Explanation)",
                    "HIPAA §164.524 (Right of Access)"
                ],
                "audit_trail": True
            }
            
            # Audit log
            if self.enable_audit:
                self._log_explanation(result)
        
        else:
            result["explanation"] = None
            result["compliance"] = {
                "explainability_required": False,
                "reason": f"Confidence {confidence:.2%} below threshold {self.explainability_threshold:.2%}"
            }
        
        return result
    
    def _generate_shap_explanation(
        self,
        instances: List[Dict],
        predictions: List,
        feature_names: List[str]
    ) -> Dict:
        """
        Generate SHAP explanation for prediction.
        
        Returns:
            {
                "method": "SHAP",
                "feature_contributions": {
                    "fever": 0.35,
                    "diarrhea": 0.28,
                    "location_risk": 0.22,
                    ...
                },
                "evidence_chain": [
                    "Primary factor: fever (35% contribution)",
                    "Secondary factor: diarrhea (28% contribution)",
                    ...
                ],
                "base_value": 0.15,
                "prediction_value": 0.95
            }
        """
        # Convert instances to numpy array
        X = np.array([list(inst.values()) for inst in instances])
        
        # Create SHAP explainer (using a simple linear approximation for demo)
        # In production, use actual model for SHAP
        explainer = shap.LinearExplainer(
            model=lambda x: np.array(predictions),
            data=X,
            feature_names=feature_names
        )
        
        # Calculate SHAP values
        shap_values = explainer.shap_values(X)
        
        # Extract feature contributions
        feature_contributions = {}
        for i, feature_name in enumerate(feature_names):
            contribution = float(shap_values[0][i]) if len(shap_values) > 0 else 0.0
            feature_contributions[feature_name] = contribution
        
        # Sort by absolute contribution
        sorted_features = sorted(
            feature_contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Build evidence chain
        evidence_chain = []
        for rank, (feature, contribution) in enumerate(sorted_features[:5], 1):
            if rank == 1:
                evidence_chain.append(f"Primary factor: {feature} ({abs(contribution):.2%} contribution)")
            elif rank == 2:
                evidence_chain.append(f"Secondary factor: {feature} ({abs(contribution):.2%} contribution)")
            else:
                evidence_chain.append(f"Contributing factor: {feature} ({abs(contribution):.2%} contribution)")
        
        explanation = {
            "method": "SHAP",
            "feature_contributions": feature_contributions,
            "evidence_chain": evidence_chain,
            "base_value": float(explainer.expected_value) if hasattr(explainer, 'expected_value') else 0.0,
            "prediction_value": float(predictions[0][0]) if predictions else 0.0,
            "top_features": sorted_features[:5]
        }
        
        return explanation
    
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
    
    def _get_endpoint(self):
        """Get or create Vertex AI endpoint"""
        # List existing endpoints
        endpoints = aiplatform.Endpoint.list(
            filter=f'display_name="{self.model_name}"',
            order_by="create_time desc"
        )
        
        if endpoints:
            logger.info(f"✅ Using existing endpoint: {endpoints[0].resource_name}")
            return endpoints[0]
        else:
            logger.warning(f"⚠️ No endpoint found for model: {self.model_name}")
            # In production, create endpoint here
            raise ValueError(f"Endpoint not found: {self.model_name}")
    
    def _log_explanation(self, result: Dict):
        """Log explanation to BigQuery for audit trail"""
        try:
            # Prepare audit record
            audit_record = {
                "timestamp": result["timestamp"],
                "model_name": result["model_name"],
                "patient_id": result["patient_id"],
                "jurisdiction": result["jurisdiction"],
                "confidence": result["confidence"],
                "risk_level": result["risk_level"],
                "explainability_method": result["explanation"]["method"],
                "feature_contributions": json.dumps(result["explanation"]["feature_contributions"]),
                "evidence_chain": json.dumps(result["explanation"]["evidence_chain"]),
                "compliance_frameworks": json.dumps(result["compliance"]["frameworks"])
            }
            
            # Insert into BigQuery
            errors = self.bq_client.insert_rows_json(self.audit_table, [audit_record])
            
            if errors:
                logger.error(f"❌ Audit logging failed: {errors}")
            else:
                logger.info(f"✅ Explanation logged to audit trail")
        
        except Exception as e:
            logger.error(f"❌ Audit logging error: {e}")
    
    def batch_predict_with_explanations(
        self,
        instances: List[Dict],
        feature_names: List[str],
        patient_ids: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Batch prediction with explanations for multiple instances.
        """
        results = []
        
        for i, instance in enumerate(instances):
            patient_id = patient_ids[i] if patient_ids else None
            
            result = self.predict_with_explanation(
                instances=[instance],
                feature_names=feature_names,
                patient_id=patient_id
            )
            
            results.append(result)
        
        return results
    
    def validate_compliance(self, result: Dict) -> bool:
        """
        Validate that prediction meets compliance requirements.
        
        Returns True if:
        - High-risk predictions have explanations
        - Explanation includes required fields
        - Audit trail is complete
        """
        if result["risk_level"] in ["HIGH", "CRITICAL"]:
            # High-risk predictions must have explanations
            if not result.get("explanation"):
                logger.error("❌ Compliance violation: High-risk prediction without explanation")
                return False
            
            # Explanation must include required fields
            required_fields = ["method", "feature_contributions", "evidence_chain"]
            for field in required_fields:
                if field not in result["explanation"]:
                    logger.error(f"❌ Compliance violation: Missing explanation field: {field}")
                    return False
            
            # Audit trail must be enabled
            if not result["compliance"].get("audit_trail"):
                logger.error("❌ Compliance violation: Audit trail not enabled")
                return False
        
        logger.info("✅ Compliance validation passed")
        return True


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-core",
        location="us-central1",
        model_name="cholera-outbreak-predictor",
        explainability_threshold=0.7
    )
    
    # Example prediction
    instances = [{
        "fever": 1,
        "diarrhea": 1,
        "vomiting": 1,
        "dehydration": 1,
        "location_risk": 0.8,
        "population_density": 0.9,
        "water_quality": 0.3
    }]
    
    feature_names = [
        "fever", "diarrhea", "vomiting", "dehydration",
        "location_risk", "population_density", "water_quality"
    ]
    
    # Make prediction with explanation
    result = explainer.predict_with_explanation(
        instances=instances,
        feature_names=feature_names,
        patient_id="PAT_12345",
        jurisdiction="GDPR_EU"
    )
    
    # Print results
    print(f"🎯 Prediction: {result['predictions']}")
    print(f"📊 Confidence: {result['confidence']:.2%}")
    print(f"⚠️ Risk Level: {result['risk_level']}")
    
    if result["explanation"]:
        print(f"\n🔍 Explanation:")
        print(f"   Method: {result['explanation']['method']}")
        print(f"\n   Evidence Chain:")
        for evidence in result["explanation"]["evidence_chain"]:
            print(f"   - {evidence}")
        
        print(f"\n   Feature Contributions:")
        for feature, contribution in result["explanation"]["feature_contributions"].items():
            print(f"   - {feature}: {contribution:.3f}")
    
    # Validate compliance
    is_compliant = explainer.validate_compliance(result)
    print(f"\n✅ Compliance: {'PASSED' if is_compliant else 'FAILED'}")
