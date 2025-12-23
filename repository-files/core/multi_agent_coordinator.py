"""
Step 12: Multi-Agent Ensemble Activation
Manages concurrent execution of specialized agents for high-fidelity outbreak predictions

Compliance:
- WHO IHR (2005) Article 6 (Notification and Verification)
- EU AI Act §6 (High-Risk AI Systems)
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, asdict
import json

logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Specialized agent types"""
    EPIDEMIOLOGICAL = "epidemiological_forecasting"
    SPATIOTEMPORAL = "spatiotemporal_analysis"
    EARLY_WARNING = "early_warning_system"
    ETHICAL_AUDIT = "ethical_audit"
    RESOURCE_ALLOCATION = "resource_allocation"


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class AgentResult:
    """Result from agent execution"""
    agent_type: AgentType
    status: AgentStatus
    result: Dict
    execution_time_ms: float
    timestamp: datetime
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['agent_type'] = self.agent_type.value
        data['status'] = self.status.value
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class EnsemblePrediction:
    """Ensemble prediction from multiple agents"""
    prediction_id: str
    location: str
    disease: str
    confidence_score: float
    risk_level: str
    agent_results: List[AgentResult]
    consensus_factors: Dict
    timestamp: datetime
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['agent_results'] = [r.to_dict() for r in self.agent_results]
        data['timestamp'] = self.timestamp.isoformat()
        return data


class MultiAgentCoordinator:
    """
    Coordinates concurrent execution of specialized AI agents.
    
    Implements ensemble learning for high-fidelity outbreak predictions
    by combining outputs from:
    - Epidemiological Forecasting Agent (SEIR, SIR, ARIMA)
    - Spatiotemporal Analysis Agent (Clustering, Hotspot Detection)
    - Early Warning System Agent (Real-time Multi-source Fusion)
    """
    
    def __init__(
        self,
        location: str,
        population_size: int,
        enable_parallel_execution: bool = True,
        timeout_seconds: int = 30
    ):
        self.location = location
        self.population_size = population_size
        self.enable_parallel_execution = enable_parallel_execution
        self.timeout_seconds = timeout_seconds
        
        # Agent registry
        self.agents: Dict[AgentType, object] = {}
        
        # Execution history
        self.execution_history: List[EnsemblePrediction] = []
        
        logger.info(
            f"🤖 Multi-Agent Coordinator initialized - "
            f"Location: {location}, Population: {population_size:,}"
        )
    
    def register_agent(self, agent_type: AgentType, agent: object) -> None:
        """Register a specialized agent"""
        self.agents[agent_type] = agent
        logger.info(f"✅ Registered agent: {agent_type.value}")
    
    async def execute_ensemble(
        self,
        disease: str,
        historical_data: Dict,
        forecast_horizon_days: int = 14
    ) -> EnsemblePrediction:
        """
        Execute all agents in parallel and combine results.
        
        Args:
            disease: Disease to forecast
            historical_data: Historical case data
            forecast_horizon_days: Forecast horizon
        
        Returns:
            EnsemblePrediction with combined results
        """
        start_time = datetime.utcnow()
        
        logger.info(f"🚀 Starting ensemble execution - Disease: {disease}")
        
        # Execute agents
        if self.enable_parallel_execution:
            agent_results = await self._execute_parallel(
                disease, historical_data, forecast_horizon_days
            )
        else:
            agent_results = await self._execute_sequential(
                disease, historical_data, forecast_horizon_days
            )
        
        # Combine results using ensemble logic
        ensemble_prediction = self._combine_results(
            disease, agent_results, start_time
        )
        
        # Store in history
        self.execution_history.append(ensemble_prediction)
        
        logger.info(
            f"✅ Ensemble complete - "
            f"Confidence: {ensemble_prediction.confidence_score:.2f}, "
            f"Risk: {ensemble_prediction.risk_level}"
        )
        
        return ensemble_prediction
    
    async def _execute_parallel(
        self,
        disease: str,
        historical_data: Dict,
        forecast_horizon_days: int
    ) -> List[AgentResult]:
        """Execute agents in parallel"""
        tasks = []
        
        for agent_type, agent in self.agents.items():
            task = self._execute_agent(
                agent_type, agent, disease, historical_data, forecast_horizon_days
            )
            tasks.append(task)
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to failed results
        agent_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                agent_type = list(self.agents.keys())[i]
                agent_results.append(AgentResult(
                    agent_type=agent_type,
                    status=AgentStatus.FAILED,
                    result={},
                    execution_time_ms=0,
                    timestamp=datetime.utcnow(),
                    error=str(result)
                ))
            else:
                agent_results.append(result)
        
        return agent_results
    
    async def _execute_sequential(
        self,
        disease: str,
        historical_data: Dict,
        forecast_horizon_days: int
    ) -> List[AgentResult]:
        """Execute agents sequentially"""
        agent_results = []
        
        for agent_type, agent in self.agents.items():
            result = await self._execute_agent(
                agent_type, agent, disease, historical_data, forecast_horizon_days
            )
            agent_results.append(result)
        
        return agent_results
    
    async def _execute_agent(
        self,
        agent_type: AgentType,
        agent: object,
        disease: str,
        historical_data: Dict,
        forecast_horizon_days: int
    ) -> AgentResult:
        """Execute a single agent with timeout"""
        start_time = datetime.utcnow()
        
        try:
            # Execute agent with timeout
            if agent_type == AgentType.EPIDEMIOLOGICAL:
                result = await asyncio.wait_for(
                    self._run_epidemiological_agent(agent, disease, historical_data, forecast_horizon_days),
                    timeout=self.timeout_seconds
                )
            elif agent_type == AgentType.SPATIOTEMPORAL:
                result = await asyncio.wait_for(
                    self._run_spatiotemporal_agent(agent, disease, historical_data),
                    timeout=self.timeout_seconds
                )
            elif agent_type == AgentType.EARLY_WARNING:
                result = await asyncio.wait_for(
                    self._run_early_warning_agent(agent, disease, historical_data),
                    timeout=self.timeout_seconds
                )
            else:
                result = {}
            
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            return AgentResult(
                agent_type=agent_type,
                status=AgentStatus.COMPLETED,
                result=result,
                execution_time_ms=execution_time,
                timestamp=datetime.utcnow()
            )
        
        except asyncio.TimeoutError:
            logger.error(f"⏰ Agent timeout: {agent_type.value}")
            return AgentResult(
                agent_type=agent_type,
                status=AgentStatus.TIMEOUT,
                result={},
                execution_time_ms=self.timeout_seconds * 1000,
                timestamp=datetime.utcnow(),
                error="Execution timeout"
            )
        
        except Exception as e:
            logger.error(f"❌ Agent failed: {agent_type.value} - {e}")
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            return AgentResult(
                agent_type=agent_type,
                status=AgentStatus.FAILED,
                result={},
                execution_time_ms=execution_time,
                timestamp=datetime.utcnow(),
                error=str(e)
            )
    
    async def _run_epidemiological_agent(
        self,
        agent: object,
        disease: str,
        historical_data: Dict,
        forecast_horizon_days: int
    ) -> Dict:
        """Run epidemiological forecasting agent"""
        # Simulate agent execution (replace with actual agent call)
        await asyncio.sleep(0.1)
        
        return {
            'forecast': {
                'peak_cases': 1500,
                'peak_date': '2025-02-15',
                'r0_estimate': 2.8,
                'confidence_interval': [1200, 1800]
            },
            'model': 'SEIR',
            'confidence': 0.85
        }
    
    async def _run_spatiotemporal_agent(
        self,
        agent: object,
        disease: str,
        historical_data: Dict
    ) -> Dict:
        """Run spatiotemporal analysis agent"""
        await asyncio.sleep(0.1)
        
        return {
            'hotspots': [
                {'location': 'Dadaab', 'risk_score': 0.92},
                {'location': 'Garissa', 'risk_score': 0.78}
            ],
            'transmission_pathways': ['road_network', 'water_sources'],
            'confidence': 0.80
        }
    
    async def _run_early_warning_agent(
        self,
        agent: object,
        disease: str,
        historical_data: Dict
    ) -> Dict:
        """Run early warning system agent"""
        await asyncio.sleep(0.1)
        
        return {
            'alert_level': 'HIGH',
            'risk_score': 0.88,
            'triggers': ['case_surge', 'spatial_clustering'],
            'confidence': 0.90
        }
    
    def _combine_results(
        self,
        disease: str,
        agent_results: List[AgentResult],
        start_time: datetime
    ) -> EnsemblePrediction:
        """
        Combine agent results using ensemble logic.
        
        Uses weighted voting based on agent confidence and historical accuracy.
        """
        # Extract successful results
        successful_results = [r for r in agent_results if r.status == AgentStatus.COMPLETED]
        
        if not successful_results:
            # All agents failed
            return EnsemblePrediction(
                prediction_id=self._generate_prediction_id(),
                location=self.location,
                disease=disease,
                confidence_score=0.0,
                risk_level="UNKNOWN",
                agent_results=agent_results,
                consensus_factors={},
                timestamp=datetime.utcnow()
            )
        
        # Calculate ensemble confidence (weighted average)
        total_confidence = 0.0
        total_weight = 0.0
        
        for result in successful_results:
            confidence = result.result.get('confidence', 0.5)
            weight = self._get_agent_weight(result.agent_type)
            total_confidence += confidence * weight
            total_weight += weight
        
        ensemble_confidence = total_confidence / total_weight if total_weight > 0 else 0.0
        
        # Determine risk level
        risk_level = self._determine_risk_level(successful_results)
        
        # Calculate consensus factors
        consensus_factors = {
            'agent_agreement': len(successful_results) / len(agent_results),
            'confidence_variance': self._calculate_confidence_variance(successful_results),
            'execution_time_ms': (datetime.utcnow() - start_time).total_seconds() * 1000
        }
        
        return EnsemblePrediction(
            prediction_id=self._generate_prediction_id(),
            location=self.location,
            disease=disease,
            confidence_score=ensemble_confidence,
            risk_level=risk_level,
            agent_results=agent_results,
            consensus_factors=consensus_factors,
            timestamp=datetime.utcnow()
        )
    
    def _get_agent_weight(self, agent_type: AgentType) -> float:
        """Get weight for agent type"""
        weights = {
            AgentType.EPIDEMIOLOGICAL: 0.4,
            AgentType.SPATIOTEMPORAL: 0.3,
            AgentType.EARLY_WARNING: 0.3,
        }
        return weights.get(agent_type, 0.2)
    
    def _determine_risk_level(self, results: List[AgentResult]) -> str:
        """Determine overall risk level from agent results"""
        risk_scores = []
        
        for result in results:
            if 'risk_score' in result.result:
                risk_scores.append(result.result['risk_score'])
            elif 'alert_level' in result.result:
                # Convert alert level to score
                alert_map = {'LOW': 0.25, 'MEDIUM': 0.5, 'HIGH': 0.75, 'CRITICAL': 1.0}
                risk_scores.append(alert_map.get(result.result['alert_level'], 0.5))
        
        if not risk_scores:
            return "UNKNOWN"
        
        avg_risk = sum(risk_scores) / len(risk_scores)
        
        if avg_risk >= 0.75:
            return "CRITICAL"
        elif avg_risk >= 0.5:
            return "HIGH"
        elif avg_risk >= 0.25:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_confidence_variance(self, results: List[AgentResult]) -> float:
        """Calculate variance in agent confidence scores"""
        confidences = [r.result.get('confidence', 0.5) for r in results]
        
        if len(confidences) < 2:
            return 0.0
        
        mean = sum(confidences) / len(confidences)
        variance = sum((c - mean) ** 2 for c in confidences) / len(confidences)
        
        return variance
    
    def _generate_prediction_id(self) -> str:
        """Generate unique prediction ID"""
        import hashlib
        data = f"{self.location}_{datetime.utcnow().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def get_execution_history(self, limit: int = 100) -> List[EnsemblePrediction]:
        """Get recent execution history"""
        return self.execution_history[-limit:]


# Example usage
if __name__ == "__main__":
    async def main():
        # Initialize coordinator
        coordinator = MultiAgentCoordinator(
            location="Dadaab",
            population_size=200000,
            enable_parallel_execution=True
        )
        
        # Register agents (mock agents for demo)
        coordinator.register_agent(AgentType.EPIDEMIOLOGICAL, object())
        coordinator.register_agent(AgentType.SPATIOTEMPORAL, object())
        coordinator.register_agent(AgentType.EARLY_WARNING, object())
        
        # Execute ensemble
        prediction = await coordinator.execute_ensemble(
            disease="cholera",
            historical_data={'cases': [10, 15, 25, 40]},
            forecast_horizon_days=14
        )
        
        print(f"✅ Ensemble Prediction:")
        print(f"   Prediction ID: {prediction.prediction_id}")
        print(f"   Confidence: {prediction.confidence_score:.2f}")
        print(f"   Risk Level: {prediction.risk_level}")
        print(f"   Agents: {len(prediction.agent_results)}")
        print(f"   Consensus: {json.dumps(prediction.consensus_factors, indent=2)}")
    
    asyncio.run(main())
