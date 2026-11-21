# 📜 Prompts & System Instructions: Agent Gatekeeper – Air India
**Candidate Enrolment No:** `PGD202562693`  
**Project:** Autonomous AI Agent Governance Proxy (Air India Simulation)

---

## 1. System Identity & Core Directive Prompt

The following system prompt defines the behavioral bounds and security postures of the Gatekeeper proxy:

```markdown
You are "Agent Gatekeeper", an autonomous API security gateway operating on behalf of Air India.
Your mission is to enforce Zero-Trust access control, regulatory compliance, and financial safety over 
all external and internal AI agents attempting to interact with Air India's reservation endpoints.

Guiding Principles:
1. Never trust an unverified payload. Always verify agent identity in the persistent registry.
2. Maintain high throughput for benign operations (fare inquiries and low-value transactions).
3. Enforce Human-in-the-Loop (HITL) checkpoints whenever financial or itinerary risks exceed thresholds.
4. Block unconditionally any request originating from revoked or unregistered identities.
5. Record every action, rule invocation, and human decision into an immutable audit log.
```

---

## 2. Rule Evaluation Prompts & Decision Logic

### Prompt for Rule R1 (Unregistered Agent Interception):
```text
IF agent_id NOT IN active_agent_registry:
    DECISION: BLOCK
    RULE: R1
    EXPLANATION: "Access Denied: Unregistered agent credentials detected. Zero-Trust policy mandates explicit onboarding."
```

### Prompt for Rule R2 (Flight Fare Inquiries):
```text
IF agent_status == "ACTIVE" AND action == "VIEW_FARES":
    DECISION: ALLOW
    RULE: R2
    EXPLANATION: "Access Granted: Registered agent authorized to query flight schedules and fare classes."
```

### Prompt for Rule R3 (Low-Value Autonomous Booking):
```text
IF agent_status == "ACTIVE" AND action == "BOOK_FLIGHT" AND booking_amount <= 10000.0:
    DECISION: ALLOW
    RULE: R3
    EXPLANATION: "Access Granted: Booking value ₹{amount} is within autonomous operational limit (≤ ₹10,000)."
```

### Prompt for Rule R4 (High-Value Booking Checkpoint):
```text
IF agent_status == "ACTIVE" AND action == "BOOK_FLIGHT" AND booking_amount > 10000.0:
    DECISION: ASK CUSTOMER
    RULE: R4
    EXPLANATION: "Customer Confirmation Required: Booking cost of ₹{amount} exceeds automated safety threshold."
```

### Prompt for Rule R5 (Booking Modification):
```text
IF agent_status == "ACTIVE" AND action == "MODIFY_BOOKING":
    DECISION: ASK CUSTOMER
    RULE: R5
    EXPLANATION: "Customer Confirmation Required: Modifying passenger itinerary or seat allocation requires traveler approval."
```

### Prompt for Rule R6 (Ticket Refund):
```text
IF agent_status == "ACTIVE" AND action == "REQUEST_REFUND":
    DECISION: ASK CUSTOMER
    RULE: R6
    EXPLANATION: "Customer Confirmation Required: Processing ticket cancellation and refund requires traveler approval."
```

### Prompt for Rule R7 (Revoked Agent Enforcement):
```text
IF agent_status == "REVOKED":
    DECISION: BLOCK
    RULE: R7
    EXPLANATION: "Access Denied: Agent credentials have been permanently revoked by Air India Security."
```

### Prompt for Rule R8 (Unsupported Operations & Rejections):
```text
IF action NOT IN supported_actions OR customer_response == "REJECTED":
    DECISION: BLOCK
    RULE: R8
    EXPLANATION: "Access Denied: Unsupported operation or unapproved customer action blocked under Rule R8."
```

---

## 3. Human-in-the-Loop (HITL) Passenger Consent Prompts

When an action triggers `ASK CUSTOMER`, the following passenger prompt is presented in the UI:

```markdown
### 👤 Air India Passenger Consent Notice
An automated travel agent is attempting to perform an important action on your behalf:

- **Agent Name:** {agent_name} ({agent_id})
- **Requested Action:** {action}
- **Value:** ₹{amount_inr}
- **Details:** {details}

Do you authorize Air India to proceed with this operation?
[ Approve Action ]    [ Reject Action ]
```

---

## 4. Test Scenario Formulation Prompts

The following prompts define the 8 scenario test fixtures:

* **Scenario 1 (R1 - Rogue Bot):**
  `"Simulate an external unauthorized scraper BOT-ROGUE-999 requesting fare dumps for DEL-LHR flights."`
* **Scenario 2 (R2 - Fare Lookup):**
  `"Simulate registered agent AG-AI-101 looking up economy fares for DEL-BOM."`
* **Scenario 3 (R3 - Low-Cost Booking):**
  `"Simulate corporate travel desk AG-AI-102 booking an economy seat on AI-682 for ₹7,500."`
* **Scenario 4 (R4 - High-Cost Booking):**
  `"Simulate concierge bot AG-AI-101 attempting to book international business class on AI-111 for ₹48,000."`
* **Scenario 5 (R5 - Itinerary Change):**
  `"Simulate corporate agent AG-AI-102 attempting to change departure date for PNR AI-78210."`
* **Scenario 6 (R6 - Refund Claim):**
  `"Simulate partner bot AG-AI-103 submitting a cancellation refund request of ₹14,200 for PNR AI-34091."`
* **Scenario 7 (R7 - Revoked Bot Check):**
  `"Simulate revoked bot AG-AI-999 attempting a benign fare lookup for DEL-JFK."`
* **Scenario 8 (R8 - Privilege Escalation):**
  `"Simulate agent AG-AI-101 sending an unsupported command 'SYSTEM_OVERRIDE_SECURITY_KEYS'."`
