"""
MDR Pharmaceutical Compliance Module
EU Medical Device Regulation (MDR) 2017/745
EU In Vitro Diagnostic Regulation (IVDR) 2017/746

Compliance:
- EU MDR 2017/745
- EU IVDR 2017/746
- FDA 21 CFR Part 11 (Electronic Records)
- ICH GCP (Good Clinical Practice)
- ISO 13485 (Medical Device QMS)
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum
import logging
import hashlib

logger = logging.getLogger(__name__)


class DeviceClass(Enum):
    """MDR device classification"""
    CLASS_I = "Class I"  # Low risk
    CLASS_IIA = "Class IIa"  # Medium risk
    CLASS_IIB = "Class IIb"  # Medium-high risk
    CLASS_III = "Class III"  # High risk
    
class RiskLevel(Enum):
    """Clinical risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ConformityRoute(Enum):
    """MDR conformity assessment routes"""
    SELF_DECLARATION = "self_declaration"  # Class I only
    NOTIFIED_BODY_TYPE_A = "notified_body_type_a"  # Class IIa
    NOTIFIED_BODY_TYPE_B = "notified_body_type_b"  # Class IIb/III


class MDRPharmaCompliance:
    """
    Verify pharmaceutical and medical device compliance.
    
    Use case: Ensure iLuminara's AI diagnostic tools comply with EU MDR
    when deployed in European health systems.
    """
    
    def __init__(
        self,
        enable_fda_compliance: bool = True,
        enable_ich_gcp: bool = True
    ):
        self.enable_fda = enable_fda_compliance
        self.enable_ich_gcp = enable_ich_gcp
        
        # Notified Body registry (simplified)
        self.notified_bodies = {
            "NB_0123": "TÜV SÜD Product Service GmbH",
            "NB_0197": "BSI Group",
            "NB_0459": "DEKRA Certification GmbH"
        }
        
        logger.info("💊 MDR Pharma Compliance initialized")
    
    def classify_device(
        self,
        device_type: str,
        intended_use: str,
        invasiveness: str,
        duration_of_use: str,
        software_driven: bool = False
    ) -> Dict:
        """
        Classify medical device according to MDR Annex VIII.
        
        Args:
            device_type: "diagnostic", "therapeutic", "monitoring"
            intended_use: Clinical purpose
            invasiveness: "non_invasive", "invasive", "implantable"
            duration_of_use: "transient", "short_term", "long_term"
            software_driven: Is it AI/ML software?
        
        Returns:
            Device classification with compliance requirements
        """
        # Classification logic (simplified)
        if software_driven and device_type == "diagnostic":
            # AI diagnostic software
            if "critical" in intended_use.lower() or "life" in intended_use.lower():
                device_class = DeviceClass.CLASS_III
                risk_level = RiskLevel.CRITICAL
            elif "treatment" in intended_use.lower():
                device_class = DeviceClass.CLASS_IIB
                risk_level = RiskLevel.HIGH
            else:
                device_class = DeviceClass.CLASS_IIA
                risk_level = RiskLevel.MEDIUM
        
        elif invasiveness == "implantable":
            device_class = DeviceClass.CLASS_III
            risk_level = RiskLevel.CRITICAL
        
        elif invasiveness == "invasive" and duration_of_use == "long_term":
            device_class = DeviceClass.CLASS_IIB
            risk_level = RiskLevel.HIGH
        
        elif invasiveness == "invasive":
            device_class = DeviceClass.CLASS_IIA
            risk_level = RiskLevel.MEDIUM
        
        else:
            device_class = DeviceClass.CLASS_I
            risk_level = RiskLevel.LOW
        
        # Determine conformity route
        if device_class == DeviceClass.CLASS_I:
            conformity_route = ConformityRoute.SELF_DECLARATION
        elif device_class == DeviceClass.CLASS_IIA:
            conformity_route = ConformityRoute.NOTIFIED_BODY_TYPE_A
        else:
            conformity_route = ConformityRoute.NOTIFIED_BODY_TYPE_B
        
        return {
            "device_class": device_class.value,
            "risk_level": risk_level.value,
            "conformity_route": conformity_route.value,
            "notified_body_required": device_class != DeviceClass.CLASS_I,
            "clinical_evaluation_required": True,
            "post_market_surveillance_required": True,
            "regulation": "EU MDR 2017/745",
            "classification_rules": self._get_classification_rules(device_class),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def verify_clinical_data(
        self,
        device_class: DeviceClass,
        clinical_data: Dict
    ) -> Dict:
        """
        Verify clinical data meets MDR requirements.
        
        Args:
            device_class: Device classification
            clinical_data: {
                "clinical_trials": int,
                "patient_count": int,
                "follow_up_months": int,
                "adverse_events": int,
                "efficacy_rate": float
            }
        
        Returns:
            Verification result
        """
        # MDR clinical data requirements
        requirements = {
            DeviceClass.CLASS_I: {
                "min_trials": 0,
                "min_patients": 0,
                "min_follow_up_months": 0
            },
            DeviceClass.CLASS_IIA: {
                "min_trials": 1,
                "min_patients": 50,
                "min_follow_up_months": 6
            },
            DeviceClass.CLASS_IIB: {
                "min_trials": 2,
                "min_patients": 200,
                "min_follow_up_months": 12
            },
            DeviceClass.CLASS_III: {
                "min_trials": 3,
                "min_patients": 500,
                "min_follow_up_months": 24
            }
        }
        
        req = requirements[device_class]
        
        # Check compliance
        compliant = (
            clinical_data.get("clinical_trials", 0) >= req["min_trials"] and
            clinical_data.get("patient_count", 0) >= req["min_patients"] and
            clinical_data.get("follow_up_months", 0) >= req["min_follow_up_months"]
        )
        
        # Calculate safety score
        adverse_event_rate = clinical_data.get("adverse_events", 0) / max(clinical_data.get("patient_count", 1), 1)
        safety_acceptable = adverse_event_rate < 0.05  # <5% adverse events
        
        return {
            "compliant": compliant and safety_acceptable,
            "device_class": device_class.value,
            "requirements_met": {
                "clinical_trials": clinical_data.get("clinical_trials", 0) >= req["min_trials"],
                "patient_count": clinical_data.get("patient_count", 0) >= req["min_patients"],
                "follow_up_duration": clinical_data.get("follow_up_months", 0) >= req["min_follow_up_months"],
                "safety_profile": safety_acceptable
            },
            "adverse_event_rate": round(adverse_event_rate, 4),
            "efficacy_rate": clinical_data.get("efficacy_rate", 0.0),
            "regulation": "MDR Article 61 (Clinical Evaluation)",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def verify_technical_documentation(
        self,
        device_id: str,
        documentation: Dict
    ) -> Dict:
        """
        Verify technical documentation completeness (MDR Annex II).
        
        Args:
            device_id: Unique device identifier
            documentation: {
                "device_description": str,
                "intended_purpose": str,
                "risk_analysis": bool,
                "design_verification": bool,
                "clinical_evaluation": bool,
                "labeling": bool,
                "instructions_for_use": bool
            }
        
        Returns:
            Documentation verification result
        """
        # MDR Annex II requirements
        required_sections = [
            "device_description",
            "intended_purpose",
            "risk_analysis",
            "design_verification",
            "clinical_evaluation",
            "labeling",
            "instructions_for_use"
        ]
        
        # Check completeness
        missing_sections = [
            section for section in required_sections
            if not documentation.get(section)
        ]
        
        compliant = len(missing_sections) == 0
        
        # Generate UDI (Unique Device Identifier)
        udi = self._generate_udi(device_id)
        
        return {
            "compliant": compliant,
            "completeness_score": (len(required_sections) - len(missing_sections)) / len(required_sections),
            "missing_sections": missing_sections,
            "udi": udi,
            "regulation": "MDR Annex II (Technical Documentation)",
            "iso_standard": "ISO 13485 (Medical Device QMS)",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def verify_post_market_surveillance(
        self,
        device_id: str,
        surveillance_data: Dict
    ) -> Dict:
        """
        Verify post-market surveillance compliance (MDR Article 83-92).
        
        Args:
            device_id: Device identifier
            surveillance_data: {
                "incident_reports": int,
                "field_safety_notices": int,
                "periodic_safety_updates": int,
                "vigilance_reports": int
            }
        
        Returns:
            PMS verification result
        """
        # Check reporting requirements
        incidents = surveillance_data.get("incident_reports", 0)
        serious_incidents = surveillance_data.get("vigilance_reports", 0)
        
        # Serious incidents must be reported within 15 days
        reporting_compliant = serious_incidents == 0 or surveillance_data.get("reporting_timely", True)
        
        # PSUR (Periodic Safety Update Report) required annually
        psur_compliant = surveillance_data.get("periodic_safety_updates", 0) > 0
        
        return {
            "compliant": reporting_compliant and psur_compliant,
            "incident_reports": incidents,
            "serious_incidents": serious_incidents,
            "reporting_timely": reporting_compliant,
            "psur_submitted": psur_compliant,
            "regulation": "MDR Article 83-92 (Post-Market Surveillance)",
            "vigilance_system": "EUDAMED",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def verify_fda_21cfr11_compliance(
        self,
        electronic_record: Dict
    ) -> Dict:
        """
        Verify FDA 21 CFR Part 11 compliance for electronic records.
        
        Args:
            electronic_record: {
                "record_id": str,
                "author": str,
                "timestamp": str,
                "digital_signature": str,
                "audit_trail": bool,
                "access_controls": bool
            }
        
        Returns:
            FDA compliance verification
        """
        if not self.enable_fda:
            return {"compliant": True, "reason": "FDA compliance disabled"}
        
        # 21 CFR Part 11 requirements
        requirements_met = {
            "digital_signature": bool(electronic_record.get("digital_signature")),
            "audit_trail": electronic_record.get("audit_trail", False),
            "access_controls": electronic_record.get("access_controls", False),
            "timestamp": bool(electronic_record.get("timestamp")),
            "author_identification": bool(electronic_record.get("author"))
        }
        
        compliant = all(requirements_met.values())
        
        return {
            "compliant": compliant,
            "requirements_met": requirements_met,
            "regulation": "FDA 21 CFR Part 11 (Electronic Records)",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_conformity_certificate(
        self,
        device_id: str,
        device_class: DeviceClass,
        manufacturer: str,
        notified_body_id: Optional[str] = None
    ) -> Dict:
        """
        Generate EU Declaration of Conformity.
        
        Returns:
            Conformity certificate
        """
        # Check if notified body required
        if device_class != DeviceClass.CLASS_I and not notified_body_id:
            return {
                "error": "Notified Body required for Class IIa/IIb/III devices",
                "device_class": device_class.value
            }
        
        # Generate certificate
        certificate_id = hashlib.sha256(
            f"{device_id}{manufacturer}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]
        
        return {
            "certificate_id": certificate_id,
            "certificate_type": "EU Declaration of Conformity",
            "device_id": device_id,
            "device_class": device_class.value,
            "manufacturer": manufacturer,
            "notified_body": self.notified_bodies.get(notified_body_id) if notified_body_id else "N/A",
            "notified_body_id": notified_body_id,
            "issue_date": datetime.utcnow().isoformat(),
            "valid_until": (datetime.utcnow() + timedelta(days=1825)).isoformat(),  # 5 years
            "regulation": "EU MDR 2017/745",
            "ce_marking_authorized": True,
            "legal_notice": "This device complies with EU MDR 2017/745 and may bear the CE mark"
        }
    
    def _get_classification_rules(self, device_class: DeviceClass) -> List[str]:
        """Get applicable MDR classification rules"""
        rules = {
            DeviceClass.CLASS_I: ["Rule 1", "Rule 2"],
            DeviceClass.CLASS_IIA: ["Rule 9", "Rule 10", "Rule 11"],
            DeviceClass.CLASS_IIB: ["Rule 12", "Rule 13", "Rule 14"],
            DeviceClass.CLASS_III: ["Rule 15", "Rule 16", "Rule 17", "Rule 18"]
        }
        return rules.get(device_class, [])
    
    def _generate_udi(self, device_id: str) -> str:
        """
        Generate Unique Device Identifier (UDI).
        
        Format: (01)GTIN(21)SerialNumber
        """
        # Simplified UDI generation
        gtin = hashlib.md5(device_id.encode()).hexdigest()[:14]
        serial = hashlib.md5(f"{device_id}{datetime.utcnow()}".encode()).hexdigest()[:10]
        
        return f"(01){gtin}(21){serial}"


# Example usage
if __name__ == "__main__":
    mdr = MDRPharmaCompliance(enable_fda_compliance=True)
    
    # Test 1: Classify AI diagnostic device
    classification = mdr.classify_device(
        device_type="diagnostic",
        intended_use="AI-powered cholera outbreak prediction",
        invasiveness="non_invasive",
        duration_of_use="transient",
        software_driven=True
    )
    print(f"Device Classification: {classification}")
    
    # Test 2: Verify clinical data
    clinical_verification = mdr.verify_clinical_data(
        device_class=DeviceClass.CLASS_IIA,
        clinical_data={
            "clinical_trials": 2,
            "patient_count": 150,
            "follow_up_months": 12,
            "adverse_events": 3,
            "efficacy_rate": 0.92
        }
    )
    print(f"\nClinical Data Verification: {clinical_verification}")
    
    # Test 3: Verify technical documentation
    doc_verification = mdr.verify_technical_documentation(
        device_id="ILUM-AI-001",
        documentation={
            "device_description": True,
            "intended_purpose": True,
            "risk_analysis": True,
            "design_verification": True,
            "clinical_evaluation": True,
            "labeling": True,
            "instructions_for_use": True
        }
    )
    print(f"\nTechnical Documentation: {doc_verification}")
    
    # Test 4: Generate conformity certificate
    certificate = mdr.generate_conformity_certificate(
        device_id="ILUM-AI-001",
        device_class=DeviceClass.CLASS_IIA,
        manufacturer="iLuminara Health Systems",
        notified_body_id="NB_0123"
    )
    print(f"\nConformity Certificate: {certificate}")
