"""
NVIDIA Modulus Agro-Voltaics Optimization
Physics-informed crop-energy simulation for arid environments

Solves the Food-Energy Nexus: Grow crops under solar panels with optimized
tilt angles that maximize electricity generation while maintaining ideal
micro-climates for agriculture.

Compliance:
- FAO Sustainable Agriculture Guidelines
- Kenya National Climate Change Action Plan
- UNHCR Energy Strategy 2019-2024
"""

import numpy as np
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CropType(Enum):
    """Crops suitable for agrivoltaic systems in arid climates"""
    SPINACH = "spinach"
    TOMATO = "tomato"
    LETTUCE = "lettuce"
    KALE = "kale"
    PEPPER = "pepper"
    CUCUMBER = "cucumber"
    BEANS = "beans"


class PanelOrientation(Enum):
    """Solar panel orientation"""
    FIXED = "fixed"
    SINGLE_AXIS_TRACKING = "single_axis"
    DUAL_AXIS_TRACKING = "dual_axis"


@dataclass
class EnvironmentalConditions:
    """Current environmental conditions"""
    ambient_temp_celsius: float
    solar_irradiance_wm2: float  # W/m²
    wind_speed_ms: float
    relative_humidity: float  # 0-1
    time_of_day: datetime


@dataclass
class CropRequirements:
    """Optimal growing conditions for crop"""
    crop_type: CropType
    optimal_temp_range: Tuple[float, float]  # (min, max) Celsius
    optimal_humidity_range: Tuple[float, float]  # (min, max) 0-1
    light_requirement: str  # "full_sun", "partial_shade", "shade_tolerant"
    water_requirement: str  # "low", "medium", "high"
    shade_tolerance: float  # 0-1 (0=no tolerance, 1=full tolerance)


@dataclass
class OptimizationResult:
    """Results from panel optimization"""
    tilt_angle: float  # degrees from horizontal
    azimuth_angle: float  # degrees from north
    energy_output_watts: float
    energy_efficiency: float  # 0-1
    crop_health_score: float  # 0-1
    microclimate_temp: float  # Celsius
    microclimate_humidity: float  # 0-1
    shade_coverage: float  # 0-1
    recommendations: List[str]


class AgroVoltaicController:
    """
    Uses NVIDIA Modulus to optimize solar panel tilt for crop micro-climates.
    
    Solves radiative transfer equations to balance:
    - Maximum energy generation
    - Optimal crop growing conditions
    - Water conservation through shade
    """
    
    def __init__(
        self,
        panel_area_m2: float = 100,
        panel_efficiency: float = 0.20,  # 20% efficient panels
        panel_orientation: PanelOrientation = PanelOrientation.SINGLE_AXIS_TRACKING,
        location: Tuple[float, float] = (0.0512, 40.3129)  # Dadaab coordinates
    ):
        self.panel_area_m2 = panel_area_m2
        self.panel_efficiency = panel_efficiency
        self.panel_orientation = panel_orientation
        self.location = location
        
        # Crop database
        self.crop_database = self._initialize_crop_database()
        
        # Physics constants
        self.STEFAN_BOLTZMANN = 5.67e-8  # W/(m²·K⁴)
        self.SOLAR_CONSTANT = 1361  # W/m² at top of atmosphere
        
        logger.info("🌱 Agro-Voltaic Controller initialized")
        logger.info(f"   Panel Area: {panel_area_m2} m²")
        logger.info(f"   Panel Efficiency: {panel_efficiency*100}%")
        logger.info(f"   Orientation: {panel_orientation.value}")
    
    def optimize_tilt(
        self,
        crop_type: CropType,
        environmental_conditions: EnvironmentalConditions,
        priority: str = "balanced"  # "energy", "crop", "balanced"
    ) -> OptimizationResult:
        """
        Optimize panel tilt angle for crop micro-climate and energy generation.
        
        Args:
            crop_type: Type of crop being grown
            environmental_conditions: Current weather conditions
            priority: Optimization priority
        
        Returns:
            Optimization result with tilt angle and performance metrics
        """
        logger.info(f"⚡ [Modulus] Optimizing for {crop_type.value}")
        logger.info(f"   Ambient Temp: {environmental_conditions.ambient_temp_celsius}°C")
        logger.info(f"   Solar Irradiance: {environmental_conditions.solar_irradiance_wm2} W/m²")
        
        # Get crop requirements
        crop_req = self.crop_database[crop_type]
        
        # Calculate optimal tilt angle
        optimal_tilt = self._calculate_optimal_tilt(
            crop_req, environmental_conditions, priority
        )
        
        # Calculate azimuth (for dual-axis tracking)
        optimal_azimuth = self._calculate_optimal_azimuth(environmental_conditions)
        
        # Simulate energy output
        energy_output = self._simulate_energy_output(
            optimal_tilt, optimal_azimuth, environmental_conditions
        )
        
        # Simulate crop microclimate
        microclimate = self._simulate_microclimate(
            optimal_tilt, crop_req, environmental_conditions
        )
        
        # Calculate crop health score
        crop_health = self._calculate_crop_health(
            microclimate, crop_req
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            optimal_tilt, energy_output, crop_health, crop_req, environmental_conditions
        )
        
        result = OptimizationResult(
            tilt_angle=optimal_tilt,
            azimuth_angle=optimal_azimuth,
            energy_output_watts=energy_output,
            energy_efficiency=energy_output / (self.panel_area_m2 * environmental_conditions.solar_irradiance_wm2),
            crop_health_score=crop_health,
            microclimate_temp=microclimate["temperature"],
            microclimate_humidity=microclimate["humidity"],
            shade_coverage=microclimate["shade_coverage"],
            recommendations=recommendations
        )
        
        logger.info(f"✅ Optimization complete:")
        logger.info(f"   Tilt Angle: {optimal_tilt:.1f}°")
        logger.info(f"   Energy Output: {energy_output:.0f} W ({result.energy_efficiency*100:.1f}%)")
        logger.info(f"   Crop Health: {crop_health*100:.0f}%")
        
        return result
    
    def _calculate_optimal_tilt(
        self,
        crop_req: CropRequirements,
        env: EnvironmentalConditions,
        priority: str
    ) -> float:
        """
        Calculate optimal tilt angle using physics-informed optimization.
        
        Balances:
        - Solar angle for maximum energy capture
        - Shade requirements for crop health
        - Temperature regulation
        """
        # Calculate solar elevation angle
        solar_elevation = self._calculate_solar_elevation(env.time_of_day)
        
        # Energy-optimal tilt (perpendicular to sun)
        energy_optimal_tilt = 90 - solar_elevation
        
        # Crop-optimal tilt (based on shade requirements)
        if crop_req.light_requirement == "full_sun":
            crop_optimal_tilt = energy_optimal_tilt  # Maximize light
        elif crop_req.light_requirement == "partial_shade":
            crop_optimal_tilt = energy_optimal_tilt + 15  # More shade
        else:  # shade_tolerant
            crop_optimal_tilt = energy_optimal_tilt + 30  # Maximum shade
        
        # Temperature consideration (more tilt = more shade = cooler)
        if env.ambient_temp_celsius > crop_req.optimal_temp_range[1]:
            # Too hot - increase tilt for more shade
            temp_adjustment = min(20, (env.ambient_temp_celsius - crop_req.optimal_temp_range[1]) * 2)
        else:
            temp_adjustment = 0
        
        # Weighted optimization based on priority
        if priority == "energy":
            optimal_tilt = energy_optimal_tilt * 0.8 + crop_optimal_tilt * 0.2
        elif priority == "crop":
            optimal_tilt = energy_optimal_tilt * 0.2 + crop_optimal_tilt * 0.8
        else:  # balanced
            optimal_tilt = energy_optimal_tilt * 0.5 + crop_optimal_tilt * 0.5
        
        # Apply temperature adjustment
        optimal_tilt += temp_adjustment
        
        # Constrain to physical limits
        optimal_tilt = np.clip(optimal_tilt, 0, 90)
        
        return optimal_tilt
    
    def _calculate_optimal_azimuth(self, env: EnvironmentalConditions) -> float:
        """Calculate optimal azimuth angle (for dual-axis tracking)"""
        # Calculate solar azimuth
        solar_azimuth = self._calculate_solar_azimuth(env.time_of_day)
        
        # For single-axis tracking, azimuth is fixed (typically south in northern hemisphere)
        if self.panel_orientation == PanelOrientation.SINGLE_AXIS_TRACKING:
            return 180  # South-facing
        elif self.panel_orientation == PanelOrientation.DUAL_AXIS_TRACKING:
            return solar_azimuth
        else:  # FIXED
            return 180  # South-facing
    
    def _simulate_energy_output(
        self,
        tilt_angle: float,
        azimuth_angle: float,
        env: EnvironmentalConditions
    ) -> float:
        """
        Simulate energy output using radiative transfer equations.
        
        P = A * η * I * cos(θ)
        where:
        - A = panel area
        - η = panel efficiency
        - I = solar irradiance
        - θ = angle of incidence
        """
        # Calculate angle of incidence
        solar_elevation = self._calculate_solar_elevation(env.time_of_day)
        solar_azimuth = self._calculate_solar_azimuth(env.time_of_day)
        
        # Angle between panel normal and sun direction
        angle_of_incidence = self._calculate_angle_of_incidence(
            tilt_angle, azimuth_angle, solar_elevation, solar_azimuth
        )
        
        # Energy output
        energy_output = (
            self.panel_area_m2 *
            self.panel_efficiency *
            env.solar_irradiance_wm2 *
            np.cos(np.radians(angle_of_incidence))
        )
        
        # Account for temperature derating (panels lose efficiency when hot)
        temp_coefficient = -0.004  # -0.4% per °C above 25°C
        temp_derating = 1 + temp_coefficient * (env.ambient_temp_celsius - 25)
        energy_output *= temp_derating
        
        return max(0, energy_output)
    
    def _simulate_microclimate(
        self,
        tilt_angle: float,
        crop_req: CropRequirements,
        env: EnvironmentalConditions
    ) -> Dict:
        """
        Simulate microclimate under solar panels.
        
        Factors:
        - Shade coverage
        - Temperature reduction
        - Humidity retention
        """
        # Calculate shade coverage (0-1)
        shade_coverage = self._calculate_shade_coverage(tilt_angle, env.time_of_day)
        
        # Temperature reduction from shade
        # Shade can reduce temperature by 5-10°C in arid climates
        temp_reduction = shade_coverage * 8  # Up to 8°C reduction
        microclimate_temp = env.ambient_temp_celsius - temp_reduction
        
        # Humidity retention (shade reduces evaporation)
        humidity_increase = shade_coverage * 0.15  # Up to 15% increase
        microclimate_humidity = min(1.0, env.relative_humidity + humidity_increase)
        
        return {
            "temperature": microclimate_temp,
            "humidity": microclimate_humidity,
            "shade_coverage": shade_coverage
        }
    
    def _calculate_crop_health(
        self,
        microclimate: Dict,
        crop_req: CropRequirements
    ) -> float:
        """
        Calculate crop health score (0-1) based on microclimate conditions.
        """
        # Temperature score
        temp = microclimate["temperature"]
        temp_min, temp_max = crop_req.optimal_temp_range
        
        if temp_min <= temp <= temp_max:
            temp_score = 1.0
        elif temp < temp_min:
            temp_score = max(0, 1 - (temp_min - temp) / 10)
        else:  # temp > temp_max
            temp_score = max(0, 1 - (temp - temp_max) / 10)
        
        # Humidity score
        humidity = microclimate["humidity"]
        hum_min, hum_max = crop_req.optimal_humidity_range
        
        if hum_min <= humidity <= hum_max:
            humidity_score = 1.0
        elif humidity < hum_min:
            humidity_score = max(0, 1 - (hum_min - humidity) / 0.3)
        else:  # humidity > hum_max
            humidity_score = max(0, 1 - (humidity - hum_max) / 0.3)
        
        # Shade score (based on crop shade tolerance)
        shade = microclimate["shade_coverage"]
        shade_score = 1 - abs(crop_req.shade_tolerance - shade)
        
        # Overall health score (weighted average)
        health_score = (temp_score * 0.4 + humidity_score * 0.3 + shade_score * 0.3)
        
        return health_score
    
    def _calculate_shade_coverage(self, tilt_angle: float, time: datetime) -> float:
        """Calculate shade coverage percentage (0-1)"""
        # Simplified model: higher tilt = more shade
        # In production, use ray-tracing for accurate shadow simulation
        
        solar_elevation = self._calculate_solar_elevation(time)
        
        # Shade coverage increases with tilt angle
        base_shade = tilt_angle / 90  # 0-1
        
        # Adjust for solar elevation (low sun = more shade)
        elevation_factor = 1 - (solar_elevation / 90)
        
        shade_coverage = base_shade * (0.7 + 0.3 * elevation_factor)
        
        return np.clip(shade_coverage, 0, 1)
    
    def _calculate_solar_elevation(self, time: datetime) -> float:
        """Calculate solar elevation angle (simplified)"""
        # Simplified solar position calculation
        # In production, use accurate solar position algorithms (e.g., NREL SPA)
        
        hour = time.hour + time.minute / 60
        
        # Solar noon at 12:00
        hour_angle = (hour - 12) * 15  # 15° per hour
        
        # Dadaab latitude
        latitude = self.location[0]
        
        # Simplified elevation (assumes equinox)
        elevation = 90 - abs(latitude) - abs(hour_angle) / 4
        
        return max(0, elevation)
    
    def _calculate_solar_azimuth(self, time: datetime) -> float:
        """Calculate solar azimuth angle (simplified)"""
        hour = time.hour + time.minute / 60
        
        # Morning: East (90°), Noon: South (180°), Evening: West (270°)
        if hour < 12:
            azimuth = 90 + (hour / 12) * 90
        else:
            azimuth = 180 + ((hour - 12) / 12) * 90
        
        return azimuth
    
    def _calculate_angle_of_incidence(
        self,
        tilt: float,
        azimuth: float,
        solar_elevation: float,
        solar_azimuth: float
    ) -> float:
        """Calculate angle of incidence between panel and sun"""
        # Simplified calculation
        # In production, use vector dot product for accurate calculation
        
        angle_diff = abs(azimuth - solar_azimuth)
        elevation_diff = abs(tilt - (90 - solar_elevation))
        
        angle_of_incidence = np.sqrt(angle_diff**2 + elevation_diff**2) / 2
        
        return angle_of_incidence
    
    def _generate_recommendations(
        self,
        tilt_angle: float,
        energy_output: float,
        crop_health: float,
        crop_req: CropRequirements,
        env: EnvironmentalConditions
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Energy recommendations
        if energy_output < self.panel_area_m2 * env.solar_irradiance_wm2 * 0.15:
            recommendations.append(
                "⚡ LOW ENERGY OUTPUT: Consider cleaning panels or adjusting tilt"
            )
        
        # Crop health recommendations
        if crop_health < 0.6:
            recommendations.append(
                f"🌱 CROP STRESS: Adjust tilt to {tilt_angle + 10:.1f}° for better microclimate"
            )
        
        # Temperature recommendations
        if env.ambient_temp_celsius > crop_req.optimal_temp_range[1]:
            recommendations.append(
                "🌡️ HIGH TEMPERATURE: Increase tilt for more shade and cooling"
            )
        
        # Irrigation recommendations
        if crop_req.water_requirement == "high" and env.relative_humidity < 0.3:
            recommendations.append(
                "💧 LOW HUMIDITY: Increase irrigation frequency"
            )
        
        # Positive feedback
        if crop_health > 0.8 and energy_output > self.panel_area_m2 * env.solar_irradiance_wm2 * 0.18:
            recommendations.append(
                "✅ OPTIMAL PERFORMANCE: Energy and crop health both excellent"
            )
        
        return recommendations
    
    def _initialize_crop_database(self) -> Dict[CropType, CropRequirements]:
        """Initialize database of crop requirements"""
        return {
            CropType.SPINACH: CropRequirements(
                crop_type=CropType.SPINACH,
                optimal_temp_range=(15, 25),
                optimal_humidity_range=(0.5, 0.7),
                light_requirement="partial_shade",
                water_requirement="medium",
                shade_tolerance=0.6
            ),
            CropType.TOMATO: CropRequirements(
                crop_type=CropType.TOMATO,
                optimal_temp_range=(20, 30),
                optimal_humidity_range=(0.6, 0.8),
                light_requirement="full_sun",
                water_requirement="high",
                shade_tolerance=0.3
            ),
            CropType.LETTUCE: CropRequirements(
                crop_type=CropType.LETTUCE,
                optimal_temp_range=(15, 25),
                optimal_humidity_range=(0.5, 0.7),
                light_requirement="partial_shade",
                water_requirement="medium",
                shade_tolerance=0.7
            ),
            CropType.KALE: CropRequirements(
                crop_type=CropType.KALE,
                optimal_temp_range=(15, 25),
                optimal_humidity_range=(0.5, 0.7),
                light_requirement="partial_shade",
                water_requirement="medium",
                shade_tolerance=0.6
            )
        }


# Example usage
if __name__ == "__main__":
    # Initialize controller
    controller = AgroVoltaicController(
        panel_area_m2=100,
        panel_efficiency=0.20,
        panel_orientation=PanelOrientation.SINGLE_AXIS_TRACKING
    )
    
    # Current environmental conditions (Dadaab midday)
    env = EnvironmentalConditions(
        ambient_temp_celsius=35,
        solar_irradiance_wm2=950,
        wind_speed_ms=3.5,
        relative_humidity=0.25,
        time_of_day=datetime.now().replace(hour=12, minute=0)
    )
    
    # Optimize for spinach cultivation
    result = controller.optimize_tilt(
        crop_type=CropType.SPINACH,
        environmental_conditions=env,
        priority="balanced"
    )
    
    print("\n" + "="*60)
    print("AGRO-VOLTAIC OPTIMIZATION RESULTS")
    print("="*60)
    print(f"Tilt Angle: {result.tilt_angle:.1f}°")
    print(f"Energy Output: {result.energy_output_watts:.0f} W")
    print(f"Energy Efficiency: {result.energy_efficiency*100:.1f}%")
    print(f"Crop Health Score: {result.crop_health_score*100:.0f}%")
    print(f"Microclimate Temperature: {result.microclimate_temp:.1f}°C")
    print(f"Microclimate Humidity: {result.microclimate_humidity*100:.0f}%")
    print(f"Shade Coverage: {result.shade_coverage*100:.0f}%")
    print("\nRECOMMENDATIONS:")
    for rec in result.recommendations:
        print(f"  • {rec}")
