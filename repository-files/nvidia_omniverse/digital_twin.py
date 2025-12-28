"""
NVIDIA Omniverse Digital Twin Integration
Real-time 3D simulation of refugee camps, health facilities, and outbreak scenarios

Compliance:
- ISO 27001 A.12.1 (Operational Procedures)
- NIST CSF (Identify, Protect, Detect, Respond, Recover)
- WHO IHR (2005) Art. 6 (Notification)
"""

import omni.client
import omni.usd
from pxr import Usd, UsdGeom, Gf, Sdf
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class RefugeeCampDigitalTwin:
    """
    Digital twin of refugee camp with real-time health surveillance visualization.
    
    Features:
    - 3D visualization of camp layout
    - Real-time outbreak heatmaps
    - Water source monitoring
    - Population density tracking
    - Emergency response simulation
    """
    
    def __init__(
        self,
        camp_name: str,
        omniverse_server: str = "omniverse://localhost",
        stage_path: str = "/Projects/iLuminara/RefugeeCamps"
    ):
        self.camp_name = camp_name
        self.omniverse_server = omniverse_server
        self.stage_path = f"{stage_path}/{camp_name}.usd"
        
        # Initialize Omniverse connection
        self.stage = None
        self.root_prim = None
        
        logger.info(f"🌐 Initializing Digital Twin for {camp_name}")
    
    def initialize_stage(self):
        """Initialize USD stage for the camp"""
        # Create new stage
        self.stage = Usd.Stage.CreateNew(self.stage_path)
        
        # Set up axis and units
        UsdGeom.SetStageUpAxis(self.stage, UsdGeom.Tokens.z)
        UsdGeom.SetStageMetersPerUnit(self.stage, 1.0)
        
        # Create root prim
        self.root_prim = UsdGeom.Xform.Define(self.stage, f"/{self.camp_name}")
        self.stage.SetDefaultPrim(self.root_prim.GetPrim())
        
        logger.info(f"✅ Stage initialized: {self.stage_path}")
    
    def create_camp_layout(
        self,
        blocks: List[Dict],
        facilities: List[Dict],
        water_sources: List[Dict]
    ):
        """
        Create 3D layout of refugee camp.
        
        Args:
            blocks: List of residential blocks with coordinates
            facilities: List of health facilities, schools, etc.
            water_sources: List of water points
        """
        # Create blocks layer
        blocks_xform = UsdGeom.Xform.Define(
            self.stage,
            f"/{self.camp_name}/Blocks"
        )
        
        for i, block in enumerate(blocks):
            block_path = f"/{self.camp_name}/Blocks/Block_{block['id']}"
            block_geom = UsdGeom.Cube.Define(self.stage, block_path)
            
            # Set position
            block_geom.AddTranslateOp().Set(Gf.Vec3d(
                block['x'],
                block['y'],
                0.0
            ))
            
            # Set size
            block_geom.GetSizeAttr().Set(block.get('size', 50.0))
            
            # Set color based on population density
            density = block.get('population_density', 0.5)
            color = self._density_to_color(density)
            block_geom.GetDisplayColorAttr().Set([color])
        
        # Create facilities layer
        facilities_xform = UsdGeom.Xform.Define(
            self.stage,
            f"/{self.camp_name}/Facilities"
        )
        
        for facility in facilities:
            facility_path = f"/{self.camp_name}/Facilities/{facility['type']}_{facility['id']}"
            facility_geom = UsdGeom.Sphere.Define(self.stage, facility_path)
            
            # Set position
            facility_geom.AddTranslateOp().Set(Gf.Vec3d(
                facility['x'],
                facility['y'],
                5.0  # Elevated for visibility
            ))
            
            # Set size based on capacity
            radius = facility.get('capacity', 100) / 20.0
            facility_geom.GetRadiusAttr().Set(radius)
            
            # Color by facility type
            color = self._facility_type_to_color(facility['type'])
            facility_geom.GetDisplayColorAttr().Set([color])
        
        # Create water sources layer
        water_xform = UsdGeom.Xform.Define(
            self.stage,
            f"/{self.camp_name}/WaterSources"
        )
        
        for water in water_sources:
            water_path = f"/{self.camp_name}/WaterSources/Water_{water['id']}"
            water_geom = UsdGeom.Cylinder.Define(self.stage, water_path)
            
            # Set position
            water_geom.AddTranslateOp().Set(Gf.Vec3d(
                water['x'],
                water['y'],
                0.0
            ))
            
            # Set size
            water_geom.GetRadiusAttr().Set(5.0)
            water_geom.GetHeightAttr().Set(2.0)
            
            # Color by water quality
            quality = water.get('quality_score', 1.0)
            color = self._water_quality_to_color(quality)
            water_geom.GetDisplayColorAttr().Set([color])
        
        # Save stage
        self.stage.Save()
        logger.info(f"✅ Camp layout created with {len(blocks)} blocks, {len(facilities)} facilities, {len(water_sources)} water sources")
    
    def update_outbreak_heatmap(
        self,
        case_data: List[Dict],
        disease: str = "cholera"
    ):
        """
        Update real-time outbreak heatmap overlay.
        
        Args:
            case_data: List of cases with location and severity
            disease: Disease type
        """
        # Create or update heatmap layer
        heatmap_path = f"/{self.camp_name}/Heatmaps/{disease}"
        
        # Remove existing heatmap if present
        if self.stage.GetPrimAtPath(heatmap_path):
            self.stage.RemovePrim(heatmap_path)
        
        heatmap_xform = UsdGeom.Xform.Define(self.stage, heatmap_path)
        
        # Create heatmap grid
        grid_size = 10  # 10x10 meter cells
        heatmap_grid = {}
        
        for case in case_data:
            # Snap to grid
            grid_x = int(case['x'] / grid_size) * grid_size
            grid_y = int(case['y'] / grid_size) * grid_size
            grid_key = (grid_x, grid_y)
            
            # Accumulate cases
            if grid_key not in heatmap_grid:
                heatmap_grid[grid_key] = 0
            heatmap_grid[grid_key] += case.get('severity', 1)
        
        # Create heatmap cells
        max_severity = max(heatmap_grid.values()) if heatmap_grid else 1
        
        for (grid_x, grid_y), severity in heatmap_grid.items():
            cell_path = f"{heatmap_path}/Cell_{grid_x}_{grid_y}"
            cell_geom = UsdGeom.Cube.Define(self.stage, cell_path)
            
            # Set position (elevated for overlay)
            cell_geom.AddTranslateOp().Set(Gf.Vec3d(
                grid_x + grid_size/2,
                grid_y + grid_size/2,
                0.5
            ))
            
            # Set size
            cell_geom.GetSizeAttr().Set(grid_size)
            
            # Color by severity (normalized)
            normalized_severity = severity / max_severity
            color = self._severity_to_color(normalized_severity)
            cell_geom.GetDisplayColorAttr().Set([color])
            
            # Set opacity
            opacity = 0.3 + (normalized_severity * 0.5)
            cell_geom.CreateAttribute("primvars:displayOpacity", Sdf.ValueTypeNames.Float).Set(opacity)
        
        # Save stage
        self.stage.Save()
        logger.info(f"✅ Outbreak heatmap updated: {len(heatmap_grid)} cells, disease: {disease}")
    
    def simulate_emergency_response(
        self,
        outbreak_location: Tuple[float, float],
        response_teams: List[Dict]
    ):
        """
        Simulate emergency response to outbreak.
        
        Args:
            outbreak_location: (x, y) coordinates of outbreak epicenter
            response_teams: List of response teams with routes
        """
        # Create response layer
        response_path = f"/{self.camp_name}/EmergencyResponse"
        
        # Remove existing response if present
        if self.stage.GetPrimAtPath(response_path):
            self.stage.RemovePrim(response_path)
        
        response_xform = UsdGeom.Xform.Define(self.stage, response_path)
        
        # Mark outbreak epicenter
        epicenter_path = f"{response_path}/Epicenter"
        epicenter_geom = UsdGeom.Sphere.Define(self.stage, epicenter_path)
        epicenter_geom.AddTranslateOp().Set(Gf.Vec3d(
            outbreak_location[0],
            outbreak_location[1],
            10.0
        ))
        epicenter_geom.GetRadiusAttr().Set(15.0)
        epicenter_geom.GetDisplayColorAttr().Set([Gf.Vec3f(1.0, 0.0, 0.0)])  # Red
        
        # Create response team paths
        for i, team in enumerate(response_teams):
            team_path = f"{response_path}/Team_{i}"
            
            # Create team marker
            team_geom = UsdGeom.Cone.Define(self.stage, team_path)
            team_geom.AddTranslateOp().Set(Gf.Vec3d(
                team['start_x'],
                team['start_y'],
                5.0
            ))
            team_geom.GetRadiusAttr().Set(3.0)
            team_geom.GetHeightAttr().Set(6.0)
            team_geom.GetDisplayColorAttr().Set([Gf.Vec3f(0.0, 1.0, 0.0)])  # Green
            
            # Create route line
            route_path = f"{response_path}/Route_{i}"
            route_geom = UsdGeom.BasisCurves.Define(self.stage, route_path)
            
            # Define route points
            points = [
                Gf.Vec3f(team['start_x'], team['start_y'], 5.0),
                Gf.Vec3f(outbreak_location[0], outbreak_location[1], 10.0)
            ]
            route_geom.GetPointsAttr().Set(points)
            route_geom.GetCurveVertexCountsAttr().Set([len(points)])
            route_geom.GetWidthsAttr().Set([2.0])
            route_geom.GetDisplayColorAttr().Set([Gf.Vec3f(0.0, 1.0, 0.0)])
        
        # Save stage
        self.stage.Save()
        logger.info(f"✅ Emergency response simulated: {len(response_teams)} teams deployed")
    
    def export_snapshot(self, output_path: str):
        """Export current state as snapshot"""
        snapshot = {
            "camp_name": self.camp_name,
            "timestamp": datetime.utcnow().isoformat(),
            "stage_path": self.stage_path,
            "metadata": {
                "blocks": self._count_prims("Blocks"),
                "facilities": self._count_prims("Facilities"),
                "water_sources": self._count_prims("WaterSources"),
                "heatmaps": self._count_prims("Heatmaps")
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(snapshot, f, indent=2)
        
        logger.info(f"✅ Snapshot exported: {output_path}")
    
    def _count_prims(self, layer_name: str) -> int:
        """Count primitives in a layer"""
        layer_path = f"/{self.camp_name}/{layer_name}"
        if not self.stage.GetPrimAtPath(layer_path):
            return 0
        
        prim = self.stage.GetPrimAtPath(layer_path)
        return len(list(prim.GetChildren()))
    
    def _density_to_color(self, density: float) -> Gf.Vec3f:
        """Convert population density to color (green to red)"""
        # Green (low) to Yellow (medium) to Red (high)
        if density < 0.5:
            # Green to Yellow
            r = density * 2
            g = 1.0
            b = 0.0
        else:
            # Yellow to Red
            r = 1.0
            g = 2.0 * (1.0 - density)
            b = 0.0
        
        return Gf.Vec3f(r, g, b)
    
    def _facility_type_to_color(self, facility_type: str) -> Gf.Vec3f:
        """Convert facility type to color"""
        colors = {
            "clinic": Gf.Vec3f(0.0, 0.8, 1.0),  # Cyan
            "school": Gf.Vec3f(1.0, 0.8, 0.0),  # Yellow
            "distribution": Gf.Vec3f(0.8, 0.0, 1.0),  # Magenta
            "admin": Gf.Vec3f(0.5, 0.5, 0.5)  # Gray
        }
        return colors.get(facility_type, Gf.Vec3f(1.0, 1.0, 1.0))
    
    def _water_quality_to_color(self, quality: float) -> Gf.Vec3f:
        """Convert water quality to color (red to blue)"""
        # Red (poor) to Blue (good)
        r = 1.0 - quality
        g = 0.5
        b = quality
        return Gf.Vec3f(r, g, b)
    
    def _severity_to_color(self, severity: float) -> Gf.Vec3f:
        """Convert outbreak severity to color (yellow to red)"""
        # Yellow (low) to Red (high)
        r = 1.0
        g = 1.0 - severity
        b = 0.0
        return Gf.Vec3f(r, g, b)


# Example usage
if __name__ == "__main__":
    # Initialize digital twin for Dadaab refugee camp
    twin = RefugeeCampDigitalTwin(
        camp_name="Dadaab_Ifo",
        omniverse_server="omniverse://localhost"
    )
    
    # Initialize stage
    twin.initialize_stage()
    
    # Create camp layout
    blocks = [
        {"id": "C1", "x": 0, "y": 0, "population_density": 0.8},
        {"id": "C2", "x": 100, "y": 0, "population_density": 0.6},
        {"id": "C3", "x": 0, "y": 100, "population_density": 0.9},
        {"id": "C4", "x": 100, "y": 100, "population_density": 0.7}
    ]
    
    facilities = [
        {"id": "1", "type": "clinic", "x": 50, "y": 50, "capacity": 200},
        {"id": "2", "type": "school", "x": 150, "y": 50, "capacity": 500}
    ]
    
    water_sources = [
        {"id": "1", "x": 25, "y": 25, "quality_score": 0.8},
        {"id": "2", "x": 75, "y": 75, "quality_score": 0.3}  # Contaminated
    ]
    
    twin.create_camp_layout(blocks, facilities, water_sources)
    
    # Update outbreak heatmap
    case_data = [
        {"x": 10, "y": 10, "severity": 9},
        {"x": 15, "y": 12, "severity": 8},
        {"x": 8, "y": 15, "severity": 7}
    ]
    
    twin.update_outbreak_heatmap(case_data, disease="cholera")
    
    # Simulate emergency response
    response_teams = [
        {"start_x": 200, "start_y": 200},
        {"start_x": 250, "start_y": 200}
    ]
    
    twin.simulate_emergency_response(
        outbreak_location=(10, 10),
        response_teams=response_teams
    )
    
    # Export snapshot
    twin.export_snapshot("dadaab_snapshot.json")
    
    print("✅ Digital Twin created successfully")
