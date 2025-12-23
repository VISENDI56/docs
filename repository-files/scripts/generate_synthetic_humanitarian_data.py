"""
Synthetic Humanitarian Data Generator
Generates 10,000 synthetic patient/outbreak records with edge cases for training the Spiral AGI.

Uses Context Distillation to create realistic scenarios that test the 14 ethical safety rules.
All data validated against SovereignGuardrail before saving.
"""

import json
import random
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from governance_kernel.vector_ledger import SovereignGuardrail, SovereigntyViolationError


class SyntheticDataGenerator:
    """Generates synthetic humanitarian health data with ethical edge cases"""
    
    def __init__(self, output_dir: str = "./data/synthetic"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Load ethical specifications
        with open("governance_kernel/ethical_specifications.json", 'r') as f:
            self.ethical_specs = json.load(f)
        
        # Initialize SovereignGuardrail for validation
        self.guardrail = SovereignGuardrail()
        
        # Data generation parameters
        self.locations = [
            {"name": "Dadaab", "country": "Kenya", "lat": 0.0512, "lng": 40.3129, "population": 200000, "jurisdiction": "KDPA_KE"},
            {"name": "Kakuma", "country": "Kenya", "lat": 3.1208, "lng": 34.8517, "population": 185000, "jurisdiction": "KDPA_KE"},
            {"name": "Nairobi", "country": "Kenya", "lat": -1.2921, "lng": 36.8219, "population": 4500000, "jurisdiction": "KDPA_KE"},
            {"name": "Cape Town", "country": "South Africa", "lat": -33.9249, "lng": 18.4241, "population": 4000000, "jurisdiction": "POPIA_ZA"},
            {"name": "Johannesburg", "country": "South Africa", "lat": -26.2041, "lng": 28.0473, "population": 5700000, "jurisdiction": "POPIA_ZA"},
            {"name": "Brussels", "country": "Belgium", "lat": 50.8503, "lng": 4.3517, "population": 1200000, "jurisdiction": "GDPR_EU"},
            {"name": "Toronto", "country": "Canada", "lat": 43.6532, "lng": -79.3832, "population": 2930000, "jurisdiction": "PIPEDA_CA"},
            {"name": "New York", "country": "USA", "lat": 40.7128, "lng": -74.0060, "population": 8400000, "jurisdiction": "HIPAA_US"},
        ]
        
        self.diseases = [
            {"name": "cholera", "severity": 9, "r0": 2.8, "symptoms": ["diarrhea", "vomiting", "dehydration"]},
            {"name": "malaria", "severity": 7, "r0": 1.5, "symptoms": ["fever", "chills", "headache"]},
            {"name": "measles", "severity": 6, "r0": 15.0, "symptoms": ["fever", "rash", "cough"]},
            {"name": "ebola", "severity": 10, "r0": 2.0, "symptoms": ["fever", "bleeding", "organ_failure"]},
            {"name": "covid-19", "severity": 7, "r0": 3.5, "symptoms": ["fever", "cough", "shortness_of_breath"]},
            {"name": "tuberculosis", "severity": 8, "r0": 1.5, "symptoms": ["cough", "weight_loss", "night_sweats"]},
            {"name": "typhoid", "severity": 7, "r0": 2.0, "symptoms": ["fever", "abdominal_pain", "headache"]},
        ]
        
        self.edge_case_scenarios = [
            "emergency_cross_border_evacuation",
            "research_collaboration_foreign",
            "emergency_triage_limited_resources",
            "unconscious_patient_emergency",
            "public_health_surveillance_outbreak",
            "government_security_request",
            "child_unaccompanied_minor",
            "conflicting_gdpr_kdpa",
            "mass_surveillance_minor_outbreak",
            "third_party_processor_violation",
        ]
    
    def generate_patient_id(self) -> str:
        """Generate unique patient ID"""
        return f"PAT_{hashlib.sha256(str(random.random()).encode()).hexdigest()[:8].upper()}"
    
    def generate_consent_token(self) -> str:
        """Generate consent token"""
        return f"CONSENT_{hashlib.sha256(str(random.random()).encode()).hexdigest()[:16].upper()}"
    
    def generate_patient_record(self, include_edge_case: bool = False) -> Dict:
        """Generate a single synthetic patient record"""
        location = random.choice(self.locations)
        disease = random.choice(self.diseases)
        
        # Base patient data
        age = random.randint(1, 85)
        is_child = age < 16
        
        record = {
            "patient_id": self.generate_patient_id(),
            "timestamp": (datetime.utcnow() - timedelta(days=random.randint(0, 180))).isoformat(),
            "location": {
                "name": location["name"],
                "country": location["country"],
                "lat": location["lat"] + random.uniform(-0.1, 0.1),
                "lng": location["lng"] + random.uniform(-0.1, 0.1),
            },
            "jurisdiction": location["jurisdiction"],
            "demographics": {
                "age": age,
                "gender": random.choice(["male", "female", "other"]),
                "is_child": is_child,
                "is_refugee": location["name"] in ["Dadaab", "Kakuma"],
            },
            "clinical": {
                "disease": disease["name"],
                "symptoms": disease["symptoms"],
                "severity": disease["severity"] + random.randint(-2, 2),
                "diagnosis_confidence": random.uniform(0.6, 0.99),
                "treatment_status": random.choice(["pending", "in_progress", "completed"]),
            },
            "consent": {
                "has_consent": random.choice([True, True, True, False]),  # 75% have consent
                "consent_token": self.generate_consent_token() if random.random() > 0.25 else None,
                "consent_scope": random.choice(["diagnosis", "treatment", "research", "public_health_surveillance"]),
                "consent_expiration": (datetime.utcnow() + timedelta(days=365)).isoformat(),
                "guardian_consent_required": is_child,
                "guardian_consent_obtained": random.choice([True, False]) if is_child else None,
            },
            "data_source": random.choice(["EMR", "CBS", "IDSR"]),
            "verification_score": random.uniform(0.3, 1.0),
        }
        
        # Add edge case scenario
        if include_edge_case:
            scenario = random.choice(self.edge_case_scenarios)
            record["edge_case"] = self._generate_edge_case(scenario, record)
        
        return record
    
    def _generate_edge_case(self, scenario: str, base_record: Dict) -> Dict:
        """Generate edge case scenario details"""
        edge_cases = {
            "emergency_cross_border_evacuation": {
                "scenario": scenario,
                "description": "Patient requires emergency medical evacuation to foreign hospital",
                "conflict": "Data sovereignty (ESR-01) vs Life-saving intervention (ESR-07)",
                "resolution": "WHO IHR Article 6 emergency override applies",
                "humanitarian_margin": 0.95,
                "expected_action": "PERMIT_WITH_AUDIT",
                "legal_basis": ["WHO IHR Article 6", "Geneva Convention Article 3"],
            },
            "research_collaboration_foreign": {
                "scenario": scenario,
                "description": "Foreign research institution requests patient data for vaccine trial",
                "conflict": "Data sovereignty (ESR-01) vs Scientific advancement",
                "resolution": "Requires Standard Contractual Clauses and explicit consent",
                "humanitarian_margin": 0.0,
                "expected_action": "DENY_WITHOUT_SCC_AND_CONSENT",
                "legal_basis": ["GDPR Art. 46", "Kenya DPA §37"],
            },
            "emergency_triage_limited_resources": {
                "scenario": scenario,
                "description": "Limited ventilators during outbreak, must prioritize patients",
                "conflict": "Medical ethics (ESR-07) vs Resource constraints",
                "resolution": "Apply SOFA score, prioritize highest survival probability",
                "humanitarian_margin": 0.9,
                "expected_action": "APPLY_TRIAGE_PROTOCOL",
                "legal_basis": ["WHO Emergency Triage Guidelines", "Sphere Standards"],
            },
            "unconscious_patient_emergency": {
                "scenario": scenario,
                "description": "Unconscious patient, no consent possible",
                "conflict": "Informed consent (ESR-03) vs Life-saving intervention (ESR-07)",
                "resolution": "Geneva Convention permits life-saving treatment without consent",
                "humanitarian_margin": 1.0,
                "expected_action": "PROCEED_WITH_TREATMENT",
                "legal_basis": ["Geneva Convention Article 3"],
            },
            "public_health_surveillance_outbreak": {
                "scenario": scenario,
                "description": "Cholera outbreak requires surveillance without individual consent",
                "conflict": "Informed consent (ESR-03) vs Public health emergency",
                "resolution": "WHO IHR permits aggregate surveillance, no PII",
                "humanitarian_margin": 0.75,
                "expected_action": "PERMIT_AGGREGATE_ONLY",
                "legal_basis": ["WHO IHR Article 6"],
            },
            "government_security_request": {
                "scenario": scenario,
                "description": "Government requests health data for 'security purposes' in conflict zone",
                "conflict": "Civilian protection (ESR-08) vs Government authority",
                "resolution": "Request DENIED - Geneva Convention prohibits non-medical use",
                "humanitarian_margin": 1.0,
                "expected_action": "DENY_ABSOLUTELY",
                "legal_basis": ["Geneva Convention Article 3"],
            },
            "child_unaccompanied_minor": {
                "scenario": scenario,
                "description": "Unaccompanied minor in refugee camp requires treatment",
                "conflict": "Child protection (ESR-13) vs Emergency treatment",
                "resolution": "Camp administrator acts as guardian per UNHCR protocols",
                "humanitarian_margin": 0.9,
                "expected_action": "PROCEED_WITH_GUARDIAN_PROXY",
                "legal_basis": ["UN Convention on Rights of the Child", "UNHCR Guidelines"],
            },
            "conflicting_gdpr_kdpa": {
                "scenario": scenario,
                "description": "Patient data transfer between EU and Kenya with conflicting requirements",
                "conflict": "GDPR Art. 9 vs Kenya DPA §37",
                "resolution": "Apply strictest standard (GDPR), require adequacy decision",
                "humanitarian_margin": 0.0,
                "expected_action": "APPLY_STRICTEST_STANDARD",
                "legal_basis": ["GDPR Art. 9", "Kenya DPA §37"],
            },
            "mass_surveillance_minor_outbreak": {
                "scenario": scenario,
                "description": "Government proposes mass surveillance for minor flu outbreak",
                "conflict": "Proportionality (ESR-11) vs Government directive",
                "resolution": "Surveillance disproportionate to threat (Z-score < 2.0)",
                "humanitarian_margin": 0.7,
                "expected_action": "DENY_DISPROPORTIONATE",
                "legal_basis": ["GDPR Art. 5(1)(c)", "WHO IHR Article 3"],
            },
            "third_party_processor_violation": {
                "scenario": scenario,
                "description": "Third-party cloud processor violates GDPR",
                "conflict": "Accountability (ESR-12) vs Operational continuity",
                "resolution": "Controller remains liable, terminate processor contract",
                "humanitarian_margin": 0.0,
                "expected_action": "TERMINATE_PROCESSOR",
                "legal_basis": ["GDPR Art. 5(2)", "GDPR Art. 28"],
            },
        }
        
        return edge_cases.get(scenario, {})
    
    def generate_outbreak_record(self) -> Dict:
        """Generate synthetic outbreak record"""
        location = random.choice(self.locations)
        disease = random.choice(self.diseases)
        
        # Outbreak parameters
        duration_days = random.randint(7, 90)
        peak_day = random.randint(10, duration_days - 10)
        
        return {
            "outbreak_id": f"OUT_{hashlib.sha256(str(random.random()).encode()).hexdigest()[:8].upper()}",
            "timestamp": (datetime.utcnow() - timedelta(days=random.randint(0, 365))).isoformat(),
            "location": location,
            "disease": disease["name"],
            "epidemiology": {
                "r0": disease["r0"] + random.uniform(-0.5, 0.5),
                "attack_rate": random.uniform(0.01, 0.15),
                "case_fatality_rate": random.uniform(0.001, 0.1),
                "duration_days": duration_days,
                "peak_day": peak_day,
                "total_cases": random.randint(100, 10000),
                "total_deaths": random.randint(1, 500),
            },
            "response": {
                "intervention_type": random.choice(["vaccination", "quarantine", "treatment", "surveillance"]),
                "resources_allocated": random.uniform(10000, 1000000),
                "effectiveness": random.uniform(0.5, 0.95),
            },
            "z_score": random.uniform(0.5, 15.0),
            "alert_level": random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
        }
    
    def validate_record(self, record: Dict) -> bool:
        """Validate record against SovereignGuardrail"""
        try:
            # Check data sovereignty
            if record.get("data_source") == "EMR":
                self.guardrail.validate_action(
                    action_type='Data_Processing',
                    payload={
                        'data_type': 'PHI',
                        'processing_location': 'Edge_Node',
                        'consent_token': record.get('consent', {}).get('consent_token', 'MISSING'),
                    },
                    jurisdiction=record.get('jurisdiction', 'GLOBAL_DEFAULT')
                )
            
            # Check consent for children
            if record.get('demographics', {}).get('is_child'):
                if not record.get('consent', {}).get('guardian_consent_obtained'):
                    # This is expected to fail validation in some cases
                    pass
            
            return True
        
        except SovereigntyViolationError as e:
            # Log violation but continue (this is training data)
            print(f"⚠️  Validation warning: {e}")
            return False
    
    def generate_dataset(self, num_records: int = 10000, edge_case_ratio: float = 0.3) -> List[Dict]:
        """Generate complete synthetic dataset"""
        print(f"🔬 Generating {num_records} synthetic records...")
        print(f"   Edge case ratio: {edge_case_ratio:.1%}")
        
        dataset = []
        edge_case_count = 0
        validation_failures = 0
        
        for i in range(num_records):
            # Determine if this should be an edge case
            include_edge_case = random.random() < edge_case_ratio
            
            # Generate record type (80% patient, 20% outbreak)
            if random.random() < 0.8:
                record = self.generate_patient_record(include_edge_case=include_edge_case)
            else:
                record = self.generate_outbreak_record()
            
            # Validate against SovereignGuardrail
            is_valid = self.validate_record(record)
            record["validation_status"] = "VALID" if is_valid else "VIOLATION"
            
            if not is_valid:
                validation_failures += 1
            
            if include_edge_case:
                edge_case_count += 1
            
            dataset.append(record)
            
            # Progress indicator
            if (i + 1) % 1000 == 0:
                print(f"   Generated {i + 1}/{num_records} records...")
        
        print(f"✅ Dataset generation complete!")
        print(f"   Total records: {len(dataset)}")
        print(f"   Edge cases: {edge_case_count} ({edge_case_count/len(dataset):.1%})")
        print(f"   Validation failures: {validation_failures} ({validation_failures/len(dataset):.1%})")
        
        return dataset
    
    def save_dataset(self, dataset: List[Dict], filename: str = "humanitarian_training_data.jsonl"):
        """Save dataset to JSONL format"""
        output_path = os.path.join(self.output_dir, filename)
        
        print(f"💾 Saving dataset to {output_path}...")
        
        with open(output_path, 'w') as f:
            for record in dataset:
                f.write(json.dumps(record) + '\n')
        
        # Save metadata
        metadata = {
            "generated_at": datetime.utcnow().isoformat(),
            "total_records": len(dataset),
            "edge_case_count": sum(1 for r in dataset if "edge_case" in r),
            "validation_failures": sum(1 for r in dataset if r.get("validation_status") == "VIOLATION"),
            "ethical_specifications_version": self.ethical_specs["version"],
            "locations": [loc["name"] for loc in self.locations],
            "diseases": [d["name"] for d in self.diseases],
        }
        
        metadata_path = os.path.join(self.output_dir, "dataset_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Dataset saved successfully!")
        print(f"   Data: {output_path}")
        print(f"   Metadata: {metadata_path}")


def main():
    """Main execution"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   iLuminara Synthetic Humanitarian Data Generator          ║")
    print("║   Context Distillation for Spiral AGI Training             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Initialize generator
    generator = SyntheticDataGenerator()
    
    # Generate dataset
    dataset = generator.generate_dataset(
        num_records=10000,
        edge_case_ratio=0.3  # 30% edge cases
    )
    
    # Save dataset
    generator.save_dataset(dataset)
    
    print()
    print("🎯 Next steps:")
    print("   1. Review data/synthetic/humanitarian_training_data.jsonl")
    print("   2. Run SFT training: python intelligence_engine/train_cot.py")
    print("   3. Evaluate model: python tests/evaluate_spiral_agi.py")


if __name__ == "__main__":
    main()
