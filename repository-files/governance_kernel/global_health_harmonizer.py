"""
Global Health Harmonizer
Orchestrates IHR 2005, GHSA, JEE, and WHO Event Information Site integration

Features:
- Automatic WHO notification (IHR Art. 6)
- PHEIC event detection
- JEE indicator mapping
- One Health zoonotic signal fusion
- Real-time surveillance feeds
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging
import json

logger = logging.getLogger(__name__)


class PHEICStatus(Enum):
    """Public Health Emergency of International Concern status"""
    NO_EVENT = "no_event"
    MONITORING = "monitoring"
    ALERT = "alert"
    PHEIC_DECLARED = "pheic_declared"


class IHRCapacity(Enum):
    """IHR core capacity areas"""
    LEGISLATION = "legislation"
    COORDINATION = "coordination"
    SURVEILLANCE = "surveillance"
    RESPONSE = "response"
    PREPAREDNESS = "preparedness"
    RISK_COMMUNICATION = "risk_communication"
    HUMAN_RESOURCES = "human_resources"
    LABORATORY = "laboratory"
    POINTS_OF_ENTRY = "points_of_entry"
    ZOONOTIC_EVENTS = "zoonotic_events"
    FOOD_SAFETY = "food_safety"
    CHEMICAL_EVENTS = "chemical_events"
    RADIONUCLEAR_EMERGENCIES = "radionuclear_emergencies"


@dataclass
class OutbreakEvent:
    """Outbreak event for IHR notification"""
    event_id: str
    disease: str
    location: Dict[str, Any]
    case_count: int
    death_count: int
    attack_rate: float
    r_effective: float
    severity_score: float
    detection_timestamp: str
    notification_required: bool = False
    notification_sent: bool = False
    pheic_status: PHEICStatus = PHEICStatus.NO_EVENT
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JEEIndicator:
    """Joint External Evaluation indicator"""
    indicator_id: str
    capacity: IHRCapacity
    score: int  # 1-5 scale
    description: str
    evidence: List[str]
    timestamp: str


class GlobalHealthHarmonizer:
    """
    Global Health Security orchestration engine
    
    Implements:
    - IHR 2005 (with 2025 amendments)
    - Global Health Security Agenda (GHSA)
    - Joint External Evaluation (JEE) Standards
    - WHO Event Information Site integration
    """
    
    def __init__(
        self,
        national_focal_point: str,
        country_code: str,
        enable_auto_notification: bool = True
    ):
        self.national_focal_point = national_focal_point
        self.country_code = country_code
        self.enable_auto_notification = enable_auto_notification
        
        # Event registry
        self.events: Dict[str, OutbreakEvent] = {}
        
        # JEE indicators
        self.jee_indicators: Dict[str, JEEIndicator] = {}
        
        # Notification log
        self.notification_log: List[Dict] = []
        
        logger.info(f"🌍 Global Health Harmonizer initialized - Country: {country_code}")
    
    def assess_notification_requirement(
        self,
        event: OutbreakEvent
    ) -> Tuple[bool, str]:
        """
        Assess if event requires IHR Art. 6 notification
        
        Decision instrument (Annex 2):
        1. Is the public health impact serious?
        2. Is the event unusual or unexpected?
        3. Is there significant risk of international spread?
        4. Is there significant risk of international travel/trade restrictions?
        
        Args:
            event: Outbreak event
        
        Returns:
            (requires_notification, reason)
        """
        reasons = []
        
        # Criterion 1: Serious public health impact
        if event.case_count > 100 or event.death_count > 10:
            reasons.append("Serious public health impact (>100 cases or >10 deaths)")
        
        if event.severity_score > 0.7:
            reasons.append(f"High severity score ({event.severity_score:.2f})")
        
        # Criterion 2: Unusual or unexpected
        if event.r_effective > 2.0:
            reasons.append(f"High transmission rate (R0={event.r_effective:.2f})")
        
        # Criterion 3: Risk of international spread
        if event.location.get("border_proximity", False):
            reasons.append("Event near international border")
        
        if event.location.get("transport_hub", False):
            reasons.append("Event at major transport hub")
        
        # Criterion 4: Risk of trade/travel restrictions
        if event.disease.lower() in ["cholera", "yellow_fever", "plague", "viral_hemorrhagic_fever"]:
            reasons.append(f"Disease of international concern: {event.disease}")
        
        # Decision
        requires_notification = len(reasons) >= 2  # At least 2 criteria met
        
        reason_text = "; ".join(reasons) if reasons else "No notification criteria met"
        
        return requires_notification, reason_text
    
    def notify_who(
        self,
        event: OutbreakEvent,
        urgency: str = "IMMEDIATE"
    ) -> Dict[str, Any]:
        """
        Send IHR Art. 6 notification to WHO
        
        Timeline:
        - Within 24 hours of assessment
        - Immediate for PHEIC-level events
        
        Args:
            event: Outbreak event
            urgency: IMMEDIATE | ROUTINE
        
        Returns:
            Notification receipt
        """
        if not self.enable_auto_notification:
            logger.warning("⚠️ Auto-notification disabled - manual notification required")
            return {"status": "DISABLED"}
        
        # Check if already notified
        if event.notification_sent:
            logger.info(f"ℹ️ Event {event.event_id} already notified")
            return {"status": "ALREADY_NOTIFIED"}
        
        # Prepare notification
        notification = {
            "notification_id": f"IHR-{self.country_code}-{event.event_id}",
            "country": self.country_code,
            "national_focal_point": self.national_focal_point,
            "event_id": event.event_id,
            "disease": event.disease,
            "location": event.location,
            "case_count": event.case_count,
            "death_count": event.death_count,
            "attack_rate": event.attack_rate,
            "r_effective": event.r_effective,
            "severity_score": event.severity_score,
            "detection_timestamp": event.detection_timestamp,
            "notification_timestamp": datetime.utcnow().isoformat(),
            "urgency": urgency,
            "pheic_status": event.pheic_status.value,
            "metadata": event.metadata
        }
        
        # Log notification
        self.notification_log.append(notification)
        
        # Mark as notified
        event.notification_sent = True
        
        logger.info(f"📡 WHO notification sent: {notification['notification_id']}")
        
        # In production, this would send to WHO Event Information Site
        # For now, return receipt
        return {
            "status": "SENT",
            "notification_id": notification["notification_id"],
            "timestamp": notification["notification_timestamp"],
            "receipt": "WHO-RECEIPT-" + notification["notification_id"]
        }
    
    def detect_pheic_event(
        self,
        event: OutbreakEvent
    ) -> PHEICStatus:
        """
        Detect if event constitutes a PHEIC
        
        PHEIC criteria:
        - Extraordinary event
        - Public health risk to other States
        - Potentially requires coordinated international response
        
        Args:
            event: Outbreak event
        
        Returns:
            PHEICStatus
        """
        pheic_score = 0
        
        # Extraordinary event
        if event.case_count > 1000:
            pheic_score += 1
        
        if event.r_effective > 3.0:
            pheic_score += 1
        
        # Public health risk to other States
        if event.location.get("international_airport", False):
            pheic_score += 1
        
        if event.disease.lower() in ["ebola", "sars", "mers", "novel_coronavirus"]:
            pheic_score += 2
        
        # Requires coordinated response
        if event.severity_score > 0.8:
            pheic_score += 1
        
        # Determine status
        if pheic_score >= 4:
            status = PHEICStatus.PHEIC_DECLARED
        elif pheic_score >= 3:
            status = PHEICStatus.ALERT
        elif pheic_score >= 1:
            status = PHEICStatus.MONITORING
        else:
            status = PHEICStatus.NO_EVENT
        
        event.pheic_status = status
        
        logger.info(f"🚨 PHEIC assessment: {status.value} (score: {pheic_score})")
        
        return status
    
    def map_to_jee_indicators(
        self,
        platform_metrics: Dict[str, Any]
    ) -> List[JEEIndicator]:
        """
        Map iLuminara platform metrics to JEE indicators
        
        JEE 3.0 Technical Areas:
        - D.1.1: Indicator and event-based surveillance systems
        - D.2.1: Interoperable, interconnected, electronic real-time reporting
        - D.3.1: Analysis of surveillance data
        
        Args:
            platform_metrics: iLuminara metrics
        
        Returns:
            List of JEE indicators
        """
        indicators = []
        
        # D.1.1: Surveillance systems
        surveillance_score = 5 if platform_metrics.get("cbs_coverage", 0) > 0.7 else 3
        indicators.append(JEEIndicator(
            indicator_id="D.1.1",
            capacity=IHRCapacity.SURVEILLANCE,
            score=surveillance_score,
            description="Indicator and event-based surveillance systems",
            evidence=[
                f"CBS coverage: {platform_metrics.get('cbs_coverage', 0):.1%}",
                f"EMR integration: {platform_metrics.get('emr_integration', False)}",
                f"IDSR compliance: {platform_metrics.get('idsr_compliance', False)}"
            ],
            timestamp=datetime.utcnow().isoformat()
        ))
        
        # D.2.1: Real-time reporting
        realtime_score = 5 if platform_metrics.get("realtime_reporting", False) else 2
        indicators.append(JEEIndicator(
            indicator_id="D.2.1",
            capacity=IHRCapacity.SURVEILLANCE,
            score=realtime_score,
            description="Interoperable, interconnected, electronic real-time reporting",
            evidence=[
                f"Golden Thread fusion: {platform_metrics.get('golden_thread_active', False)}",
                f"API latency: {platform_metrics.get('api_latency_ms', 0)}ms",
                f"Offline capability: {platform_metrics.get('offline_capable', False)}"
            ],
            timestamp=datetime.utcnow().isoformat()
        ))
        
        # D.3.1: Data analysis
        analysis_score = 5 if platform_metrics.get("ai_forecasting", False) else 3
        indicators.append(JEEIndicator(
            indicator_id="D.3.1",
            capacity=IHRCapacity.SURVEILLANCE,
            score=analysis_score,
            description="Analysis of surveillance data",
            evidence=[
                f"AI forecasting: {platform_metrics.get('ai_forecasting', False)}",
                f"Z-score analysis: {platform_metrics.get('z_score_active', False)}",
                f"Verification rate: {platform_metrics.get('verification_rate', 0):.1%}"
            ],
            timestamp=datetime.utcnow().isoformat()
        ))
        
        # Store indicators
        for indicator in indicators:
            self.jee_indicators[indicator.indicator_id] = indicator
        
        logger.info(f"📊 Mapped {len(indicators)} JEE indicators")
        
        return indicators
    
    def fuse_one_health_signals(
        self,
        human_health: Dict[str, Any],
        animal_health: Optional[Dict[str, Any]] = None,
        environmental: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Fuse One Health signals (human, animal, environmental)
        
        Supports:
        - Zoonotic disease detection
        - Environmental risk factors
        - Cross-species transmission
        
        Args:
            human_health: Human health signals
            animal_health: Animal health signals
            environmental: Environmental signals
        
        Returns:
            Fused One Health assessment
        """
        one_health_assessment = {
            "timestamp": datetime.utcnow().isoformat(),
            "human_health": human_health,
            "animal_health": animal_health,
            "environmental": environmental,
            "zoonotic_risk": 0.0,
            "transmission_pathways": [],
            "recommendations": []
        }
        
        # Calculate zoonotic risk
        risk_factors = []
        
        if human_health.get("disease") in ["rabies", "anthrax", "brucellosis", "avian_influenza"]:
            risk_factors.append("Known zoonotic disease")
            one_health_assessment["zoonotic_risk"] += 0.3
        
        if animal_health and animal_health.get("outbreak_detected"):
            risk_factors.append("Animal outbreak detected")
            one_health_assessment["zoonotic_risk"] += 0.4
        
        if environmental and environmental.get("vector_density") == "high":
            risk_factors.append("High vector density")
            one_health_assessment["zoonotic_risk"] += 0.2
        
        if human_health.get("location", {}).get("livestock_proximity"):
            risk_factors.append("Human-livestock proximity")
            one_health_assessment["zoonotic_risk"] += 0.1
        
        # Identify transmission pathways
        if animal_health:
            one_health_assessment["transmission_pathways"].append("Animal-to-human")
        
        if environmental and environmental.get("water_contamination"):
            one_health_assessment["transmission_pathways"].append("Environmental (water)")
        
        # Generate recommendations
        if one_health_assessment["zoonotic_risk"] > 0.5:
            one_health_assessment["recommendations"].extend([
                "Activate One Health coordination mechanism",
                "Conduct joint human-animal surveillance",
                "Implement vector control measures"
            ])
        
        logger.info(f"🌿 One Health assessment: Zoonotic risk = {one_health_assessment['zoonotic_risk']:.2f}")
        
        return one_health_assessment
    
    def process_outbreak_event(
        self,
        event: OutbreakEvent
    ) -> Dict[str, Any]:
        """
        Complete outbreak event processing pipeline
        
        Steps:
        1. Assess notification requirement
        2. Detect PHEIC status
        3. Notify WHO if required
        4. Update JEE indicators
        
        Args:
            event: Outbreak event
        
        Returns:
            Processing result
        """
        result = {
            "event_id": event.event_id,
            "timestamp": datetime.utcnow().isoformat(),
            "steps": []
        }
        
        # Step 1: Assess notification
        requires_notification, reason = self.assess_notification_requirement(event)
        event.notification_required = requires_notification
        
        result["steps"].append({
            "step": "notification_assessment",
            "requires_notification": requires_notification,
            "reason": reason
        })
        
        # Step 2: Detect PHEIC
        pheic_status = self.detect_pheic_event(event)
        
        result["steps"].append({
            "step": "pheic_detection",
            "status": pheic_status.value
        })
        
        # Step 3: Notify WHO
        if requires_notification:
            urgency = "IMMEDIATE" if pheic_status in [PHEICStatus.ALERT, PHEICStatus.PHEIC_DECLARED] else "ROUTINE"
            notification_receipt = self.notify_who(event, urgency)
            
            result["steps"].append({
                "step": "who_notification",
                "receipt": notification_receipt
            })
        
        # Step 4: Store event
        self.events[event.event_id] = event
        
        result["final_status"] = "PROCESSED"
        
        logger.info(f"✅ Outbreak event processed: {event.event_id}")
        
        return result


# Example usage
if __name__ == "__main__":
    # Initialize harmonizer
    harmonizer = GlobalHealthHarmonizer(
        national_focal_point="kenya.nfp@health.go.ke",
        country_code="KE",
        enable_auto_notification=True
    )
    
    # Create outbreak event
    event = OutbreakEvent(
        event_id="KE-CHOLERA-2025-001",
        disease="cholera",
        location={
            "name": "Dadaab",
            "coordinates": {"lat": 0.0512, "lng": 40.3129},
            "border_proximity": True,
            "transport_hub": False
        },
        case_count=156,
        death_count=12,
        attack_rate=0.04,
        r_effective=2.8,
        severity_score=0.75,
        detection_timestamp=datetime.utcnow().isoformat()
    )
    
    # Process event
    result = harmonizer.process_outbreak_event(event)
    
    print(f"\n{'='*60}")
    print("OUTBREAK EVENT PROCESSING")
    print(f"{'='*60}")
    print(json.dumps(result, indent=2))
    
    # Map to JEE indicators
    platform_metrics = {
        "cbs_coverage": 0.85,
        "emr_integration": True,
        "idsr_compliance": True,
        "realtime_reporting": True,
        "golden_thread_active": True,
        "api_latency_ms": 45,
        "offline_capable": True,
        "ai_forecasting": True,
        "z_score_active": True,
        "verification_rate": 0.92
    }
    
    jee_indicators = harmonizer.map_to_jee_indicators(platform_metrics)
    
    print(f"\n{'='*60}")
    print("JEE INDICATORS")
    print(f"{'='*60}")
    for indicator in jee_indicators:
        print(f"{indicator.indicator_id}: Score {indicator.score}/5")
        print(f"  {indicator.description}")
        for evidence in indicator.evidence:
            print(f"    - {evidence}")
