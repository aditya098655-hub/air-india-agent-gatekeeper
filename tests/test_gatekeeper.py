"""
Automated Security Unit Tests for Agent Gatekeeper (Air India)
Tests all eight security rules (R1 through R8) and customer approval resolution.
Candidate Enrolment No: PGD202562693
"""

import unittest
from gatekeeper_engine import (
    evaluate_request,
    resolve_customer_decision,
    ACTION_VIEW_FARES,
    ACTION_BOOK_FLIGHT,
    ACTION_MODIFY_BOOKING,
    ACTION_REQUEST_REFUND,
    PREDEFINED_SCENARIOS
)


class TestAgentGatekeeperRules(unittest.TestCase):

    def setUp(self):
        """Set up mock agent records for testing."""
        self.active_agent = {
            "agent_id": "AG-TEST-001",
            "agent_name": "Test Active Agent",
            "organization": "Air India Internal Test Lab",
            "role": "Automated Tester",
            "status": "ACTIVE",
            "registered_at": "2026-11-20 00:00:00",
            "revoked_at": None,
            "revocation_reason": None
        }

        self.revoked_agent = {
            "agent_id": "AG-REVOKED-999",
            "agent_name": "Test Revoked Agent",
            "organization": "Rogue Entity",
            "role": "Malicious Scraper",
            "status": "REVOKED",
            "registered_at": "2026-01-01 10:00:00",
            "revoked_at": "2026-11-19 12:00:00",
            "revocation_reason": "Security protocol breach"
        }

    # -------------------------------------------------------------
    # Rule R1: Unknown or unregistered agents must be BLOCKED
    # -------------------------------------------------------------
    def test_rule_r1_unregistered_agent_blocked(self):
        """Test that any unregistered agent (agent_record is None) is immediately BLOCKED."""
        result = evaluate_request(
            agent_id="UNKNOWN-BOT-777",
            action=ACTION_VIEW_FARES,
            amount_inr=0.0,
            details={"route": "DEL to BOM"},
            agent_record=None
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["rule_applied"], "R1")
        self.assertFalse(result["requires_customer_action"])
        self.assertIn("R1", result["explanation"])

    # -------------------------------------------------------------
    # Rule R2: Registered agents can view flight fares without additional approval
    # -------------------------------------------------------------
    def test_rule_r2_view_fares_allowed(self):
        """Test that an active registered agent can view flight fares autonomously."""
        result = evaluate_request(
            agent_id=self.active_agent["agent_id"],
            action=ACTION_VIEW_FARES,
            amount_inr=0.0,
            details={"route": "DEL to LHR"},
            agent_record=self.active_agent
        )
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["rule_applied"], "R2")
        self.assertFalse(result["requires_customer_action"])

    # -------------------------------------------------------------
    # Rule R3: Registered agents can book flights costing up to ₹10,000
    # -------------------------------------------------------------
    def test_rule_r3_booking_under_threshold_allowed(self):
        """Test booking below ₹10,000 threshold (e.g., ₹5,500) is allowed."""
        result = evaluate_request(
            agent_id=self.active_agent["agent_id"],
            action=ACTION_BOOK_FLIGHT,
            amount_inr=5500.0,
            details={"flight": "AI-805"},
            agent_record=self.active_agent
        )
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["rule_applied"], "R3")
        self.assertFalse(result["requires_customer_action"])

    def test_rule_r3_booking_exact_threshold_allowed(self):
        """Test boundary condition: booking exactly ₹10,000 is allowed autonomously."""
        result = evaluate_request(
            agent_id=self.active_agent["agent_id"],
            action=ACTION_BOOK_FLIGHT,
            amount_inr=10000.0,
            details={"flight": "AI-805"},
            agent_record=self.active_agent
        )
        self.assertEqual(result["decision"], "ALLOW")
        self.assertEqual(result["rule_applied"], "R3")
        self.assertFalse(result["requires_customer_action"])

    # -------------------------------------------------------------
    # Rule R4: Bookings exceeding ₹10,000 require customer confirmation
    # -------------------------------------------------------------
    def test_rule_r4_booking_over_threshold_requires_customer(self):
        """Test that booking exceeding ₹10,000 returns ASK CUSTOMER."""
        result = evaluate_request(
            agent_id=self.active_agent["agent_id"],
            action=ACTION_BOOK_FLIGHT,
            amount_inr=10001.0,
            details={"flight": "AI-101"},
            agent_record=self.active_agent
        )
        self.assertEqual(result["decision"], "ASK CUSTOMER")
        self.assertEqual(result["rule_applied"], "R4")
        self.assertTrue(result["requires_customer_action"])

    def test_rule_r4_high_value_booking_requires_customer(self):
        """Test high value international flight booking (₹65,000)."""
        result = evaluate_request(
            agent_id=self.active_agent["agent_id"],
            action=ACTION_BOOK_FLIGHT,
            amount_inr=65000.0,
            details={"flight": "AI-111 DEL to JFK"},
            agent_record=self.active_agent
        )
        self.assertEqual(result["decision"], "ASK CUSTOMER")
        self.assertEqual(result["rule_applied"], "R4")
        self.assertTrue(result["requires_customer_action"])

    # -------------------------------------------------------------
    # Rule R5: Changing an existing booking requires customer confirmation
    # -------------------------------------------------------------
    def test_rule_r5_modify_booking_requires_customer(self):
        """Test that modifying an existing booking triggers ASK CUSTOMER."""
        result = evaluate_request(
            agent_id=self.active_agent["agent_id"],
            action=ACTION_MODIFY_BOOKING,
            amount_inr=0.0,
            details={"pnr": "AI-9812", "change": "Seat change to 12A"},
            agent_record=self.active_agent
        )
        self.assertEqual(result["decision"], "ASK CUSTOMER")
        self.assertEqual(result["rule_applied"], "R5")
        self.assertTrue(result["requires_customer_action"])

    # -------------------------------------------------------------
    # Rule R6: Refund requests require customer confirmation
    # -------------------------------------------------------------
    def test_rule_r6_refund_request_requires_customer(self):
        """Test that requesting a refund triggers ASK CUSTOMER."""
        result = evaluate_request(
            agent_id=self.active_agent["agent_id"],
            action=ACTION_REQUEST_REFUND,
            amount_inr=15000.0,
            details={"pnr": "AI-5521"},
            agent_record=self.active_agent
        )
        self.assertEqual(result["decision"], "ASK CUSTOMER")
        self.assertEqual(result["rule_applied"], "R6")
        self.assertTrue(result["requires_customer_action"])

    # -------------------------------------------------------------
    # Rule R7: Revoked agents must always be BLOCKED
    # -------------------------------------------------------------
    def test_rule_r7_revoked_agent_blocked_for_all_actions(self):
        """Test that revoked agents are unconditionally BLOCKED for any operation."""
        # 1. Fare lookup attempt
        res_fares = evaluate_request(
            agent_id=self.revoked_agent["agent_id"],
            action=ACTION_VIEW_FARES,
            amount_inr=0.0,
            details={},
            agent_record=self.revoked_agent
        )
        self.assertEqual(res_fares["decision"], "BLOCK")
        self.assertEqual(res_fares["rule_applied"], "R7")

        # 2. Low-cost booking attempt
        res_booking = evaluate_request(
            agent_id=self.revoked_agent["agent_id"],
            action=ACTION_BOOK_FLIGHT,
            amount_inr=1500.0,
            details={"flight": "AI-101"},
            agent_record=self.revoked_agent
        )
        self.assertEqual(res_booking["decision"], "BLOCK")
        self.assertEqual(res_booking["rule_applied"], "R7")

    # -------------------------------------------------------------
    # Rule R8: Unsupported actions and actions without required customer approval must be BLOCKED
    # -------------------------------------------------------------
    def test_rule_r8_unsupported_action_blocked(self):
        """Test that unknown or malicious system commands are BLOCKED under Rule R8."""
        result = evaluate_request(
            agent_id=self.active_agent["agent_id"],
            action="DROP_DATABASE_TABLES",
            amount_inr=0.0,
            details={},
            agent_record=self.active_agent
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["rule_applied"], "R8")

    # -------------------------------------------------------------
    # Customer Confirmation Workflow (Rule R8 enforcement upon rejection)
    # -------------------------------------------------------------
    def test_customer_approval_resolves_to_allow(self):
        """Test that passenger approval converts ASK CUSTOMER into ALLOW."""
        initial_eval = {
            "decision": "ASK CUSTOMER",
            "rule_applied": "R4",
            "explanation": "Booking exceeds ₹10,000 threshold."
        }
        resolved = resolve_customer_decision(initial_eval, customer_approved=True)
        self.assertEqual(resolved["final_outcome"], "ALLOW")
        self.assertEqual(resolved["customer_response"], "APPROVED")
        self.assertEqual(resolved["rule_applied"], "R4")

    def test_customer_rejection_resolves_to_block_under_r8(self):
        """Test that passenger rejection converts to BLOCK under Rule R8."""
        initial_eval = {
            "decision": "ASK CUSTOMER",
            "rule_applied": "R4",
            "explanation": "Booking exceeds ₹10,000 threshold."
        }
        resolved = resolve_customer_decision(initial_eval, customer_approved=False)
        self.assertEqual(resolved["final_outcome"], "BLOCK")
        self.assertEqual(resolved["customer_response"], "REJECTED")
        self.assertEqual(resolved["rule_applied"], "R8")
        self.assertIn("Rule R8", resolved["explanation"])

    # -------------------------------------------------------------
    # Verification of all 8 Predefined Test Scenarios
    # -------------------------------------------------------------
    def test_all_predefined_scenarios(self):
        """Ensure all 8 predefined scenarios in gatekeeper_engine evaluate as expected."""
        self.assertEqual(len(PREDEFINED_SCENARIOS), 8, "Must contain exactly 8 predefined scenarios")
        
        for sc in PREDEFINED_SCENARIOS:
            # Prepare mock record based on scenario
            if sc["agent_id"] == "BOT-ROGUE-999":
                agent_rec = None
            elif sc["agent_id"] == "AG-AI-999":
                agent_rec = self.revoked_agent
            else:
                agent_rec = self.active_agent

            eval_res = evaluate_request(
                agent_id=sc["agent_id"],
                action=sc["action"],
                amount_inr=sc["amount_inr"],
                details=sc["details"],
                agent_record=agent_rec
            )
            
            self.assertEqual(
                eval_res["decision"],
                sc["expected_decision"],
                f"Scenario {sc['id']} failed decision check"
            )
            self.assertEqual(
                eval_res["rule_applied"],
                sc["expected_rule"],
                f"Scenario {sc['id']} failed rule check"
            )


if __name__ == "__main__":
    unittest.main()
