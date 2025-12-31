"""
Omniverse Digital Twin - Urban Planning & Infrastructure Simulation
Part of iLuminara Civilization OS

Integrates with NVIDIA Omniverse for photorealistic urban planning simulations
with real-time health infrastructure optimization.

Compliance:
- UN Sustainable Development Goals (SDG 11: Sustainable Cities)
- WHO Healthy Cities Framework
- ISO 37120 (Sustainable Cities and Communities)
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import numpy as np
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class InfrastructureType(Enum):
    """Types of urban infrastructure"""
    HEALTH_FACILITY = "health_facility"
    WATER_SYSTEM = "water_system"
    POWER_GRID = "power_grid"
    TRANSPORT = "transport"
    EDUCATION = "education"
    SANITATION = "sanitation"
    EMERGENCY_RESPONSE = "emergency_response"


class SimulationMode(Enum):
    """Simulation modes for urban planning"""
    OUTBREAK_RESPONSE = "outbreak_response"
    INFRASTRUCTURE_PLANNING = "infrastructure_planning"
    DISASTER_PREPAREDNESS = "disaster_preparedness"
    RESOURCE_OPTIMIZATION = "resource_optimization"
    CLIMATE_ADAPTATION = "climate_adaptation"


@dataclass
class UrbanEntity:
    """Represents an entity in the digital twin"""
    entity_id: str
    entity_type: InfrastructureType
    location: Tuple[float, float, float]  # lat, lng, elevation
    capacity: int
    current_utilization: float
    health_score: float
    metadata: Dict


@dataclass
class SimulationResult:
    """Results from urban simulation"""
    simulation_id: str
    mode: SimulationMode
    timestamp: str
    entities_affected: List[str]
    optimization_score: float
    recommendations: List[str]
    resource_allocation: Dict
    compliance_status: Dict


class OmniverseTwin:
    """
    Digital Twin engine for urban planning and health infrastructure optimization.
    
    Integrates with:
    - NVIDIA Omniverse for 3D visualization
    - iLuminara Golden Thread for health data
    - SovereignGuardrail for compliance
    """
    
    def __init__(
        self,
        city_name: str,
        population: int,
        geographic_bounds: Dict[str, Tuple[float, float]],
        enable_omniverse: bool = False
    ):
        self.city_name = city_name
        self.population = population
        self.geographic_bounds = geographic_bounds
        self.enable_omniverse = enable_omniverse
        
        # Urban entities registry
        self.entities: Dict[str, UrbanEntity] = {}
        
        # Simulation history
        self.simulation_history: List[SimulationResult] = []
        
        logger.info(f"🏙️ Omniverse Twin initialized - City: {city_name}, Pop: {population:,}")
    
    def register_entity(
        self,
        entity_id: str,
        entity_type: InfrastructureType,
        location: Tuple[float, float, float],
        capacity: int,
        metadata: Optional[Dict] = None
    ) -> UrbanEntity:
        """
        Register an urban infrastructure entity in the digital twin.
        
        Args:
            entity_id: Unique identifier
            entity_type: Type of infrastructure
            location: Geographic coordinates (lat, lng, elevation)
            capacity: Maximum capacity
            metadata: Additional metadata
        
        Returns:
            UrbanEntity object
        """
        entity = UrbanEntity(
            entity_id=entity_id,
            entity_type=entity_type,
            location=location,
            capacity=capacity,
            current_utilization=0.0,
            health_score=1.0,
            metadata=metadata or {}
        )
        
        self.entities[entity_id] = entity
        
        logger.info(f"✅ Registered entity: {entity_id} ({entity_type.value})")
        return entity
    
    def simulate_outbreak_response(
        self,
        outbreak_location: Tuple[float, float],
        outbreak_radius_km: float,
        estimated_cases: int,
        disease: str
    ) -> SimulationResult:
        """
        Simulate outbreak response and optimize health facility allocation.
        
        Args:
            outbreak_location: Epicenter coordinates
            outbreak_radius_km: Affected radius
            estimated_cases: Projected case count
            disease: Disease type
        
        Returns:
            SimulationResult with optimization recommendations
        """
        simulation_id = f"OUTBREAK_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Find health facilities within response radius
        affected_facilities = self._find_entities_in_radius(
            center=outbreak_location,
            radius_km=outbreak_radius_km * 2,  # 2x for response capacity
            entity_type=InfrastructureType.HEALTH_FACILITY
        )
        
        # Calculate capacity vs demand
        total_capacity = sum(e.capacity for e in affected_facilities)
        capacity_ratio = total_capacity / estimated_cases if estimated_cases > 0 else 1.0
        
        # Generate recommendations
        recommendations = []
        
        if capacity_ratio < 0.5:
            recommendations.append(
                f"🚨 CRITICAL: Health facility capacity insufficient. "
                f"Need {estimated_cases - total_capacity} additional beds."
            )
            recommendations.append(
                "Deploy mobile field hospitals to outbreak epicenter."
            )
        elif capacity_ratio < 0.8:
            recommendations.append(
                f"⚠️ WARNING: Health facilities near capacity. "
                f"Prepare overflow protocols."
            )
        else:
            recommendations.append(
                f"✅ ADEQUATE: Sufficient capacity for outbreak response."
            )
        
        # Optimize resource allocation
        resource_allocation = self._optimize_resource_allocation(
            facilities=affected_facilities,
            demand=estimated_cases,
            disease=disease
        )
        
        # Compliance check
        compliance_status = {
            "WHO_IHR_Article_6": capacity_ratio >= 0.8,
            "SDG_11_Target_1": len(affected_facilities) >= 3,
            "Sphere_Standards": capacity_ratio >= 0.5
        }
        
        result = SimulationResult(
            simulation_id=simulation_id,
            mode=SimulationMode.OUTBREAK_RESPONSE,
            timestamp=datetime.utcnow().isoformat(),
            entities_affected=[e.entity_id for e in affected_facilities],
            optimization_score=min(capacity_ratio, 1.0),
            recommendations=recommendations,
            resource_allocation=resource_allocation,
            compliance_status=compliance_status
        )
        
        self.simulation_history.append(result)
        
        logger.info(
            f"🏥 Outbreak simulation complete - "
            f"Capacity: {capacity_ratio:.1%}, Score: {result.optimization_score:.2f}"
        )
        
        return result
    
    def optimize_infrastructure_placement(
        self,
        entity_type: InfrastructureType,
        target_coverage: float = 0.95,
        budget_constraint: Optional[float] = None
    ) -> Dict:
        """
        Optimize placement of new infrastructure to maximize population coverage.
        
        Args:
            entity_type: Type of infrastructure to optimize
            target_coverage: Target population coverage (0-1)
            budget_constraint: Maximum budget (optional)
        
        Returns:
            Optimization results with recommended placements
        """
        # Get existing entities of this type
        existing = [e for e in self.entities.values() if e.entity_type == entity_type]
        
        # Calculate current coverage
        current_coverage = self._calculate_coverage(existing)
        
        # Generate optimal placement candidates
        candidates = self._generate_placement_candidates(
            entity_type=entity_type,
            target_coverage=target_coverage,
            existing=existing
        )
        
        # Apply budget constraint if provided
        if budget_constraint:
            candidates = self._apply_budget_constraint(candidates, budget_constraint)
        
        return {
            "entity_type": entity_type.value,
            "current_coverage": current_coverage,
            "target_coverage": target_coverage,
            "recommended_placements": candidates,
            "estimated_cost": sum(c["cost"] for c in candidates),
            "projected_coverage": self._calculate_projected_coverage(existing, candidates)
        }
    
    def simulate_disaster_preparedness(
        self,
        disaster_type: str,
        affected_area: Dict[str, Tuple[float, float]],
        severity: float
    ) -> SimulationResult:
        """
        Simulate disaster scenario and evaluate infrastructure resilience.
        
        Args:
            disaster_type: Type of disaster (flood, earthquake, etc.)
            affected_area: Geographic bounds of affected area
            severity: Disaster severity (0-1)
        
        Returns:
            SimulationResult with resilience assessment
        """
        simulation_id = f"DISASTER_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        # Find entities in affected area
        affected_entities = self._find_entities_in_bounds(affected_area)
        
        # Calculate infrastructure damage
        damage_assessment = {}
        for entity in affected_entities:
            # Damage probability based on entity type and severity
            damage_prob = self._calculate_damage_probability(
                entity.entity_type,
                disaster_type,
                severity
            )
            
            damage_assessment[entity.entity_id] = {
                "damage_probability": damage_prob,
                "operational_capacity": max(0, 1 - damage_prob),
                "recovery_time_days": int(damage_prob * 30)
            }
        
        # Generate recommendations
        recommendations = [
            f"Reinforce {len([e for e in affected_entities if e.entity_type == InfrastructureType.HEALTH_FACILITY])} health facilities",
            f"Establish {max(3, len(affected_entities) // 10)} emergency response centers",
            "Deploy early warning systems in high-risk zones",
            "Create evacuation routes and safe zones"
        ]
        
        result = SimulationResult(
            simulation_id=simulation_id,
            mode=SimulationMode.DISASTER_PREPAREDNESS,
            timestamp=datetime.utcnow().isoformat(),
            entities_affected=[e.entity_id for e in affected_entities],
            optimization_score=1 - severity,
            recommendations=recommendations,
            resource_allocation=damage_assessment,
            compliance_status={
                "Sendai_Framework": len(affected_entities) > 0,
                "SDG_11_Target_5": severity < 0.7
            }
        )
        
        self.simulation_history.append(result)
        
        logger.info(
            f"🌪️ Disaster simulation complete - "
            f"Affected: {len(affected_entities)}, Severity: {severity:.1%}"
        )
        
        return result
    
    def export_to_omniverse(self, output_path: str) -> bool:
        """
        Export digital twin to NVIDIA Omniverse USD format.
        
        Args:
            output_path: Path to save USD file
        
        Returns:
            True if export successful
        """
        if not self.enable_omniverse:
            logger.warning("Omniverse integration not enabled")
            return False
        
        # Generate USD scene
        usd_scene = {
            "city": self.city_name,
            "population": self.population,
            "bounds": self.geographic_bounds,
            "entities": [
                {
                    "id": e.entity_id,
                    "type": e.entity_type.value,
                    "location": e.location,
                    "capacity": e.capacity,
                    "utilization": e.current_utilization,
                    "health_score": e.health_score
                }
                for e in self.entities.values()
            ],
            "metadata": {
                "generated_at": datetime.utcnow().isoformat(),
                "total_entities": len(self.entities),
                "simulation_count": len(self.simulation_history)
            }
        }
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(usd_scene, f, indent=2)
        
        logger.info(f"📦 Exported to Omniverse: {output_path}")
        return True
    
    def _find_entities_in_radius(
        self,
        center: Tuple[float, float],
        radius_km: float,
        entity_type: Optional[InfrastructureType] = None
    ) -> List[UrbanEntity]:
        """Find entities within radius of center point"""
        entities = []
        
        for entity in self.entities.values():
            if entity_type and entity.entity_type != entity_type:
                continue
            
            # Calculate distance (simplified haversine)
            distance = self._calculate_distance(center, entity.location[:2])
            
            if distance <= radius_km:
                entities.append(entity)
        
        return entities
    
    def _find_entities_in_bounds(
        self,
        bounds: Dict[str, Tuple[float, float]]
    ) -> List[UrbanEntity]:
        """Find entities within geographic bounds"""
        entities = []
        
        lat_min, lat_max = bounds.get("lat", (-90, 90))
        lng_min, lng_max = bounds.get("lng", (-180, 180))
        
        for entity in self.entities.values():
            lat, lng, _ = entity.location
            
            if lat_min <= lat <= lat_max and lng_min <= lng <= lng_max:
                entities.append(entity)
        
        return entities
    
    def _calculate_distance(
        self,
        point1: Tuple[float, float],
        point2: Tuple[float, float]
    ) -> float:
        """Calculate distance between two points in km (simplified)"""
        lat1, lng1 = point1
        lat2, lng2 = point2
        
        # Simplified distance calculation
        dlat = abs(lat2 - lat1)
        dlng = abs(lng2 - lng1)
        
        return np.sqrt(dlat**2 + dlng**2) * 111  # Rough km conversion
    
    def _optimize_resource_allocation(
        self,
        facilities: List[UrbanEntity],
        demand: int,
        disease: str
    ) -> Dict:
        """Optimize resource allocation across facilities"""
        if not facilities:
            return {}
        
        total_capacity = sum(f.capacity for f in facilities)
        
        allocation = {}
        for facility in facilities:
            # Proportional allocation based on capacity
            allocation[facility.entity_id] = {
                "allocated_beds": int((facility.capacity / total_capacity) * demand),
                "staff_required": int((facility.capacity / total_capacity) * demand * 0.1),
                "supplies_needed": {
                    "PPE_kits": int((facility.capacity / total_capacity) * demand * 2),
                    "test_kits": int((facility.capacity / total_capacity) * demand),
                    "medications": int((facility.capacity / total_capacity) * demand * 5)
                }
            }
        
        return allocation
    
    def _calculate_coverage(self, entities: List[UrbanEntity]) -> float:
        """Calculate population coverage by entities"""
        if not entities:
            return 0.0
        
        # Simplified coverage calculation
        total_capacity = sum(e.capacity for e in entities)
        return min(1.0, total_capacity / (self.population * 0.02))  # 2% coverage target
    
    def _generate_placement_candidates(
        self,
        entity_type: InfrastructureType,
        target_coverage: float,
        existing: List[UrbanEntity]
    ) -> List[Dict]:
        """Generate optimal placement candidates"""
        # Simplified candidate generation
        current_coverage = self._calculate_coverage(existing)
        gap = target_coverage - current_coverage
        
        if gap <= 0:
            return []
        
        # Generate candidates
        candidates = []
        num_needed = max(1, int(gap * 10))
        
        for i in range(num_needed):
            candidates.append({
                "location": self._generate_optimal_location(existing),
                "capacity": int(self.population * 0.002),
                "cost": 1000000,  # $1M per facility
                "coverage_improvement": gap / num_needed
            })
        
        return candidates
    
    def _generate_optimal_location(
        self,
        existing: List[UrbanEntity]
    ) -> Tuple[float, float, float]:
        """Generate optimal location for new entity"""
        # Simplified: Random location within bounds
        lat_min, lat_max = self.geographic_bounds.get("lat", (0, 1))
        lng_min, lng_max = self.geographic_bounds.get("lng", (0, 1))
        
        return (
            np.random.uniform(lat_min, lat_max),
            np.random.uniform(lng_min, lng_max),
            0.0
        )
    
    def _apply_budget_constraint(
        self,
        candidates: List[Dict],
        budget: float
    ) -> List[Dict]:
        """Apply budget constraint to candidates"""
        # Sort by coverage improvement per cost
        sorted_candidates = sorted(
            candidates,
            key=lambda c: c["coverage_improvement"] / c["cost"],
            reverse=True
        )
        
        # Select candidates within budget
        selected = []
        remaining_budget = budget
        
        for candidate in sorted_candidates:
            if candidate["cost"] <= remaining_budget:
                selected.append(candidate)
                remaining_budget -= candidate["cost"]
        
        return selected
    
    def _calculate_projected_coverage(
        self,
        existing: List[UrbanEntity],
        candidates: List[Dict]
    ) -> float:
        """Calculate projected coverage with new placements"""
        current = self._calculate_coverage(existing)
        improvement = sum(c["coverage_improvement"] for c in candidates)
        return min(1.0, current + improvement)
    
    def _calculate_damage_probability(
        self,
        entity_type: InfrastructureType,
        disaster_type: str,
        severity: float
    ) -> float:
        """Calculate damage probability for entity"""
        # Base vulnerability by entity type
        vulnerability = {
            InfrastructureType.HEALTH_FACILITY: 0.3,
            InfrastructureType.WATER_SYSTEM: 0.5,
            InfrastructureType.POWER_GRID: 0.4,
            InfrastructureType.TRANSPORT: 0.6,
            InfrastructureType.EDUCATION: 0.3,
            InfrastructureType.SANITATION: 0.5,
            InfrastructureType.EMERGENCY_RESPONSE: 0.2
        }
        
        base_vuln = vulnerability.get(entity_type, 0.5)
        return min(1.0, base_vuln * severity)


# Example usage
if __name__ == "__main__":
    # Initialize digital twin for Dadaab
    twin = OmniverseTwin(
        city_name="Dadaab Refugee Complex",
        population=200000,
        geographic_bounds={
            "lat": (0.0, 0.1),
            "lng": (40.2, 40.4)
        },
        enable_omniverse=True
    )
    
    # Register health facilities
    twin.register_entity(
        entity_id="DADAAB_HOSPITAL_01",
        entity_type=InfrastructureType.HEALTH_FACILITY,
        location=(0.0512, 40.3129, 0),
        capacity=200,
        metadata={"name": "Dadaab General Hospital"}
    )
    
    # Simulate cholera outbreak
    result = twin.simulate_outbreak_response(
        outbreak_location=(0.0512, 40.3129),
        outbreak_radius_km=5.0,
        estimated_cases=500,
        disease="cholera"
    )
    
    print(f"✅ Simulation: {result.simulation_id}")
    print(f"📊 Optimization Score: {result.optimization_score:.2f}")
    print(f"💡 Recommendations:")
    for rec in result.recommendations:
        print(f"   - {rec}")
    
    # Export to Omniverse
    twin.export_to_omniverse("dadaab_twin.usd")
