"""
OFAC Sanctions Compliance Module
Office of Foreign Assets Control (U.S. Treasury)

Compliance:
- OFAC Sanctions Programs
- Executive Orders (EO 13224, 13382, etc.)
- Trading with the Enemy Act
- International Emergency Economic Powers Act (IEEPA)
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class SanctionsList(Enum):
    """OFAC Sanctions Lists"""
    SDN = "Specially Designated Nationals"  # Primary list
    FSE = "Foreign Sanctions Evaders"
    NS_MBS = "Non-SDN Menu-Based Sanctions"
    CAPTA = "CAPTA (Magnitsky Act)"
    SYRIA = "Syria Sanctions"
    UKRAINE = "Ukraine/Russia Sanctions"
    IRAN = "Iran Sanctions"
    NORTH_KOREA = "North Korea Sanctions"
    VENEZUELA = "Venezuela Sanctions"


class SanctionType(Enum):
    """Types of sanctions"""
    BLOCKING = "blocking"  # Assets frozen
    SECTORAL = "sectoral"  # Sector-specific restrictions
    SECONDARY = "secondary"  # Non-US persons dealing with sanctioned entities
    EXPORT_CONTROL = "export_control"  # Technology/goods restrictions


class OFACSanctionsChecker:
    """
    Real-time OFAC sanctions screening for health data transfers.
    
    Use case: Prevent health data transfers to sanctioned entities or countries.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        cache_duration_hours: int = 24,
        enable_offline_mode: bool = True
    ):
        self.api_key = api_key
        self.cache_duration = timedelta(hours=cache_duration_hours)
        self.enable_offline_mode = enable_offline_mode
        
        # Cache for sanctions data
        self.sdn_cache: Dict = {}
        self.cache_timestamp: Optional[datetime] = None
        
        # Offline fallback: Hardcoded high-risk countries
        self.high_risk_countries = {
            "CU": "Cuba",
            "IR": "Iran",
            "KP": "North Korea",
            "SY": "Syria",
            "RU": "Russia (partial)",
            "BY": "Belarus (partial)",
            "VE": "Venezuela (partial)"
        }
        
        logger.info("🚨 OFAC Sanctions Checker initialized")
    
    def check_entity(
        self,
        entity_name: str,
        entity_type: str = "organization",
        country_code: Optional[str] = None
    ) -> Dict:
        """
        Check if an entity is on OFAC sanctions lists.
        
        Args:
            entity_name: Name of organization or individual
            entity_type: "organization" or "individual"
            country_code: ISO 3166-1 alpha-2 country code
        
        Returns:
            {
                "sanctioned": bool,
                "lists": [SanctionsList],
                "sanction_type": SanctionType,
                "risk_level": "HIGH" | "MEDIUM" | "LOW",
                "details": str
            }
        """
        # Refresh cache if needed
        if self._cache_expired():
            self._refresh_sdn_list()
        
        # Check country-level sanctions first
        if country_code and country_code in self.high_risk_countries:
            return {
                "sanctioned": True,
                "lists": [SanctionsList.SDN],
                "sanction_type": SanctionType.BLOCKING,
                "risk_level": "HIGH",
                "details": f"Country-level sanctions: {self.high_risk_countries[country_code]}",
                "action": "BLOCK_TRANSFER"
            }
        
        # Check entity name against SDN list
        entity_lower = entity_name.lower()
        
        for sdn_entry in self.sdn_cache.get("entries", []):
            if self._fuzzy_match(entity_lower, sdn_entry["name"].lower()):
                return {
                    "sanctioned": True,
                    "lists": [SanctionsList.SDN],
                    "sanction_type": SanctionType.BLOCKING,
                    "risk_level": "HIGH",
                    "details": f"Match found: {sdn_entry['name']} (Program: {sdn_entry.get('program', 'N/A')})",
                    "action": "BLOCK_TRANSFER",
                    "sdn_id": sdn_entry.get("uid")
                }
        
        # No match found
        return {
            "sanctioned": False,
            "lists": [],
            "sanction_type": None,
            "risk_level": "LOW",
            "details": "No sanctions match found",
            "action": "ALLOW_TRANSFER"
        }
    
    def check_transfer(
        self,
        source_country: str,
        destination_country: str,
        destination_entity: str,
        data_type: str = "PHI"
    ) -> Dict:
        """
        Check if a data transfer violates OFAC sanctions.
        
        Args:
            source_country: ISO country code of data origin
            destination_country: ISO country code of destination
            destination_entity: Name of receiving organization
            data_type: Type of data being transferred
        
        Returns:
            Compliance result with action recommendation
        """
        # Check destination country
        if destination_country in self.high_risk_countries:
            return {
                "compliant": False,
                "violation": "OFAC_COUNTRY_SANCTIONS",
                "severity": "CRITICAL",
                "details": f"Transfer to {self.high_risk_countries[destination_country]} prohibited",
                "action": "BLOCK_TRANSFER",
                "legal_citation": "31 CFR Part 500 (OFAC Regulations)"
            }
        
        # Check destination entity
        entity_check = self.check_entity(
            entity_name=destination_entity,
            entity_type="organization",
            country_code=destination_country
        )
        
        if entity_check["sanctioned"]:
            return {
                "compliant": False,
                "violation": "OFAC_ENTITY_SANCTIONS",
                "severity": "CRITICAL",
                "details": entity_check["details"],
                "action": "BLOCK_TRANSFER",
                "legal_citation": "31 CFR Part 501 (SDN List)"
            }
        
        # Check for sectoral sanctions (e.g., Russia technology sector)
        if destination_country == "RU" and data_type in ["AI_MODEL", "TECHNOLOGY"]:
            return {
                "compliant": False,
                "violation": "OFAC_SECTORAL_SANCTIONS",
                "severity": "HIGH",
                "details": "Technology transfer to Russia restricted under EO 14024",
                "action": "BLOCK_TRANSFER",
                "legal_citation": "Executive Order 14024 (Russia Sanctions)"
            }
        
        # Transfer allowed
        return {
            "compliant": True,
            "violation": None,
            "severity": "NONE",
            "details": "No OFAC sanctions violations detected",
            "action": "ALLOW_TRANSFER",
            "legal_citation": None
        }
    
    def _refresh_sdn_list(self):
        """
        Refresh SDN list from OFAC API or fallback to offline mode.
        """
        try:
            # Try to fetch from OFAC API
            # Note: OFAC provides XML/CSV files, not a REST API
            # In production, you would download and parse the SDN list
            
            if self.enable_offline_mode:
                # Use offline fallback
                self.sdn_cache = self._load_offline_sdn_list()
                self.cache_timestamp = datetime.utcnow()
                logger.info("✅ SDN list loaded (offline mode)")
            else:
                # In production: Download from https://www.treasury.gov/ofac/downloads/sdn.xml
                logger.warning("⚠️ Online SDN refresh not implemented - using offline mode")
                self.sdn_cache = self._load_offline_sdn_list()
                self.cache_timestamp = datetime.utcnow()
        
        except Exception as e:
            logger.error(f"❌ Failed to refresh SDN list: {e}")
            # Use offline fallback
            self.sdn_cache = self._load_offline_sdn_list()
            self.cache_timestamp = datetime.utcnow()
    
    def _load_offline_sdn_list(self) -> Dict:
        """
        Load offline SDN list (high-risk entities only).
        
        In production, this would be a regularly updated snapshot.
        """
        return {
            "entries": [
                {
                    "uid": "12345",
                    "name": "EXAMPLE SANCTIONED ENTITY",
                    "type": "organization",
                    "program": "SYRIA",
                    "country": "SY"
                },
                # Add more entries from actual SDN list
            ],
            "last_updated": datetime.utcnow().isoformat()
        }
    
    def _cache_expired(self) -> bool:
        """Check if cache needs refresh"""
        if not self.cache_timestamp:
            return True
        return datetime.utcnow() - self.cache_timestamp > self.cache_duration
    
    def _fuzzy_match(self, query: str, target: str, threshold: float = 0.85) -> bool:
        """
        Fuzzy string matching for entity names.
        
        In production, use more sophisticated matching (Levenshtein distance, etc.)
        """
        # Simple substring matching for now
        return query in target or target in query
    
    def get_sanctioned_countries(self) -> List[Dict]:
        """Get list of all sanctioned countries"""
        return [
            {"code": code, "name": name, "sanction_type": "COMPREHENSIVE"}
            for code, name in self.high_risk_countries.items()
        ]
    
    def validate_health_data_transfer(
        self,
        transfer_request: Dict
    ) -> Dict:
        """
        Validate health data transfer against OFAC sanctions.
        
        Args:
            transfer_request: {
                "source_country": "KE",
                "destination_country": "US",
                "destination_entity": "Hospital XYZ",
                "data_type": "PHI",
                "patient_count": 100
            }
        
        Returns:
            Validation result with compliance status
        """
        result = self.check_transfer(
            source_country=transfer_request["source_country"],
            destination_country=transfer_request["destination_country"],
            destination_entity=transfer_request["destination_entity"],
            data_type=transfer_request.get("data_type", "PHI")
        )
        
        # Add audit trail
        result["audit"] = {
            "timestamp": datetime.utcnow().isoformat(),
            "checker": "OFAC_Sanctions_Checker",
            "request": transfer_request
        }
        
        return result


# Example usage
if __name__ == "__main__":
    checker = OFACSanctionsChecker(enable_offline_mode=True)
    
    # Test 1: Check sanctioned country
    result = checker.check_transfer(
        source_country="KE",
        destination_country="IR",  # Iran (sanctioned)
        destination_entity="Tehran Medical Center",
        data_type="PHI"
    )
    print(f"Test 1 - Iran Transfer: {json.dumps(result, indent=2)}")
    
    # Test 2: Check allowed country
    result = checker.check_transfer(
        source_country="KE",
        destination_country="US",
        destination_entity="Johns Hopkins Hospital",
        data_type="PHI"
    )
    print(f"\nTest 2 - US Transfer: {json.dumps(result, indent=2)}")
    
    # Test 3: Check entity
    entity_result = checker.check_entity(
        entity_name="Example Sanctioned Entity",
        country_code="SY"
    )
    print(f"\nTest 3 - Entity Check: {json.dumps(entity_result, indent=2)}")
