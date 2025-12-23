"""
HSTPU-Bounded Decision Windows
═════════════════════════════════════════════════════════════════════════════

Implements time-bounded decision windows using HSTPU (Health Surveillance Time 
Processing Unit) to prevent decision paralysis during outbreak response.

Cognitive Hardening Protocol:
- Forces decisions within bounded time windows
- Escalates to human oversight if AI cannot decide
- Prevents infinite loops and analysis paralysis
- Maintains audit trail of decision timing

Compliance:
- EU AI Act §14 (Human Oversight)
- ISO 27001 A.12.1.4 (Separation of Development, Testing and Operational Facilities)
"""

import time
from typing import Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import logging
import json

logger = logging.getLogger(__name__)


class DecisionUrgency(Enum):
    """Decision urgency levels with time bounds"""
    CRITICAL = 30  # 30 seconds - Life-threatening
    URGENT = 300  # 5 minutes - Outbreak response
    ROUTINE = 1800  # 30 minutes - Standard surveillance
    ANALYTICAL = 7200  # 2 hours - Research/planning


class DecisionOutcome(Enum):
    """Possible decision outcomes"""
    DECIDED = "decided"
    ESCALATED = "escalated"
    TIMEOUT = "timeout"
    ERROR = "error"


class HSTPUDecisionWindow:
    """
    Time-bounded decision window that forces AI to decide or escalate.
    
    Prevents analysis paralysis by enforcing strict time limits on AI decisions.
    """
    
    def __init__(
        self,
        urgency: DecisionUrgency = DecisionUrgency.ROUTINE,
        enable_escalation: bool = True,
        enable_audit: bool = True
    ):
        self.urgency = urgency
        self.enable_escalation = enable_escalation
        self.enable_audit = enable_audit
        self.audit_log = []
        
        logger.info(f"🕐 HSTPU Decision Window initialized - Urgency: {urgency.name}, Timeout: {urgency.value}s")
    
    def execute_decision(
        self,
        decision_function: Callable,
        context: Dict[str, Any],
        decision_id: str,
        escalation_handler: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Execute a decision function within a bounded time window.
        
        Args:
            decision_function: Function that makes the decision
            context: Decision context (patient data, outbreak info, etc.)
            decision_id: Unique identifier for this decision
            escalation_handler: Function to call if decision times out
        
        Returns:
            Decision result with timing metadata
        """
        start_time = time.time()
        timeout_seconds = self.urgency.value
        
        logger.info(f"⏱️  Starting decision {decision_id} - Timeout: {timeout_seconds}s")
        
        try:
            # Execute decision with timeout
            result = self._execute_with_timeout(
                decision_function,
                context,
                timeout_seconds
            )
            
            elapsed_time = time.time() - start_time
            
            if result is None:
                # Timeout occurred
                logger.warning(f"⏰ Decision {decision_id} TIMEOUT after {elapsed_time:.2f}s")
                
                if self.enable_escalation and escalation_handler:
                    logger.info(f"🚨 Escalating decision {decision_id} to human oversight")
                    result = escalation_handler(context)
                    outcome = DecisionOutcome.ESCALATED
                else:
                    result = {"error": "Decision timeout", "escalation_required": True}
                    outcome = DecisionOutcome.TIMEOUT
            else:
                outcome = DecisionOutcome.DECIDED
                logger.info(f"✅ Decision {decision_id} completed in {elapsed_time:.2f}s")
            
            # Build response
            response = {
                "decision_id": decision_id,
                "outcome": outcome.value,
                "urgency": self.urgency.name,
                "timeout_seconds": timeout_seconds,
                "elapsed_seconds": elapsed_time,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "result": result,
                "within_bounds": elapsed_time <= timeout_seconds
            }
            
            # Audit log
            if self.enable_audit:
                self._log_decision(response)
            
            return response
        
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"❌ Decision {decision_id} ERROR: {e}")
            
            response = {
                "decision_id": decision_id,
                "outcome": DecisionOutcome.ERROR.value,
                "urgency": self.urgency.name,
                "timeout_seconds": timeout_seconds,
                "elapsed_seconds": elapsed_time,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "error": str(e),
                "within_bounds": False
            }
            
            if self.enable_audit:
                self._log_decision(response)
            
            return response
    
    def _execute_with_timeout(
        self,
        func: Callable,
        context: Dict[str, Any],
        timeout_seconds: float
    ) -> Optional[Any]:
        """
        Execute function with timeout.
        
        Note: This is a simplified implementation. In production, use
        multiprocessing or threading with proper timeout handling.
        """
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Decision timeout")
        
        # Set timeout alarm (Unix only)
        try:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(int(timeout_seconds))
            
            result = func(context)
            
            signal.alarm(0)  # Cancel alarm
            return result
        
        except TimeoutError:
            return None
        except AttributeError:
            # Windows doesn't support signal.SIGALRM
            # Fall back to simple execution
            logger.warning("⚠️  Timeout not supported on this platform - executing without timeout")
            return func(context)
    
    def _log_decision(self, decision_data: Dict[str, Any]):
        """Log decision to audit trail"""
        self.audit_log.append(decision_data)
        
        # Persist to file
        audit_file = f"logs/hstpu_decisions_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        try:
            with open(audit_file, 'a') as f:
                f.write(json.dumps(decision_data) + '\n')
        except Exception as e:
            logger.error(f"Failed to write audit log: {e}")
    
    def get_decision_metrics(self) -> Dict[str, Any]:
        """Get metrics on decision timing"""
        if not self.audit_log:
            return {"total_decisions": 0}
        
        total = len(self.audit_log)
        decided = sum(1 for d in self.audit_log if d["outcome"] == DecisionOutcome.DECIDED.value)
        escalated = sum(1 for d in self.audit_log if d["outcome"] == DecisionOutcome.ESCALATED.value)
        timeout = sum(1 for d in self.audit_log if d["outcome"] == DecisionOutcome.TIMEOUT.value)
        
        avg_time = sum(d["elapsed_seconds"] for d in self.audit_log) / total
        
        return {
            "total_decisions": total,
            "decided": decided,
            "escalated": escalated,
            "timeout": timeout,
            "average_time_seconds": avg_time,
            "decision_rate": decided / total if total > 0 else 0,
            "escalation_rate": escalated / total if total > 0 else 0
        }


# Example usage
if __name__ == "__main__":
    import random
    
    # Simulate a decision function
    def diagnose_patient(context: Dict[str, Any]) -> Dict[str, Any]:
        """Simulated AI diagnosis function"""
        # Simulate processing time
        time.sleep(random.uniform(0.5, 2.0))
        
        symptoms = context.get("symptoms", [])
        
        if "diarrhea" in symptoms and "vomiting" in symptoms:
            return {
                "diagnosis": "cholera",
                "confidence": 0.92,
                "recommendation": "Immediate ORS and isolation"
            }
        elif "fever" in symptoms:
            return {
                "diagnosis": "malaria",
                "confidence": 0.85,
                "recommendation": "RDT and antimalarial treatment"
            }
        else:
            return {
                "diagnosis": "unknown",
                "confidence": 0.3,
                "recommendation": "Further assessment required"
            }
    
    # Escalation handler
    def escalate_to_human(context: Dict[str, Any]) -> Dict[str, Any]:
        """Human oversight escalation"""
        return {
            "escalated": True,
            "message": "Decision escalated to clinical officer",
            "context": context
        }
    
    # Create decision window
    window = HSTPUDecisionWindow(
        urgency=DecisionUrgency.URGENT,
        enable_escalation=True
    )
    
    # Execute decision
    result = window.execute_decision(
        decision_function=diagnose_patient,
        context={
            "patient_id": "PAT_001",
            "symptoms": ["diarrhea", "vomiting", "dehydration"],
            "location": "Dadaab"
        },
        decision_id="DIAG_001",
        escalation_handler=escalate_to_human
    )
    
    print(json.dumps(result, indent=2))
    
    # Get metrics
    metrics = window.get_decision_metrics()
    print(f"\n📊 Decision Metrics:")
    print(json.dumps(metrics, indent=2))
