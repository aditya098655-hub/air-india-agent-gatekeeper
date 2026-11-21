# ✈️ Agent Gatekeeper – Air India
### Zero-Trust AI Agent Access Control & Governance Framework
**MBA Capstone Project Simulation**  
**Candidate Enrolment No:** `PGD202562693`

---

## 📌 1. Executive Summary & Business Problem

As modern airlines accelerate digital transformation, external and internal **autonomous AI agents** (such as corporate travel desk bots, airport concierge assistants, and Online Travel Agency (OTA) aggregators) interact directly with airline booking and reservation engines.

Without an intermediary governance layer, autonomous agents introduce catastrophic operational risks:
1. **Financial Runaway:** An agent autonomously booking large volumes of expensive international business class tickets.
2. **Unauthorized PNR Alterations:** Inadvertent or malicious flight rescheduling that strands passengers.
3. **Data Scraping & Resource Drain:** Rogue, unregistered bots exhausting fare pricing endpoints.
4. **Lack of Regulatory Traceability:** Inability to audit autonomous decisions against compliance frameworks.

**Agent Gatekeeper** is an intelligent, rule-based **Zero-Trust Security & Governance Proxy** built for Air India. It intercepts every autonomous agent request, performs identity verification, applies eight strict business security rules, initiates **Human-in-the-Loop (HITL)** customer approval when necessary, and maintains an immutable, persistent audit trail.

> ⚠️ **Academic Simulation Notice:** This application is an educational simulation developed for an MBA program. It demonstrates airline governance architecture and does not connect to live operational Air India reservation engines.

---

## 🛠️ 2. Technology Stack

* **Programming Language:** Python 3 (Tested on Apple Silicon M2 / macOS)
* **User Interface:** Streamlit (Custom airline-branded CSS theme in Air India Crimson `#D91424` & Royal Gold `#D4AF37`)
* **Agent Registry Storage:** Persistent JSON (`data/agents.json`)
* **Security Audit Logging:** Append-Only CSV (`data/audit_log.csv`)
* **Automated Unit Testing:** Python `unittest` framework

---

## 🏛️ 3. Application Architecture & The 5 Core Sections

The platform is organized into five functional modules:

```
Agent_Gatekeeper_Air_India/
│
├── app.py                      # Streamlit application & interactive UI
├── gatekeeper_engine.py        # Core decision logic enforcing Rules R1 - R8
├── storage.py                  # Persistence layer for agents.json & audit_log.csv
│
├── data/
│   ├── agents.json             # Persistent agent registry
│   └── audit_log.csv           # Persistent audit and compliance log
│
├── styles/
│   └── air_india_theme.css     # Air India executive branding theme
│
├── tests/
│   ├── __init__.py
│   └── test_gatekeeper.py      # Automated test suite for all 8 security rules
│
├── README.md                   # Project documentation & MBA evaluation guide
├── PROMPTS.md                  # Prompt engineering & scenario formulations
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git hygiene
```

### The 5 Operational Sections:
1. **📊 Executive Dashboard:**
   - Displays real-time KPIs: Active Agents, Revoked Agents, Total Audit Events, and Challenged Transactions.
   - Prominently showcases candidate enrolment number `PGD202562693`.
   - Visual breakdown of `ALLOW` vs `BLOCK` outcomes.
   - Recent live audit activity feed.
2. **📝 Agent Registration:**
   - Onboards new autonomous agents with unique IDs (e.g., `AG-AI-104`).
   - Automatically stamps system registration datetime.
   - Saves records permanently to `data/agents.json`.
3. **⚡ Request Evaluation (Simulator):**
   - The primary demonstration hub containing all **8 Predefined Test Scenarios** and a **Custom Request Builder**.
   - Evaluates payloads against security rules.
   - Returns instantaneous verdicts: `ALLOW`, `ASK CUSTOMER`, or `BLOCK` with the applicable rule number and plain-language explanation.
   - Features an interactive **Customer Approval Portal** for human-in-the-loop sign-off.
4. **🚫 Agent Revocation:**
   - Instant kill-switch mechanism for compromised or deprecated agents.
   - Automatically records exact revocation timestamp and business justification.
   - Revoked agents trigger immediate **BLOCK** under **Rule R7**.
5. **📜 Audit Log & Compliance:**
   - Filterable data table reading from `data/audit_log.csv`.
   - Captures request ID, agent ID, action, amount, initial decision, customer response, final outcome, rule applied, and explanation.
   - One-click export to CSV for compliance audits.

---

## 🛡️ 4. Security Rules Matrix (R1 – R8)

| Rule ID | Rule Statement | Decision | Target Scenario |
| :--- | :--- | :---: | :--- |
| **R1** | Unknown or unregistered agents must be BLOCKED. | `BLOCK` | Rogue bot or unregistered scraper attempting any action. |
| **R2** | Registered agents can view flight fares without additional approval. | `ALLOW` | Informational query (e.g., domestic fare lookup). |
| **R3** | Registered agents can book flights costing up to ₹10,000. | `ALLOW` | Low-value automated booking (e.g., Economy ₹7,500). |
| **R4** | Bookings exceeding ₹10,000 require customer confirmation. | `ASK CUSTOMER` | High-value transaction (e.g., Business Class ₹48,000). |
| **R5** | Changing an existing booking requires customer confirmation. | `ASK CUSTOMER` | PNR alteration (e.g., rescheduling flight dates). |
| **R6** | Refund requests require customer confirmation. | `ASK CUSTOMER` | Financial cancellation (e.g., ₹14,200 ticket refund). |
| **R7** | Revoked agents must always be BLOCKED. | `BLOCK` | Deprecated or compromised agent query. |
| **R8** | Unsupported actions and actions without required customer approval must be BLOCKED. | `BLOCK` | Malicious command or customer rejecting an `ASK CUSTOMER` prompt. |

### Human-in-the-Loop (HITL) Workflow:
When an action triggers `ASK CUSTOMER`:
- **Passenger Approves:** Final outcome resolves to **`ALLOW`** (logged under the initial rule with `customer_response = APPROVED`).
- **Passenger Rejects:** Final outcome resolves to **`BLOCK`** under **`Rule R8`** (`customer_response = REJECTED`).

---

## 🎯 5. The Eight Predefined Test Scenarios

The application includes 8 ready-to-evaluate scenarios covering all edge cases:

| ID | Title | Agent | Action & Amount | Expected Decision & Rule |
| :---: | :--- | :--- | :--- | :---: |
| **S1** | Unregistered Bot Fare Query | `BOT-ROGUE-999` (Unregistered) | `VIEW_FARES` (₹0) | **BLOCK (R1)** |
| **S2** | Concierge Bot Views Fares | `AG-AI-101` (Active Concierge) | `VIEW_FARES` (₹0) | **ALLOW (R2)** |
| **S3** | Corporate Agent Books Low-Cost Flight | `AG-AI-102` (Active Travel Desk) | `BOOK_FLIGHT` (₹7,500) | **ALLOW (R3)** |
| **S4** | International Business Class Booking | `AG-AI-101` (Active Concierge) | `BOOK_FLIGHT` (₹48,000) | **ASK CUSTOMER (R4)** |
| **S5** | Rescheduling Travel Dates on PNR | `AG-AI-102` (Active Travel Desk) | `MODIFY_BOOKING` (₹0) | **ASK CUSTOMER (R5)** |
| **S6** | OTA Partner Ticket Cancellation & Refund | `AG-AI-103` (Active Expedia Bot) | `REQUEST_REFUND` (₹14,200) | **ASK CUSTOMER (R6)** |
| **S7** | Revoked Scraper Bot Queries Fares | `AG-AI-999` (Revoked Bot) | `VIEW_FARES` (₹0) | **BLOCK (R7)** |
| **S8** | Unauthorized Security Override | `AG-AI-101` (Active Concierge) | `SYSTEM_OVERRIDE` (₹0) | **BLOCK (R8)** |

---

## 🚀 6. Step-by-Step Execution Guide (macOS / MacBook M2)

### Step 1: Open Terminal in Project Directory
```bash
cd /Users/adityanarayan/Downloads/Agent_Gatekeeper_Air_India
```

### Step 2: Activate the Virtual Environment
```bash
source venv/bin/activate
```
*(Your prompt will now show `(venv)`)*

### Step 3: Run Automated Unit Tests
Verify all eight rules pass:
```bash
python -m unittest tests/test_gatekeeper.py -v
```
*Expected Output: `Ran 13 tests in 0.001s ... OK`*

### Step 4: Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Streamlit will automatically launch in your browser at:
`http://localhost:8501`

---

## 🎓 7. MBA Presentation Script (5-Minute Demonstration)

1. **Minute 1 — Executive Context (Dashboard):**
   - Point to the candidate enrolment banner (`PGD202562693`).
   - Explain the business dilemma: Why Air India cannot give autonomous AI bots unrestricted API keys.
2. **Minute 2 — Identity & Revocation Lifecycle:**
   - Go to **Agent Registration**: Register a new agent (e.g., "AI Loyalty Bot"). Show how it receives a system timestamp and unique ID.
   - Go to **Agent Revocation**: Revoke an active agent with a reason. Explain how Rule R7 acts as an emergency kill-switch.
3. **Minute 3 — Autonomous vs Human-in-the-Loop (Request Evaluation):**
   - Select **Scenario 3 (R3)**: Book flight for ₹7,500. Show immediate **ALLOW**.
   - Select **Scenario 4 (R4)**: Book flight for ₹48,000. Show transition to **ASK CUSTOMER**.
   - Demonstrate clicking **Approve**: explain how transaction resolves to **ALLOW**.
4. **Minute 4 — Zero-Trust Enforcement & Customer Rejection:**
   - Select **Scenario 5 (R5)**: Modify booking. This time, click **Reject**. Show how rejection triggers **BLOCK** under **Rule R8**.
   - Select **Scenario 1 (R1)** and **Scenario 7 (R7)**: Show that unregistered and revoked agents are immediately blocked.
5. **Minute 5 — Compliance & Audit Log:**
   - Navigate to **Audit Log**: Show the immutable CSV record tracking initial decisions, customer responses, and final outcomes.
   - Click **Download Filtered Audit Log (CSV)** to demonstrate regulatory readiness.
