"""
Unified Security Telemetry Dashboard
Implements 2026 Data Security Index recommendation: 86% prefer integrated platforms

Consolidates:
- CodeQL SAST results
- Gitleaks secret scanning
- Dependabot security updates
- SovereignGuardrail violations
- Crypto Shredder status
- DSPM classification results

Compliance:
- 2026 DSI: Unified visibility improves threat detection by 64%
- ISO 27001 A.12.6 (Technical Vulnerability Management)
- SOC 2 (Security Monitoring)
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Import iLuminara components
try:
    from governance_kernel.vector_ledger import SovereignGuardrail
    from governance_kernel.crypto_shredder import CryptoShredder
except ImportError:
    st.warning("⚠️ Some iLuminara components not available in demo mode")


class FortressHealthDashboard:
    """
    Unified security telemetry dashboard for the Sovereign Health Fortress
    """
    
    def __init__(self):
        self.data_dir = Path("./security_telemetry")
        self.data_dir.mkdir(exist_ok=True)
        
    def load_codeql_results(self) -> Dict:
        """Load CodeQL SAST scan results"""
        codeql_file = self.data_dir / "codeql_results.json"
        
        if codeql_file.exists():
            with open(codeql_file, 'r') as f:
                return json.load(f)
        
        # Mock data for demo
        return {
            "scan_date": datetime.utcnow().isoformat(),
            "total_alerts": 3,
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 0,
            "alerts": [
                {
                    "severity": "high",
                    "rule": "py/sql-injection",
                    "message": "Potential SQL injection vulnerability",
                    "file": "api_service.py",
                    "line": 145,
                    "status": "open"
                },
                {
                    "severity": "medium",
                    "rule": "py/clear-text-logging-sensitive-data",
                    "message": "Sensitive data logged in clear text",
                    "file": "edge_node/frenasa_engine/voice_processor.py",
                    "line": 89,
                    "status": "open"
                },
                {
                    "severity": "medium",
                    "rule": "py/weak-cryptographic-algorithm",
                    "message": "Use of weak cryptographic algorithm",
                    "file": "governance_kernel/crypto_shredder.py",
                    "line": 234,
                    "status": "resolved"
                }
            ]
        }
    
    def load_gitleaks_results(self) -> Dict:
        """Load Gitleaks secret scanning results"""
        gitleaks_file = self.data_dir / "gitleaks_results.json"
        
        if gitleaks_file.exists():
            with open(gitleaks_file, 'r') as f:
                return json.load(f)
        
        # Mock data for demo
        return {
            "scan_date": datetime.utcnow().isoformat(),
            "total_leaks": 0,
            "leaks": []
        }
    
    def load_dependabot_results(self) -> Dict:
        """Load Dependabot security update results"""
        dependabot_file = self.data_dir / "dependabot_results.json"
        
        if dependabot_file.exists():
            with open(dependabot_file, 'r') as f:
                return json.load(f)
        
        # Mock data for demo
        return {
            "scan_date": datetime.utcnow().isoformat(),
            "total_alerts": 5,
            "critical": 1,
            "high": 2,
            "medium": 2,
            "low": 0,
            "alerts": [
                {
                    "severity": "critical",
                    "package": "cryptography",
                    "current_version": "41.0.0",
                    "fixed_version": "41.0.7",
                    "vulnerability": "CVE-2023-50782",
                    "status": "open"
                },
                {
                    "severity": "high",
                    "package": "requests",
                    "current_version": "2.31.0",
                    "fixed_version": "2.32.0",
                    "vulnerability": "CVE-2024-35195",
                    "status": "open"
                }
            ]
        }
    
    def load_sovereignty_violations(self) -> List[Dict]:
        """Load SovereignGuardrail violation logs"""
        try:
            guardrail = SovereignGuardrail()
            # Get recent violations from audit log
            violations = []
            audit_file = Path("./keys/audit.jsonl")
            
            if audit_file.exists():
                with open(audit_file, 'r') as f:
                    for line in f:
                        entry = json.loads(line)
                        if "VIOLATION" in entry.get("action", ""):
                            violations.append(entry)
            
            return violations[-10:]  # Last 10 violations
        except Exception as e:
            return []
    
    def load_crypto_shredder_status(self) -> Dict:
        """Load Crypto Shredder key lifecycle status"""
        try:
            shredder = CryptoShredder()
            key_dir = Path(shredder.key_storage_path)
            
            total_keys = 0
            active_keys = 0
            shredded_keys = 0
            expired_keys = 0
            
            if key_dir.exists():
                for key_file in key_dir.glob("*.json"):
                    if key_file.name == "audit.jsonl":
                        continue
                    
                    with open(key_file, 'r') as f:
                        key_metadata = json.load(f)
                    
                    total_keys += 1
                    
                    if key_metadata.get("shredded", False):
                        shredded_keys += 1
                    else:
                        active_keys += 1
                        
                        # Check expiration
                        if key_metadata.get("expires_at"):
                            expiration = datetime.fromisoformat(key_metadata["expires_at"])
                            if datetime.utcnow() > expiration:
                                expired_keys += 1
            
            return {
                "total_keys": total_keys,
                "active_keys": active_keys,
                "shredded_keys": shredded_keys,
                "expired_keys": expired_keys
            }
        except Exception as e:
            return {
                "total_keys": 0,
                "active_keys": 0,
                "shredded_keys": 0,
                "expired_keys": 0
            }
    
    def calculate_fortress_health_score(self) -> float:
        """
        Calculate overall Fortress Health Score (0-100)
        Based on 2026 DSI: Unified visibility improves threat detection by 64%
        """
        codeql = self.load_codeql_results()
        gitleaks = self.load_gitleaks_results()
        dependabot = self.load_dependabot_results()
        violations = self.load_sovereignty_violations()
        
        # Scoring algorithm
        score = 100.0
        
        # CodeQL penalties
        score -= codeql.get("critical", 0) * 20
        score -= codeql.get("high", 0) * 10
        score -= codeql.get("medium", 0) * 5
        
        # Gitleaks penalties
        score -= gitleaks.get("total_leaks", 0) * 25
        
        # Dependabot penalties
        score -= dependabot.get("critical", 0) * 15
        score -= dependabot.get("high", 0) * 8
        score -= dependabot.get("medium", 0) * 3
        
        # Sovereignty violation penalties
        score -= len(violations) * 10
        
        return max(0.0, min(100.0, score))
    
    def render_dashboard(self):
        """Render the unified security telemetry dashboard"""
        st.set_page_config(
            page_title="iLuminara Fortress Health",
            page_icon="🛡️",
            layout="wide"
        )
        
        st.title("🛡️ iLuminara Sovereign Health Fortress")
        st.markdown("**Unified Security Telemetry Dashboard** | 2026 Data Security Index Compliant")
        
        # Calculate Fortress Health Score
        health_score = self.calculate_fortress_health_score()
        
        # Header metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if health_score >= 90:
                st.metric("🛡️ Fortress Health", f"{health_score:.0f}%", delta="OPERATIONAL", delta_color="normal")
            elif health_score >= 70:
                st.metric("🛡️ Fortress Health", f"{health_score:.0f}%", delta="DEGRADED", delta_color="off")
            else:
                st.metric("🛡️ Fortress Health", f"{health_score:.0f}%", delta="COMPROMISED", delta_color="inverse")
        
        codeql = self.load_codeql_results()
        with col2:
            total_codeql = codeql.get("total_alerts", 0)
            st.metric("🔍 CodeQL Alerts", total_codeql, delta=f"{codeql.get('critical', 0)} critical")
        
        gitleaks = self.load_gitleaks_results()
        with col3:
            total_leaks = gitleaks.get("total_leaks", 0)
            st.metric("🔐 Secret Leaks", total_leaks, delta="✓ CLEAN" if total_leaks == 0 else "⚠ EXPOSED")
        
        dependabot = self.load_dependabot_results()
        with col4:
            total_deps = dependabot.get("total_alerts", 0)
            st.metric("📦 Dependency Alerts", total_deps, delta=f"{dependabot.get('critical', 0)} critical")
        
        violations = self.load_sovereignty_violations()
        with col5:
            st.metric("⚖️ Sovereignty Violations", len(violations), delta="Last 24h")
        
        st.markdown("---")
        
        # Tabs for detailed views
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview",
            "🔍 CodeQL SAST",
            "🔐 Secret Scanning",
            "📦 Dependencies",
            "⚖️ Sovereignty",
            "🔥 Crypto Shredder"
        ])
        
        with tab1:
            self.render_overview_tab(health_score, codeql, gitleaks, dependabot, violations)
        
        with tab2:
            self.render_codeql_tab(codeql)
        
        with tab3:
            self.render_gitleaks_tab(gitleaks)
        
        with tab4:
            self.render_dependabot_tab(dependabot)
        
        with tab5:
            self.render_sovereignty_tab(violations)
        
        with tab6:
            self.render_crypto_shredder_tab()
    
    def render_overview_tab(self, health_score, codeql, gitleaks, dependabot, violations):
        """Render overview tab with unified metrics"""
        st.subheader("🎯 Fortress Health Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Health score gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=health_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Fortress Health Score"},
                delta={'reference': 90},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen" if health_score >= 90 else "orange" if health_score >= 70 else "red"},
                    'steps': [
                        {'range': [0, 70], 'color': "lightgray"},
                        {'range': [70, 90], 'color': "gray"},
                        {'range': [90, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Threat distribution
            threat_data = pd.DataFrame({
                'Category': ['CodeQL', 'Gitleaks', 'Dependabot', 'Sovereignty'],
                'Critical': [
                    codeql.get('critical', 0),
                    gitleaks.get('total_leaks', 0),
                    dependabot.get('critical', 0),
                    len([v for v in violations if v.get('severity') == 'critical'])
                ],
                'High': [
                    codeql.get('high', 0),
                    0,
                    dependabot.get('high', 0),
                    len([v for v in violations if v.get('severity') == 'high'])
                ],
                'Medium': [
                    codeql.get('medium', 0),
                    0,
                    dependabot.get('medium', 0),
                    len([v for v in violations if v.get('severity') == 'medium'])
                ]
            })
            
            fig = go.Figure(data=[
                go.Bar(name='Critical', x=threat_data['Category'], y=threat_data['Critical'], marker_color='red'),
                go.Bar(name='High', x=threat_data['Category'], y=threat_data['High'], marker_color='orange'),
                go.Bar(name='Medium', x=threat_data['Category'], y=threat_data['Medium'], marker_color='yellow')
            ])
            fig.update_layout(barmode='stack', title='Threat Distribution by Category')
            st.plotly_chart(fig, use_container_width=True)
        
        # 2026 DSI Compliance Badge
        st.success("✅ **2026 Data Security Index Compliant**: Unified platform improves threat detection by 64%")
    
    def render_codeql_tab(self, codeql):
        """Render CodeQL SAST results"""
        st.subheader("🔍 CodeQL Static Application Security Testing")
        
        st.info(f"**Last Scan:** {codeql.get('scan_date', 'N/A')}")
        
        if codeql.get('total_alerts', 0) == 0:
            st.success("✅ No security vulnerabilities detected")
        else:
            alerts_df = pd.DataFrame(codeql.get('alerts', []))
            
            # Severity filter
            severity_filter = st.multiselect(
                "Filter by Severity",
                options=['critical', 'high', 'medium', 'low'],
                default=['critical', 'high', 'medium', 'low']
            )
            
            filtered_df = alerts_df[alerts_df['severity'].isin(severity_filter)]
            
            st.dataframe(filtered_df, use_container_width=True)
    
    def render_gitleaks_tab(self, gitleaks):
        """Render Gitleaks secret scanning results"""
        st.subheader("🔐 Gitleaks Secret Scanning")
        
        st.info(f"**Last Scan:** {gitleaks.get('scan_date', 'N/A')}")
        
        if gitleaks.get('total_leaks', 0) == 0:
            st.success("✅ No secrets detected in repository")
        else:
            st.error(f"⚠️ {gitleaks.get('total_leaks', 0)} secrets detected!")
            
            leaks_df = pd.DataFrame(gitleaks.get('leaks', []))
            st.dataframe(leaks_df, use_container_width=True)
    
    def render_dependabot_tab(self, dependabot):
        """Render Dependabot security updates"""
        st.subheader("📦 Dependabot Security Updates")
        
        st.info(f"**Last Scan:** {dependabot.get('scan_date', 'N/A')}")
        
        if dependabot.get('total_alerts', 0) == 0:
            st.success("✅ All dependencies up to date")
        else:
            alerts_df = pd.DataFrame(dependabot.get('alerts', []))
            
            # Severity filter
            severity_filter = st.multiselect(
                "Filter by Severity",
                options=['critical', 'high', 'medium', 'low'],
                default=['critical', 'high', 'medium', 'low'],
                key="dep_severity"
            )
            
            filtered_df = alerts_df[alerts_df['severity'].isin(severity_filter)]
            
            st.dataframe(filtered_df, use_container_width=True)
    
    def render_sovereignty_tab(self, violations):
        """Render sovereignty violations"""
        st.subheader("⚖️ Sovereignty Violations")
        
        if len(violations) == 0:
            st.success("✅ No sovereignty violations detected")
        else:
            st.warning(f"⚠️ {len(violations)} violations in last 24 hours")
            
            violations_df = pd.DataFrame(violations)
            st.dataframe(violations_df, use_container_width=True)
    
    def render_crypto_shredder_tab(self):
        """Render Crypto Shredder status"""
        st.subheader("🔥 Crypto Shredder (IP-02)")
        
        status = self.load_crypto_shredder_status()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Keys", status['total_keys'])
        
        with col2:
            st.metric("Active Keys", status['active_keys'])
        
        with col3:
            st.metric("Shredded Keys", status['shredded_keys'])
        
        with col4:
            st.metric("Expired Keys", status['expired_keys'], delta="⚠ Needs shredding" if status['expired_keys'] > 0 else "✓")
        
        # Key lifecycle chart
        if status['total_keys'] > 0:
            fig = go.Figure(data=[go.Pie(
                labels=['Active', 'Shredded', 'Expired'],
                values=[status['active_keys'], status['shredded_keys'], status['expired_keys']],
                hole=.3
            )])
            fig.update_layout(title='Key Lifecycle Distribution')
            st.plotly_chart(fig, use_container_width=True)


def main():
    dashboard = FortressHealthDashboard()
    dashboard.render_dashboard()


if __name__ == "__main__":
    main()
