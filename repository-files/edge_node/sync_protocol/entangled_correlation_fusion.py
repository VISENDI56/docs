"""
Entangled Correlation Fusion (ECF) - IP-05 Enhancement
Quantum-inspired weak signal fusion for outbreak detection.

This module implements quantum-inspired correlation analysis to fuse weak,
noisy signals from multiple sources (CBS, EMR, IoT) into verified outbreak
intelligence. Uses tensor networks and belief propagation to emulate
quantum entanglement effects for signal amplification.

Compliance:
- GDPR Art. 22 (Right to Explanation) - Explainable fusion logic
- EU AI Act §6 (High-Risk AI) - Transparent correlation tracking
- ISO 27001 A.12.4 (Logging) - Complete audit trail

Author: iLuminara-Core Team
License: Proprietary - Nuclear IP Stack
"""

import numpy as np
from scipy import linalg, stats, sparse
from scipy.special import logsumexp
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Optional, Any
import heapq
import warnings
import time
import logging

logger = logging.getLogger(__name__)


class EntangledCorrelationFusion:
    """
    Quantum-inspired Entangled Correlation Fusion for weak signal fusion.
    Emulates non-local quantum correlations using classical tensor networks.
    
    This is the core of IP-05 (Golden Thread) enhancement, providing:
    - Multi-source signal fusion (CBS + EMR + IDSR + IoT)
    - Quantum-inspired correlation amplification
    - Temporal consistency verification
    - Pattern emergence detection
    """
    
    def __init__(self, 
                 max_signals: int = 1000,
                 correlation_threshold: float = 0.3,
                 time_window: float = 7.0,
                 spatial_resolution: float = 10.0,
                 entanglement_dim: int = 4):
        """
        Initialize ECF system.
        
        Args:
            max_signals: Maximum number of signals to track
            correlation_threshold: Minimum correlation to establish entanglement
            time_window: Default temporal window for correlation (days)
            spatial_resolution: Grid resolution for spatial hashing (km)
            entanglement_dim: Dimension of entangled correlation tensor
        """
        self.max_signals = max_signals
        self.correlation_threshold = correlation_threshold
        self.time_window = time_window
        self.spatial_resolution = spatial_resolution
        self.entanglement_dim = entanglement_dim
        
        # Core data structures
        self.signals = []  # List of signal dictionaries
        self.signal_index = {}  # Quick lookup by ID
        
        # Quantum-inspired structures
        self.correlation_graph = {}  # Adjacency list for entangled correlations
        self.belief_tensor = None  # Multi-dimensional belief state
        self.evidence_matrix = None  # Dempster-Shafer evidence
        
        # Temporal tracking
        self.temporal_chain = []  # Ordered signals by time
        self.time_indices = {}  # Time -> signal indices mapping
        
        # Performance optimization
        self.spatial_hash = defaultdict(list)
        self.symptom_hash = defaultdict(list)
        
        # Quantum-inspired parameters
        self.von_neumann_entropy = 0.0
        self.entanglement_strength = np.zeros((0, 0))
        self.coherence_factor = 1.0
        
        # Bayesian priors
        self.prior_belief = 0.01  # Base rate for outbreak
        self.false_positive_rate = 0.05
        
        # Initialize tensors
        self._initialize_tensors()
        
        logger.info(f"🔗 ECF initialized - Max signals: {max_signals}, Entanglement dim: {entanglement_dim}")
        
    def _initialize_tensors(self):
        """Initialize quantum-inspired tensor structures."""
        self.belief_tensor = np.ones((self.entanglement_dim, self.entanglement_dim)) / self.entanglement_dim
        self.evidence_matrix = np.eye(2)  # Identity for Dempster-Shafer
        self.entanglement_strength = np.zeros((self.max_signals, self.max_signals))
        
    def _encode_signal_features(self, signal: Dict) -> np.ndarray:
        """
        Quantum-inspired feature encoding similar to ZZFeatureMap.
        Creates pairwise interaction terms for entanglement simulation.
        """
        features = np.zeros(self.entanglement_dim)
        
        # Time component (cyclic encoding)
        if 'time' in signal:
            t = signal['time'] % 24  # Hour of day
            features[0] = np.sin(2 * np.pi * t / 24)
            features[1] = np.cos(2 * np.pi * t / 24)
        
        # Spatial components (if available)
        if 'location' in signal:
            lat, lon = signal['location']
            features[2] = np.sin(np.pi * lat / 180)
            features[3] = np.cos(np.pi * lon / 180)
        
        # Confidence encoding
        if 'confidence' in signal:
            conf = signal['confidence']
            features[:2] *= conf  # Modulate time components by confidence
        
        # Symptom type encoding (one-hot inspired)
        if 'symptom_type' in signal:
            symptom_hash = hash(signal['symptom_type']) % (self.entanglement_dim - 4)
            if symptom_hash >= 0:
                features[4 + symptom_hash] = 1.0
        
        # Normalize
        norm = np.linalg.norm(features)
        if norm > 0:
            features /= norm
            
        return features
    
    def _compute_quantum_correlation(self, feat1: np.ndarray, feat2: np.ndarray) -> float:
        """
        Compute quantum-inspired correlation using tensor contraction.
        Emulates entanglement through high-dimensional interactions.
        """
        # Outer product for entanglement simulation
        outer = np.outer(feat1, feat2)
        
        # Tensor contraction along multiple dimensions
        correlation = np.trace(outer @ outer.T)
        
        # Add non-linear phase for interference effects
        phase = np.exp(1j * np.pi * correlation)
        correlation = np.abs(phase * correlation)
        
        # Bell-like persistence across bases
        rotated1 = np.roll(feat1, 1)
        rotated2 = np.roll(feat2, 1)
        cross_correlation = np.abs(np.dot(rotated1, rotated2))
        
        # Combine correlations
        total_correlation = 0.7 * correlation + 0.3 * cross_correlation
        
        return np.clip(total_correlation, 0, 1)
    
    def _dempster_shafer_fusion(self, evidence_list: List[np.ndarray]) -> np.ndarray:
        """
        Improved Dempster-Shafer evidence fusion with quantum-inspired adjustments.
        """
        if not evidence_list:
            return np.array([0.5, 0.5])  # Maximum uncertainty
        
        # Start with first evidence
        combined = evidence_list[0].copy()
        
        # Sequential fusion with conflict handling
        for evidence in evidence_list[1:]:
            # Compute conflict
            conflict = 1 - np.sum(combined * evidence)
            
            # Quantum-inspired conflict resolution
            if conflict > 0.5:  # High conflict
                # Use interference model
                combined = 0.5 * (combined + evidence)
            else:
                # Normal D-S combination
                combined = combined * evidence
                combined /= np.sum(combined)
            
            # Apply coherence factor
            combined = self.coherence_factor * combined + (1 - self.coherence_factor) * np.array([0.5, 0.5])
        
        return combined
    
    def _belief_propagation_update(self):
        """
        Quantum-inspired belief propagation across correlation graph.
        Mimics instantaneous collapse of entangled states.
        """
        if len(self.signals) < 2:
            return
        
        n = len(self.signals)
        messages = np.ones((n, n, 2))  # Messages between nodes [belief_neg, belief_pos]
        
        # Initialize with local beliefs
        for i, signal in enumerate(self.signals):
            if 'confidence' in signal and 'is_event' in signal:
                confidence = signal['confidence']
                is_event = signal['is_event']
                if is_event:
                    messages[i, :, 1] = confidence
                    messages[i, :, 0] = 1 - confidence
                else:
                    messages[i, :, 1] = 1 - confidence
                    messages[i, :, 0] = confidence
        
        # Loopy belief propagation (simulated entanglement)
        for iteration in range(10):  # Fixed iterations for resource constraint
            new_messages = messages.copy()
            
            for i in range(n):
                neighbors = self.correlation_graph.get(i, [])
                for j in neighbors:
                    if i == j:
                        continue
                    
                    # Collect beliefs from all other neighbors
                    product_neg = 1.0
                    product_pos = 1.0
                    
                    for k in neighbors:
                        if k == j:
                            continue
                        
                        # Quantum-inspired correlation weighting
                        weight = self.entanglement_strength[i, k]
                        product_neg *= (1 - weight) * messages[k, i, 0] + weight * messages[k, i, 1]
                        product_pos *= (1 - weight) * messages[k, i, 1] + weight * messages[k, i, 0]
                    
                    # Update message with interference
                    new_messages[i, j, 0] = product_neg
                    new_messages[i, j, 1] = product_pos
                    
                    # Normalize
                    norm = new_messages[i, j, 0] + new_messages[i, j, 1]
                    if norm > 0:
                        new_messages[i, j] /= norm
            
            # Check convergence
            if np.max(np.abs(new_messages - messages)) < 0.01:
                break
                
            messages = new_messages
        
        # Update signal beliefs
        for i in range(n):
            if i in self.correlation_graph:
                neighbors = self.correlation_graph[i]
                if neighbors:
                    # Fuse messages using quantum-inspired combination
                    neighbor_beliefs = [messages[j, i] for j in neighbors]
                    fused = self._dempster_shafer_fusion(neighbor_beliefs)
                    
                    # Update signal with reinforced belief
                    if 'confidence' not in self.signals[i]:
                        self.signals[i]['confidence'] = 0.5
                    
                    # Constructive interference amplification
                    old_conf = self.signals[i]['confidence']
                    new_conf = fused[1]  # Belief in positive event
                    
                    # Amplify if multiple sources agree (constructive interference)
                    if new_conf > 0.7 and old_conf > 0.6:
                        new_conf = min(1.0, new_conf * 1.2)
                    
                    self.signals[i]['confidence'] = new_conf
                    self.signals[i]['entangled_belief'] = fused
    
    def _build_tensor_network(self):
        """
        Construct PEPS-like tensor network for multi-way correlation.
        """
        n = len(self.signals)
        if n == 0:
            return None
        
        # Create core tensor (simplified PEPS)
        tensor = np.zeros((self.entanglement_dim,) * 4)  # 4D for space-time correlations
        
        # Fill tensor with correlation strengths
        for i in range(n):
            for j in self.correlation_graph.get(i, []):
                if i < j:
                    # Get feature vectors
                    feat_i = self._encode_signal_features(self.signals[i])
                    feat_j = self._encode_signal_features(self.signals[j])
                    
                    # Create entangled pair state
                    pair_state = np.outer(feat_i, feat_j)
                    
                    # Add to tensor network (simplified contraction)
                    idx_i = i % self.entanglement_dim
                    idx_j = j % self.entanglement_dim
                    
                    # Update tensor with entangled correlation
                    for k in range(self.entanglement_dim):
                        for l in range(self.entanglement_dim):
                            tensor[idx_i, idx_j, k, l] += pair_state[k, l] * self.entanglement_strength[i, j]
        
        # Normalize tensor
        norm = np.sqrt(np.sum(tensor**2))
        if norm > 0:
            tensor /= norm
            
        return tensor
    
    def _compute_von_neumann_entropy(self, covariance: np.ndarray) -> float:
        """
        Compute von Neumann entropy from correlation matrix.
        Quantum analogue for system entanglement.
        """
        if covariance.size == 0:
            return 0.0
        
        # Ensure positive semi-definite
        covariance = (covariance + covariance.T) / 2
        covariance += np.eye(covariance.shape[0]) * 1e-10
        
        # Compute eigenvalues
        eigenvalues = np.linalg.eigvalsh(covariance)
        eigenvalues = np.maximum(eigenvalues, 1e-12)  # Avoid log(0)
        
        # Normalize for density matrix
        eigenvalues = eigenvalues / np.sum(eigenvalues)
        
        # Von Neumann entropy
        entropy = -np.sum(eigenvalues * np.log2(eigenvalues))
        
        return entropy
    
    def add_signal(self, signal_data: Dict, metadata: Optional[Dict] = None):
        """
        Add a new signal to the ECF system.
        
        Args:
            signal_data: Dictionary containing signal information
                        Required: at least one of {time, location, symptom_type}
                        Optional: confidence, is_event, source
            metadata: Additional metadata for correlation rules
        """
        # Generate unique ID
        signal_id = len(self.signals)
        
        # Ensure required fields
        if 'time' not in signal_data:
            signal_data['time'] = time.time() / 3600  # Hours since epoch
        
        if 'confidence' not in signal_data:
            signal_data['confidence'] = 0.5  # Default uncertainty
        
        if 'is_event' not in signal_data:
            signal_data['is_event'] = True  # Assume positive event
        
        # Store signal
        self.signals.append(signal_data)
        self.signal_index[signal_id] = signal_data
        
        # Update indices
        self.temporal_chain.append((signal_data['time'], signal_id))
        self.temporal_chain.sort(key=lambda x: x[0])
        
        # Spatial hashing
        if 'location' in signal_data:
            lat, lon = signal_data['location']
            grid_x = int(lat / self.spatial_resolution)
            grid_y = int(lon / self.spatial_resolution)
            self.spatial_hash[(grid_x, grid_y)].append(signal_id)
        
        # Symptom hashing
        if 'symptom_type' in signal_data:
            self.symptom_hash[signal_data['symptom_type']].append(signal_id)
        
        # Update time indices
        time_key = int(signal_data['time'] / self.time_window)
        if time_key not in self.time_indices:
            self.time_indices[time_key] = []
        self.time_indices[time_key].append(signal_id)
        
        # Update correlation graph
        self._update_correlations(signal_id)
        
        # Resize matrices if needed
        if len(self.signals) > self.entanglement_strength.shape[0]:
            new_size = min(len(self.signals) * 2, self.max_signals)
            self._resize_matrices(new_size)
        
        logger.debug(f"✅ Signal {signal_id} added - Confidence: {signal_data['confidence']:.2f}")
    
    def _update_correlations(self, new_signal_id: int):
        """Update correlation graph with new signal."""
        if len(self.signals) <= 1:
            return
        
        new_signal = self.signals[new_signal_id]
        new_features = self._encode_signal_features(new_signal)
        
        # Initialize correlation graph for new signal
        self.correlation_graph[new_signal_id] = []
        
        # Find potentially correlated signals
        candidate_ids = set()
        
        # Spatial correlation
        if 'location' in new_signal:
            lat, lon = new_signal['location']
            grid_x = int(lat / self.spatial_resolution)
            grid_y = int(lon / self.spatial_resolution)
            
            # Check neighboring cells (3x3 grid)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    key = (grid_x + dx, grid_y + dy)
                    candidate_ids.update(self.spatial_hash.get(key, []))
        
        # Temporal correlation
        time_key = int(new_signal['time'] / self.time_window)
        for dt in [-1, 0, 1]:
            candidate_ids.update(self.time_indices.get(time_key + dt, []))
        
        # Symptom correlation
        if 'symptom_type' in new_signal:
            candidate_ids.update(self.symptom_hash.get(new_signal['symptom_type'], []))
        
        # Remove self
        candidate_ids.discard(new_signal_id)
        
        # Compute correlations and establish entanglement
        for other_id in candidate_ids:
            if other_id >= len(self.signals):
                continue
                
            other_signal = self.signals[other_id]
            other_features = self._encode_signal_features(other_signal)
            
            # Compute quantum-inspired correlation
            correlation = self._compute_quantum_correlation(new_features, other_features)
            
            # Update entanglement strength matrix
            if correlation > self.correlation_threshold:
                self.entanglement_strength[new_signal_id, other_id] = correlation
                self.entanglement_strength[other_id, new_signal_id] = correlation
                
                # Add to correlation graph
                if other_id not in self.correlation_graph:
                    self.correlation_graph[other_id] = []
                if new_signal_id not in self.correlation_graph[other_id]:
                    self.correlation_graph[other_id].append(new_signal_id)
                if other_id not in self.correlation_graph[new_signal_id]:
                    self.correlation_graph[new_signal_id].append(other_id)
    
    def _resize_matrices(self, new_size: int):
        """Resize internal matrices efficiently."""
        old_size = self.entanglement_strength.shape[0]
        if new_size <= old_size:
            return
        
        # Create new matrices
        new_entanglement = np.zeros((new_size, new_size))
        new_entanglement[:old_size, :old_size] = self.entanglement_strength
        
        # Update references
        self.entanglement_strength = new_entanglement
    
    def fuse(self, max_iterations: int = 5) -> Dict:
        """
        Perform entangled correlation fusion.
        
        Args:
            max_iterations: Maximum belief propagation iterations
            
        Returns:
            Dictionary with fusion results and metrics
        """
        if len(self.signals) == 0:
            return {"status": "no_signals", "outbreak_probability": 0.0}
        
        logger.info(f"🔗 Starting ECF fusion - {len(self.signals)} signals")
        
        # Build tensor network
        tensor_network = self._build_tensor_network()
        
        # Multiple rounds of belief propagation (emulating measurement collapse)
        for iteration in range(max_iterations):
            self._belief_propagation_update()
            
            # Update coherence factor (simulates decoherence)
            self.coherence_factor *= 0.9  # Gradual decoherence
        
        # Compute overall outbreak probability
        outbreak_prob = self._compute_outbreak_probability()
        
        # Compute entanglement metrics
        n = len(self.signals)
        if n > 1:
            # Use correlation submatrix for entropy calculation
            submatrix = self.entanglement_strength[:n, :n]
            self.von_neumann_entropy = self._compute_von_neumann_entropy(submatrix)
        
        # Construct result
        result = {
            "status": "success",
            "outbreak_probability": outbreak_prob,
            "entanglement_entropy": self.von_neumann_entropy,
            "signals_fused": n,
            "entangled_clusters": len(self._find_entangled_clusters()),
            "coherence_factor": self.coherence_factor,
            "timestamp": time.time()
        }
        
        logger.info(f"✅ ECF fusion complete - Outbreak prob: {outbreak_prob:.3f}, Entropy: {self.von_neumann_entropy:.3f}")
        
        return result
    
    def _compute_outbreak_probability(self) -> float:
        """Compute overall outbreak probability from fused signals."""
        if not self.signals:
            return 0.0
        
        # Collect beliefs from all signals
        beliefs = []
        for signal in self.signals:
            if 'entangled_belief' in signal:
                beliefs.append(signal['entangled_belief'])
            elif 'confidence' in signal and 'is_event' in signal:
                conf = signal['confidence']
                if signal['is_event']:
                    beliefs.append(np.array([1 - conf, conf]))
                else:
                    beliefs.append(np.array([conf, 1 - conf]))
        
        if not beliefs:
            return 0.0
        
        # Fuse using quantum-inspired D-S
        fused_belief = self._dempster_shafer_fusion(beliefs)
        
        # Apply prior
        posterior = fused_belief[1] * self.prior_belief
        posterior /= posterior + (1 - fused_belief[1]) * (1 - self.prior_belief)
        
        return float(posterior)
    
    def verify_timeline(self, max_gap: float = 24.0) -> Dict:
        """
        Verify temporal consistency of signals.
        Detects forks, loops, or tampering via entanglement fidelity.
        
        Args:
            max_gap: Maximum allowed time gap (hours)
            
        Returns:
            Dictionary with timeline verification results
        """
        if len(self.temporal_chain) < 2:
            return {"status": "insufficient_data", "consistency_score": 1.0}
        
        # Sort by time
        timeline = sorted(self.temporal_chain, key=lambda x: x[0])
        
        inconsistencies = []
        total_checks = 0
        
        # Check temporal consistency
        for i in range(len(timeline) - 1):
            t1, id1 = timeline[i]
            t2, id2 = timeline[i + 1]
            
            total_checks += 1
            
            # Check time gap
            if t2 - t1 > max_gap:
                inconsistencies.append({
                    "type": "time_gap",
                    "gap_hours": t2 - t1,
                    "signal_ids": [id1, id2]
                })
            
            # Check entanglement consistency
            if id1 in self.correlation_graph and id2 in self.correlation_graph:
                # Signals should be correlated if close in time
                correlation = self.entanglement_strength[id1, id2]
                expected_correlation = np.exp(-(t2 - t1) / self.time_window)
                
                if correlation < 0.5 * expected_correlation:
                    inconsistencies.append({
                        "type": "entanglement_break",
                        "expected": expected_correlation,
                        "actual": correlation,
                        "signal_ids": [id1, id2]
                    })
        
        # Check for causal violations (forks)
        clusters = self._find_entangled_clusters()
        for cluster in clusters:
            if len(cluster) > 2:
                # Check if cluster forms a consistent timeline
                cluster_times = [self.signals[id]['time'] for id in cluster if 'time' in self.signals[id]]
                if len(cluster_times) > 1:
                    time_std = np.std(cluster_times)
                    if time_std > self.time_window:
                        inconsistencies.append({
                            "type": "temporal_fork",
                            "cluster_size": len(cluster),
                            "time_std": time_std,
                            "signal_ids": list(cluster)
                        })
        
        # Compute consistency score
        consistency_score = 1.0 - len(inconsistencies) / max(total_checks, 1)
        
        return {
            "status": "verified" if consistency_score > 0.8 else "suspicious",
            "consistency_score": consistency_score,
            "inconsistencies": inconsistencies,
            "total_signals": len(timeline),
            "checks_performed": total_checks
        }
    
    def _find_entangled_clusters(self, min_correlation: float = 0.4) -> List[List[int]]:
        """
        Find clusters of entangled signals using DFS.
        
        Args:
            min_correlation: Minimum correlation for entanglement
            
        Returns:
            List of clusters (each cluster is list of signal IDs)
        """
        visited = set()
        clusters = []
        
        for signal_id in range(len(self.signals)):
            if signal_id not in visited:
                # Start new cluster
                cluster = []
                stack = [signal_id]
                
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        cluster.append(current)
                        
                        # Add strongly correlated neighbors
                        if current in self.correlation_graph:
                            for neighbor in self.correlation_graph[current]:
                                if (neighbor not in visited and 
                                    self.entanglement_strength[current, neighbor] >= min_correlation):
                                    stack.append(neighbor)
                
                if len(cluster) > 1:
                    clusters.append(cluster)
        
        return clusters
    
    def get_emerged_pattern(self, threshold: float = 0.7) -> Dict:
        """
        Extract emerged patterns from fused signals.
        
        Args:
            threshold: Confidence threshold for pattern inclusion
            
        Returns:
            Dictionary with emerged patterns
        """
        if not self.signals:
            return {"patterns": [], "confidence": 0.0}
        
        # Find high-confidence clusters
        clusters = self._find_entangled_clusters()
        patterns = []
        
        for cluster in clusters:
            # Compute cluster statistics
            confidences = []
            times = []
            locations = []
            symptoms = set()
            
            for signal_id in cluster:
                signal = self.signals[signal_id]
                if 'confidence' in signal:
                    confidences.append(signal['confidence'])
                if 'time' in signal:
                    times.append(signal['time'])
                if 'location' in signal:
                    locations.append(signal['location'])
                if 'symptom_type' in signal:
                    symptoms.add(signal['symptom_type'])
            
            if confidences and np.mean(confidences) >= threshold:
                pattern = {
                    "cluster_size": len(cluster),
                    "average_confidence": float(np.mean(confidences)),
                    "time_span": float(max(times) - min(times)) if times else 0.0,
                    "symptom_types": list(symptoms),
                    "signal_ids": cluster,
                    "spatial_spread": len(set(locations)) if locations else 0
                }
                patterns.append(pattern)
        
        # Sort patterns by confidence and size
        patterns.sort(key=lambda x: x["average_confidence"] * np.log1p(x["cluster_size"]), reverse=True)
        
        # Compute overall pattern confidence
        overall_conf = 0.0
        if patterns:
            weights = [p["cluster_size"] for p in patterns]
            confidences = [p["average_confidence"] for p in patterns]
            overall_conf = np.average(confidences, weights=weights)
        
        return {
            "patterns": patterns,
            "overall_confidence": float(overall_conf),
            "total_patterns": len(patterns),
            "most_significant": patterns[0] if patterns else None
        }
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics."""
        n = len(self.signals)
        
        # Compute correlation density
        total_possible = n * (n - 1) / 2 if n > 1 else 0
        actual_edges = sum(len(neighbors) for neighbors in self.correlation_graph.values()) / 2
        
        correlation_density = actual_edges / total_possible if total_possible > 0 else 0
        
        return {
            "total_signals": n,
            "correlation_density": correlation_density,
            "average_entanglement": float(np.mean(self.entanglement_strength[:n, :n])) if n > 0 else 0.0,
            "von_neumann_entropy": self.von_neumann_entropy,
            "coherence_factor": self.coherence_factor,
            "memory_usage_MB": (self.entanglement_strength.nbytes + 
                               len(self.signals) * 1000) / (1024 * 1024)  # Rough estimate
        }
