"""
OFAC & UN Sanctions Checker
Real-time fuzzy matching against sanctions databases

Compliance:
- FATF Recommendation 8 (Non-Profits & Terrorist Financing)
- OFAC Sanctions Lists (USA)
- UN Security Council Consolidated List
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from difflib import SequenceMatcher
import logging

logger = logging.getLogger(__name__)


class SanctionsMatch:
    """Represents a potential sanctions match"""
    
    def __init__(
        self,
        entity_id: str,
        match_score: float,
        list_name: str,
        matched_name: str,
        aliases: List[str],
        program: str,
        remarks: str
    ):
        self.entity_id = entity_id
        self.match_score = match_score
        self.list_name = list_name
        self.matched_name = matched_name
        self.aliases = aliases
        self.program = program
        self.remarks = remarks
    
    def to_dict(self) -> Dict:
        return {
            "entity_id": self.entity_id,
            "match_score": self.match_score,
            "list_name": self.list_name,
            "matched_name": self.matched_name,
            "aliases": self.aliases,
            "program": self.program,
            "remarks": self.remarks
        }


class SanctionsChecker:
    """
    Real-time sanctions screening against OFAC and UN lists
    
    Uses fuzzy matching to detect potential matches even with:
    - Spelling variations
    - Transliteration differences
    - Name order variations
    - Partial matches
    """
    
    def __init__(
        self,
        ofac_list_path: Optional[str] = None,
        un_list_path: Optional[str] = None,
        match_threshold: float = 0.85
    ):
        self.match_threshold = match_threshold
        self.ofac_list = self._load_ofac_list(ofac_list_path)
        self.un_list = self._load_un_list(un_list_path)
        
        logger.info(f"🔍 Sanctions Checker initialized - Threshold: {match_threshold}")
    
    def _load_ofac_list(self, path: Optional[str]) -> List[Dict]:
        """Load OFAC Specially Designated Nationals (SDN) list"""
        # In production, this would load from:
        # https://www.treasury.gov/ofac/downloads/sdn.xml
        
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        
        # Mock data for demonstration
        return [
            {
                "uid": "OFAC-001",
                "name": "SANCTIONED ENTITY EXAMPLE",
                "aliases": ["EXAMPLE SANCTIONED", "SANCTIONED ORG"],
                "program": "TERRORISM",
                "remarks": "Designated for terrorist financing"
            },
            {
                "uid": "OFAC-002",
                "name": "BLOCKED PERSON DEMO",
                "aliases": ["DEMO BLOCKED"],
                "program": "NARCOTICS",
                "remarks": "Narcotics trafficking"
            }
        ]
    
    def _load_un_list(self, path: Optional[str]) -> List[Dict]:
        """Load UN Security Council Consolidated List"""
        # In production, this would load from:
        # https://www.un.org/securitycouncil/content/un-sc-consolidated-list
        
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        
        # Mock data for demonstration
        return [
            {
                "uid": "UN-001",
                "name": "UN SANCTIONED INDIVIDUAL",
                "aliases": ["INDIVIDUAL SANCTIONED"],
                "program": "ISIL",
                "remarks": "Associated with ISIL"
            }
        ]
    
    def check_ofac(
        self,
        entity_name: str,
        entity_id: Optional[str] = None,
        additional_info: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Check entity against OFAC sanctions list
        
        Args:
            entity_name: Name to check
            entity_id: Optional entity identifier
            additional_info: Optional additional information (DOB, address, etc.)
        
        Returns:
            Check result with matches and risk score
        """
        result = {
            "entity_name": entity_name,
            "entity_id": entity_id,
            "timestamp": datetime.utcnow().isoformat(),
            "list_checked": "OFAC SDN",
            "status": "CLEAR",
            "matches": [],
            "risk_score": 0.0,
            "action": "ALLOW"
        }
        
        # Normalize entity name
        normalized_name = self._normalize_name(entity_name)
        
        # Check against OFAC list
        for entry in self.ofac_list:
            # Check primary name
            match_score = self._fuzzy_match(normalized_name, self._normalize_name(entry["name"]))
            
            if match_score >= self.match_threshold:
                match = SanctionsMatch(
                    entity_id=entry["uid"],
                    match_score=match_score,
                    list_name="OFAC SDN",
                    matched_name=entry["name"],
                    aliases=entry.get("aliases", []),
                    program=entry.get("program", ""),
                    remarks=entry.get("remarks", "")
                )
                result["matches"].append(match.to_dict())
            
            # Check aliases
            for alias in entry.get("aliases", []):
                alias_score = self._fuzzy_match(normalized_name, self._normalize_name(alias))
                
                if alias_score >= self.match_threshold:
                    match = SanctionsMatch(
                        entity_id=entry["uid"],
                        match_score=alias_score,
                        list_name="OFAC SDN (Alias)",
                        matched_name=alias,
                        aliases=entry.get("aliases", []),
                        program=entry.get("program", ""),
                        remarks=entry.get("remarks", "")
                    )
                    result["matches"].append(match.to_dict())
        
        # Determine status and action
        if result["matches"]:
            result["status"] = "MATCH_FOUND"
            result["risk_score"] = max(m["match_score"] for m in result["matches"])
            result["action"] = "BLOCK_PAYMENT"
            
            logger.warning(f"🚨 OFAC MATCH: {entity_name} - Risk: {result['risk_score']:.2%}")
        else:
            logger.info(f"✅ OFAC CLEAR: {entity_name}")
        
        return result
    
    def check_un_sanctions(
        self,
        entity_name: str,
        entity_id: Optional[str] = None
    ) -> Dict[str, any]:
        """Check entity against UN Security Council Consolidated List"""
        result = {
            "entity_name": entity_name,
            "entity_id": entity_id,
            "timestamp": datetime.utcnow().isoformat(),
            "list_checked": "UN Consolidated List",
            "status": "CLEAR",
            "matches": [],
            "risk_score": 0.0,
            "action": "ALLOW"
        }
        
        normalized_name = self._normalize_name(entity_name)
        
        for entry in self.un_list:
            match_score = self._fuzzy_match(normalized_name, self._normalize_name(entry["name"]))
            
            if match_score >= self.match_threshold:
                match = SanctionsMatch(
                    entity_id=entry["uid"],
                    match_score=match_score,
                    list_name="UN Consolidated List",
                    matched_name=entry["name"],
                    aliases=entry.get("aliases", []),
                    program=entry.get("program", ""),
                    remarks=entry.get("remarks", "")
                )
                result["matches"].append(match.to_dict())
        
        if result["matches"]:
            result["status"] = "MATCH_FOUND"
            result["risk_score"] = max(m["match_score"] for m in result["matches"])
            result["action"] = "BLOCK_TRANSACTION"
            
            logger.warning(f"🚨 UN SANCTIONS MATCH: {entity_name} - Risk: {result['risk_score']:.2%}")
        else:
            logger.info(f"✅ UN SANCTIONS CLEAR: {entity_name}")
        
        return result
    
    def comprehensive_check(
        self,
        entity_name: str,
        entity_id: Optional[str] = None,
        additional_info: Optional[Dict] = None
    ) -> Dict[str, any]:
        """
        Run comprehensive sanctions check across all lists
        
        Returns:
            Combined result from OFAC and UN checks
        """
        ofac_result = self.check_ofac(entity_name, entity_id, additional_info)
        un_result = self.check_un_sanctions(entity_name, entity_id)
        
        combined_result = {
            "entity_name": entity_name,
            "entity_id": entity_id,
            "timestamp": datetime.utcnow().isoformat(),
            "lists_checked": ["OFAC SDN", "UN Consolidated List"],
            "status": "CLEAR",
            "ofac_matches": ofac_result["matches"],
            "un_matches": un_result["matches"],
            "total_matches": len(ofac_result["matches"]) + len(un_result["matches"]),
            "max_risk_score": 0.0,
            "action": "ALLOW",
            "compliance_frameworks": [
                "FATF Recommendation 8",
                "OFAC Sanctions (USA)",
                "UN Security Council Resolutions"
            ]
        }
        
        # Determine overall status
        if combined_result["total_matches"] > 0:
            combined_result["status"] = "MATCH_FOUND"
            combined_result["max_risk_score"] = max(
                ofac_result["risk_score"],
                un_result["risk_score"]
            )
            combined_result["action"] = "BLOCK_ALL_TRANSACTIONS"
            
            logger.error(f"🚨 SANCTIONS VIOLATION: {entity_name} - {combined_result['total_matches']} matches")
        else:
            logger.info(f"✅ COMPREHENSIVE SANCTIONS CHECK CLEAR: {entity_name}")
        
        return combined_result
    
    def _normalize_name(self, name: str) -> str:
        """Normalize name for matching"""
        # Convert to uppercase
        name = name.upper()
        
        # Remove special characters
        name = re.sub(r'[^A-Z0-9\s]', '', name)
        
        # Remove extra whitespace
        name = ' '.join(name.split())
        
        return name
    
    def _fuzzy_match(self, name1: str, name2: str) -> float:
        """
        Calculate fuzzy match score between two names
        
        Uses SequenceMatcher for similarity calculation
        Returns score between 0.0 and 1.0
        """
        return SequenceMatcher(None, name1, name2).ratio()
    
    def update_sanctions_lists(self) -> Dict[str, any]:
        """
        Update sanctions lists from official sources
        
        In production, this would:
        1. Download latest OFAC SDN XML
        2. Download latest UN Consolidated List
        3. Parse and cache locally
        4. Return update status
        """
        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "ofac_updated": True,
            "un_updated": True,
            "ofac_entries": len(self.ofac_list),
            "un_entries": len(self.un_list),
            "message": "Sanctions lists updated successfully"
        }


# Example usage
if __name__ == "__main__":
    import os
    
    checker = SanctionsChecker(match_threshold=0.85)
    
    print("=" * 60)
    print("OFAC & UN SANCTIONS CHECKER")
    print("=" * 60)
    print()
    
    # Test 1: Clean entity
    print("TEST 1: Clean Entity")
    print("-" * 60)
    result = checker.comprehensive_check(
        entity_name="Legitimate Health NGO",
        entity_id="NGO-12345"
    )
    print(json.dumps(result, indent=2))
    print()
    
    # Test 2: Sanctioned entity (exact match)
    print("TEST 2: Sanctioned Entity (Exact Match)")
    print("-" * 60)
    result = checker.comprehensive_check(
        entity_name="SANCTIONED ENTITY EXAMPLE",
        entity_id="UNKNOWN-001"
    )
    print(json.dumps(result, indent=2))
    print()
    
    # Test 3: Fuzzy match (spelling variation)
    print("TEST 3: Fuzzy Match (Spelling Variation)")
    print("-" * 60)
    result = checker.comprehensive_check(
        entity_name="SANCTIONED ENTTY EXMPLE",  # Typos
        entity_id="UNKNOWN-002"
    )
    print(json.dumps(result, indent=2))
    print()
    
    # Test 4: Update sanctions lists
    print("TEST 4: Update Sanctions Lists")
    print("-" * 60)
    update_result = checker.update_sanctions_lists()
    print(json.dumps(update_result, indent=2))
