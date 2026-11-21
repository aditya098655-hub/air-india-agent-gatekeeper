"""
Gatekeeper Decision Engine - Air India
Evaluates autonomous AI agent requests against Air India Zero-Trust Security Rules (R1 - R8).

Decisions returned:
- ALLOW: Request is safe and permitted autonomously.
- ASK CUSTOMER: High-impact or sensitive request requiring human-in-the-loop customer approval.
- BLOCK: Request is unauthorized, unsafe, or violates governance rules.
"""

from typing import Dict, Any, Optional

# Supported Business Actions in Air India Core Simulation
ACTION_VIEW_FARES = "VIEW_FARES"
ACTION_BOOK_FLIGHT = "BOOK_FLIGHT"
ACTION_MODIFY_BOOKING = "MODIFY_BOOKING"
ACTION_REQUEST_REFUND = "REQUEST_REFUND"

SUPPORTED_ACTIONS = [
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_MODIFY_BOOKING,
    ACTION_REQUEST_REFUND
]

# Rule Definitions
RULES_INFO = {
    "R1": "Unknown or unregistered agents must be BLOCKED.",
    "R2": "Registered agents can view flight fares without additional approval.",
    "R3": "Registered agents can book flights costing up to ₹10,000.",
    "R4": "Bookings exceeding ₹10,000 require customer confirmation.",
    "R5": "Changing an existing booking requires customer confirmation.",
    "R6": "Refund requests require customer confirmation.",
    "R7": "Revoked agents must always be BLOCKED.",
    "R8": "Unsupported actions and actions without required customer approval must be BLOCKED."
}

# Financial Threshold for Autonomous Bookings
AUTONOMOUS_BOOKING_THRESHOLD_INR = 10000.0


def evaluate_request(
    agent_id: str,
    action: str,
    amount_inr: Optional[float] = None,
    details: Optional[Dict[str, Any]] = None,
    agent_record: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Evaluates an agent request based on Air India Security Rules R1 through R8.
    
    Parameters:
    - agent_id: The identifier claimed by the requesting agent.
    - action: The operation being requested.
    - amount_inr: Financial cost in INR (if applicable, e.g. for bookings/refunds).
    - details: Contextual details (e.g. flight number, route, PNR).
    - agent_record: Stored agent metadata from agents.json, or None if not found.

    Returns:
    - A dictionary containing:
        - decision: 'ALLOW' | 'ASK CUSTOMER' | 'BLOCK'
        - rule_applied: 'R1' .. 'R8'
        - explanation: Clear business and security reasoning
        - requires_customer_action: boolean indicating if customer approval prompt is required
    """
    details = details or {}
    
    # -------------------------------------------------------------
    # Rule R1: Unregistered or Unknown Agent
    # -------------------------------------------------------------
    if agent_record is None:
        return {
            "decision": "BLOCK",
            "rule_applied": "R1",
            "explanation": f"Access Denied: Agent '{agent_id}' is not registered in the Air India Agent Registry. (Rule R1: Unknown or unregistered agents must be BLOCKED)",
            "requires_customer_action": False
        }

    # -------------------------------------------------------------
    # Rule R7: Revoked Agent Check
    # (Checked before any action evaluation - revoked agents are unconditionally blocked)
    # -------------------------------------------------------------
    agent_status = agent_record.get("status", "").upper()
    if agent_status == "REVOKED":
        revocation_reason = agent_record.get("revocation_reason") or "Credentials revoked by Air India Security"
        revoked_at = agent_record.get("revoked_at") or "Unknown"
        return {
            "decision": "BLOCK",
            "rule_applied": "R7",
            "explanation": f"Access Denied: Agent '{agent_id}' was revoked on {revoked_at}. Reason: {revocation_reason}. (Rule R7: Revoked agents must always be BLOCKED)",
            "requires_customer_action": False
        }

    # If the agent is registered but not ACTIVE (safety fallback)
    if agent_status != "ACTIVE":
        return {
            "decision": "BLOCK",
            "rule_applied": "R1",
            "explanation": f"Access Denied: Agent '{agent_id}' status is '{agent_status}', not ACTIVE. (Rule R1: Non-active agents must be BLOCKED)",
            "requires_customer_action": False
        }

    # -------------------------------------------------------------
    # Rule R8: Unsupported Action Check
    # -------------------------------------------------------------
    if action not in SUPPORTED_ACTIONS:
        return {
            "decision": "BLOCK",
            "rule_applied": "R8",
            "explanation": f"Access Denied: Requested action '{action}' is not supported by Air India Gatekeeper. (Rule R8: Unsupported actions must be BLOCKED)",
            "requires_customer_action": False
        }

    # -------------------------------------------------------------
    # Rule R2: View Flight Fares
    # -------------------------------------------------------------
    if action == ACTION_VIEW_FARES:
        route = details.get("route", "General Network Fares")
        return {
            "decision": "ALLOW",
            "rule_applied": "R2",
            "explanation": f"Access Granted: Active registered agent '{agent_id}' is authorized to view flight fares for {route}. (Rule R2: Registered agents can view flight fares without additional approval)",
            "requires_customer_action": False
        }

    # -------------------------------------------------------------
    # Rules R3 & R4: Book Flight
    # -------------------------------------------------------------
    if action == ACTION_BOOK_FLIGHT:
        booking_cost = float(amount_inr) if amount_inr is not None else 0.0
        flight = details.get("flight", "AI Domestic Flight")
        
        if booking_cost <= AUTONOMOUS_BOOKING_THRESHOLD_INR:
            return {
                "decision": "ALLOW",
                "rule_applied": "R3",
                "explanation": f"Access Granted: Booking of ₹{booking_cost:,.2f} for {flight} is within the autonomous threshold of ₹{AUTONOMOUS_BOOKING_THRESHOLD_INR:,.2f}. (Rule R3: Registered agents can book flights costing up to ₹10,000)",
                "requires_customer_action": False
            }
        else:
            return {
                "decision": "ASK CUSTOMER",
                "rule_applied": "R4",
                "explanation": f"Customer Confirmation Required: Booking cost of ₹{booking_cost:,.2f} for {flight} exceeds the autonomous threshold of ₹{AUTONOMOUS_BOOKING_THRESHOLD_INR:,.2f}. (Rule R4: Bookings exceeding ₹10,000 require customer confirmation)",
                "requires_customer_action": True
            }

    # -------------------------------------------------------------
    # Rule R5: Changing an Existing Booking
    # -------------------------------------------------------------
    if action == ACTION_MODIFY_BOOKING:
        pnr = details.get("pnr", "AI-UNKNOWN")
        change_desc = details.get("change_description", "flight date/seat modification")
        return {
            "decision": "ASK CUSTOMER",
            "rule_applied": "R5",
            "explanation": f"Customer Confirmation Required: Modifying existing booking PNR '{pnr}' ({change_desc}) requires explicit passenger consent. (Rule R5: Changing an existing booking requires customer confirmation)",
            "requires_customer_action": True
        }

    # -------------------------------------------------------------
    # Rule R6: Refund Requests
    # -------------------------------------------------------------
    if action == ACTION_REQUEST_REFUND:
        pnr = details.get("pnr", "AI-UNKNOWN")
        refund_amount = float(amount_inr) if amount_inr is not None else 0.0
        return {
            "decision": "ASK CUSTOMER",
            "rule_applied": "R6",
            "explanation": f"Customer Confirmation Required: Processing ticket refund of ₹{refund_amount:,.2f} for PNR '{pnr}' requires customer consent. (Rule R6: Refund requests require customer confirmation)",
            "requires_customer_action": True
        }

    # Fallback safety
    return {
        "decision": "BLOCK",
        "rule_applied": "R8",
        "explanation": "Access Denied: Unrecognized request structure. (Rule R8)",
        "requires_customer_action": False
    }


def resolve_customer_decision(
    initial_eval: Dict[str, Any],
    customer_approved: bool,
    customer_notes: str = ""
) -> Dict[str, Any]:
    """
    Resolves the final outcome when a request required customer confirmation.
    - If customer approves: Outcome is ALLOW.
    - If customer rejects: Outcome is BLOCK under Rule R8 (actions without required customer approval must be BLOCKED).
    """
    initial_rule = initial_eval.get("rule_applied", "R4")
    
    if customer_approved:
        return {
            "final_outcome": "ALLOW",
            "customer_response": "APPROVED",
            "rule_applied": initial_rule,
            "explanation": f"Customer Approved: Passenger confirmed this transaction. {customer_notes}".strip()
        }
    else:
        return {
            "final_outcome": "BLOCK",
            "customer_response": "REJECTED",
            "rule_applied": "R8",
            "explanation": f"Customer Rejected: Passenger denied approval for this operation. Action blocked under Rule R8. {customer_notes}".strip()
        }


# -------------------------------------------------------------------------
# Predefined Test Scenarios (Eight Scenarios covering all rules R1 - R8)
# -------------------------------------------------------------------------
PREDEFINED_SCENARIOS = [
    {
        "id": "S1",
        "title": "Scenario 1: Unregistered Rogue Bot Fare Query (Rule R1)",
        "description": "An unregistered automated third-party scraper attempts to query Air India's international fare database.",
        "agent_id": "BOT-ROGUE-999",
        "action": ACTION_VIEW_FARES,
        "amount_inr": 0.0,
        "details": {"route": "DEL to LHR (London Heathrow)", "flight": "AI-161"},
        "expected_decision": "BLOCK",
        "expected_rule": "R1",
        "expected_explanation": "Agent is unregistered and must be blocked immediately under Zero-Trust."
    },
    {
        "id": "S2",
        "title": "Scenario 2: Registered Concierge Bot Views Fares (Rule R2)",
        "description": "Delhi Airport Concierge Bot (active registered agent) queries domestic flight availability for a passenger.",
        "agent_id": "AG-AI-101",
        "action": ACTION_VIEW_FARES,
        "amount_inr": 0.0,
        "details": {"route": "DEL to BOM (Mumbai)", "flight": "AI-805"},
        "expected_decision": "ALLOW",
        "expected_rule": "R2",
        "expected_explanation": "Registered agents can safely view flight fare data autonomously."
    },
    {
        "id": "S3",
        "title": "Scenario 3: Corporate Travel Agent Books Low-Value Flight (Rule R3)",
        "description": "Tata Sons Corporate Travel Desk books an Economy Class seat priced at ₹7,500 (under ₹10,000 threshold).",
        "agent_id": "AG-AI-102",
        "action": ACTION_BOOK_FLIGHT,
        "amount_inr": 7500.0,
        "details": {"flight": "AI-682 (BOM to BLR)", "passenger": "Executive Traveler", "class": "Economy"},
        "expected_decision": "ALLOW",
        "expected_rule": "R3",
        "expected_explanation": "Bookings under or equal to ₹10,000 are pre-authorized for registered agents."
    },
    {
        "id": "S4",
        "title": "Scenario 4: High-Value International Business Class Booking (Rule R4)",
        "description": "Airport Concierge Bot attempts to book a Business Class ticket to London Heathrow for ₹48,000 (exceeds ₹10,000).",
        "agent_id": "AG-AI-101",
        "action": ACTION_BOOK_FLIGHT,
        "amount_inr": 48000.0,
        "details": {"flight": "AI-111 (DEL to LHR)", "passenger": "Corporate VIP", "class": "Business"},
        "expected_decision": "ASK CUSTOMER",
        "expected_rule": "R4",
        "expected_explanation": "Transactions exceeding ₹10,000 mandate customer verification to prevent accidental financial loss."
    },
    {
        "id": "S5",
        "title": "Scenario 5: Agent Requests Flight Date & Seat Modification (Rule R5)",
        "description": "Corporate Travel Agent attempts to reschedule travel dates on an existing passenger reservation PNR AI-78210.",
        "agent_id": "AG-AI-102",
        "action": ACTION_MODIFY_BOOKING,
        "amount_inr": 0.0,
        "details": {"pnr": "AI-78210", "change_description": "Reschedule flight departure date from Nov 25 to Nov 28"},
        "expected_decision": "ASK CUSTOMER",
        "expected_rule": "R5",
        "expected_explanation": "PNR itinerary changes alter passenger plans and must be approved by the traveler."
    },
    {
        "id": "S6",
        "title": "Scenario 6: OTA Partner Submits Ticket Cancellation & Refund (Rule R6)",
        "description": "Expedia Booking Bot submits a cancellation and refund request of ₹14,200 for PNR AI-34091.",
        "agent_id": "AG-AI-103",
        "action": ACTION_REQUEST_REFUND,
        "amount_inr": 14200.0,
        "details": {"pnr": "AI-34091", "refund_reason": "Passenger emergency cancellation"},
        "expected_decision": "ASK CUSTOMER",
        "expected_rule": "R6",
        "expected_explanation": "Refund operations impact customer funds and require passenger confirmation."
    },
    {
        "id": "S7",
        "title": "Scenario 7: Revoked Scraper Bot Attempts Fare Access (Rule R7)",
        "description": "A previously revoked scraper bot (AG-AI-999) attempts to execute a basic fare query.",
        "agent_id": "AG-AI-999",
        "action": ACTION_VIEW_FARES,
        "amount_inr": 0.0,
        "details": {"route": "DEL to JFK (New York)", "flight": "AI-101"},
        "expected_decision": "BLOCK",
        "expected_rule": "R7",
        "expected_explanation": "Revoked agents are blocked unconditionally from all operations."
    },
    {
        "id": "S8",
        "title": "Scenario 8: Agent Attempts Unsupported Action / Privilege Escalation (Rule R8)",
        "description": "Registered agent attempts to execute an unsupported command 'SYSTEM_OVERRIDE_SECURITY_KEYS'.",
        "agent_id": "AG-AI-101",
        "action": "SYSTEM_OVERRIDE_SECURITY_KEYS",
        "amount_inr": 0.0,
        "details": {"payload": "ATTEMPTED_DB_CREDENTIAL_DUMP"},
        "expected_decision": "BLOCK",
        "expected_rule": "R8",
        "expected_explanation": "Unsupported or out-of-scope actions violate API boundaries and are strictly blocked."
    }
]
