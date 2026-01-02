# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# Bio-Threat Response Agent - Wrapper for BioNeMo Pipelines
# Integrates with existing agentic_clinical triage system
# ------------------------------------------------------------------------------

"""
Bio-Threat Response Agent

Wrapper agent that orchestrates protein binder design and genomic triage
pipelines in response to Patient Zero flags and bio-threat detection.

Integrates with:
- core/research/blueprints/protein_binder.py
- core/research/blueprints/genomic_triage.py
- agentic_clinical/copilot_hub.py (existing triage agents)
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

import structlog

# Import BioNeMo pipelines
import sys
sys.path.append(str(Path(__file__).parent.parent))

from research.blueprints.protein_binder import (
    ProteinBinderPipeline,
    design_binder_for_threat
)
from research.blueprints.genomic_triage import (
    GenomicTriagePipeline,
    triage_patient_genomics,
    SingleCellData
)

logger = structlog.get_logger(__name__)


class ThreatLevel(Enum):
    """Bio-threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    PANDEMIC = "pandemic"


class ResponseAction(Enum):
    """Response actions"""
    MONITOR = "monitor"
    ISOLATE = "isolate"
    TREAT = "treat"
    DESIGN_THERAPEUTIC = "design_therapeutic"
    EMERGENCY_PROTOCOL = "emergency_protocol"


@dataclass
class BioThreatAlert:
    """Bio-threat alert from Patient Zero detection"""
    alert_id: str
    patient_id: str
    threat_type: str  # "viral", "bacterial", "unknown"
    pathogen_name: Optional[str]
    pathogen_sequence: Optional[str]
    threat_level: ThreatLevel
    detection_timestamp: datetime
    clinical_data: Dict[str, Any] = field(default_factory=dict)
    genomic_data: Optional[Dict[str, Any]] = None


@dataclass
class ResponsePlan:
    """Generated response plan"""
    plan_id: str
    alert_id: str
    threat_level: ThreatLevel
    recommended_actions: List[ResponseAction]
    therapeutic_design: Optional[Dict[str, Any]] = None
    genomic_triage: Optional[Dict[str, Any]] = None
    containment_strategy: List[str] = field(default_factory=list)
    monitoring_protocol: List[str] = field(default_factory=list)
    estimated_response_time: float = 0.0  # hours
    confidence: float = 0.0
    generated_at: datetime = field(default_factory=datetime.now)


class BioThreatResponseAgent:
    """
    Orchestrates bio-threat response using BioNeMo pipelines
    
    Triggered by:
    - Patient Zero flags from agentic_clinical/copilot_hub.py
    - Outbreak detection from surveillance systems
    - Manual escalation from clinicians
    """
    
    def __init__(
        self,
        protein_binder_pipeline: Optional[ProteinBinderPipeline] = None,
        genomic_triage_pipeline: Optional[GenomicTriagePipeline] = None,
        output_dir: str = "/data/bionemo/outputs/threat_response",
        enable_auto_response: bool = False
    ):
        """
        Initialize bio-threat response agent
        
        Args:
            protein_binder_pipeline: Protein binder design pipeline
            genomic_triage_pipeline: Genomic triage pipeline
            output_dir: Output directory for response plans
            enable_auto_response: Enable automatic therapeutic design
        """
        self.binder_pipeline = protein_binder_pipeline or ProteinBinderPipeline()
        self.triage_pipeline = genomic_triage_pipeline or GenomicTriagePipeline()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.enable_auto_response = enable_auto_response
        
        logger.info(
            "bio_threat_response_agent_initialized",
            output_dir=str(self.output_dir),
            auto_response=enable_auto_response
        )
    
    async def respond_to_threat(
        self,
        alert: BioThreatAlert
    ) -> ResponsePlan:
        """
        Generate comprehensive response plan for bio-threat
        
        Args:
            alert: Bio-threat alert
            
        Returns:
            Response plan with therapeutic design and triage
        """
        plan_id = f"response_{alert.alert_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(
            "threat_response_initiated",
            plan_id=plan_id,
            alert_id=alert.alert_id,
            threat_level=alert.threat_level.value
        )
        
        start_time = datetime.now()
        
        try:
            # Determine response actions based on threat level
            recommended_actions = self._determine_actions(alert)
            
            # Initialize response plan
            response_plan = ResponsePlan(
                plan_id=plan_id,
                alert_id=alert.alert_id,
                threat_level=alert.threat_level,
                recommended_actions=recommended_actions
            )
            
            # Execute response pipelines in parallel
            tasks = []
            
            # 1. Therapeutic Design (if pathogen identified)
            if alert.pathogen_sequence and ResponseAction.DESIGN_THERAPEUTIC in recommended_actions:
                logger.info("initiating_therapeutic_design")
                tasks.append(self._design_therapeutic(alert))
            
            # 2. Genomic Triage (if genomic data available)
            if alert.genomic_data and ResponseAction.TREAT in recommended_actions:
                logger.info("initiating_genomic_triage")
                tasks.append(self._perform_genomic_triage(alert))
            
            # Execute pipelines
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                for result in results:
                    if isinstance(result, Exception):
                        logger.error("pipeline_failed", error=str(result))
                        continue
                    
                    if "binder" in result:
                        response_plan.therapeutic_design = result
                    elif "triage" in result:
                        response_plan.genomic_triage = result
            
            # 3. Generate containment strategy
            response_plan.containment_strategy = self._generate_containment_strategy(
                alert,
                response_plan
            )
            
            # 4. Generate monitoring protocol
            response_plan.monitoring_protocol = self._generate_monitoring_protocol(
                alert,
                response_plan
            )
            
            # Calculate response time and confidence
            elapsed_time = (datetime.now() - start_time).total_seconds() / 3600.0
            response_plan.estimated_response_time = elapsed_time
            response_plan.confidence = self._calculate_confidence(response_plan)
            
            # Save response plan
            await self._save_response_plan(response_plan)
            
            logger.info(
                "threat_response_completed",
                plan_id=plan_id,
                confidence=response_plan.confidence,
                response_time_hours=elapsed_time
            )
            
            return response_plan
            
        except Exception as e:
            logger.error("threat_response_failed", plan_id=plan_id, error=str(e))
            raise
    
    def _determine_actions(self, alert: BioThreatAlert) -> List[ResponseAction]:
        """Determine recommended actions based on threat level"""
        actions = []
        
        if alert.threat_level == ThreatLevel.LOW:
            actions = [ResponseAction.MONITOR]
        elif alert.threat_level == ThreatLevel.MEDIUM:
            actions = [ResponseAction.MONITOR, ResponseAction.ISOLATE]
        elif alert.threat_level == ThreatLevel.HIGH:
            actions = [
                ResponseAction.ISOLATE,
                ResponseAction.TREAT,
                ResponseAction.DESIGN_THERAPEUTIC
            ]
        elif alert.threat_level in [ThreatLevel.CRITICAL, ThreatLevel.PANDEMIC]:
            actions = [
                ResponseAction.EMERGENCY_PROTOCOL,
                ResponseAction.ISOLATE,
                ResponseAction.TREAT,
                ResponseAction.DESIGN_THERAPEUTIC
            ]
        
        return actions
    
    async def _design_therapeutic(self, alert: BioThreatAlert) -> Dict[str, Any]:
        """Design neutralizing therapeutic using protein binder pipeline"""
        logger.info("designing_therapeutic", pathogen=alert.pathogen_name)
        
        result = await self.binder_pipeline.design_neutralizing_binder(
            pathogen_sequence=alert.pathogen_sequence,
            pathogen_name=alert.pathogen_name or "unknown_pathogen"
        )
        
        return {"binder": result}
    
    async def _perform_genomic_triage(self, alert: BioThreatAlert) -> Dict[str, Any]:
        """Perform genomic triage using genomic triage pipeline"""
        logger.info("performing_genomic_triage", patient_id=alert.patient_id)
        
        # Convert genomic data to SingleCellData
        genomic_data = alert.genomic_data
        sc_data = SingleCellData(
            cell_ids=genomic_data.get("cell_ids", []),
            gene_expression=genomic_data.get("gene_expression", []),
            gene_names=genomic_data.get("gene_names", []),
            patient_id=alert.patient_id
        )
        
        result = await self.triage_pipeline.analyze_patient_genomics(
            single_cell_data=sc_data,
            dna_sequence=genomic_data.get("dna_sequence"),
            clinical_context=alert.clinical_data
        )
        
        return {"triage": result}
    
    def _generate_containment_strategy(
        self,
        alert: BioThreatAlert,
        plan: ResponsePlan
    ) -> List[str]:
        """Generate containment strategy"""
        strategy = []
        
        if alert.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL, ThreatLevel.PANDEMIC]:
            strategy.extend([
                "Immediate patient isolation in negative pressure room",
                "Contact tracing for all exposed individuals (72-hour window)",
                "PPE protocol: Level 3 biosafety for all healthcare workers",
                "Quarantine all close contacts for 14 days"
            ])
        
        if plan.therapeutic_design:
            strategy.append(
                f"Prepare neutralizing binder for emergency use authorization: "
                f"{plan.therapeutic_design.get('binder', {}).get('final_binder', {}).get('binder_id', 'N/A')}"
            )
        
        if alert.threat_level == ThreatLevel.PANDEMIC:
            strategy.extend([
                "Activate emergency operations center",
                "Coordinate with WHO and CDC",
                "Implement community-wide surveillance",
                "Prepare mass vaccination/treatment protocols"
            ])
        
        return strategy
    
    def _generate_monitoring_protocol(
        self,
        alert: BioThreatAlert,
        plan: ResponsePlan
    ) -> List[str]:
        """Generate monitoring protocol"""
        protocol = [
            "Vital signs monitoring every 4 hours",
            "Daily clinical assessment",
            "Serial viral load testing (if applicable)"
        ]
        
        if plan.genomic_triage:
            triage_result = plan.genomic_triage.get("triage", {})
            if triage_result.get("triage_priority") in ["critical", "high"]:
                protocol.extend([
                    "Continuous cardiac monitoring",
                    "Hourly respiratory assessment",
                    "Serial inflammatory marker testing (CRP, IL-6, ferritin)",
                    "Daily single-cell RNA-seq for immune profiling"
                ])
        
        protocol.append("Weekly genomic surveillance for viral evolution")
        
        return protocol
    
    def _calculate_confidence(self, plan: ResponsePlan) -> float:
        """Calculate confidence in response plan"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence if therapeutic designed
        if plan.therapeutic_design:
            binder_confidence = plan.therapeutic_design.get("binder", {}).get(
                "final_binder", {}
            ).get("confidence", 0.0)
            confidence += binder_confidence * 0.3
        
        # Increase confidence if genomic triage performed
        if plan.genomic_triage:
            triage_confidence = plan.genomic_triage.get("triage", {}).get(
                "risk_score", 0.0
            )
            confidence += (1 - triage_confidence) * 0.2  # Lower risk = higher confidence
        
        return min(confidence, 1.0)
    
    async def _save_response_plan(self, plan: ResponsePlan) -> None:
        """Save response plan to disk"""
        output_path = self.output_dir / plan.plan_id
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Convert to JSON-serializable format
        plan_dict = {
            "plan_id": plan.plan_id,
            "alert_id": plan.alert_id,
            "threat_level": plan.threat_level.value,
            "recommended_actions": [a.value for a in plan.recommended_actions],
            "therapeutic_design": plan.therapeutic_design,
            "genomic_triage": plan.genomic_triage,
            "containment_strategy": plan.containment_strategy,
            "monitoring_protocol": plan.monitoring_protocol,
            "estimated_response_time_hours": plan.estimated_response_time,
            "confidence": plan.confidence,
            "generated_at": plan.generated_at.isoformat()
        }
        
        with open(output_path / "response_plan.json", "w") as f:
            json.dump(plan_dict, f, indent=2, default=str)
        
        logger.info("response_plan_saved", output_path=str(output_path))


# Integration hooks for existing agentic_clinical system

async def handle_patient_zero_alert(
    patient_id: str,
    pathogen_sequence: Optional[str] = None,
    pathogen_name: Optional[str] = None,
    clinical_data: Optional[Dict[str, Any]] = None,
    genomic_data: Optional[Dict[str, Any]] = None,
    threat_level: str = "high"
) -> Dict[str, Any]:
    """
    Entry point for Patient Zero alerts from agentic_clinical/copilot_hub.py
    
    Args:
        patient_id: Patient identifier
        pathogen_sequence: Identified pathogen sequence
        pathogen_name: Pathogen name
        clinical_data: Clinical context
        genomic_data: Patient genomic data
        threat_level: Threat severity
        
    Returns:
        Response plan
    """
    # Create alert
    alert = BioThreatAlert(
        alert_id=f"alert_{patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        patient_id=patient_id,
        threat_type="viral" if pathogen_sequence else "unknown",
        pathogen_name=pathogen_name,
        pathogen_sequence=pathogen_sequence,
        threat_level=ThreatLevel[threat_level.upper()],
        detection_timestamp=datetime.now(),
        clinical_data=clinical_data or {},
        genomic_data=genomic_data
    )
    
    # Initialize response agent
    agent = BioThreatResponseAgent(enable_auto_response=True)
    
    logger.info(
        "patient_zero_alert_received",
        patient_id=patient_id,
        threat_level=threat_level
    )
    
    # Generate response
    response_plan = await agent.respond_to_threat(alert)
    
    return {
        "plan_id": response_plan.plan_id,
        "threat_level": response_plan.threat_level.value,
        "actions": [a.value for a in response_plan.recommended_actions],
        "confidence": response_plan.confidence,
        "containment_strategy": response_plan.containment_strategy,
        "monitoring_protocol": response_plan.monitoring_protocol
    }


if __name__ == "__main__":
    # Example usage
    async def main():
        # Mock Patient Zero alert
        alert = BioThreatAlert(
            alert_id="alert_001",
            patient_id="patient_zero_001",
            threat_type="viral",
            pathogen_name="novel_coronavirus",
            pathogen_sequence="MKTIIALSYIFCLVKAQKDQYQKDQYQKDQYQ",
            threat_level=ThreatLevel.CRITICAL,
            detection_timestamp=datetime.now(),
            clinical_data={"symptoms": ["fever", "cough", "dyspnea"]},
            genomic_data={
                "cell_ids": [f"cell_{i}" for i in range(100)],
                "gene_expression": [[0.5] * 1000 for _ in range(100)],
                "gene_names": [f"GENE_{i}" for i in range(1000)]
            }
        )
        
        agent = BioThreatResponseAgent(enable_auto_response=True)
        response = await agent.respond_to_threat(alert)
        
        print(f"Response Plan ID: {response.plan_id}")
        print(f"Threat Level: {response.threat_level.value}")
        print(f"Confidence: {response.confidence:.3f}")
        print(f"Actions: {[a.value for a in response.recommended_actions]}")
    
    asyncio.run(main())
