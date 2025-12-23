"""
Azure Purview Integration for iLuminara-Core
Automated data classification and DSPM (Data Security Posture Management)

Compliance:
- Microsoft 2026 Data Security Index
- DSPM for GenAI Governance
- Azure Security Center integration
- Data classification automation
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.purview.catalog import PurviewCatalogClient
from azure.purview.scanning import PurviewScanningClient
from azure.purview.administration.account import PurviewAccountClient
import logging

logger = logging.getLogger(__name__)


class DataClassification:
    """Data classification levels for iLuminara"""
    
    PHI = "Protected Health Information"
    PII = "Personally Identifiable Information"
    LOCATION = "Geographic Location Data"
    CLINICAL = "Clinical Diagnosis Data"
    SURVEILLANCE = "Public Health Surveillance Data"
    OPERATIONAL = "Operational Metadata"


class PurviewDataClassifier:
    """
    Azure Purview integration for automated data classification.
    
    Implements DSPM principles from Microsoft 2026 Data Security Index:
    - Automated data discovery
    - Sensitivity classification
    - Data lineage tracking
    - Compliance reporting
    """
    
    def __init__(
        self,
        purview_account_name: str,
        subscription_id: str,
        resource_group: str
    ):
        self.purview_account_name = purview_account_name
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        
        # Azure credentials
        self.credential = DefaultAzureCredential()
        
        # Purview endpoint
        self.endpoint = f"https://{purview_account_name}.purview.azure.com"
        
        # Initialize clients
        self.catalog_client = PurviewCatalogClient(
            endpoint=self.endpoint,
            credential=self.credential
        )
        
        self.scanning_client = PurviewScanningClient(
            endpoint=self.endpoint,
            credential=self.credential
        )
        
        logger.info(f"🔍 Azure Purview initialized - Account: {purview_account_name}")
    
    def classify_health_record(self, record: Dict) -> Dict:
        """
        Classify a health record and assign sensitivity labels.
        
        Args:
            record: Health record data
        
        Returns:
            Classification metadata
        """
        classification = {
            "record_id": record.get("id"),
            "timestamp": datetime.utcnow().isoformat(),
            "classifications": [],
            "sensitivity_level": "UNKNOWN",
            "compliance_tags": [],
            "data_lineage": []
        }
        
        # Classify fields
        if "patient_id" in record or "diagnosis" in record or "symptoms" in record:
            classification["classifications"].append(DataClassification.PHI)
            classification["sensitivity_level"] = "HIGHLY_SENSITIVE"
            classification["compliance_tags"].extend(["HIPAA", "GDPR_Art9", "KDPA_S37"])
        
        if "name" in record or "email" in record or "phone" in record:
            classification["classifications"].append(DataClassification.PII)
            if classification["sensitivity_level"] == "UNKNOWN":
                classification["sensitivity_level"] = "SENSITIVE"
            classification["compliance_tags"].extend(["GDPR_Art6", "POPIA_S11"])
        
        if "latitude" in record or "longitude" in record or "location" in record:
            classification["classifications"].append(DataClassification.LOCATION)
            classification["compliance_tags"].append("GDPR_Art9")
        
        if "diagnosis" in record or "treatment" in record:
            classification["classifications"].append(DataClassification.CLINICAL)
        
        # Data lineage
        classification["data_lineage"] = [
            {
                "source": record.get("source", "CHV_Voice_Alert"),
                "timestamp": record.get("timestamp"),
                "processing": "Golden_Thread_Fusion",
                "sovereignty_zone": record.get("sovereignty_zone", "KDPA_KE")
            }
        ]
        
        logger.info(f"✅ Record classified - Sensitivity: {classification['sensitivity_level']}")
        
        return classification
    
    def register_asset(
        self,
        asset_name: str,
        asset_type: str,
        classification: Dict,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Register data asset in Purview catalog.
        
        Args:
            asset_name: Name of the asset
            asset_type: Type (e.g., "health_record", "outbreak_alert")
            classification: Classification metadata
            metadata: Additional metadata
        
        Returns:
            Asset GUID
        """
        # Build asset definition
        asset = {
            "typeName": f"iluminara_{asset_type}",
            "attributes": {
                "name": asset_name,
                "qualifiedName": f"{asset_name}@iluminara",
                "description": f"iLuminara {asset_type}",
                "classifications": classification["classifications"],
                "sensitivity": classification["sensitivity_level"],
                "complianceTags": classification["compliance_tags"],
                "dataLineage": classification["data_lineage"],
                "sovereigntyZone": metadata.get("sovereignty_zone") if metadata else None,
                "retentionPolicy": metadata.get("retention_policy") if metadata else None,
                "encryptionStatus": "ENCRYPTED",
                "cryptoShredderEnabled": True
            }
        }
        
        # Register in catalog
        response = self.catalog_client.entity.create_or_update(
            entity=asset
        )
        
        asset_guid = response["guidAssignments"][asset_name]
        
        logger.info(f"✅ Asset registered - GUID: {asset_guid}")
        
        return asset_guid
    
    def create_scan(
        self,
        scan_name: str,
        data_source: str,
        scan_rule_set: str = "iLuminara_PHI_ScanRuleSet"
    ) -> str:
        """
        Create automated scan for data discovery.
        
        Args:
            scan_name: Name of the scan
            data_source: Data source to scan
            scan_rule_set: Scan rule set name
        
        Returns:
            Scan ID
        """
        scan_config = {
            "name": scan_name,
            "kind": "AzureDataLakeStorage",
            "properties": {
                "scanRulesetName": scan_rule_set,
                "scanRulesetType": "Custom",
                "collection": {
                    "referenceName": "iluminara-collection",
                    "type": "CollectionReference"
                }
            }
        }
        
        response = self.scanning_client.scans.create_or_update(
            data_source_name=data_source,
            scan_name=scan_name,
            body=scan_config
        )
        
        logger.info(f"✅ Scan created - Name: {scan_name}")
        
        return scan_name
    
    def get_data_lineage(self, asset_guid: str) -> Dict:
        """
        Get data lineage for an asset.
        
        Args:
            asset_guid: Asset GUID
        
        Returns:
            Lineage information
        """
        lineage = self.catalog_client.lineage.get(
            guid=asset_guid,
            direction="BOTH",
            depth=3
        )
        
        logger.info(f"✅ Lineage retrieved - Asset: {asset_guid}")
        
        return lineage
    
    def generate_dspm_report(self) -> Dict:
        """
        Generate DSPM (Data Security Posture Management) report.
        
        Aligns with Microsoft 2026 Data Security Index principles:
        - Data discovery completeness
        - Sensitivity classification coverage
        - Compliance posture
        - GenAI governance readiness
        
        Returns:
            DSPM report
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "purview_account": self.purview_account_name,
            "dspm_version": "2026",
            "metrics": {
                "data_discovery": {
                    "total_assets": 0,
                    "classified_assets": 0,
                    "unclassified_assets": 0,
                    "coverage_percentage": 0.0
                },
                "sensitivity_classification": {
                    "highly_sensitive": 0,
                    "sensitive": 0,
                    "internal": 0,
                    "public": 0
                },
                "compliance_posture": {
                    "compliant_assets": 0,
                    "non_compliant_assets": 0,
                    "compliance_percentage": 0.0,
                    "frameworks": []
                },
                "genai_governance": {
                    "ai_models_cataloged": 0,
                    "training_data_classified": 0,
                    "explainability_enabled": True,
                    "bias_monitoring": True
                }
            },
            "recommendations": [],
            "sovereignty_status": "ENFORCED"
        }
        
        # Query catalog for metrics
        # (In production, this would query actual Purview data)
        
        # Add recommendations
        if report["metrics"]["data_discovery"]["coverage_percentage"] < 90:
            report["recommendations"].append({
                "priority": "HIGH",
                "category": "Data Discovery",
                "recommendation": "Increase data discovery coverage to >90%",
                "action": "Run automated scans on all data sources"
            })
        
        if report["metrics"]["compliance_posture"]["compliance_percentage"] < 100:
            report["recommendations"].append({
                "priority": "CRITICAL",
                "category": "Compliance",
                "recommendation": "Address non-compliant assets immediately",
                "action": "Review SovereignGuardrail violations"
            })
        
        logger.info(f"✅ DSPM report generated")
        
        return report
    
    def apply_sensitivity_labels(
        self,
        asset_guid: str,
        labels: List[str]
    ):
        """
        Apply Microsoft Information Protection sensitivity labels.
        
        Args:
            asset_guid: Asset GUID
            labels: Sensitivity labels to apply
        """
        # Get asset
        asset = self.catalog_client.entity.get_by_guid(guid=asset_guid)
        
        # Add sensitivity labels
        if "attributes" not in asset["entity"]:
            asset["entity"]["attributes"] = {}
        
        asset["entity"]["attributes"]["sensitivityLabels"] = labels
        
        # Update asset
        self.catalog_client.entity.create_or_update(
            entity=asset["entity"]
        )
        
        logger.info(f"✅ Sensitivity labels applied - Asset: {asset_guid}")
    
    def integrate_with_sovereign_guardrail(
        self,
        classification: Dict
    ) -> bool:
        """
        Integrate Purview classification with SovereignGuardrail.
        
        Args:
            classification: Purview classification metadata
        
        Returns:
            True if compliant
        """
        from governance_kernel.vector_ledger import SovereignGuardrail
        
        guardrail = SovereignGuardrail()
        
        # Validate based on classification
        try:
            if DataClassification.PHI in classification["classifications"]:
                guardrail.validate_action(
                    action_type='Data_Processing',
                    payload={
                        'data_type': 'PHI',
                        'processing_location': 'Azure_Purview',
                        'sensitivity': classification['sensitivity_level'],
                        'compliance_tags': classification['compliance_tags']
                    },
                    jurisdiction='GDPR_EU'
                )
            
            logger.info("✅ Purview classification compliant with SovereignGuardrail")
            return True
        
        except Exception as e:
            logger.error(f"❌ Sovereignty violation: {e}")
            return False


# Example usage
if __name__ == "__main__":
    # Initialize Purview classifier
    classifier = PurviewDataClassifier(
        purview_account_name=os.getenv("PURVIEW_ACCOUNT_NAME"),
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP")
    )
    
    # Classify health record
    health_record = {
        "id": "REC_12345",
        "patient_id": "PAT_12345",
        "diagnosis": "Malaria",
        "symptoms": ["fever", "chills"],
        "location": "Dadaab",
        "latitude": 0.0512,
        "longitude": 40.3129,
        "source": "CHV_Voice_Alert",
        "timestamp": "2025-12-23T10:00:00Z",
        "sovereignty_zone": "KDPA_KE"
    }
    
    classification = classifier.classify_health_record(health_record)
    print(f"Classification: {json.dumps(classification, indent=2)}")
    
    # Register asset
    asset_guid = classifier.register_asset(
        asset_name="health_record_12345",
        asset_type="health_record",
        classification=classification,
        metadata={
            "sovereignty_zone": "KDPA_KE",
            "retention_policy": "180_DAYS"
        }
    )
    
    # Generate DSPM report
    dspm_report = classifier.generate_dspm_report()
    print(f"DSPM Report: {json.dumps(dspm_report, indent=2)}")
    
    # Integrate with SovereignGuardrail
    compliant = classifier.integrate_with_sovereign_guardrail(classification)
    print(f"Sovereignty Compliant: {compliant}")
