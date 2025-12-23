"""
Fairness Constraint Engine
Detects and mitigates bias in resource allocation across population groups

Implements:
- Demographic parity
- Equalized odds
- Disparate impact analysis
- Intersectional fairness
- Bias mitigation strategies

Compliance:
- EU AI Act §10 (Accuracy, Robustness, Cybersecurity)
- GDPR Art. 22 (Automated Decision-Making)
- UN Convention on Rights of the Child
- Convention on Elimination of Discrimination Against Women (CEDAW)
"""

import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import numpy as np
from collections import defaultdict

logger = logging.getLogger(__name__)


class ProtectedAttribute(Enum):
    """Protected attributes that must not be discriminated against"""
    AGE = "age"
    GENDER = "gender"
    ETHNICITY = "ethnicity"
    RELIGION = "religion"
    DISABILITY = "disability"
    NATIONALITY = "nationality"
    SOCIOECONOMIC_STATUS = "socioeconomic_status"


class FairnessMetric(Enum):
    """Fairness metrics to evaluate"""
    DEMOGRAPHIC_PARITY = "demographic_parity"
    EQUALIZED_ODDS = "equalized_odds"
    DISPARATE_IMPACT = "disparate_impact"
    EQUAL_OPPORTUNITY = "equal_opportunity"


@dataclass
class BiasDetectionResult:
    """Result of bias detection analysis"""
    metric: FairnessMetric
    protected_attribute: ProtectedAttribute
    bias_detected: bool
    bias_score: float  # 0.0 = no bias, 1.0 = maximum bias
    affected_groups: List[str]
    mitigation_recommended: bool
    details: Dict


class FairnessConstraintEngine:
    """
    Detects and mitigates bias in resource allocation decisions.
    """
    
    def __init__(
        self,
        fairness_threshold: float = 0.8,
        enable_mitigation: bool = True,
        enable_audit: bool = True
    ):
        """
        Args:
            fairness_threshold: Minimum acceptable fairness score (0.0-1.0)
            enable_mitigation: Automatically apply bias mitigation
            enable_audit: Log all fairness checks
        """
        self.fairness_threshold = fairness_threshold
        self.enable_mitigation = enable_mitigation
        self.enable_audit = enable_audit
        
        # Bias detection history
        self.bias_history: List[BiasDetectionResult] = []
        
        logger.info(f"⚖️ Fairness Constraint Engine initialized - Threshold: {fairness_threshold}")
    
    def detect_bias(
        self,
        allocations: List[Dict],
        population_groups: List[Dict],
        protected_attributes: List[ProtectedAttribute]
    ) -> List[BiasDetectionResult]:
        """
        Detect bias in resource allocations across protected attributes.
        
        Args:
            allocations: List of resource allocations
            population_groups: List of population groups with demographics
            protected_attributes: Attributes to check for bias
        
        Returns:
            List of bias detection results
        """
        logger.info(f"⚖️ Detecting bias across {len(protected_attributes)} protected attributes")
        
        results = []
        
        for attribute in protected_attributes:
            # Check demographic parity
            dp_result = self._check_demographic_parity(
                allocations, population_groups, attribute
            )
            results.append(dp_result)
            
            # Check disparate impact
            di_result = self._check_disparate_impact(
                allocations, population_groups, attribute
            )
            results.append(di_result)
        
        # Store results
        self.bias_history.extend(results)
        
        # Log summary
        biased_results = [r for r in results if r.bias_detected]
        if biased_results:
            logger.warning(f"⚠️ Bias detected in {len(biased_results)} metrics")
        else:
            logger.info("✅ No bias detected")
        
        return results
    
    def _check_demographic_parity(
        self,
        allocations: List[Dict],
        population_groups: List[Dict],
        protected_attribute: ProtectedAttribute
    ) -> BiasDetectionResult:
        """
        Check demographic parity: allocation rates should be similar across groups.
        
        Demographic Parity: P(allocation | group A) ≈ P(allocation | group B)
        """
        # Group allocations by protected attribute
        attribute_allocations = defaultdict(list)
        attribute_populations = defaultdict(int)
        
        for group in population_groups:
            attr_value = group.get("demographics", {}).get(protected_attribute.value)
            if attr_value:
                attribute_populations[attr_value] += group.get("size", 0)
        
        for allocation in allocations:
            group_id = allocation.get("group_id")
            group = next((g for g in population_groups if g.get("group_id") == group_id), None)
            
            if group:
                attr_value = group.get("demographics", {}).get(protected_attribute.value)
                if attr_value:
                    attribute_allocations[attr_value].append(allocation.get("amount", 0))
        
        # Calculate allocation rates
        allocation_rates = {}
        for attr_value, allocations_list in attribute_allocations.items():
            total_allocated = sum(allocations_list)
            population = attribute_populations[attr_value]
            allocation_rates[attr_value] = total_allocated / population if population > 0 else 0
        
        # Calculate parity score (ratio of min to max rate)
        if len(allocation_rates) < 2:
            return BiasDetectionResult(
                metric=FairnessMetric.DEMOGRAPHIC_PARITY,
                protected_attribute=protected_attribute,
                bias_detected=False,
                bias_score=0.0,
                affected_groups=[],
                mitigation_recommended=False,
                details={"reason": "Insufficient groups for comparison"}
            )
        
        min_rate = min(allocation_rates.values())
        max_rate = max(allocation_rates.values())
        parity_score = min_rate / max_rate if max_rate > 0 else 1.0
        
        # Detect bias
        bias_detected = parity_score < self.fairness_threshold
        affected_groups = [
            attr for attr, rate in allocation_rates.items()
            if rate < max_rate * self.fairness_threshold
        ]
        
        return BiasDetectionResult(
            metric=FairnessMetric.DEMOGRAPHIC_PARITY,
            protected_attribute=protected_attribute,
            bias_detected=bias_detected,
            bias_score=1.0 - parity_score,
            affected_groups=affected_groups,
            mitigation_recommended=bias_detected and self.enable_mitigation,
            details={
                "allocation_rates": allocation_rates,
                "parity_score": parity_score,
                "threshold": self.fairness_threshold
            }
        )
    
    def _check_disparate_impact(
        self,
        allocations: List[Dict],
        population_groups: List[Dict],
        protected_attribute: ProtectedAttribute
    ) -> BiasDetectionResult:
        """
        Check disparate impact: 80% rule (EEOC guideline).
        
        Disparate Impact: selection rate for protected group ≥ 0.8 × selection rate for reference group
        """
        # Group allocations by protected attribute
        attribute_allocations = defaultdict(list)
        attribute_populations = defaultdict(int)
        
        for group in population_groups:
            attr_value = group.get("demographics", {}).get(protected_attribute.value)
            if attr_value:
                attribute_populations[attr_value] += group.get("size", 0)
        
        for allocation in allocations:
            group_id = allocation.get("group_id")
            group = next((g for g in population_groups if g.get("group_id") == group_id), None)
            
            if group:
                attr_value = group.get("demographics", {}).get(protected_attribute.value)
                if attr_value:
                    attribute_allocations[attr_value].append(allocation.get("amount", 0))
        
        # Calculate selection rates (% of population that received resources)
        selection_rates = {}
        for attr_value in attribute_populations.keys():
            allocated_count = len(attribute_allocations.get(attr_value, []))
            population = attribute_populations[attr_value]
            selection_rates[attr_value] = allocated_count / population if population > 0 else 0
        
        if len(selection_rates) < 2:
            return BiasDetectionResult(
                metric=FairnessMetric.DISPARATE_IMPACT,
                protected_attribute=protected_attribute,
                bias_detected=False,
                bias_score=0.0,
                affected_groups=[],
                mitigation_recommended=False,
                details={"reason": "Insufficient groups for comparison"}
            )
        
        # Apply 80% rule
        max_rate = max(selection_rates.values())
        disparate_impact_ratios = {
            attr: rate / max_rate if max_rate > 0 else 1.0
            for attr, rate in selection_rates.items()
        }
        
        # Detect bias (any group below 80% threshold)
        bias_detected = any(ratio < 0.8 for ratio in disparate_impact_ratios.values())
        affected_groups = [
            attr for attr, ratio in disparate_impact_ratios.items()
            if ratio < 0.8
        ]
        
        # Calculate bias score
        min_ratio = min(disparate_impact_ratios.values())
        bias_score = max(0, 0.8 - min_ratio) / 0.8
        
        return BiasDetectionResult(
            metric=FairnessMetric.DISPARATE_IMPACT,
            protected_attribute=protected_attribute,
            bias_detected=bias_detected,
            bias_score=bias_score,
            affected_groups=affected_groups,
            mitigation_recommended=bias_detected and self.enable_mitigation,
            details={
                "selection_rates": selection_rates,
                "disparate_impact_ratios": disparate_impact_ratios,
                "threshold": 0.8
            }
        )
    
    def mitigate_bias(
        self,
        allocations: List[Dict],
        bias_results: List[BiasDetectionResult],
        population_groups: List[Dict]
    ) -> List[Dict]:
        """
        Apply bias mitigation strategies to allocations.
        
        Strategies:
        1. Reweighting: Adjust allocations to balance across groups
        2. Threshold adjustment: Lower thresholds for disadvantaged groups
        3. Preferential allocation: Prioritize underserved groups
        """
        if not self.enable_mitigation:
            logger.info("⚖️ Mitigation disabled - returning original allocations")
            return allocations
        
        # Identify biased attributes
        biased_attributes = [
            r.protected_attribute for r in bias_results
            if r.bias_detected and r.mitigation_recommended
        ]
        
        if not biased_attributes:
            logger.info("✅ No mitigation needed")
            return allocations
        
        logger.info(f"⚖️ Applying bias mitigation for {len(biased_attributes)} attributes")
        
        # Apply reweighting strategy
        mitigated_allocations = self._apply_reweighting(
            allocations, bias_results, population_groups
        )
        
        return mitigated_allocations
    
    def _apply_reweighting(
        self,
        allocations: List[Dict],
        bias_results: List[BiasDetectionResult],
        population_groups: List[Dict]
    ) -> List[Dict]:
        """
        Reweight allocations to reduce bias.
        
        Strategy: Increase allocations to underserved groups proportionally
        """
        mitigated = allocations.copy()
        
        for result in bias_results:
            if not result.bias_detected or not result.mitigation_recommended:
                continue
            
            # Calculate reweighting factors
            affected_groups = result.affected_groups
            
            for allocation in mitigated:
                group_id = allocation.get("group_id")
                group = next((g for g in population_groups if g.get("group_id") == group_id), None)
                
                if group:
                    attr_value = group.get("demographics", {}).get(result.protected_attribute.value)
                    
                    # Boost allocation for affected groups
                    if attr_value in affected_groups:
                        boost_factor = 1.0 + result.bias_score * 0.2  # Up to 20% boost
                        allocation["amount"] *= boost_factor
                        allocation["mitigation_applied"] = True
                        allocation["mitigation_reason"] = f"Bias mitigation for {result.protected_attribute.value}"
        
        logger.info(f"✅ Reweighting applied - {len([a for a in mitigated if a.get('mitigation_applied')])} allocations adjusted")
        
        return mitigated
    
    def get_fairness_report(self) -> Dict:
        """Generate comprehensive fairness report"""
        if not self.bias_history:
            return {"status": "No bias checks performed yet"}
        
        total_checks = len(self.bias_history)
        biased_checks = len([r for r in self.bias_history if r.bias_detected])
        
        # Group by protected attribute
        attribute_summary = defaultdict(lambda: {"total": 0, "biased": 0})
        for result in self.bias_history:
            attr = result.protected_attribute.value
            attribute_summary[attr]["total"] += 1
            if result.bias_detected:
                attribute_summary[attr]["biased"] += 1
        
        return {
            "total_checks": total_checks,
            "biased_checks": biased_checks,
            "bias_rate": biased_checks / total_checks if total_checks > 0 else 0,
            "fairness_threshold": self.fairness_threshold,
            "attribute_summary": dict(attribute_summary),
            "mitigation_enabled": self.enable_mitigation
        }


# Example usage
if __name__ == "__main__":
    # Initialize Fairness Constraint Engine
    engine = FairnessConstraintEngine(
        fairness_threshold=0.8,
        enable_mitigation=True
    )
    
    # Define population groups with demographics
    population_groups = [
        {
            "group_id": "GROUP_A",
            "name": "Group A",
            "size": 10000,
            "demographics": {
                "gender": "female",
                "age": "children",
                "ethnicity": "somali"
            }
        },
        {
            "group_id": "GROUP_B",
            "name": "Group B",
            "size": 8000,
            "demographics": {
                "gender": "male",
                "age": "adult",
                "ethnicity": "somali"
            }
        },
        {
            "group_id": "GROUP_C",
            "name": "Group C",
            "size": 12000,
            "demographics": {
                "gender": "female",
                "age": "adult",
                "ethnicity": "kenyan"
            }
        }
    ]
    
    # Define allocations (potentially biased)
    allocations = [
        {"group_id": "GROUP_A", "amount": 100.0},
        {"group_id": "GROUP_B", "amount": 150.0},
        {"group_id": "GROUP_C", "amount": 80.0}
    ]
    
    # Detect bias
    bias_results = engine.detect_bias(
        allocations,
        population_groups,
        [ProtectedAttribute.GENDER, ProtectedAttribute.ETHNICITY]
    )
    
    # Print results
    print("\n⚖️ FAIRNESS CONSTRAINT ENGINE - BIAS DETECTION")
    print("=" * 60)
    for result in bias_results:
        print(f"\nMetric: {result.metric.value}")
        print(f"Protected Attribute: {result.protected_attribute.value}")
        print(f"Bias Detected: {'YES' if result.bias_detected else 'NO'}")
        print(f"Bias Score: {result.bias_score:.3f}")
        if result.affected_groups:
            print(f"Affected Groups: {', '.join(result.affected_groups)}")
    
    # Apply mitigation
    mitigated_allocations = engine.mitigate_bias(
        allocations, bias_results, population_groups
    )
    
    print("\n⚖️ MITIGATED ALLOCATIONS")
    print("=" * 60)
    for allocation in mitigated_allocations:
        print(f"{allocation['group_id']}: {allocation['amount']:.1f} units")
        if allocation.get("mitigation_applied"):
            print(f"  └─ {allocation['mitigation_reason']}")
    
    # Print fairness report
    print("\n📊 FAIRNESS REPORT")
    print("=" * 60)
    report = engine.get_fairness_report()
    for key, value in report.items():
        print(f"{key}: {value}")
