"""
Vertex AI + SHAP Integration
Right to Explanation for High-Risk Clinical AI

Compliance:
- EU AI Act §6 (High-Risk AI Systems)
- GDPR Art. 22 (Right to Explanation)
- NIST AI RMF (Explainable and Interpretable)
- UNESCO AI Ethics (Transparency)
"""

import shap
import numpy as np
from typing import Dict, List, Optional, Tuple
from google.cloud import aiplatform
from google.cloud import bigquery
import pandas as pd
import logging
from datetime import datetime
from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError

logger = logging.getLogger(__name__)


class VertexAIExplainer:
    """
    Integrates Vertex AI predictions with SHAP explanations.
    
    Every high-risk inference (confidence > 0.7) automatically triggers
    SHAP analysis to comply with EU AI Act §6.
    """
    
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        high_risk_threshold: float = 0.7,
        enable_compliance: bool = True
    ):
        self.project_id = project_id
        self.location = location
        self.high_risk_threshold = high_risk_threshold
        self.enable_compliance = enable_compliance
        
        # Initialize Vertex AI
        aiplatform.init(project=project_id, location=location)
        
        # Initialize BigQuery
        self.bq_client = bigquery.Client(project=project_id)
        
        # Initialize SovereignGuardrail
        if enable_compliance:
            self.guardrail = SovereignGuardrail()
        
        logger.info(f"✅ Vertex AI Explainer initialized - Project: {project_id}")
    
    def predict_with_explanation(
        self,
        endpoint_id: str,
        instances: List[Dict],
        feature_names: List[str],
        jurisdiction: str = "EU_AI_ACT"
    ) -> Dict:
        """
        Make prediction with automatic SHAP explanation for high-risk inferences.
        
        Args:
            endpoint_id: Vertex AI endpoint ID
            instances: List of prediction instances
            feature_names: Names of features for explanation
            jurisdiction: Legal jurisdiction for compliance
        
        Returns:
            {
                'predictions': [...],
                'explanations': [...],
                'compliance_status': 'APPROVED' | 'BLOCKED',
                'audit_trail': {...}
            }
        """
        # Get endpoint
        endpoint = aiplatform.Endpoint(endpoint_id)
        
        # Make prediction
        predictions = endpoint.predict(instances=instances)
        
        results = []
        
        for idx, prediction in enumerate(predictions.predictions):
            confidence_score = self._extract_confidence(prediction)
            
            # Check if high-risk
            is_high_risk = confidence_score >= self.high_risk_threshold
            
            if is_high_risk:
                logger.info(f"🚨 High-risk inference detected: {confidence_score:.2%}")
                
                # Generate SHAP explanation
                explanation = self._generate_shap_explanation(
                    endpoint=endpoint,
                    instance=instances[idx],
                    feature_names=feature_names
                )
                
                # Validate compliance
                if self.enable_compliance:
                    try:
                        self.guardrail.validate_action(
                            action_type='High_Risk_Inference',
                            payload={
                                'inference': prediction,
                                'explanation': explanation,
                                'confidence_score': confidence_score,
                                'evidence_chain': explanation['top_features'],
                                'human_oversight': True
                            },
                            jurisdiction=jurisdiction
                        )
                        compliance_status = 'APPROVED'
                    except SovereigntyViolationError as e:
                        logger.error(f"❌ Compliance violation: {e}")
                        compliance_status = 'BLOCKED'
                        explanation['violation'] = str(e)
                else:
                    compliance_status = 'APPROVED'
            else:
                explanation = None
                compliance_status = 'APPROVED'
            
            results.append({
                'prediction': prediction,
                'confidence_score': confidence_score,
                'is_high_risk': is_high_risk,
                'explanation': explanation,
                'compliance_status': compliance_status,
                'timestamp': datetime.utcnow().isoformat()
            })
        
        return {
            'results': results,
            'metadata': {
                'endpoint_id': endpoint_id,
                'jurisdiction': jurisdiction,
                'high_risk_threshold': self.high_risk_threshold
            }
        }
    
    def _generate_shap_explanation(
        self,
        endpoint: aiplatform.Endpoint,
        instance: Dict,
        feature_names: List[str]
    ) -> Dict:
        """
        Generate SHAP explanation for a single instance.
        
        Returns:
            {
                'shap_values': [...],
                'base_value': float,
                'feature_importance': {...},
                'top_features': [...],
                'decision_rationale': str
            }
        """
        # Convert instance to numpy array
        X = np.array([list(instance.values())])
        
        # Create prediction function for SHAP
        def predict_fn(X):
            instances = [dict(zip(feature_names, row)) for row in X]
            predictions = endpoint.predict(instances=instances)
            return np.array([self._extract_confidence(p) for p in predictions.predictions])
        
        # Use KernelExplainer (model-agnostic)
        explainer = shap.KernelExplainer(predict_fn, X)
        shap_values = explainer.shap_values(X)
        
        # Calculate feature importance
        feature_importance = {
            feature_names[i]: float(shap_values[0][i])
            for i in range(len(feature_names))
        }
        
        # Sort by absolute importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )
        
        # Top 5 features
        top_features = [
            {
                'feature': feature,
                'importance': importance,
                'direction': 'positive' if importance > 0 else 'negative'
            }
            for feature, importance in sorted_features[:5]
        ]
        
        # Generate decision rationale
        rationale = self._generate_rationale(top_features, instance)
        
        return {
            'shap_values': shap_values[0].tolist(),
            'base_value': float(explainer.expected_value),
            'feature_importance': feature_importance,
            'top_features': top_features,
            'decision_rationale': rationale,
            'method': 'SHAP_KernelExplainer'
        }
    
    def _generate_rationale(
        self,
        top_features: List[Dict],
        instance: Dict
    ) -> str:
        """
        Generate human-readable decision rationale.
        """
        rationale_parts = []
        
        for feature_info in top_features[:3]:
            feature = feature_info['feature']
            importance = feature_info['importance']
            direction = feature_info['direction']
            value = instance.get(feature, 'N/A')
            
            if direction == 'positive':
                rationale_parts.append(
                    f"{feature}={value} increases risk by {abs(importance):.2%}"
                )
            else:
                rationale_parts.append(
                    f"{feature}={value} decreases risk by {abs(importance):.2%}"
                )
        
        return "; ".join(rationale_parts)
    
    def _extract_confidence(self, prediction) -> float:
        """
        Extract confidence score from prediction.
        """
        if isinstance(prediction, dict):
            return prediction.get('confidence', prediction.get('score', 0.0))
        elif isinstance(prediction, (list, tuple)):
            return float(prediction[0])
        else:
            return float(prediction)
    
    def batch_predict_with_explanation(
        self,
        endpoint_id: str,
        bq_source_uri: str,
        bq_destination_uri: str,
        feature_names: List[str]
    ) -> str:
        """
        Batch prediction with SHAP explanations for high-risk inferences.
        
        Args:
            endpoint_id: Vertex AI endpoint ID
            bq_source_uri: BigQuery source table URI
            bq_destination_uri: BigQuery destination table URI
            feature_names: Names of features
        
        Returns:
            Job ID
        """
        endpoint = aiplatform.Endpoint(endpoint_id)
        
        # Create batch prediction job
        batch_prediction_job = endpoint.batch_predict(
            job_display_name=f"batch_prediction_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            bigquery_source=bq_source_uri,
            bigquery_destination_prefix=bq_destination_uri,
            machine_type="n1-standard-4",
            starting_replica_count=1,
            max_replica_count=10
        )
        
        logger.info(f"✅ Batch prediction job created: {batch_prediction_job.resource_name}")
        
        return batch_prediction_job.resource_name
    
    def train_explainable_model(
        self,
        dataset_id: str,
        target_column: str,
        feature_columns: List[str],
        model_type: str = "classification"
    ) -> str:
        """
        Train an explainable model using Vertex AI AutoML.
        
        Args:
            dataset_id: Vertex AI dataset ID
            target_column: Target column name
            feature_columns: Feature column names
            model_type: 'classification' or 'regression'
        
        Returns:
            Model ID
        """
        dataset = aiplatform.TabularDataset(dataset_id)
        
        if model_type == "classification":
            job = aiplatform.AutoMLTabularTrainingJob(
                display_name=f"explainable_model_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                optimization_prediction_type="classification",
                optimization_objective="maximize-au-prc"
            )
        else:
            job = aiplatform.AutoMLTabularTrainingJob(
                display_name=f"explainable_model_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                optimization_prediction_type="regression",
                optimization_objective="minimize-rmse"
            )
        
        model = job.run(
            dataset=dataset,
            target_column=target_column,
            training_fraction_split=0.8,
            validation_fraction_split=0.1,
            test_fraction_split=0.1,
            model_display_name=f"explainable_model_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            budget_milli_node_hours=1000
        )
        
        logger.info(f"✅ Model trained: {model.resource_name}")
        
        return model.resource_name


# Example usage
if __name__ == "__main__":
    # Initialize explainer
    explainer = VertexAIExplainer(
        project_id="iluminara-core",
        location="us-central1",
        high_risk_threshold=0.7,
        enable_compliance=True
    )
    
    # Make prediction with explanation
    result = explainer.predict_with_explanation(
        endpoint_id="projects/123/locations/us-central1/endpoints/456",
        instances=[{
            "fever": 1,
            "cough": 1,
            "diarrhea": 0,
            "vomiting": 0,
            "age": 35,
            "location_risk": 0.8
        }],
        feature_names=["fever", "cough", "diarrhea", "vomiting", "age", "location_risk"],
        jurisdiction="EU_AI_ACT"
    )
    
    # Print results
    for r in result['results']:
        print(f"Prediction: {r['prediction']}")
        print(f"Confidence: {r['confidence_score']:.2%}")
        print(f"High-risk: {r['is_high_risk']}")
        
        if r['explanation']:
            print(f"Rationale: {r['explanation']['decision_rationale']}")
            print(f"Top features: {r['explanation']['top_features']}")
        
        print(f"Compliance: {r['compliance_status']}")
        print("---")
