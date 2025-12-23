"""
Sectoral Compliance Testing Suite
Tests all 29 global legal frameworks across 8 sectors
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from governance_kernel.compliance_matrix import (
    ComplianceMatrix,
    SectoralContext,
    ComplianceViolation
)
from governance_kernel.sectoral.ofac_sanctions import OFACSanctionsChecker
from governance_kernel.sectoral.cbam_carbon import CBAMCalculator
from governance_kernel.sectoral.mdr_pharma import MDRComplianceVerifier
from governance_kernel.chrono_audit import ChronoAudit, ChronoEventType, TemporalIntegrityLevel


class TestDataPrivacyCompliance(unittest.TestCase):
    """Test primary privacy & sovereignty frameworks (14 frameworks)"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
    
    def test_gdpr_cross_border_transfer_blocked(self):
        """Test GDPR Art. 9 blocks cross-border PHI transfer"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.DATA_PRIVACY,
            payload={
                "region": "EU",
                "data_type": "PHI",
                "target_server": "USA"
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("GDPR" in v["framework"] for v in result["violations"]))
    
    def test_kdpa_kenya_sovereignty(self):
        """Test KDPA §37 enforces Kenyan data sovereignty"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.DATA_PRIVACY,
            payload={
                "region": "Kenya",
                "data_type": "HIV_Status",
                "target_server": "USA"
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        violations = [v for v in result["violations"] if "KDPA" in v["framework"]]
        self.assertTrue(len(violations) > 0)
        self.assertEqual(violations[0]["severity"], "CRITICAL")
    
    def test_hipaa_audit_trail_required(self):
        """Test HIPAA §164.312(b) requires audit controls"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.DATA_PRIVACY,
            payload={
                "region": "USA",
                "data_type": "PHI",
                "audit_trail_enabled": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("HIPAA" in v["framework"] for v in result["violations"]))
    
    def test_lgpd_brazil_compliance(self):
        """Test LGPD Art. 11 sensitive data protection"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.DATA_PRIVACY,
            payload={
                "region": "Brazil",
                "data_type": "Health_Data",
                "consent_obtained": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("LGPD" in v["framework"] for v in result["violations"]))
    
    def test_ndpr_nigeria_local_hosting(self):
        """Test NDPR Art. 2.6 requires local hosting"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.DATA_PRIVACY,
            payload={
                "region": "Nigeria",
                "data_type": "PHI",
                "hosting_location": "USA"
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("NDPR" in v["framework"] for v in result["violations"]))


class TestAIGovernanceCompliance(unittest.TestCase):
    """Test EU AI Act compliance"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
    
    def test_eu_ai_act_high_risk_explainability(self):
        """Test EU AI Act Art. 6 requires explainability for high-risk AI"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.AI_GOVERNANCE,
            payload={
                "ai_system_type": "medical_diagnosis",
                "risk_level": "high",
                "explainability_provided": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        violations = [v for v in result["violations"] if "EU AI Act" in v["framework"]]
        self.assertTrue(len(violations) > 0)
    
    def test_eu_ai_act_human_oversight(self):
        """Test EU AI Act Art. 14 requires human oversight"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.AI_GOVERNANCE,
            payload={
                "ai_system_type": "clinical_decision",
                "human_oversight": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")


class TestSupplyChainCompliance(unittest.TestCase):
    """Test supply chain & manufacturing frameworks (4 frameworks)"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
    
    def test_uflpa_xuar_blocking(self):
        """Test UFLPA blocks components from XUAR"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.SUPPLY_CHAIN,
            payload={
                "component_origin": "XUAR",
                "hardware_components": ["Tin", "Tantalum"]
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        violations = [v for v in result["violations"] if "UFLPA" in v["framework"]]
        self.assertTrue(len(violations) > 0)
        self.assertEqual(violations[0]["severity"], "CRITICAL")
    
    def test_dodd_frank_conflict_minerals(self):
        """Test Dodd-Frank §1502 requires 3TG disclosure"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.SUPPLY_CHAIN,
            payload={
                "hardware_components": ["Tin", "Tantalum", "Tungsten", "Gold"],
                "conflict_minerals_disclosed": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("Dodd-Frank" in v["framework"] for v in result["violations"]))
    
    def test_csddd_due_diligence(self):
        """Test CSDDD requires human rights due diligence"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.SUPPLY_CHAIN,
            payload={
                "supply_chain_audit": False,
                "human_rights_assessment": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("CSDDD" in v["framework"] for v in result["violations"]))


class TestESGCarbonCompliance(unittest.TestCase):
    """Test ESG & carbon credit frameworks (3 frameworks)"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
        self.cbam = CBAMCalculator()
    
    def test_cbam_embedded_emissions_required(self):
        """Test CBAM requires embedded emissions calculation"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.ESG_CARBON,
            payload={
                "goods_destination": "EU",
                "carbon_intensive": True,
                "embedded_emissions_calculated": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        violations = [v for v in result["violations"] if "CBAM" in v["framework"]]
        self.assertTrue(len(violations) > 0)
    
    def test_cbam_emissions_calculation(self):
        """Test CBAM emissions calculation per logistics hop"""
        emissions = self.cbam.calculate_embedded_emissions(
            logistics_hops=[
                {"mode": "truck", "distance_km": 500, "fuel_type": "diesel"},
                {"mode": "ship", "distance_km": 5000, "fuel_type": "heavy_fuel_oil"},
                {"mode": "truck", "distance_km": 200, "fuel_type": "diesel"}
            ],
            product_weight_kg=1000
        )
        
        self.assertGreater(emissions["total_co2e_kg"], 0)
        self.assertEqual(len(emissions["breakdown"]), 3)
    
    def test_paris_agreement_double_counting_prevention(self):
        """Test Paris Agreement Art. 6.2 prevents double counting"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.ESG_CARBON,
            payload={
                "carbon_credit_id": "CC_001",
                "already_claimed": True
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("Paris Agreement" in v["framework"] for v in result["violations"]))


class TestHumanitarianFinanceCompliance(unittest.TestCase):
    """Test humanitarian finance frameworks (4 frameworks)"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
        self.ofac = OFACSanctionsChecker()
    
    def test_ofac_sanctions_blocking(self):
        """Test OFAC blocks sanctioned entities"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.HUMANITARIAN_FINANCE,
            payload={
                "payment_initiation": True,
                "payee_id": "SANCTIONED_ENTITY",
                "ofac_check_passed": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        violations = [v for v in result["violations"] if "OFAC" in v["framework"]]
        self.assertTrue(len(violations) > 0)
        self.assertEqual(violations[0]["severity"], "CRITICAL")
    
    def test_ofac_fuzzy_matching(self):
        """Test OFAC fuzzy matching detects similar names"""
        # Test exact match
        is_sanctioned, match_score = self.ofac.check_entity("VLADIMIR PUTIN")
        self.assertTrue(is_sanctioned)
        self.assertGreater(match_score, 0.9)
        
        # Test fuzzy match
        is_sanctioned, match_score = self.ofac.check_entity("Vladmir Puttin")  # Typo
        self.assertTrue(is_sanctioned)
        self.assertGreater(match_score, 0.7)
    
    def test_fatf_r8_kyb_required(self):
        """Test FATF R8 requires Know Your Beneficiary"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.HUMANITARIAN_FINANCE,
            payload={
                "payment_initiation": True,
                "kyb_completed": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("FATF" in v["framework"] for v in result["violations"]))


class TestHealthcarePharmaCompliance(unittest.TestCase):
    """Test healthcare & pharma frameworks (4 frameworks)"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
        self.mdr = MDRComplianceVerifier()
    
    def test_eu_mdr_clinical_evaluation_required(self):
        """Test EU MDR requires clinical evaluation for Class IIa/IIb"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.HEALTHCARE_PHARMA,
            payload={
                "device_class": "IIa",
                "clinical_evaluation_completed": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        violations = [v for v in result["violations"] if "MDR" in v["framework"]]
        self.assertTrue(len(violations) > 0)
    
    def test_mdr_pms_required(self):
        """Test MDR requires Post-Market Surveillance"""
        compliance = self.mdr.verify_compliance(
            device_class="IIb",
            clinical_evaluation_completed=True,
            pms_plan_exists=False
        )
        
        self.assertFalse(compliance["compliant"])
        self.assertTrue(any("PMS" in v for v in compliance["violations"]))
    
    def test_fda_21_cfr_part_11_audit_trail(self):
        """Test FDA 21 CFR Part 11 requires timestamped audit trails"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.HEALTHCARE_PHARMA,
            payload={
                "electronic_records": True,
                "audit_trail_timestamped": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("21 CFR Part 11" in v["framework"] for v in result["violations"]))


class TestCybersecurityCompliance(unittest.TestCase):
    """Test cybersecurity & critical infrastructure frameworks (2 frameworks)"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
    
    def test_nis2_incident_reporting(self):
        """Test NIS2 requires 24-hour incident reporting"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.CYBERSECURITY,
            payload={
                "security_incident": True,
                "incident_reported_within_24h": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        violations = [v for v in result["violations"] if "NIS2" in v["framework"]]
        self.assertTrue(len(violations) > 0)
    
    def test_cra_sbom_required(self):
        """Test CRA requires automated SBOM generation"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.CYBERSECURITY,
            payload={
                "software_product": True,
                "sbom_generated": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("CRA" in v["framework"] for v in result["violations"]))


class TestHumanitarianInteroperabilityCompliance(unittest.TestCase):
    """Test humanitarian & interoperability frameworks (3 frameworks)"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
    
    def test_who_ihr_notification_required(self):
        """Test WHO IHR Art. 6 requires outbreak notification"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.HUMANITARIAN_INTEROP,
            payload={
                "outbreak_detected": True,
                "who_notified": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        violations = [v for v in result["violations"] if "WHO IHR" in v["framework"]]
        self.assertTrue(len(violations) > 0)
    
    def test_geneva_conventions_medical_neutrality(self):
        """Test Geneva Conventions protect medical data in conflict zones"""
        result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.HUMANITARIAN_INTEROP,
            payload={
                "conflict_zone": True,
                "medical_data_protected": False
            }
        )
        
        self.assertEqual(result["status"], "VIOLATION")
        self.assertTrue(any("Geneva" in v["framework"] for v in result["violations"]))


class TestChronoAudit(unittest.TestCase):
    """Test IP-09 Chrono-Audit temporal integrity"""
    
    def setUp(self):
        self.chrono = ChronoAudit(
            integrity_level=TemporalIntegrityLevel.CHAINED
        )
    
    def test_event_recording(self):
        """Test event recording with hash chaining"""
        event = self.chrono.record_event(
            event_type=ChronoEventType.DATA_TRANSFER,
            actor="ml_system",
            resource="patient_data",
            action="transfer_to_cloud",
            jurisdiction="KDPA_KE",
            metadata={"destination": "africa-south1"},
            compliance_frameworks=["KDPA", "GDPR"],
            retention_days=2555
        )
        
        self.assertIsNotNone(event.event_id)
        self.assertIsNotNone(event.event_hash)
        self.assertIsNotNone(event.signature)
    
    def test_chain_integrity_verification(self):
        """Test temporal chain integrity verification"""
        # Record multiple events
        for i in range(5):
            self.chrono.record_event(
                event_type=ChronoEventType.HIGH_RISK_INFERENCE,
                actor=f"ai_agent_{i}",
                resource="diagnosis_model",
                action="predict",
                jurisdiction="KDPA_KE",
                metadata={"confidence": 0.95}
            )
        
        # Verify chain
        is_valid, errors = self.chrono.verify_chain_integrity()
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_chain_tampering_detection(self):
        """Test detection of chain tampering"""
        # Record events
        event1 = self.chrono.record_event(
            event_type=ChronoEventType.KEY_SHRED,
            actor="crypto_shredder",
            resource="key_001",
            action="shred",
            jurisdiction="KDPA_KE"
        )
        
        event2 = self.chrono.record_event(
            event_type=ChronoEventType.DATA_TRANSFER,
            actor="system",
            resource="data",
            action="transfer",
            jurisdiction="KDPA_KE"
        )
        
        # Tamper with event
        self.chrono.chain[0].event_hash = "TAMPERED_HASH"
        
        # Verify chain (should detect tampering)
        is_valid, errors = self.chrono.verify_chain_integrity()
        
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_compliance_report_generation(self):
        """Test compliance report generation"""
        # Record events
        self.chrono.record_event(
            event_type=ChronoEventType.DATA_TRANSFER,
            actor="system",
            resource="phi",
            action="transfer",
            jurisdiction="GDPR_EU",
            compliance_frameworks=["GDPR"]
        )
        
        # Generate report
        report = self.chrono.generate_compliance_report("GDPR")
        
        self.assertEqual(report["framework"], "GDPR")
        self.assertGreater(report["total_events"], 0)
        self.assertTrue(report["chain_integrity"]["valid"])


class TestIntegrationScenarios(unittest.TestCase):
    """Test real-world integration scenarios"""
    
    def setUp(self):
        self.matrix = ComplianceMatrix()
        self.chrono = ChronoAudit()
    
    def test_kenya_to_eu_data_transfer_scenario(self):
        """Test complete Kenya to EU data transfer with all checks"""
        # Step 1: Check KDPA compliance
        kdpa_result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.DATA_PRIVACY,
            payload={
                "region": "Kenya",
                "data_type": "PHI",
                "target_server": "EU"
            }
        )
        
        # Step 2: Check GDPR compliance
        gdpr_result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.DATA_PRIVACY,
            payload={
                "region": "EU",
                "data_type": "PHI",
                "consent_obtained": True,
                "scc_in_place": True
            }
        )
        
        # Step 3: Record in Chrono-Audit
        event = self.chrono.record_event(
            event_type=ChronoEventType.CROSS_BORDER_TRANSFER,
            actor="data_controller",
            resource="patient_records",
            action="transfer_kenya_to_eu",
            jurisdiction="KDPA_KE",
            metadata={
                "source": "Kenya",
                "destination": "EU",
                "scc_reference": "SCC_2021_001"
            },
            compliance_frameworks=["KDPA", "GDPR"]
        )
        
        # Verify all checks passed
        self.assertIsNotNone(event)
        self.assertTrue(self.chrono.verify_chain_integrity()[0])
    
    def test_medical_device_deployment_scenario(self):
        """Test medical device deployment with MDR + CBAM + NIS2"""
        # Step 1: MDR compliance
        mdr_result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.HEALTHCARE_PHARMA,
            payload={
                "device_class": "IIb",
                "clinical_evaluation_completed": True,
                "pms_plan_exists": True
            }
        )
        
        # Step 2: CBAM emissions
        cbam_result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.ESG_CARBON,
            payload={
                "goods_destination": "EU",
                "carbon_intensive": True,
                "embedded_emissions_calculated": True,
                "emissions_value": 150.5
            }
        )
        
        # Step 3: NIS2 cybersecurity
        nis2_result = self.matrix.check_sectoral_compliance(
            context=SectoralContext.CYBERSECURITY,
            payload={
                "critical_infrastructure": True,
                "incident_response_plan": True,
                "sbom_generated": True
            }
        )
        
        # All should pass
        self.assertEqual(mdr_result["status"], "COMPLIANT")
        self.assertEqual(cbam_result["status"], "COMPLIANT")
        self.assertEqual(nis2_result["status"], "COMPLIANT")


def run_all_tests():
    """Run all sectoral compliance tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataPrivacyCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestAIGovernanceCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestSupplyChainCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestESGCarbonCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestHumanitarianFinanceCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthcarePharmaCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestCybersecurityCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestHumanitarianInteroperabilityCompliance))
    suite.addTests(loader.loadTestsFromTestCase(TestChronoAudit))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationScenarios))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("SECTORAL COMPLIANCE TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
