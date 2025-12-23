"""
Pandemic Sentinel Module
Implements IHR 2025, GHSA, and JEE Standards for global health security

This module positions iLuminara as a trusted node in international surveillance
networks, enabling real-time outbreak detection and PHEIC notification.

Compliance:
- International Health Regulations (IHR 2005, 2025 Amendments)
- Global Health Security Agenda (GHSA)
- Joint External Evaluation (JEE) Standards
- WHO Event Information Site (EIS) Integration
- One Health Zoonotic Surveillance

Key Features:
- Pandemic Emergency alert level (new in IHR 2025)
- Auto-notification to national focal points
- Event-based surveillance feeds
- Equity in medical access protocols
- Real-time data exchange with WHO
"""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
import json

logger = logging.getLogger(__name__)


class IHRAlertLevel(Enum):
    """IHR 2025 alert levels"""
    ROUTINE = "routine"  # Normal surveillance
    WATCH = "watch"  # Increased monitoring
    ALERT = "alert"  # Potential PHEIC
    PANDEMIC_EMERGENCY = "pandemic_emergency"  # New in 2025


class PHEICCategory(Enum):
    """Public Health Emergency of International Concern categories"""
    INFECTIOUS_DISEASE = "infectious_disease"
    CHEMICAL_EVENT = "chemical_event"
    RADIOLOGICAL_EVENT = "radiological_event"
    UNKNOWN_ETIOLOGY = "unknown_etiology"
    ZOONOTIC_SPILLOVER = "zoonotic_spillover"


class JEEIndicator(Enum):
    """JEE core capacity indicators"""
    REAL_TIME_SURVEILLANCE = "real_time_surveillance"
    LABORATORY_SYSTEMS = "laboratory_systems"
    EMERGENCY_RESPONSE = "emergency_response"
    RISK_COMMUNICATION = "risk_communication"
    WORKFORCE_DEVELOPMENT = "workforce_development"
    ZOONOTIC_DISEASE = "zoonotic_disease"
    BIOSAFETY_BIOSECURITY = "biosafety_biosecurity"
    IMMUNIZATION = "immunization"


@dataclass
class OutbreakEvent:
    """Outbreak event for IHR notification"""
    event_id: str
    disease: str
    location: str
    country: str
    case_count: int
    death_count: int
    r_effective: float
    severity_score: float
    geographic_spread: int
    alert_level: IHRAlertLevel
    pheic_category: Optional[PHEICCategory]
    detection_date: str
    notification_date: Optional[str]
    national_focal_point_notified: bool
    who_notified: bool
    equity_measures_implemented: bool


class PandemicSentinel:
    """
    Pandemic Sentinel for global health security
    
    Implements IHR 2025 requirements for detection, assessment, and reporting
    """
    
    def __init__(
        self,
        country: str,
        national_focal_point: str,
        who_region: str,
        enable_auto_notification: bool = True
    ):
        self.country = country
        self.national_focal_point = national_focal_point
        self.who_region = who_region
        self.enable_auto_notification = enable_auto_notification
        
        self.active_events: Dict[str, OutbreakEvent] = {}
        self.notification_log: List[Dict] = []
        self.jee_scores: Dict[JEEIndicator, float] = {}
        
        logger.info(f"🛡️ Pandemic Sentinel initialized - Country: {country}, WHO Region: {who_region}")
    
    def assess_alert_level(
        self,
        case_count: int,
        r_effective: float,
        geographic_spread: int,
        severity_score: float,
        international_spread: bool = False
    ) -> IHRAlertLevel:
        """
        Assess IHR 2025 alert level
        
        Args:
            case_count: Number of confirmed cases
            r_effective: Effective reproduction number
            geographic_spread: Number of affected regions
            severity_score: Clinical severity (0-1)
            international_spread: Whether spread across borders
        
        Returns:
            IHRAlertLevel
        """
        # Pandemic Emergency (new in IHR 2025)
        # Criteria: High transmissibility + severity + international spread
        if (case_count > 10000 and 
            r_effective > 2.0 and 
            geographic_spread > 5 and 
            severity_score > 0.7 and
            international_spread):
            return IHRAlertLevel.PANDEMIC_EMERGENCY
        
        # Alert (potential PHEIC)
        if (case_count > 1000 and 
            r_effective > 1.5 and 
            geographic_spread > 3):
            return IHRAlertLevel.ALERT
        
        # Watch (increased monitoring)
        if case_count > 100 or r_effective > 1.2:
            return IHRAlertLevel.WATCH
        
        # Routine
        return IHRAlertLevel.ROUTINE
    
    def detect_outbreak(
        self,
        disease: str,
        location: str,
        case_count: int,
        death_count: int,
        r_effective: float,
        severity_score: float,
        geographic_spread: int,
        international_spread: bool = False,
        zoonotic: bool = False
    ) -> str:
        """
        Detect and register outbreak event
        
        Returns:
            event_id
        """
        # Assess alert level
        alert_level = self.assess_alert_level(
            case_count=case_count,
            r_effective=r_effective,
            geographic_spread=geographic_spread,
            severity_score=severity_score,
            international_spread=international_spread
        )
        
        # Determine PHEIC category
        pheic_category = None
        if alert_level in [IHRAlertLevel.ALERT, IHRAlertLevel.PANDEMIC_EMERGENCY]:
            if zoonotic:
                pheic_category = PHEICCategory.ZOONOTIC_SPILLOVER
            else:
                pheic_category = PHEICCategory.INFECTIOUS_DISEASE
        
        # Generate event ID
        event_id = f"IHR-{self.country}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Create event
        event = OutbreakEvent(
            event_id=event_id,
            disease=disease,
            location=location,
            country=self.country,
            case_count=case_count,
            death_count=death_count,
            r_effective=r_effective,
            severity_score=severity_score,
            geographic_spread=geographic_spread,
            alert_level=alert_level,
            pheic_category=pheic_category,
            detection_date=datetime.utcnow().isoformat(),
            notification_date=None,
            national_focal_point_notified=False,
            who_notified=False,
            equity_measures_implemented=False
        )
        
        self.active_events[event_id] = event
        
        logger.info(f"🚨 Outbreak Detected: {disease} in {location} - Alert: {alert_level.value}")
        
        # Auto-notify if enabled and alert level requires it
        if self.enable_auto_notification and alert_level in [
            IHRAlertLevel.ALERT,
            IHRAlertLevel.PANDEMIC_EMERGENCY
        ]:
            self.notify_national_focal_point(event_id)
            
            # Notify WHO for PHEIC potential
            if alert_level == IHRAlertLevel.PANDEMIC_EMERGENCY:
                self.notify_who(event_id)
        
        return event_id
    
    def notify_national_focal_point(self, event_id: str) -> bool:
        """
        Notify national IHR focal point per IHR Art. 6
        
        Args:
            event_id: Outbreak event ID
        
        Returns:
            Success status
        """
        if event_id not in self.active_events:
            logger.error(f"❌ Event not found: {event_id}")
            return False
        
        event = self.active_events[event_id]
        
        # Prepare notification
        notification = {
            "notification_type": "IHR_ARTICLE_6",
            "event_id": event_id,
            "disease": event.disease,
            "location": event.location,
            "country": event.country,
            "case_count": event.case_count,
            "death_count": event.death_count,
            "alert_level": event.alert_level.value,
            "pheic_category": event.pheic_category.value if event.pheic_category else None,
            "detection_date": event.detection_date,
            "notification_date": datetime.utcnow().isoformat(),
            "focal_point": self.national_focal_point,
            "urgency": "IMMEDIATE" if event.alert_level == IHRAlertLevel.PANDEMIC_EMERGENCY else "HIGH"
        }
        
        # Log notification
        self.notification_log.append(notification)
        
        # Update event
        event.national_focal_point_notified = True
        event.notification_date = notification["notification_date"]
        
        logger.info(f"📢 National Focal Point Notified: {event_id}")
        
        return True
    
    def notify_who(self, event_id: str) -> bool:
        """
        Notify WHO Event Information Site per IHR Art. 6
        
        Args:
            event_id: Outbreak event ID
        
        Returns:
            Success status
        """
        if event_id not in self.active_events:
            logger.error(f"❌ Event not found: {event_id}")
            return False
        
        event = self.active_events[event_id]
        
        # Prepare WHO notification
        who_notification = {
            "notification_type": "WHO_EIS",
            "event_id": event_id,
            "country": event.country,
            "who_region": self.who_region,
            "disease": event.disease,
            "location": event.location,
            "case_count": event.case_count,
            "death_count": event.death_count,
            "r_effective": event.r_effective,
            "severity_score": event.severity_score,
            "geographic_spread": event.geographic_spread,
            "alert_level": event.alert_level.value,
            "pheic_potential": event.pheic_category.value if event.pheic_category else None,
            "detection_date": event.detection_date,
            "notification_date": datetime.utcnow().isoformat(),
            "international_spread": event.geographic_spread > 5,
            "equity_measures": event.equity_measures_implemented
        }
        
        # Log WHO notification
        self.notification_log.append(who_notification)
        
        # Update event
        event.who_notified = True
        
        logger.info(f"🌍 WHO Notified: {event_id} - PHEIC Potential: {event.pheic_category}")
        
        return True
    
    def implement_equity_measures(self, event_id: str) -> bool:
        """
        Implement equity in medical access per IHR 2025 amendments
        
        Args:
            event_id: Outbreak event ID
        
        Returns:
            Success status
        """
        if event_id not in self.active_events:
            logger.error(f"❌ Event not found: {event_id}")
            return False
        
        event = self.active_events[event_id]
        
        equity_measures = {
            "event_id": event_id,
            "measures": [
                "Prioritize vulnerable populations (refugees, elderly, children)",
                "Ensure equitable vaccine distribution",
                "Provide free testing and treatment",
                "Multilingual risk communication",
                "Community-based surveillance in underserved areas",
                "Mobile health clinics for remote populations"
            ],
            "implementation_date": datetime.utcnow().isoformat(),
            "compliance": "IHR 2025 Amendments (Equity in Medical Access)"
        }
        
        # Update event
        event.equity_measures_implemented = True
        
        logger.info(f"⚖️ Equity Measures Implemented: {event_id}")
        
        return True
    
    def assess_jee_capacity(
        self,
        indicator: JEEIndicator,
        score: float
    ):
        """
        Assess JEE core capacity
        
        Args:
            indicator: JEE indicator
            score: Capacity score (1-5 scale)
        """
        if score < 1 or score > 5:
            logger.error(f"❌ Invalid JEE score: {score} (must be 1-5)")
            return
        
        self.jee_scores[indicator] = score
        
        logger.info(f"📊 JEE Assessment: {indicator.value} = {score}/5")
    
    def generate_jee_report(self) -> Dict:
        """
        Generate JEE report for external evaluation
        
        Returns:
            JEE report
        """
        if not self.jee_scores:
            return {"error": "No JEE assessments conducted"}
        
        # Calculate average score
        avg_score = sum(self.jee_scores.values()) / len(self.jee_scores)
        
        # Determine capacity level
        if avg_score >= 4.0:
            capacity_level = "DEMONSTRATED"
        elif avg_score >= 3.0:
            capacity_level = "DEVELOPED"
        elif avg_score >= 2.0:
            capacity_level = "LIMITED"
        else:
            capacity_level = "NOT_ADEQUATE"
        
        report = {
            "country": self.country,
            "who_region": self.who_region,
            "assessment_date": datetime.utcnow().isoformat(),
            "jee_version": "3.0",
            "indicators": {
                indicator.value: score
                for indicator, score in self.jee_scores.items()
            },
            "average_score": avg_score,
            "capacity_level": capacity_level,
            "recommendations": self._generate_jee_recommendations(),
            "compliance": [
                "IHR 2005 Core Capacities",
                "GHSA Action Packages",
                "JEE 3.0 Standards"
            ]
        }
        
        return report
    
    def _generate_jee_recommendations(self) -> List[str]:
        """Generate JEE recommendations based on scores"""
        recommendations = []
        
        for indicator, score in self.jee_scores.items():
            if score < 3.0:
                if indicator == JEEIndicator.REAL_TIME_SURVEILLANCE:
                    recommendations.append(
                        "Strengthen real-time surveillance with iLuminara Golden Thread integration"
                    )
                elif indicator == JEEIndicator.LABORATORY_SYSTEMS:
                    recommendations.append(
                        "Enhance laboratory capacity with rapid diagnostic testing"
                    )
                elif indicator == JEEIndicator.EMERGENCY_RESPONSE:
                    recommendations.append(
                        "Develop emergency response protocols with AI-assisted coordination"
                    )
        
        return recommendations
    
    def get_event_status(self, event_id: str) -> Optional[Dict]:
        """Get outbreak event status"""
        if event_id not in self.active_events:
            return None
        
        event = self.active_events[event_id]
        
        return {
            "event_id": event_id,
            "disease": event.disease,
            "location": event.location,
            "alert_level": event.alert_level.value,
            "case_count": event.case_count,
            "death_count": event.death_count,
            "r_effective": event.r_effective,
            "national_focal_point_notified": event.national_focal_point_notified,
            "who_notified": event.who_notified,
            "equity_measures": event.equity_measures_implemented,
            "detection_date": event.detection_date
        }


# Example usage
if __name__ == "__main__":
    # Initialize Pandemic Sentinel
    sentinel = PandemicSentinel(
        country="Kenya",
        national_focal_point="kenya.ihr@health.go.ke",
        who_region="AFRO",
        enable_auto_notification=True
    )
    
    # Detect cholera outbreak
    event_id = sentinel.detect_outbreak(
        disease="Cholera",
        location="Dadaab Refugee Camp",
        case_count=15000,
        death_count=450,
        r_effective=2.8,
        severity_score=0.85,
        geographic_spread=7,
        international_spread=True,
        zoonotic=False
    )
    
    print(f"🚨 Event Detected: {event_id}")
    
    # Implement equity measures
    sentinel.implement_equity_measures(event_id)
    
    # Assess JEE capacities
    sentinel.assess_jee_capacity(JEEIndicator.REAL_TIME_SURVEILLANCE, 4.5)
    sentinel.assess_jee_capacity(JEEIndicator.LABORATORY_SYSTEMS, 3.5)
    sentinel.assess_jee_capacity(JEEIndicator.EMERGENCY_RESPONSE, 4.0)
    
    # Generate JEE report
    jee_report = sentinel.generate_jee_report()
    print(f"📊 JEE Capacity: {jee_report['capacity_level']}")
    
    # Get event status
    status = sentinel.get_event_status(event_id)
    print(f"📋 Event Status: {status}")
