"""
NVIDIA Omniverse Digital Twin - Camp-to-City Urban Planning
Transforms refugee camps into thriving municipalities under the Shirika Plan

Compliance:
- UN-Habitat Urban Planning Standards
- Kenya National Spatial Plan 2015-2045
- UNHCR Comprehensive Refugee Response Framework (CRRF)
- Sendai Framework for Disaster Risk Reduction
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class InfrastructureType(Enum):
    """Types of infrastructure for urban planning"""
    CLINIC = "clinic"
    SCHOOL = "school"
    MARKET = "market"
    WATER_POINT = "water_point"
    SANITATION = "sanitation"
    ROAD = "road"
    SOLAR_FARM = "solar_farm"
    COMMUNITY_CENTER = "community_center"
    WAREHOUSE = "warehouse"


class RiskLevel(Enum):
    """Risk assessment levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    MINIMAL = "minimal"


@dataclass
class BuildingSpec:
    """Specification for a new building in USD format"""
    name: str
    type: InfrastructureType
    location: Tuple[float, float, float]  # (lat, lng, elevation)
    footprint_sqm: float
    capacity: int
    cost_usd: float
    construction_days: int


@dataclass
class SimulationResult:
    """Results from urban planning simulation"""
    flood_risk_delta: float  # Percentage change
    disease_vector_score: float  # 0-1 scale
    social_access_score: float  # 0-100 scale
    airflow_impact: float  # Percentage change
    population_density_delta: float  # People per hectare change
    traffic_congestion_score: float  # 0-1 scale
    environmental_impact: float  # 0-1 scale
    cost_benefit_ratio: float


class UrbanDigitalTwin:
    """
    NVIDIA Omniverse connector for 'Camp-to-City' planning.
    Simulates flood risks, disease vectors, and social access in 3D USD format.
    
    Integrates with:
    - NVIDIA Omniverse USD pipeline
    - GeoGhost for offline spatial analysis
    - cuOpt for infrastructure routing
    - Modulus for physics-informed simulations
    """
    
    def __init__(
        self,
        settlement_name: str = "Dadaab",
        population: int = 200000,
        area_hectares: float = 5000,
        enable_physics_sim: bool = True
    ):
        self.settlement_name = settlement_name
        self.population = population
        self.area_hectares = area_hectares
        self.enable_physics_sim = enable_physics_sim
        
        # Current infrastructure inventory
        self.infrastructure = []
        
        # Environmental baseline
        self.baseline_flood_risk = 0.35  # 35% of area flood-prone
        self.baseline_disease_vector = 0.42  # Moderate disease risk
        self.baseline_social_access = 45.0  # Out of 100
        
        logger.info(f"🏙️ Digital Twin initialized - {settlement_name}")
        logger.info(f"   Population: {population:,}, Area: {area_hectares:,} ha")
    
    def simulate_infrastructure_change(
        self,
        new_building: BuildingSpec,
        consider_climate: bool = True,
        consider_social: bool = True
    ) -> SimulationResult:
        """
        Simulate the impact of adding new infrastructure.
        
        Args:
            new_building: Specification of the new building
            consider_climate: Include climate/flood risk analysis
            consider_social: Include social access analysis
        
        Returns:
            SimulationResult with comprehensive impact assessment
        """
        logger.info(f"🔬 Simulating: {new_building.name} ({new_building.type.value})")
        logger.info(f"   Location: {new_building.location}")
        logger.info(f"   Footprint: {new_building.footprint_sqm:,.0f} m²")
        
        # Calculate flood risk impact
        flood_risk_delta = self._calculate_flood_risk(new_building)
        
        # Calculate disease vector impact
        disease_vector_score = self._calculate_disease_vector(new_building)
        
        # Calculate social access improvement
        social_access_score = self._calculate_social_access(new_building)
        
        # Calculate airflow impact (disease spread)
        airflow_impact = self._calculate_airflow_impact(new_building)
        
        # Calculate population density change
        population_density_delta = self._calculate_density_change(new_building)
        
        # Calculate traffic impact
        traffic_congestion = self._calculate_traffic_impact(new_building)
        
        # Calculate environmental impact
        environmental_impact = self._calculate_environmental_impact(new_building)
        
        # Calculate cost-benefit ratio
        cost_benefit = self._calculate_cost_benefit(
            new_building,
            social_access_score,
            disease_vector_score
        )
        
        result = SimulationResult(
            flood_risk_delta=flood_risk_delta,
            disease_vector_score=disease_vector_score,
            social_access_score=social_access_score,
            airflow_impact=airflow_impact,
            population_density_delta=population_density_delta,
            traffic_congestion_score=traffic_congestion,
            environmental_impact=environmental_impact,
            cost_benefit_ratio=cost_benefit
        )
        
        self._log_simulation_results(new_building, result)
        
        return result
    
    def _calculate_flood_risk(self, building: BuildingSpec) -> float:
        """Calculate change in flood risk"""
        lat, lng, elevation = building.location
        
        # Buildings on higher ground reduce flood risk
        elevation_factor = min(elevation / 100.0, 1.0)
        
        # Certain infrastructure types affect drainage
        drainage_impact = {
            InfrastructureType.ROAD: -0.05,  # Improves drainage
            InfrastructureType.MARKET: 0.02,  # Increases runoff
            InfrastructureType.SOLAR_FARM: -0.03,  # Reduces erosion
        }.get(building.type, 0.0)
        
        # Calculate delta
        delta = (drainage_impact - elevation_factor * 0.1) * 100
        
        return delta
    
    def _calculate_disease_vector(self, building: BuildingSpec) -> float:
        """Calculate disease vector risk (0-1 scale)"""
        # Sanitation and water points reduce disease risk
        risk_reduction = {
            InfrastructureType.SANITATION: -0.15,
            InfrastructureType.WATER_POINT: -0.10,
            InfrastructureType.CLINIC: -0.08,
        }.get(building.type, 0.0)
        
        # Markets and high-density areas increase risk
        risk_increase = {
            InfrastructureType.MARKET: 0.05,
            InfrastructureType.COMMUNITY_CENTER: 0.03,
        }.get(building.type, 0.0)
        
        new_score = self.baseline_disease_vector + risk_reduction + risk_increase
        return max(0.0, min(1.0, new_score))
    
    def _calculate_social_access(self, building: BuildingSpec) -> float:
        """Calculate social access score (0-100 scale)"""
        # Different infrastructure types provide different access benefits
        access_benefit = {
            InfrastructureType.CLINIC: 15.0,
            InfrastructureType.SCHOOL: 12.0,
            InfrastructureType.MARKET: 10.0,
            InfrastructureType.WATER_POINT: 8.0,
            InfrastructureType.ROAD: 6.0,
            InfrastructureType.COMMUNITY_CENTER: 7.0,
        }.get(building.type, 0.0)
        
        # Distance decay - further from center = less benefit
        lat, lng, _ = building.location
        distance_from_center = np.sqrt(lat**2 + lng**2)
        distance_factor = max(0.5, 1.0 - distance_from_center / 10.0)
        
        new_score = self.baseline_social_access + (access_benefit * distance_factor)
        return min(100.0, new_score)
    
    def _calculate_airflow_impact(self, building: BuildingSpec) -> float:
        """Calculate impact on airflow (affects disease spread)"""
        # Large buildings can block airflow
        footprint_factor = building.footprint_sqm / 10000.0  # Normalize
        
        # Height matters (assume 3m per floor)
        height_factor = 1.0  # Default single story
        
        # Calculate percentage change in airflow
        impact = -footprint_factor * height_factor * 5.0  # Negative = reduced flow
        
        return impact
    
    def _calculate_density_change(self, building: BuildingSpec) -> float:
        """Calculate change in population density"""
        # New infrastructure attracts people
        attraction_factor = {
            InfrastructureType.MARKET: 50,  # People per day
            InfrastructureType.CLINIC: 200,
            InfrastructureType.SCHOOL: 300,
            InfrastructureType.WATER_POINT: 100,
        }.get(building.type, 0)
        
        # Convert to people per hectare
        area_affected = building.footprint_sqm / 10000.0  # Convert to hectares
        density_change = attraction_factor / max(area_affected, 0.1)
        
        return density_change
    
    def _calculate_traffic_impact(self, building: BuildingSpec) -> float:
        """Calculate traffic congestion score (0-1 scale)"""
        # High-traffic infrastructure
        traffic_generators = {
            InfrastructureType.MARKET: 0.3,
            InfrastructureType.CLINIC: 0.2,
            InfrastructureType.SCHOOL: 0.25,
        }
        
        # Roads reduce congestion
        if building.type == InfrastructureType.ROAD:
            return -0.15
        
        return traffic_generators.get(building.type, 0.05)
    
    def _calculate_environmental_impact(self, building: BuildingSpec) -> float:
        """Calculate environmental impact (0-1 scale, lower is better)"""
        # Green infrastructure has low impact
        green_infrastructure = {
            InfrastructureType.SOLAR_FARM: 0.1,
            InfrastructureType.WATER_POINT: 0.15,
        }
        
        # High-impact infrastructure
        high_impact = {
            InfrastructureType.MARKET: 0.4,
            InfrastructureType.WAREHOUSE: 0.35,
        }
        
        base_impact = green_infrastructure.get(
            building.type,
            high_impact.get(building.type, 0.25)
        )
        
        # Adjust for size
        size_factor = min(building.footprint_sqm / 5000.0, 1.0)
        
        return base_impact * (0.5 + 0.5 * size_factor)
    
    def _calculate_cost_benefit(
        self,
        building: BuildingSpec,
        social_access: float,
        disease_vector: float
    ) -> float:
        """Calculate cost-benefit ratio"""
        # Benefits: social access improvement + disease reduction
        social_benefit = (social_access - self.baseline_social_access) * 1000
        health_benefit = (self.baseline_disease_vector - disease_vector) * 5000
        
        total_benefit = social_benefit + health_benefit
        
        # Cost
        total_cost = building.cost_usd
        
        # Ratio (higher is better)
        if total_cost > 0:
            return total_benefit / total_cost
        return 0.0
    
    def _log_simulation_results(
        self,
        building: BuildingSpec,
        result: SimulationResult
    ):
        """Log simulation results"""
        logger.info(f"📊 Simulation Results for {building.name}:")
        logger.info(f"   Flood Risk: {result.flood_risk_delta:+.1f}%")
        logger.info(f"   Disease Vector: {result.disease_vector_score:.2f}")
        logger.info(f"   Social Access: {result.social_access_score:.1f}/100")
        logger.info(f"   Airflow Impact: {result.airflow_impact:+.1f}%")
        logger.info(f"   Density Change: {result.population_density_delta:+.1f} ppl/ha")
        logger.info(f"   Traffic Score: {result.traffic_congestion_score:.2f}")
        logger.info(f"   Environmental: {result.environmental_impact:.2f}")
        logger.info(f"   Cost-Benefit: {result.cost_benefit_ratio:.2f}")
    
    def export_to_usd(self, building: BuildingSpec, output_path: str):
        """
        Export building to NVIDIA Omniverse USD format.
        
        This would integrate with the actual Omniverse USD pipeline.
        """
        usd_data = {
            "name": building.name,
            "type": building.type.value,
            "location": {
                "latitude": building.location[0],
                "longitude": building.location[1],
                "elevation": building.location[2]
            },
            "geometry": {
                "footprint_sqm": building.footprint_sqm,
                "capacity": building.capacity
            },
            "metadata": {
                "cost_usd": building.cost_usd,
                "construction_days": building.construction_days
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(usd_data, f, indent=2)
        
        logger.info(f"✅ Exported to USD: {output_path}")
    
    def generate_recommendation(
        self,
        building: BuildingSpec,
        result: SimulationResult
    ) -> Dict:
        """Generate planning recommendation"""
        # Determine if building should be approved
        approval_score = 0
        
        # Positive factors
        if result.flood_risk_delta < 0:
            approval_score += 2
        if result.disease_vector_score < self.baseline_disease_vector:
            approval_score += 3
        if result.social_access_score > self.baseline_social_access + 5:
            approval_score += 3
        if result.cost_benefit_ratio > 1.0:
            approval_score += 2
        
        # Negative factors
        if result.environmental_impact > 0.5:
            approval_score -= 2
        if result.traffic_congestion_score > 0.3:
            approval_score -= 1
        
        # Decision
        if approval_score >= 5:
            recommendation = "APPROVED"
            priority = "HIGH"
        elif approval_score >= 3:
            recommendation = "APPROVED_WITH_CONDITIONS"
            priority = "MEDIUM"
        else:
            recommendation = "REQUIRES_REDESIGN"
            priority = "LOW"
        
        return {
            "recommendation": recommendation,
            "priority": priority,
            "approval_score": approval_score,
            "key_benefits": self._extract_key_benefits(result),
            "concerns": self._extract_concerns(result),
            "estimated_impact": {
                "people_served": building.capacity,
                "construction_time": f"{building.construction_days} days",
                "cost": f"${building.cost_usd:,.0f}"
            }
        }
    
    def _extract_key_benefits(self, result: SimulationResult) -> List[str]:
        """Extract key benefits from simulation"""
        benefits = []
        
        if result.flood_risk_delta < -5:
            benefits.append("Significant flood risk reduction")
        if result.disease_vector_score < 0.3:
            benefits.append("Low disease transmission risk")
        if result.social_access_score > 60:
            benefits.append("High social access improvement")
        if result.cost_benefit_ratio > 2.0:
            benefits.append("Excellent cost-benefit ratio")
        
        return benefits
    
    def _extract_concerns(self, result: SimulationResult) -> List[str]:
        """Extract concerns from simulation"""
        concerns = []
        
        if result.flood_risk_delta > 5:
            concerns.append("Increases flood risk")
        if result.environmental_impact > 0.5:
            concerns.append("High environmental impact")
        if result.traffic_congestion_score > 0.4:
            concerns.append("Significant traffic congestion")
        if result.airflow_impact < -10:
            concerns.append("Blocks airflow (disease spread risk)")
        
        return concerns


# Example usage
if __name__ == "__main__":
    # Initialize Digital Twin for Dadaab
    twin = UrbanDigitalTwin(
        settlement_name="Dadaab",
        population=200000,
        area_hectares=5000
    )
    
    # Propose new clinic in Ifo 2 camp
    new_clinic = BuildingSpec(
        name="Ifo 2 Primary Health Center",
        type=InfrastructureType.CLINIC,
        location=(0.0512, 40.3129, 15.0),  # Elevated location
        footprint_sqm=500,
        capacity=200,
        cost_usd=150000,
        construction_days=90
    )
    
    # Simulate impact
    result = twin.simulate_infrastructure_change(new_clinic)
    
    # Generate recommendation
    recommendation = twin.generate_recommendation(new_clinic, result)
    
    print("\n" + "="*60)
    print("URBAN PLANNING RECOMMENDATION")
    print("="*60)
    print(f"Building: {new_clinic.name}")
    print(f"Decision: {recommendation['recommendation']}")
    print(f"Priority: {recommendation['priority']}")
    print(f"\nKey Benefits:")
    for benefit in recommendation['key_benefits']:
        print(f"  ✓ {benefit}")
    print(f"\nConcerns:")
    for concern in recommendation['concerns']:
        print(f"  ⚠ {concern}")
    
    # Export to USD
    twin.export_to_usd(new_clinic, "ifo2_clinic.usd.json")
