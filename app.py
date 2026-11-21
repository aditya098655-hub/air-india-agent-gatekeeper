"""
Agent Gatekeeper - Air India (MBA Project)
Candidate Enrolment No: PGD202562693
Zero-Trust AI Agent Governance & Access Control Platform
"""

import os
import uuid
import pandas as pd
import streamlit as st
from datetime import datetime

import storage
import gatekeeper_engine as engine

# -----------------------------------------------------------------------------
# Streamlit Page Configuration & Theming
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Agent Gatekeeper | Air India",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS Theme
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles", "air_india_theme.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Ensure persistent data files exist
storage.ensure_data_files()

# Session State Initialization
if "pending_eval" not in st.session_state:
    st.session_state["pending_eval"] = None
if "last_eval_result" not in st.session_state:
    st.session_state["last_eval_result"] = None


# -----------------------------------------------------------------------------
# Global Header Component (Prominently displaying Candidate Enrolment)
# -----------------------------------------------------------------------------
def render_header():
    st.markdown("""
    <div class="enrolment-banner">
        <div>
            <div class="enrolment-title">✈️ AIR INDIA — AGENT GATEKEEPER</div>
            <div class="enrolment-subtitle">Zero-Trust AI Agent Access Control & Governance Framework • MBA Academic Simulation</div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #FFF8E7;">Candidate Enrolment</div>
            <div class="enrolment-badge">PGD202562693</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Sidebar Navigation & System Metadata
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 1rem; border-bottom: 1px solid #E5E7EB;">
    <h2 style="color: #D91424; margin-bottom: 0.2rem; font-weight: 800;">AIR INDIA</h2>
    <span style="background: #D4AF37; color: #111; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 0.75rem;">
        GATEKEEPER PROXY
    </span>
</div>
""", unsafe_allow_html=True)

nav_selection = st.sidebar.radio(
    "Navigation Menu",
    [
        "📊 Dashboard",
        "📝 Agent Registration",
        "⚡ Request Evaluation",
        "🚫 Agent Revocation",
        "📜 Audit Log"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Security Governance Rules")
st.sidebar.markdown("""
- **R1:** Unknown/Unregistered → `BLOCK`
- **R2:** View Fares → `ALLOW`
- **R3:** Booking ≤ ₹10,000 → `ALLOW`
- **R4:** Booking > ₹10,000 → `ASK CUSTOMER`
- **R5:** Modify Booking → `ASK CUSTOMER`
- **R6:** Refund Request → `ASK CUSTOMER`
- **R7:** Revoked Agent → `BLOCK`
- **R8:** Unsupported/Unapproved → `BLOCK`
""")

st.sidebar.markdown("---")
st.sidebar.caption("⚠️ **Notice:** Academic Simulation for Air India. No connection to live operational flight systems.")


# =============================================================================
# 1. SECTION: DASHBOARD
# =============================================================================
if nav_selection == "📊 Dashboard":
    render_header()
    
    agents = storage.load_agents()
    audit_logs = storage.load_audit_logs()
    
    total_agents = len(agents)
    active_agents = len([a for a in agents if a.get("status") == "ACTIVE"])
    revoked_agents = len([a for a in agents if a.get("status") == "REVOKED"])
    
    total_evals = len(audit_logs)
    blocked_count = len([log for log in audit_logs if log.get("final_outcome") == "BLOCK"])
    allowed_count = len([log for log in audit_logs if log.get("final_outcome") == "ALLOW"])
    ask_count = len([log for log in audit_logs if log.get("initial_decision") == "ASK CUSTOMER"])

    # KPI Top Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Active Agents</div>
            <div class="kpi-number" style="color: #10B981;">{active_agents}</div>
            <small style="color: #6B7280;">Out of {total_agents} registered</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #EF4444;">
            <div class="kpi-label">Revoked Agents</div>
            <div class="kpi-number" style="color: #EF4444;">{revoked_agents}</div>
            <small style="color: #6B7280;">Enforcing Rule R7</small>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #D4AF37;">
            <div class="kpi-label">Customer Checkpoints</div>
            <div class="kpi-number" style="color: #B45309;">{ask_count}</div>
            <small style="color: #6B7280;">High-risk requests challenged</small>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #1F2937;">
            <div class="kpi-label">Total Security Audits</div>
            <div class="kpi-number">{total_evals}</div>
            <small style="color: #6B7280;">Logged with system timestamps</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Executive Overview Columns
    col_left, col_right = st.columns([1.4, 1])

    with col_left:
        st.subheader("🛡️ Zero-Trust Security Architecture Overview")
        st.markdown(f"""
        The **Agent Gatekeeper** serves as an intermediary proxy for Air India's autonomous operations.
        As external AI agents, travel aggregators, and enterprise concierge bots seek to execute booking actions, 
        each incoming payload is subjected to strict **Zero-Trust evaluation rules (R1 to R8)**.

        * **Automated Guardrails:** Safe informational queries (fares) and low-value bookings (≤ ₹10,000) are permitted autonomously to maintain high operational throughput.
        * **Human-in-the-Loop (HITL):** Financial expenditures over ₹10,000, PNR itinerary modifications, and refund claims halt for passenger confirmation.
        * **Immediate Kill-Switch:** Revoked agents and unregistered rogue bots are instantly blocked at the gateway.
        """)

        st.info("💡 **Demo Tip:** Navigate to **Request Evaluation** to run the 8 predefined test scenarios covering all governance rules.")

    with col_right:
        st.subheader("📊 Decision Breakdown")
        if total_evals > 0:
            decision_df = pd.DataFrame({
                "Outcome": ["ALLOW", "BLOCK"],
                "Count": [allowed_count, blocked_count]
            })
            st.bar_chart(decision_df.set_index("Outcome"), color="#D91424")
        else:
            st.write("No audit evaluations recorded yet. Run a test scenario to populate.")

    st.markdown("---")
    st.subheader("📋 Recent Audit Feed (Last 5 Events)")
    if audit_logs:
        recent_df = pd.DataFrame(audit_logs[-5:][::-1])
        display_cols = ["timestamp", "agent_id", "action", "initial_decision", "final_outcome", "rule_applied"]
        available_cols = [c for c in display_cols if c in recent_df.columns]
        st.dataframe(recent_df[available_cols], use_container_width=True, hide_index=True)
    else:
        st.caption("No recent transactions found.")


# =============================================================================
# 2. SECTION: AGENT REGISTRATION
# =============================================================================
elif nav_selection == "📝 Agent Registration":
    render_header()
    st.subheader("📝 Register New Autonomous AI Agent")
    st.markdown("Onboard enterprise AI agents into the Air India Gatekeeper registry. Each agent receives a cryptographically safe identifier and a system timestamp.")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        with st.form("agent_reg_form", clear_on_submit=True):
            st.markdown("##### Agent Identification & Credentials")
            agent_name = st.text_input("Agent Display Name *", placeholder="e.g. Bangalore Airport VIP Concierge")
            organization = st.text_input("Operating Organization *", placeholder="e.g. Air India Ground Services / MakeMyTrip")
            role = st.selectbox(
                "Authorized Role *",
                [
                    "Customer Concierge & Assistance",
                    "Corporate Travel Desk Agent",
                    "Third-Party Booking Partner (OTA)",
                    "Flight Status & Baggage Bot",
                    "Loyalty & Frequent Flyer Assistant"
                ]
            )
            
            submitted = st.form_submit_button("🛡️ Onboard Agent to Registry", use_container_width=True)
            if submitted:
                if not agent_name.strip() or not organization.strip():
                    st.error("Please fill in all required fields.")
                else:
                    new_agent = storage.register_agent(agent_name, organization, role)
                    st.success(f"Agent successfully registered! Assigned ID: **{new_agent['agent_id']}** at {new_agent['registered_at']}")

    with col2:
        st.markdown("##### 📌 Registration Policies")
        st.markdown("""
        * **Default Status:** Newly onboarded agents start in **ACTIVE** status.
        * **Identity Precedence:** Requests from unregistered identifiers are blocked under **Rule R1**.
        * **Timestamping:** Real-time system clocks are stamped directly into `data/agents.json`.
        * **Audit Trail:** All future requests by this Agent ID will be tracked against this identity.
        """)

    st.markdown("---")
    st.subheader("🗂️ Current Agent Registry (`agents.json`)")
    all_agents = storage.load_agents()
    if all_agents:
        agents_df = pd.DataFrame(all_agents)
        st.dataframe(
            agents_df[["agent_id", "agent_name", "organization", "role", "status", "registered_at"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Registry is currently empty.")


# =============================================================================
# 3. SECTION: REQUEST EVALUATION (THE SIMULATOR)
# =============================================================================
elif nav_selection == "⚡ Request Evaluation":
    render_header()
    st.subheader("⚡ Zero-Trust Request Evaluation Engine")
    st.markdown("Simulate agent requests against the 8 Air India security rules. You can select pre-built test scenarios or construct custom requests.")

    # Select Mode: Predefined Test Scenarios vs Custom Request
    eval_mode = st.radio(
        "Evaluation Mode:",
        ["🎯 Predefined Test Scenarios (Recommended for Evaluation)", "🛠️ Custom Request Builder"],
        horizontal=True
    )

    all_agents = storage.load_agents()
    agent_options = {f"{a['agent_id']} — {a['agent_name']} ({a['status']})": a['agent_id'] for a in all_agents}
    
    # Defaults
    selected_agent_id = "AG-AI-101"
    selected_action = engine.ACTION_VIEW_FARES
    selected_amount = 0.0
    selected_details = {}
    scenario_meta = None

    if "🎯 Predefined" in eval_mode:
        scenario_titles = [f"{s['id']}: {s['title']}" for s in engine.PREDEFINED_SCENARIOS]
        chosen_sc_index = st.selectbox("Select Test Scenario:", range(len(scenario_titles)), format_func=lambda x: scenario_titles[x])
        scenario_meta = engine.PREDEFINED_SCENARIOS[chosen_sc_index]

        # Display Scenario Card
        st.markdown(f"""
        <div style="background: #F9FAFB; border-left: 4px solid #D91424; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
            <strong style="color: #D91424;">{scenario_meta['title']}</strong><br>
            <span style="color: #374151;">{scenario_meta['description']}</span><br>
            <small style="color: #6B7280;">Target Agent: <code>{scenario_meta['agent_id']}</code> | Action: <code>{scenario_meta['action']}</code> | Expected: <span class="badge-rule">{scenario_meta['expected_rule']}</span> <b>{scenario_meta['expected_decision']}</b></small>
        </div>
        """, unsafe_allow_html=True)

        selected_agent_id = scenario_meta["agent_id"]
        selected_action = scenario_meta["action"]
        selected_amount = float(scenario_meta["amount_inr"])
        selected_details = scenario_meta["details"]

    else:
        # Custom Builder
        colA, colB, colC = st.columns(3)
        with colA:
            agent_choice = st.selectbox("Select Registered Agent (or type custom ID):", ["Custom / Unregistered ID"] + list(agent_options.keys()))
            if agent_choice == "Custom / Unregistered ID":
                selected_agent_id = st.text_input("Enter Agent ID:", value="BOT-UNREGISTERED-888")
            else:
                selected_agent_id = agent_options[agent_choice]

        with colB:
            action_choice = st.selectbox(
                "Requested Action:",
                [
                    engine.ACTION_VIEW_FARES,
                    engine.ACTION_BOOK_FLIGHT,
                    engine.ACTION_MODIFY_BOOKING,
                    engine.ACTION_REQUEST_REFUND,
                    "SYSTEM_OVERRIDE_SECURITY_KEYS (Unsupported)"
                ]
            )
            selected_action = action_choice

        with colC:
            if selected_action in [engine.ACTION_BOOK_FLIGHT, engine.ACTION_REQUEST_REFUND]:
                selected_amount = st.number_input("Transaction Value (₹ INR):", min_value=0.0, max_value=500000.0, value=12500.0, step=500.0)
            else:
                selected_amount = 0.0
                st.text_input("Transaction Value (₹ INR):", value="N/A for this action", disabled=True)

        selected_details = {"notes": "Custom interactive evaluation request"}

    st.markdown("<br>", unsafe_allow_html=True)

    # Trigger Evaluation Button
    if st.button("🚀 Evaluate Request Through Gatekeeper", type="primary", use_container_width=True):
        agent_rec = storage.get_agent_by_id(selected_agent_id)
        eval_result = engine.evaluate_request(
            agent_id=selected_agent_id,
            action=selected_action,
            amount_inr=selected_amount,
            details=selected_details,
            agent_record=agent_rec
        )
        
        request_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"
        agent_name = agent_rec.get("agent_name", "Unregistered External Entity") if agent_rec else "Unregistered Entity"

        # If decision is immediate (ALLOW or BLOCK), log directly to CSV
        if not eval_result["requires_customer_action"]:
            storage.append_audit_log(
                request_id=request_id,
                agent_id=selected_agent_id,
                agent_name=agent_name,
                action=selected_action,
                amount_inr=selected_amount,
                details=str(selected_details),
                initial_decision=eval_result["decision"],
                rule_applied=eval_result["rule_applied"],
                customer_response="N/A",
                final_outcome=eval_result["decision"],
                explanation=eval_result["explanation"]
            )
            st.session_state["pending_eval"] = None
            st.session_state["last_eval_result"] = {
                "request_id": request_id,
                "agent_id": selected_agent_id,
                "agent_name": agent_name,
                "action": selected_action,
                "amount_inr": selected_amount,
                "decision": eval_result["decision"],
                "rule": eval_result["rule_applied"],
                "explanation": eval_result["explanation"],
                "is_pending_customer": False
            }
        else:
            # Requires Customer Confirmation (Human-in-the-Loop)
            st.session_state["pending_eval"] = {
                "request_id": request_id,
                "agent_id": selected_agent_id,
                "agent_name": agent_name,
                "action": selected_action,
                "amount_inr": selected_amount,
                "details": selected_details,
                "initial_eval": eval_result
            }
            st.session_state["last_eval_result"] = None

    # Render Outcome Display
    # Case 1: Pending Customer Confirmation
    if st.session_state.get("pending_eval"):
        pending = st.session_state["pending_eval"]
        init_eval = pending["initial_eval"]

        st.markdown(f"""
        <div class="decision-card-ask">
            <div class="decision-card-header">
                <h3 class="decision-card-title">⚠️ GATEKEEPER DECISION: ASK CUSTOMER</h3>
                <span class="badge-ask">HIGH-IMPACT ACTION</span>
            </div>
            <p class="decision-card-rule">
                <strong>Applicable Rule:</strong> <span class="badge-rule">{init_eval['rule_applied']}</span> — {engine.RULES_INFO[init_eval['rule_applied']]}
            </p>
            <p class="decision-card-reason">
                <strong>Reason:</strong> {init_eval['explanation']}
            </p>
            <div class="decision-card-meta">
                <strong>Request ID:</strong> <code>{pending['request_id']}</code> &nbsp;|&nbsp; 
                <strong>Agent:</strong> {pending['agent_name']} (<code>{pending['agent_id']}</code>) &nbsp;|&nbsp; 
                <strong>Action:</strong> <code>{pending['action']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive Passenger Consent Box
        st.markdown("""
        <div class="customer-approval-box">
            <h4 style="color: #B45309; margin-top: 0;">👤 Air India Passenger Consent Portal (HITL)</h4>
            <p>An autonomous agent is requesting to execute a critical booking or financial operation on your behalf. Please confirm or decline:</p>
        </div>
        """, unsafe_allow_html=True)

        col_app, col_rej = st.columns(2)
        with col_app:
            if st.button("✅ Approve Action as Passenger", use_container_width=True, type="primary"):
                resolved = engine.resolve_customer_decision(init_eval, customer_approved=True)
                storage.append_audit_log(
                    request_id=pending["request_id"],
                    agent_id=pending["agent_id"],
                    agent_name=pending["agent_name"],
                    action=pending["action"],
                    amount_inr=pending["amount_inr"],
                    details=str(pending["details"]),
                    initial_decision=init_eval["decision"],
                    rule_applied=resolved["rule_applied"],
                    customer_response=resolved["customer_response"],
                    final_outcome=resolved["final_outcome"],
                    explanation=resolved["explanation"]
                )
                st.session_state["last_eval_result"] = {
                    "request_id": pending["request_id"],
                    "agent_id": pending["agent_id"],
                    "agent_name": pending["agent_name"],
                    "action": pending["action"],
                    "amount_inr": pending["amount_inr"],
                    "decision": resolved["final_outcome"],
                    "rule": resolved["rule_applied"],
                    "explanation": resolved["explanation"],
                    "is_pending_customer": False
                }
                st.session_state["pending_eval"] = None
                st.rerun()

        with col_rej:
            if st.button("❌ Reject Action as Passenger", use_container_width=True):
                resolved = engine.resolve_customer_decision(init_eval, customer_approved=False)
                storage.append_audit_log(
                    request_id=pending["request_id"],
                    agent_id=pending["agent_id"],
                    agent_name=pending["agent_name"],
                    action=pending["action"],
                    amount_inr=pending["amount_inr"],
                    details=str(pending["details"]),
                    initial_decision=init_eval["decision"],
                    rule_applied=resolved["rule_applied"],
                    customer_response=resolved["customer_response"],
                    final_outcome=resolved["final_outcome"],
                    explanation=resolved["explanation"]
                )
                st.session_state["last_eval_result"] = {
                    "request_id": pending["request_id"],
                    "agent_id": pending["agent_id"],
                    "agent_name": pending["agent_name"],
                    "action": pending["action"],
                    "amount_inr": pending["amount_inr"],
                    "decision": resolved["final_outcome"],
                    "rule": resolved["rule_applied"],
                    "explanation": resolved["explanation"],
                    "is_pending_customer": False
                }
                st.session_state["pending_eval"] = None
                st.rerun()

    # Case 2: Render Completed Evaluation Card
    elif st.session_state.get("last_eval_result"):
        res = st.session_state["last_eval_result"]
        dec = res["decision"]
        card_class = "decision-card-allow" if dec == "ALLOW" else "decision-card-block"
        badge_class = "badge-allow" if dec == "ALLOW" else "badge-block"
        icon = "✅" if dec == "ALLOW" else "🚫"

        st.markdown(f"""
        <div class="{card_class}">
            <div class="decision-card-header">
                <h3 class="decision-card-title">{icon} GATEKEEPER VERDICT: {dec}</h3>
                <span class="{badge_class}">{dec}</span>
            </div>
            <p class="decision-card-rule">
                <strong>Applicable Rule:</strong> <span class="badge-rule">{res['rule']}</span> — {engine.RULES_INFO.get(res['rule'], 'Custom Security Rule')}
            </p>
            <p class="decision-card-reason">
                <strong>Business Justification:</strong> {res['explanation']}
            </p>
            <div class="decision-card-meta">
                <strong>Request ID:</strong> <code>{res['request_id']}</code> &nbsp;|&nbsp; 
                <strong>Agent:</strong> {res['agent_name']} (<code>{res['agent_id']}</code>) &nbsp;|&nbsp; 
                <strong>Action:</strong> <code>{res['action']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================================================
# 4. SECTION: AGENT REVOCATION
# =============================================================================
elif nav_selection == "🚫 Agent Revocation":
    render_header()
    st.subheader("🚫 Agent Revocation & Credential Kill-Switch")
    st.markdown("Instantly revoke agent permissions to prevent rogue or compromised bots from executing actions. Revoked agents are blocked unconditionally under **Rule R7**.")

    agents = storage.load_agents()
    active_agents = [a for a in agents if a.get("status") == "ACTIVE"]

    col1, col2 = st.columns([1.2, 1])

    with col1:
        if active_agents:
            active_options = {f"{a['agent_id']} — {a['agent_name']} ({a['organization']})": a['agent_id'] for a in active_agents}
            selected_choice = st.selectbox("Select Active Agent to Revoke:", list(active_options.keys()))
            target_id = active_options[selected_choice]

            revocation_reason = st.text_area(
                "Revocation Justification *",
                placeholder="e.g. Unusual traffic anomaly detected / Partner contract terminated / API rate limit violation",
                height=100
            )

            if st.button("🚨 Revoke Agent Credentials Immediately", type="primary", use_container_width=True):
                if not revocation_reason.strip():
                    st.error("A valid revocation justification is required for regulatory audit.")
                else:
                    success = storage.revoke_agent(target_id, revocation_reason)
                    if success:
                        st.success(f"Agent {target_id} has been revoked successfully. Rule R7 is now active for this agent.")
                        st.rerun()
                    else:
                        st.error("Failed to revoke agent.")
        else:
            st.info("No active agents found in the registry.")

    with col2:
        st.markdown("##### ⚖️ Rule R7 Governance Enforcement")
        st.markdown("""
        * **Immediate Effect:** Revocation is instantaneous.
        * **Zero-Tolerance:** A revoked agent cannot perform ANY action (not even harmless fare viewing).
        * **Immutable Audit:** The exact timestamp (`datetime.now()`) and business reason are permanently saved.
        * **Demo Test:** After revoking an agent here, go to **Request Evaluation** and attempt a query with it. It will trigger an immediate **BLOCK (R7)**.
        """)

    st.markdown("---")
    st.subheader("📋 Revoked Agents Directory")
    revoked_list = [a for a in agents if a.get("status") == "REVOKED"]
    if revoked_list:
        rev_df = pd.DataFrame(revoked_list)
        st.dataframe(
            rev_df[["agent_id", "agent_name", "revoked_at", "revocation_reason"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.caption("No revoked agents currently.")


# =============================================================================
# 5. SECTION: AUDIT LOG & COMPLIANCE
# =============================================================================
elif nav_selection == "📜 Audit Log":
    render_header()
    st.subheader("📜 Real-Time Security Audit & Governance Log")
    st.markdown("Comprehensive, append-only audit trail stored in `data/audit_log.csv`. Every decision, timestamp, and customer interaction is recorded.")

    raw_logs = storage.load_audit_logs()

    if raw_logs:
        df_logs = pd.DataFrame(raw_logs)

        # Filter bar
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            decision_filter = st.multiselect("Filter by Final Outcome:", ["ALLOW", "BLOCK"], default=["ALLOW", "BLOCK"])
        with col_f2:
            all_rules = sorted(list(set(df_logs["rule_applied"].dropna().tolist())))
            rule_filter = st.multiselect("Filter by Rule Applied:", all_rules, default=all_rules)
        with col_f3:
            search_query = st.text_input("Search Agent ID / Request ID:", placeholder="e.g. AG-AI-101")

        # Apply Filters
        filtered_df = df_logs.copy()
        if decision_filter:
            filtered_df = filtered_df[filtered_df["final_outcome"].isin(decision_filter)]
        if rule_filter:
            filtered_df = filtered_df[filtered_df["rule_applied"].isin(rule_filter)]
        if search_query.strip():
            q = search_query.strip().lower()
            filtered_df = filtered_df[
                filtered_df["agent_id"].str.lower().str.contains(q) |
                filtered_df["request_id"].str.lower().str.contains(q) |
                filtered_df["agent_name"].str.lower().str.contains(q)
            ]

        # Display Stats
        st.caption(f"Displaying **{len(filtered_df)}** of **{len(df_logs)}** total records.")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

        # Export Button
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Audit Log (CSV)",
            data=csv_data,
            file_name=f"air_india_gatekeeper_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("The audit log is currently empty. Run test scenarios in the 'Request Evaluation' tab to generate records.")
