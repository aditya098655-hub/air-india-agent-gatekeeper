"""
Storage Module for Agent Gatekeeper (Air India)
Handles persistence for:
1. Agent registry (JSON file: data/agents.json)
2. Security audit log (CSV file: data/audit_log.csv)
"""

import os
import json
import csv
from datetime import datetime
from typing import List, Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
AGENTS_FILE = os.path.join(DATA_DIR, "agents.json")
AUDIT_LOG_FILE = os.path.join(DATA_DIR, "audit_log.csv")

AUDIT_CSV_HEADERS = [
    "timestamp",
    "request_id",
    "agent_id",
    "agent_name",
    "action",
    "amount_inr",
    "details",
    "initial_decision",
    "rule_applied",
    "customer_response",
    "final_outcome",
    "explanation"
]


def ensure_data_files():
    """Ensure data directory and persistent files exist with initial records."""
    os.makedirs(DATA_DIR, exist_ok=True)

    # Initialize agents.json with initial benchmark agents if not present
    if not os.path.exists(AGENTS_FILE):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        initial_agents = [
            {
                "agent_id": "AG-AI-101",
                "agent_name": "Delhi Airport Concierge Bot",
                "organization": "Air India Airport Operations",
                "role": "Customer Concierge & Assistance",
                "registered_at": current_time,
                "status": "ACTIVE",
                "revoked_at": None,
                "revocation_reason": None
            },
            {
                "agent_id": "AG-AI-102",
                "agent_name": "Corporate Travel Desk Agent",
                "organization": "Tata Sons Enterprise Travel",
                "role": "Corporate Booking Agent",
                "registered_at": current_time,
                "status": "ACTIVE",
                "revoked_at": None,
                "revocation_reason": None
            },
            {
                "agent_id": "AG-AI-103",
                "agent_name": "OTA Booking Partner (Expedia Bot)",
                "organization": "Expedia Group India",
                "role": "Third-Party Booking Partner",
                "registered_at": current_time,
                "status": "ACTIVE",
                "revoked_at": None,
                "revocation_reason": None
            },
            {
                "agent_id": "AG-AI-999",
                "agent_name": "Deprecated Fare Scraper Bot",
                "organization": "SkyScanner Scraper Service",
                "role": "High-Frequency Scraper",
                "registered_at": "2026-01-10 09:30:00",
                "status": "REVOKED",
                "revoked_at": current_time,
                "revocation_reason": "Excessive query rate violating API Fair Use Policy"
            }
        ]
        with open(AGENTS_FILE, mode="w", encoding="utf-8") as f:
            json.dump(initial_agents, f, indent=2)

    # Initialize audit_log.csv with headers if not present
    if not os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(AUDIT_CSV_HEADERS)


def load_agents() -> List[Dict]:
    """Load all registered agents from the JSON file."""
    ensure_data_files()
    try:
        with open(AGENTS_FILE, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_agents(agents: List[Dict]):
    """Persist agents list back to the JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(AGENTS_FILE, mode="w", encoding="utf-8") as f:
        json.dump(agents, f, indent=2)


def get_agent_by_id(agent_id: str) -> Optional[Dict]:
    """Retrieve an agent record by unique ID."""
    agents = load_agents()
    for agent in agents:
        if agent.get("agent_id") == agent_id:
            return agent
    return None


def register_agent(agent_name: str, organization: str, role: str) -> Dict:
    """
    Register a new agent with a unique ID and automatic system timestamp.
    """
    agents = load_agents()
    
    # Generate unique ID: AG-AI-104, AG-AI-105, etc.
    existing_ids = [a.get("agent_id", "") for a in agents]
    counter = 101 + len(agents)
    new_id = f"AG-AI-{counter}"
    while new_id in existing_ids:
        counter += 1
        new_id = f"AG-AI-{counter}"

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_agent = {
        "agent_id": new_id,
        "agent_name": agent_name.strip(),
        "organization": organization.strip(),
        "role": role.strip(),
        "registered_at": now_str,
        "status": "ACTIVE",
        "revoked_at": None,
        "revocation_reason": None
    }
    
    agents.append(new_agent)
    save_agents(agents)
    return new_agent


def revoke_agent(agent_id: str, reason: str) -> bool:
    """
    Revoke an active agent with automatic timestamp and justification.
    """
    agents = load_agents()
    updated = False
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for agent in agents:
        if agent.get("agent_id") == agent_id:
            agent["status"] = "REVOKED"
            agent["revoked_at"] = now_str
            agent["revocation_reason"] = reason.strip()
            updated = True
            break
            
    if updated:
        save_agents(agents)
    return updated


def append_audit_log(
    request_id: str,
    agent_id: str,
    agent_name: str,
    action: str,
    amount_inr: float,
    details: str,
    initial_decision: str,
    rule_applied: str,
    customer_response: str,
    final_outcome: str,
    explanation: str
):
    """
    Record an evaluation event into audit_log.csv with accurate system timestamp.
    """
    ensure_data_files()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    row = [
        now_str,
        request_id,
        agent_id,
        agent_name,
        action,
        f"{amount_inr:.2f}" if amount_inr is not None else "N/A",
        details,
        initial_decision,
        rule_applied,
        customer_response,
        final_outcome,
        explanation
    ]
    
    with open(AUDIT_LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)


def load_audit_logs() -> List[Dict]:
    """Load all audit records from CSV as a list of dictionaries."""
    ensure_data_files()
    records = []
    if not os.path.exists(AUDIT_LOG_FILE):
        return records
        
    with open(AUDIT_LOG_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records
