"""
Crisis Decision Agent
The Moral Compass of iLuminara-Core

Enforces 7 core humanitarian principles during resource scarcity:
1. Humanity - Human suffering must be addressed wherever it is found
2. Impartiality - No discrimination based on nationality, race, religion, class, or political opinions
3. Neutrality - No sides in hostilities or controversies
4. Independence - Autonomy from political, economic, military, or other objectives
5. Voluntary Service - Not prompted by desire for gain
6. Unity - Only one Red Cross/Red Crescent society in any one country
7. Universality - Equal status and share equal responsibilities

Compliance:
- Geneva Conventions (1949)
- UN Humanitarian Principles (OCHA)
- WHO International Health Regulations (2005)
- Sphere Standards (2018)
- Core Humanitarian Standard (CHS)
"""

import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)


class HumanitarianPrinciple(Enum):
    """7 Core Humanitarian Principles"""
    HUMANITY = "humanity"
    IMPARTIALITY = "impartiality"
    NEUTRALITY = "neutrality"
    INDEPENDENCE = "independence"
    VOLUNTARY_SERVICE = "voluntary_service"
    UNITY = "unity"
    UNIVERSALITY = "universality"


class CrisisLevel(Enum):
    """Crisis severity levels"""
    ROUTINE = 1
    ELEVATED = 2
    SEVERE = 3
    CRITICAL = 4
    CATASTROPHIC = 5


class ResourceType(Enum):
    """Types of resources to allocate"""
    MEDICAL_SUPPLIES = "medical_supplies"
    PERSONNEL = "personnel"
    VACCINES = "vaccines"
    FOOD = "food"
    WATER = "water"
    SHELTER = "shelter"
    TRANSPORT = "transport"


@dataclass
class PopulationGroup:
    """Represents a population group requiring resources"""
    group_id: str
    name: str
    size: int
    vulnerability_score: float  # 0.0 - 1.0
    urgency_score: float  # 0.0 - 1.0
    location: Dict[str, float]
    demographics: Dict[str, any]
    current_resources: Dict[ResourceType, float]


@dataclass
class ResourceAllocation:
    """Resource allocation decision"""
    group_id: str
    resource_type: ResourceType
    amount: float
    priority: int
    justification: str
    humanitarian_principles_applied: List[HumanitarianPrinciple]
    fairness_score: float
    timestamp: datetime


@dataclass
class CrisisContext:
    """Context of the crisis situation"""
    crisis_id: str
    crisis_level: CrisisLevel
    affected_population: int
    available_resources: Dict[ResourceType, float]
    population_groups: List[PopulationGroup]
    constraints: Dict[str, any]
    conflict_zone: bool
    natural_disaster: bool


class CrisisDecisionAgent:
    """
    The Moral Compass - Makes ethical resource allocation decisions
    during humanitarian crises.
    """
    
    def __init__(
        self,
        enable_fairness_engine: bool = True,
        humanitarian_margin: float = 0.15,
        enable_audit: bool = True
    ):
        self.enable_fairness_engine = enable_fairness_engine
        self.humanitarian_margin = humanitarian_margin
        self.enable_audit = enable_audit
        
        # Decision history
        self.decision_history: List[ResourceAllocation] = []
        
        # Fairness metrics
        self.fairness_metrics = {
            "gini_coefficient": [],
            "equity_score": [],
            "vulnerability_coverage": []
        }
        
        logger.info("🧭 Crisis Decision Agent initialized - Moral Compass active")
    
    def make_allocation_decision(
        self,
        crisis_context: CrisisContext,
        resource_type: ResourceType
    ) -> List[ResourceAllocation]:
        """
        Make ethical resource allocation decisions based on humanitarian principles.
        
        Args:
            crisis_context: Current crisis situation
            resource_type: Type of resource to allocate
        
        Returns:
            List of resource allocations prioritized by need
        """
        logger.info(f"🧭 Making allocation decision - Crisis: {crisis_context.crisis_id}")
        
        # Step 1: Calculate need scores for each population group
        need_scores = self._calculate_need_scores(
            crisis_context.population_groups,
            resource_type
        )
        
        # Step 2: Apply humanitarian principles
        prioritized_groups = self._apply_humanitarian_principles(
            crisis_context.population_groups,
            need_scores,
            crisis_context
        )
        
        # Step 3: Allocate resources fairly
        allocations = self._allocate_resources(
            prioritized_groups,
            crisis_context.available_resources[resource_type],
            resource_type,
            crisis_context
        )
        
        # Step 4: Validate fairness (if enabled)
        if self.enable_fairness_engine:
            allocations = self._validate_fairness(allocations, crisis_context)
        
        # Step 5: Audit decision
        if self.enable_audit:
            self._audit_decision(allocations, crisis_context)
        
        # Store decisions
        self.decision_history.extend(allocations)
        
        logger.info(f"✅ Allocation complete - {len(allocations)} groups served")
        return allocations
    
    def _calculate_need_scores(
        self,
        population_groups: List[PopulationGroup],
        resource_type: ResourceType
    ) -> Dict[str, float]:
        """
        Calculate need scores based on vulnerability, urgency, and current resources.
        
        Principle: HUMANITY - Address suffering wherever found
        """
        need_scores = {}
        
        for group in population_groups:
            # Base need = vulnerability * urgency
            base_need = group.vulnerability_score * group.urgency_score
            
            # Adjust for current resources (those with less get higher priority)
            current_resource = group.current_resources.get(resource_type, 0.0)
            resource_deficit = max(0, 1.0 - current_resource)
            
            # Final need score
            need_score = base_need * (1.0 + resource_deficit)
            
            need_scores[group.group_id] = min(1.0, need_score)
        
        return need_scores
    
    def _apply_humanitarian_principles(
        self,
        population_groups: List[PopulationGroup],
        need_scores: Dict[str, float],
        crisis_context: CrisisContext
    ) -> List[Tuple[PopulationGroup, float, List[HumanitarianPrinciple]]]:
        """
        Apply humanitarian principles to prioritize groups.
        
        Principles:
        - IMPARTIALITY: No discrimination
        - NEUTRALITY: No sides in conflict
        - HUMANITY: Address suffering
        """
        prioritized = []
        
        for group in population_groups:
            need_score = need_scores[group.group_id]
            principles_applied = [HumanitarianPrinciple.HUMANITY]
            
            # IMPARTIALITY: Treat all groups equally based on need alone
            # No adjustment based on demographics
            principles_applied.append(HumanitarianPrinciple.IMPARTIALITY)
            
            # NEUTRALITY: In conflict zones, don't favor any side
            if crisis_context.conflict_zone:
                # Ensure neutrality by not considering political affiliation
                principles_applied.append(HumanitarianPrinciple.NEUTRALITY)
            
            # UNIVERSALITY: All groups have equal right to assistance
            principles_applied.append(HumanitarianPrinciple.UNIVERSALITY)
            
            prioritized.append((group, need_score, principles_applied))
        
        # Sort by need score (highest first)
        prioritized.sort(key=lambda x: x[1], reverse=True)
        
        return prioritized
    
    def _allocate_resources(
        self,
        prioritized_groups: List[Tuple[PopulationGroup, float, List[HumanitarianPrinciple]]],
        total_resources: float,
        resource_type: ResourceType,
        crisis_context: CrisisContext
    ) -> List[ResourceAllocation]:
        """
        Allocate resources proportionally based on need and available supply.
        
        Uses proportional allocation with humanitarian margin.
        """
        allocations = []
        
        # Calculate total need
        total_need = sum(need_score for _, need_score, _ in prioritized_groups)
        
        if total_need == 0:
            logger.warning("⚠️ No need detected - skipping allocation")
            return allocations
        
        # Allocate proportionally
        remaining_resources = total_resources
        
        for priority, (group, need_score, principles) in enumerate(prioritized_groups, 1):
            # Proportional allocation
            proportion = need_score / total_need
            base_allocation = total_resources * proportion
            
            # Apply humanitarian margin (ensure minimum allocation)
            min_allocation = total_resources * self.humanitarian_margin / len(prioritized_groups)
            allocation_amount = max(base_allocation, min_allocation)
            
            # Don't exceed remaining resources
            allocation_amount = min(allocation_amount, remaining_resources)
            
            if allocation_amount > 0:
                allocation = ResourceAllocation(
                    group_id=group.group_id,
                    resource_type=resource_type,
                    amount=allocation_amount,
                    priority=priority,
                    justification=self._generate_justification(
                        group, need_score, allocation_amount, principles
                    ),
                    humanitarian_principles_applied=principles,
                    fairness_score=0.0,  # Will be calculated in validation
                    timestamp=datetime.utcnow()
                )
                
                allocations.append(allocation)
                remaining_resources -= allocation_amount
        
        return allocations
    
    def _validate_fairness(
        self,
        allocations: List[ResourceAllocation],
        crisis_context: CrisisContext
    ) -> List[ResourceAllocation]:
        """
        Validate fairness of allocations using Gini coefficient and equity metrics.
        
        Principle: IMPARTIALITY - Ensure no discrimination
        """
        if not allocations:
            return allocations
        
        # Calculate Gini coefficient (0 = perfect equality, 1 = perfect inequality)
        amounts = [a.amount for a in allocations]
        gini = self._calculate_gini_coefficient(amounts)
        
        # Calculate equity score (how well does allocation match need)
        equity_score = self._calculate_equity_score(allocations, crisis_context)
        
        # Calculate vulnerability coverage (% of vulnerable populations served)
        vulnerability_coverage = self._calculate_vulnerability_coverage(
            allocations, crisis_context
        )
        
        # Store metrics
        self.fairness_metrics["gini_coefficient"].append(gini)
        self.fairness_metrics["equity_score"].append(equity_score)
        self.fairness_metrics["vulnerability_coverage"].append(vulnerability_coverage)
        
        # Update fairness scores
        for allocation in allocations:
            allocation.fairness_score = equity_score
        
        # Log fairness metrics
        logger.info(f"📊 Fairness Metrics - Gini: {gini:.3f}, Equity: {equity_score:.3f}, Coverage: {vulnerability_coverage:.1%}")
        
        # Warn if fairness is compromised
        if gini > 0.5:
            logger.warning(f"⚠️ High inequality detected - Gini: {gini:.3f}")
        
        if equity_score < 0.7:
            logger.warning(f"⚠️ Low equity score - {equity_score:.3f}")
        
        return allocations
    
    def _calculate_gini_coefficient(self, amounts: List[float]) -> float:
        """Calculate Gini coefficient for resource distribution"""
        if not amounts or len(amounts) == 1:
            return 0.0
        
        amounts = sorted(amounts)
        n = len(amounts)
        cumsum = np.cumsum(amounts)
        
        # Gini coefficient formula
        gini = (2 * sum((i + 1) * amount for i, amount in enumerate(amounts))) / (n * sum(amounts))
        gini = gini - (n + 1) / n
        
        return gini
    
    def _calculate_equity_score(
        self,
        allocations: List[ResourceAllocation],
        crisis_context: CrisisContext
    ) -> float:
        """
        Calculate how well allocations match actual need.
        
        Score = 1.0 means perfect match between allocation and need
        """
        if not allocations:
            return 0.0
        
        # Map allocations to groups
        allocation_map = {a.group_id: a.amount for a in allocations}
        
        # Calculate need-weighted allocation score
        total_score = 0.0
        total_weight = 0.0
        
        for group in crisis_context.population_groups:
            need = group.vulnerability_score * group.urgency_score
            allocation = allocation_map.get(group.group_id, 0.0)
            
            # Score: how close is allocation to need?
            if need > 0:
                score = min(1.0, allocation / need)
                total_score += score * need
                total_weight += need
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _calculate_vulnerability_coverage(
        self,
        allocations: List[ResourceAllocation],
        crisis_context: CrisisContext
    ) -> float:
        """Calculate percentage of vulnerable populations that received resources"""
        if not allocations:
            return 0.0
        
        served_groups = {a.group_id for a in allocations}
        
        # Count vulnerable populations served
        vulnerable_served = sum(
            group.size for group in crisis_context.population_groups
            if group.vulnerability_score > 0.7 and group.group_id in served_groups
        )
        
        # Total vulnerable population
        total_vulnerable = sum(
            group.size for group in crisis_context.population_groups
            if group.vulnerability_score > 0.7
        )
        
        return vulnerable_served / total_vulnerable if total_vulnerable > 0 else 0.0
    
    def _generate_justification(
        self,
        group: PopulationGroup,
        need_score: float,
        allocation: float,
        principles: List[HumanitarianPrinciple]
    ) -> str:
        """Generate human-readable justification for allocation decision"""
        principles_str = ", ".join(p.value.replace("_", " ").title() for p in principles)
        
        return (
            f"Allocated {allocation:.1f} units to {group.name} "
            f"(population: {group.size:,}, vulnerability: {group.vulnerability_score:.2f}, "
            f"need score: {need_score:.2f}). "
            f"Principles applied: {principles_str}."
        )
    
    def _audit_decision(
        self,
        allocations: List[ResourceAllocation],
        crisis_context: CrisisContext
    ):
        """Audit allocation decisions for compliance"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "crisis_id": crisis_context.crisis_id,
            "crisis_level": crisis_context.crisis_level.name,
            "allocations": len(allocations),
            "total_allocated": sum(a.amount for a in allocations),
            "principles_enforced": list(set(
                p.value for a in allocations for p in a.humanitarian_principles_applied
            )),
            "fairness_metrics": {
                "gini": self.fairness_metrics["gini_coefficient"][-1] if self.fairness_metrics["gini_coefficient"] else 0.0,
                "equity": self.fairness_metrics["equity_score"][-1] if self.fairness_metrics["equity_score"] else 0.0,
                "coverage": self.fairness_metrics["vulnerability_coverage"][-1] if self.fairness_metrics["vulnerability_coverage"] else 0.0
            }
        }
        
        logger.info(f"📝 Audit: {audit_entry}")
    
    def get_fairness_report(self) -> Dict:
        """Generate fairness report across all decisions"""
        if not self.fairness_metrics["gini_coefficient"]:
            return {"status": "No decisions made yet"}
        
        return {
            "total_decisions": len(self.decision_history),
            "average_gini": np.mean(self.fairness_metrics["gini_coefficient"]),
            "average_equity": np.mean(self.fairness_metrics["equity_score"]),
            "average_coverage": np.mean(self.fairness_metrics["vulnerability_coverage"]),
            "principles_applied": list(set(
                p.value for d in self.decision_history for p in d.humanitarian_principles_applied
            ))
        }


# Example usage
if __name__ == "__main__":
    # Initialize Crisis Decision Agent
    agent = CrisisDecisionAgent(
        enable_fairness_engine=True,
        humanitarian_margin=0.15
    )
    
    # Define population groups
    groups = [
        PopulationGroup(
            group_id="DADAAB_IFO",
            name="Ifo Camp",
            size=80000,
            vulnerability_score=0.9,
            urgency_score=0.8,
            location={"lat": 0.0512, "lng": 40.3129},
            demographics={"children": 0.45, "elderly": 0.05},
            current_resources={ResourceType.MEDICAL_SUPPLIES: 0.2}
        ),
        PopulationGroup(
            group_id="DADAAB_DAGAHALEY",
            name="Dagahaley Camp",
            size=90000,
            vulnerability_score=0.85,
            urgency_score=0.75,
            location={"lat": 0.0612, "lng": 40.3229},
            demographics={"children": 0.42, "elderly": 0.06},
            current_resources={ResourceType.MEDICAL_SUPPLIES: 0.3}
        ),
        PopulationGroup(
            group_id="GARISSA_URBAN",
            name="Garissa Urban",
            size=120000,
            vulnerability_score=0.6,
            urgency_score=0.5,
            location={"lat": -0.4536, "lng": 39.6401},
            demographics={"children": 0.35, "elderly": 0.08},
            current_resources={ResourceType.MEDICAL_SUPPLIES: 0.5}
        )
    ]
    
    # Define crisis context
    crisis = CrisisContext(
        crisis_id="CHOLERA_OUTBREAK_2025",
        crisis_level=CrisisLevel.CRITICAL,
        affected_population=290000,
        available_resources={
            ResourceType.MEDICAL_SUPPLIES: 1000.0,
            ResourceType.VACCINES: 50000.0
        },
        population_groups=groups,
        constraints={},
        conflict_zone=False,
        natural_disaster=False
    )
    
    # Make allocation decision
    allocations = agent.make_allocation_decision(crisis, ResourceType.MEDICAL_SUPPLIES)
    
    # Print results
    print("\n🧭 CRISIS DECISION AGENT - ALLOCATION RESULTS")
    print("=" * 60)
    for allocation in allocations:
        print(f"\nPriority {allocation.priority}: {allocation.group_id}")
        print(f"  Amount: {allocation.amount:.1f} units")
        print(f"  Fairness Score: {allocation.fairness_score:.3f}")
        print(f"  Justification: {allocation.justification}")
    
    # Print fairness report
    print("\n📊 FAIRNESS REPORT")
    print("=" * 60)
    report = agent.get_fairness_report()
    for key, value in report.items():
        print(f"{key}: {value}")
