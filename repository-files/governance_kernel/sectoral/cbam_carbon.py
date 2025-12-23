"""
CBAM Carbon Emissions Compliance Module
EU Carbon Border Adjustment Mechanism (Regulation 2023/956)

Compliance:
- EU CBAM Regulation 2023/956
- EU Emissions Trading System (ETS)
- Paris Agreement Article 6
- ISO 14064 (GHG Accounting)
"""

from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import logging
import math

logger = logging.getLogger(__name__)


class CBAMSector(Enum):
    """CBAM covered sectors"""
    CEMENT = "cement"
    ELECTRICITY = "electricity"
    FERTILIZERS = "fertilizers"
    IRON_STEEL = "iron_steel"
    ALUMINUM = "aluminum"
    HYDROGEN = "hydrogen"
    # Healthcare-specific
    MEDICAL_DEVICES = "medical_devices"
    PHARMACEUTICALS = "pharmaceuticals"
    COLD_CHAIN = "cold_chain"  # Vaccine/medicine transport


class EmissionScope(Enum):
    """GHG Protocol emission scopes"""
    SCOPE_1 = "direct"  # Direct emissions from owned sources
    SCOPE_2 = "indirect_energy"  # Indirect from purchased energy
    SCOPE_3 = "indirect_value_chain"  # Value chain emissions


class CBAMCarbonCalculator:
    """
    Calculate carbon emissions for health data infrastructure.
    
    Use case: Ensure iLuminara's cloud infrastructure complies with EU CBAM
    when serving European health systems.
    """
    
    def __init__(
        self,
        default_carbon_price_eur: float = 80.0,  # EUR per tonne CO2e
        enable_offset_credits: bool = True
    ):
        self.carbon_price = default_carbon_price_eur
        self.enable_offset_credits = enable_offset_credits
        
        # Emission factors (kg CO2e per unit)
        self.emission_factors = {
            # Cloud computing (per kWh)
            "cloud_compute_gcp": 0.0,  # GCP is carbon neutral
            "cloud_compute_aws": 0.385,  # AWS average
            "cloud_compute_azure": 0.295,  # Azure average
            
            # Data centers (per kWh)
            "datacenter_tier3": 0.5,
            "datacenter_tier4": 0.4,
            
            # Networking (per GB transferred)
            "network_transfer": 0.001,
            
            # Cold chain (per km per kg)
            "cold_chain_transport": 0.15,
            
            # Medical devices manufacturing (per device)
            "medical_device_iot": 5.0,
            
            # Pharmaceuticals (per kg)
            "pharma_production": 2.5
        }
        
        logger.info("🌍 CBAM Carbon Calculator initialized")
    
    def calculate_cloud_emissions(
        self,
        provider: str,
        compute_hours: float,
        power_consumption_kwh: float,
        region: str
    ) -> Dict:
        """
        Calculate emissions from cloud infrastructure.
        
        Args:
            provider: "GCP", "AWS", "Azure"
            compute_hours: Hours of compute time
            power_consumption_kwh: Energy consumed
            region: Cloud region (affects grid carbon intensity)
        
        Returns:
            Emissions calculation with CBAM compliance
        """
        # Get emission factor
        factor_key = f"cloud_compute_{provider.lower()}"
        emission_factor = self.emission_factors.get(factor_key, 0.5)
        
        # Calculate emissions (kg CO2e)
        total_emissions = power_consumption_kwh * emission_factor
        
        # Apply regional grid intensity adjustment
        grid_intensity = self._get_grid_intensity(region)
        adjusted_emissions = total_emissions * grid_intensity
        
        # Calculate CBAM liability (EUR)
        cbam_liability = (adjusted_emissions / 1000) * self.carbon_price
        
        return {
            "scope": EmissionScope.SCOPE_2.value,
            "emissions_kg_co2e": round(adjusted_emissions, 2),
            "emissions_tonnes_co2e": round(adjusted_emissions / 1000, 4),
            "cbam_liability_eur": round(cbam_liability, 2),
            "provider": provider,
            "region": region,
            "grid_intensity_factor": grid_intensity,
            "calculation_method": "GHG Protocol Scope 2",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def calculate_data_transfer_emissions(
        self,
        data_volume_gb: float,
        source_region: str,
        destination_region: str
    ) -> Dict:
        """
        Calculate emissions from data transfers.
        
        Args:
            data_volume_gb: Volume of data transferred
            source_region: Origin region
            destination_region: Destination region
        
        Returns:
            Emissions calculation
        """
        # Base emission factor
        emission_factor = self.emission_factors["network_transfer"]
        
        # Calculate distance penalty (cross-continental transfers)
        distance_multiplier = self._calculate_distance_multiplier(
            source_region, destination_region
        )
        
        # Total emissions
        total_emissions = data_volume_gb * emission_factor * distance_multiplier
        
        # CBAM liability
        cbam_liability = (total_emissions / 1000) * self.carbon_price
        
        return {
            "scope": EmissionScope.SCOPE_3.value,
            "emissions_kg_co2e": round(total_emissions, 4),
            "emissions_tonnes_co2e": round(total_emissions / 1000, 6),
            "cbam_liability_eur": round(cbam_liability, 4),
            "data_volume_gb": data_volume_gb,
            "source_region": source_region,
            "destination_region": destination_region,
            "distance_multiplier": distance_multiplier,
            "calculation_method": "Network Transfer Emissions",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def calculate_cold_chain_emissions(
        self,
        cargo_weight_kg: float,
        distance_km: float,
        transport_mode: str = "refrigerated_truck"
    ) -> Dict:
        """
        Calculate emissions from cold chain transport (vaccines, medicines).
        
        Args:
            cargo_weight_kg: Weight of cargo
            distance_km: Transport distance
            transport_mode: "refrigerated_truck", "air_freight", "sea_freight"
        
        Returns:
            Emissions calculation
        """
        # Emission factors by transport mode (kg CO2e per tonne-km)
        transport_factors = {
            "refrigerated_truck": 0.15,
            "air_freight": 1.5,
            "sea_freight": 0.01
        }
        
        emission_factor = transport_factors.get(transport_mode, 0.15)
        
        # Calculate emissions
        total_emissions = (cargo_weight_kg / 1000) * distance_km * emission_factor
        
        # CBAM liability
        cbam_liability = (total_emissions / 1000) * self.carbon_price
        
        return {
            "scope": EmissionScope.SCOPE_3.value,
            "sector": CBAMSector.COLD_CHAIN.value,
            "emissions_kg_co2e": round(total_emissions, 2),
            "emissions_tonnes_co2e": round(total_emissions / 1000, 4),
            "cbam_liability_eur": round(cbam_liability, 2),
            "cargo_weight_kg": cargo_weight_kg,
            "distance_km": distance_km,
            "transport_mode": transport_mode,
            "calculation_method": "ISO 14064 Cold Chain",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def calculate_total_footprint(
        self,
        cloud_emissions: List[Dict],
        data_transfer_emissions: List[Dict],
        cold_chain_emissions: List[Dict] = None
    ) -> Dict:
        """
        Calculate total carbon footprint with CBAM compliance.
        
        Returns:
            Comprehensive emissions report
        """
        # Sum all emissions
        total_scope_1 = 0.0
        total_scope_2 = sum(e["emissions_kg_co2e"] for e in cloud_emissions)
        total_scope_3 = sum(e["emissions_kg_co2e"] for e in data_transfer_emissions)
        
        if cold_chain_emissions:
            total_scope_3 += sum(e["emissions_kg_co2e"] for e in cold_chain_emissions)
        
        total_emissions = total_scope_1 + total_scope_2 + total_scope_3
        
        # Calculate CBAM liability
        total_cbam_liability = (total_emissions / 1000) * self.carbon_price
        
        # Check compliance thresholds
        compliance_status = self._check_cbam_compliance(total_emissions / 1000)
        
        return {
            "total_emissions_kg_co2e": round(total_emissions, 2),
            "total_emissions_tonnes_co2e": round(total_emissions / 1000, 4),
            "scope_1_kg_co2e": round(total_scope_1, 2),
            "scope_2_kg_co2e": round(total_scope_2, 2),
            "scope_3_kg_co2e": round(total_scope_3, 2),
            "cbam_liability_eur": round(total_cbam_liability, 2),
            "carbon_price_eur_per_tonne": self.carbon_price,
            "compliance_status": compliance_status,
            "calculation_standard": "GHG Protocol + ISO 14064",
            "reporting_period": datetime.utcnow().strftime("%Y-%m"),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def generate_cbam_report(
        self,
        organization: str,
        reporting_period: str,
        emissions_data: Dict
    ) -> Dict:
        """
        Generate CBAM compliance report for EU customs.
        
        Args:
            organization: Organization name
            reporting_period: "2025-Q1"
            emissions_data: Output from calculate_total_footprint()
        
        Returns:
            CBAM report ready for submission
        """
        return {
            "report_type": "CBAM_Quarterly_Declaration",
            "regulation": "EU Regulation 2023/956",
            "organization": organization,
            "reporting_period": reporting_period,
            "emissions_summary": emissions_data,
            "verification_status": "PENDING_THIRD_PARTY_AUDIT",
            "submission_deadline": self._calculate_submission_deadline(reporting_period),
            "certificate_required": emissions_data["total_emissions_tonnes_co2e"] > 1.0,
            "generated_at": datetime.utcnow().isoformat(),
            "legal_notice": "This report must be verified by an accredited verifier per CBAM Article 8"
        }
    
    def _get_grid_intensity(self, region: str) -> float:
        """
        Get carbon intensity of electricity grid by region.
        
        Returns multiplier (1.0 = average, <1.0 = cleaner, >1.0 = dirtier)
        """
        grid_intensities = {
            # Clean grids
            "europe-west1": 0.3,  # Belgium (renewable-heavy)
            "europe-north1": 0.1,  # Finland (hydro/nuclear)
            "us-central1": 0.5,   # Iowa (wind)
            
            # Average grids
            "us-east1": 1.0,      # South Carolina
            "asia-southeast1": 1.2,  # Singapore
            
            # Dirty grids
            "asia-east1": 1.5,    # Taiwan (coal)
            "australia-southeast1": 1.8,  # Sydney (coal)
            
            # Africa (varies widely)
            "africa-south1": 1.3  # South Africa (coal-heavy)
        }
        
        return grid_intensities.get(region, 1.0)
    
    def _calculate_distance_multiplier(
        self,
        source: str,
        destination: str
    ) -> float:
        """
        Calculate distance penalty for data transfers.
        
        Same region: 1.0x
        Same continent: 1.2x
        Cross-continental: 1.5x
        """
        # Simplified logic - in production, use actual geographic distance
        if source == destination:
            return 1.0
        elif source.split("-")[0] == destination.split("-")[0]:
            return 1.2
        else:
            return 1.5
    
    def _check_cbam_compliance(self, emissions_tonnes: float) -> Dict:
        """
        Check CBAM compliance thresholds.
        """
        # CBAM thresholds
        if emissions_tonnes < 1.0:
            status = "EXEMPT"
            action = "No CBAM certificate required"
        elif emissions_tonnes < 10.0:
            status = "REPORTING_REQUIRED"
            action = "Submit quarterly CBAM declaration"
        else:
            status = "CERTIFICATE_REQUIRED"
            action = "Obtain CBAM certificates and third-party verification"
        
        return {
            "status": status,
            "action_required": action,
            "threshold_tonnes": emissions_tonnes,
            "regulation": "EU CBAM Regulation 2023/956"
        }
    
    def _calculate_submission_deadline(self, reporting_period: str) -> str:
        """
        Calculate CBAM submission deadline.
        
        Deadline: One month after end of quarter
        """
        # Parse period (e.g., "2025-Q1")
        year, quarter = reporting_period.split("-Q")
        quarter_end_month = int(quarter) * 3
        
        # Deadline is one month after quarter end
        deadline_month = quarter_end_month + 1
        if deadline_month > 12:
            deadline_month = 1
            year = str(int(year) + 1)
        
        return f"{year}-{deadline_month:02d}-01"


# Example usage
if __name__ == "__main__":
    calculator = CBAMCarbonCalculator(carbon_price_eur=80.0)
    
    # Test 1: Cloud emissions (GCP in Belgium)
    cloud_result = calculator.calculate_cloud_emissions(
        provider="GCP",
        compute_hours=1000,
        power_consumption_kwh=500,
        region="europe-west1"
    )
    print(f"Cloud Emissions: {cloud_result}")
    
    # Test 2: Data transfer emissions
    transfer_result = calculator.calculate_data_transfer_emissions(
        data_volume_gb=1000,
        source_region="africa-south1",
        destination_region="europe-west1"
    )
    print(f"\nData Transfer Emissions: {transfer_result}")
    
    # Test 3: Cold chain emissions (vaccine transport)
    cold_chain_result = calculator.calculate_cold_chain_emissions(
        cargo_weight_kg=100,
        distance_km=500,
        transport_mode="refrigerated_truck"
    )
    print(f"\nCold Chain Emissions: {cold_chain_result}")
    
    # Test 4: Total footprint
    total = calculator.calculate_total_footprint(
        cloud_emissions=[cloud_result],
        data_transfer_emissions=[transfer_result],
        cold_chain_emissions=[cold_chain_result]
    )
    print(f"\nTotal Footprint: {total}")
    
    # Test 5: CBAM report
    report = calculator.generate_cbam_report(
        organization="iLuminara Health Systems",
        reporting_period="2025-Q1",
        emissions_data=total
    )
    print(f"\nCBAM Report: {report}")
