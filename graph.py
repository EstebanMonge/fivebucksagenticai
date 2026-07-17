from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from telegram_node import send_telegram
from analyze_node import analyze
from report_node import report
from dokuwiki_node import create_dokuwiki_page
import subprocess

class NagiosState(TypedDict):
    # Information from Nagios
    notification_type: str
    host: str
    address: str
    service: str
    state: str
    output: str

    # Investigation
    evidence: List[Dict[str, Any]]

    # AI results
    diagnosis: str
    recommendation: str
    confidence: float

    # Execution status
    telegram_sent: bool
    investigation_complete: bool

def investigate(state):
    print("Investigating...")

    state["evidence"] = []

    result = subprocess.run(
        ["ping", "-c", "2", state["address"]],
        capture_output=True,
        text=True
    )

    state["evidence"].append({
        "tool": "ping",
        "success": result.returncode == 0,
        "output": result.stdout + result.stderr,
    })

    return state

builder = StateGraph(NagiosState)

builder.add_node("telegram", send_telegram)
builder.add_node("investigate", investigate)
builder.add_node("analyze", analyze)
builder.add_node("report", report)
builder.add_node("dokuwiki", create_dokuwiki_page)

builder.set_entry_point("telegram")

builder.add_edge("telegram", "investigate")
builder.add_edge("investigate", "analyze")
builder.add_edge("analyze", "report")
builder.add_edge("report", "dokuwiki")
builder.add_edge("dokuwiki", END)

graph = builder.compile()
