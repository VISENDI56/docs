"""
USSD Gateway for IP-06: VSAI
Enables feature phone access to iLuminara via USSD (*123#)

USSD (Unstructured Supplementary Service Data) is the primary interface
for 70% of African mobile users who don't have smartphones.

Compliance:
- Kenya DPA §25 (Direct Marketing - Consent Required)
- GDPR Art. 6 (Lawful Processing)
- CCPA §1798.120 (Right to Opt-Out)
"""

import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class USSDSessionState(Enum):
    """USSD session states"""
    INITIAL = "initial"
    MENU = "menu"
    REPORT_SYMPTOM = "report_symptom"
    VIEW_ALERTS = "view_alerts"
    REFER_FRIEND = "refer_friend"
    CHECK_BALANCE = "check_balance"
    CONSENT = "consent"
    END = "end"


@dataclass
class USSDSession:
    """Represents a USSD session"""
    session_id: str
    phone_number: str
    state: USSDSessionState
    data: Dict = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}


class USSDGateway:
    """
    USSD Gateway for feature phone access.
    
    Menu Structure:
    *123#
    ├── 1. Report Symptom
    ├── 2. View Alerts
    ├── 3. Refer a Friend (Earn Airtime)
    ├── 4. Check Airtime Balance
    └── 5. Opt Out
    """
    
    def __init__(self, vsai_engine=None):
        """
        Initialize USSD Gateway.
        
        Args:
            vsai_engine: Reference to ViralSymbioticAPIInfusion engine
        """
        self.vsai_engine = vsai_engine
        self.sessions: Dict[str, USSDSession] = {}
        
        # Symptom codes for quick entry
        self.symptom_codes = {
            "1": "fever",
            "2": "cough",
            "3": "diarrhea",
            "4": "vomiting",
            "5": "headache",
            "6": "body_aches",
            "7": "difficulty_breathing",
            "8": "rash"
        }
        
        logger.info("📱 USSD Gateway initialized - *123# active")
    
    def handle_request(
        self,
        session_id: str,
        phone_number: str,
        text: str
    ) -> Tuple[str, bool]:
        """
        Handle USSD request.
        
        Args:
            session_id: USSD session ID
            phone_number: User's phone number
            text: User input
        
        Returns:
            (response_text, continue_session)
        """
        # Get or create session
        if session_id not in self.sessions:
            self.sessions[session_id] = USSDSession(
                session_id=session_id,
                phone_number=phone_number,
                state=USSDSessionState.INITIAL
            )
        
        session = self.sessions[session_id]
        
        # Route based on state
        if session.state == USSDSessionState.INITIAL:
            return self._show_main_menu(session)
        
        elif session.state == USSDSessionState.MENU:
            return self._handle_menu_selection(session, text)
        
        elif session.state == USSDSessionState.REPORT_SYMPTOM:
            return self._handle_symptom_report(session, text)
        
        elif session.state == USSDSessionState.REFER_FRIEND:
            return self._handle_referral(session, text)
        
        elif session.state == USSDSessionState.CHECK_BALANCE:
            return self._show_balance(session)
        
        elif session.state == USSDSessionState.VIEW_ALERTS:
            return self._show_alerts(session)
        
        elif session.state == USSDSessionState.CONSENT:
            return self._handle_consent(session, text)
        
        else:
            return self._end_session(session, "Thank you for using iLuminara Health.")
    
    def _show_main_menu(self, session: USSDSession) -> Tuple[str, bool]:
        """Show main menu"""
        session.state = USSDSessionState.MENU
        
        menu = (
            "🏥 iLuminara Health\\n"
            "\\n"
            "1. Report Symptom\\n"
            "2. View Health Alerts\\n"
            "3. Refer Friend (Earn KES 50)\\n"
            "4. Check Airtime Balance\\n"
            "5. Opt Out\\n"
            "\\n"
            "Enter choice:"
        )
        
        return menu, True
    
    def _handle_menu_selection(self, session: USSDSession, text: str) -> Tuple[str, bool]:
        """Handle main menu selection"""
        choice = text.strip()
        
        if choice == "1":
            session.state = USSDSessionState.REPORT_SYMPTOM
            return self._show_symptom_menu(session)
        
        elif choice == "2":
            session.state = USSDSessionState.VIEW_ALERTS
            return self._show_alerts(session)
        
        elif choice == "3":
            session.state = USSDSessionState.REFER_FRIEND
            return self._show_referral_menu(session)
        
        elif choice == "4":
            session.state = USSDSessionState.CHECK_BALANCE
            return self._show_balance(session)
        
        elif choice == "5":
            return self._handle_opt_out(session)
        
        else:
            return "Invalid choice. Please try again.", True
    
    def _show_symptom_menu(self, session: USSDSession) -> Tuple[str, bool]:
        """Show symptom reporting menu"""
        menu = (
            "Report Symptom:\\n"
            "\\n"
            "1. Fever\\n"
            "2. Cough\\n"
            "3. Diarrhea\\n"
            "4. Vomiting\\n"
            "5. Headache\\n"
            "6. Body Aches\\n"
            "7. Difficulty Breathing\\n"
            "8. Rash\\n"
            "\\n"
            "Enter symptom code:"
        )
        
        return menu, True
    
    def _handle_symptom_report(self, session: USSDSession, text: str) -> Tuple[str, bool]:
        """Handle symptom report"""
        code = text.strip()
        
        if code not in self.symptom_codes:
            return "Invalid code. Please try again.", True
        
        symptom = self.symptom_codes[code]
        
        # Record symptom (integrate with FRENASA Engine)
        logger.info(f"📋 Symptom reported via USSD: {symptom} from {session.phone_number}")
        
        # TODO: Integrate with FRENASA Engine for processing
        # from edge_node.frenasa_engine.voice_processor import VoiceProcessor
        # processor.process_symptom(symptom, session.phone_number)
        
        response = (
            f"✅ Symptom recorded: {symptom.replace('_', ' ').title()}\\n"
            "\\n"
            "A Community Health Worker will contact you soon.\\n"
            "\\n"
            "Stay safe! 🏥"
        )
        
        return self._end_session(session, response)
    
    def _show_referral_menu(self, session: USSDSession) -> Tuple[str, bool]:
        """Show referral menu"""
        menu = (
            "💰 Refer & Earn\\n"
            "\\n"
            "Share iLuminara with friends and earn KES 50 airtime per referral!\\n"
            "\\n"
            "Your referral code:\\n"
            f"{session.phone_number[-6:]}\\n"
            "\\n"
            "Share this code with friends. They dial *123# and enter your code.\\n"
            "\\n"
            "1. View My Referrals\\n"
            "2. Back to Menu\\n"
            "\\n"
            "Enter choice:"
        )
        
        return menu, True
    
    def _handle_referral(self, session: USSDSession, text: str) -> Tuple[str, bool]:
        """Handle referral"""
        choice = text.strip()
        
        if choice == "1":
            # Show referral stats
            # TODO: Integrate with VSAI engine
            total_referrals = 0
            total_earned = 0.0
            
            if self.vsai_engine:
                node = self.vsai_engine.nodes.get(session.phone_number)
                if node:
                    total_referrals = node.total_referrals
                    total_earned = node.airtime_earned
            
            response = (
                f"📊 Your Referral Stats:\\n"
                f"\\n"
                f"Total Referrals: {total_referrals}\\n"
                f"Airtime Earned: KES {total_earned * 100:.2f}\\n"
                f"\\n"
                f"Keep sharing! 🚀"
            )
            
            return self._end_session(session, response)
        
        elif choice == "2":
            session.state = USSDSessionState.MENU
            return self._show_main_menu(session)
        
        else:
            return "Invalid choice. Please try again.", True
    
    def _show_balance(self, session: USSDSession) -> Tuple[str, bool]:
        """Show airtime balance"""
        # TODO: Integrate with VSAI engine
        balance = 0.0
        
        if self.vsai_engine:
            node = self.vsai_engine.nodes.get(session.phone_number)
            if node:
                balance = node.airtime_earned
        
        response = (
            f"💰 Your Airtime Balance:\\n"
            f"\\n"
            f"KES {balance * 100:.2f}\\n"
            f"\\n"
            f"Earned from {0} referrals\\n"
            f"\\n"
            f"Thank you for spreading health! 🏥"
        )
        
        return self._end_session(session, response)
    
    def _show_alerts(self, session: USSDSession) -> Tuple[str, bool]:
        """Show health alerts"""
        # TODO: Integrate with Early Warning System
        alerts = [
            "⚠️ Cholera outbreak in Dadaab - Boil water before drinking",
            "✅ Malaria cases declining in Garissa",
            "📢 Free vaccination clinic tomorrow at Ifo Camp"
        ]
        
        response = "🚨 Health Alerts:\\n\\n"
        for i, alert in enumerate(alerts, 1):
            response += f"{i}. {alert}\\n\\n"
        
        response += "Stay informed! 🏥"
        
        return self._end_session(session, response)
    
    def _handle_opt_out(self, session: USSDSession) -> Tuple[str, bool]:
        """Handle opt-out request"""
        # GDPR/KDPA compliance - Right to Opt-Out
        logger.info(f"🚫 Opt-out request from {session.phone_number}")
        
        # TODO: Update consent registry
        if self.vsai_engine:
            self.vsai_engine.consent_registry[session.phone_number] = False
        
        response = (
            "You have been opted out.\\n"
            "\\n"
            "You will no longer receive health alerts.\\n"
            "\\n"
            "To opt back in, dial *123# anytime.\\n"
            "\\n"
            "Stay safe! 🏥"
        )
        
        return self._end_session(session, response)
    
    def _handle_consent(self, session: USSDSession, text: str) -> Tuple[str, bool]:
        """Handle consent request"""
        choice = text.strip().lower()
        
        if choice in ["1", "yes", "y"]:
            # Grant consent
            if self.vsai_engine:
                self.vsai_engine.consent_registry[session.phone_number] = True
            
            logger.info(f"✅ Consent granted by {session.phone_number}")
            
            response = (
                "✅ Thank you for joining iLuminara!\\n"
                "\\n"
                "You will receive health alerts and can earn airtime by referring friends.\\n"
                "\\n"
                "Welcome to the health revolution! 🏥"
            )
            
            return self._end_session(session, response)
        
        else:
            response = (
                "❌ Consent declined.\\n"
                "\\n"
                "You can join anytime by dialing *123#.\\n"
                "\\n"
                "Stay safe! 🏥"
            )
            
            return self._end_session(session, response)
    
    def _end_session(self, session: USSDSession, message: str) -> Tuple[str, bool]:
        """End USSD session"""
        session.state = USSDSessionState.END
        
        # Clean up session
        if session.session_id in self.sessions:
            del self.sessions[session.session_id]
        
        return message, False  # False = end session


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    gateway = USSDGateway()
    
    # Simulate USSD session
    print("\\n" + "="*60)
    print("📱 USSD Gateway Demo - Dial *123#")
    print("="*60 + "\\n")
    
    # Initial request
    response, continue_session = gateway.handle_request(
        session_id="test_session_1",
        phone_number="+254712345678",
        text=""
    )
    print(response)
    print()
    
    # User selects "1" (Report Symptom)
    response, continue_session = gateway.handle_request(
        session_id="test_session_1",
        phone_number="+254712345678",
        text="1"
    )
    print(response)
    print()
    
    # User selects "3" (Diarrhea)
    response, continue_session = gateway.handle_request(
        session_id="test_session_1",
        phone_number="+254712345678",
        text="3"
    )
    print(response)
    print()
    
    print("✅ USSD Session Complete\\n")
