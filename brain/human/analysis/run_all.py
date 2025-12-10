"""
Full Human Intelligence Report
Runs all analysis modules and generates comprehensive report.

Usage:
    python -m context._brain.human.analysis.run_all

Generates insights across:
- Network intelligence (stale relationships, domain matches, gaps)
- Pattern detection (communication, trust, energy, blind spots)
- Goal alignment (stated vs revealed, network-goal fit)
"""

import sys
from datetime import datetime
from pathlib import Path

from . import goal_alignment, network_intel, pattern_detect


def generate_full_report() -> str:
    """Generate comprehensive human intelligence report."""
    report = []

    report.append("=" * 60)
    report.append("HUMAN INTELLIGENCE REPORT")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 60)
    report.append("")

    # Section 1: Network Intelligence
    report.append("-" * 60)
    report.append("SECTION 1: NETWORK INTELLIGENCE")
    report.append("-" * 60)
    report.append(network_intel.generate_report())

    # Section 2: Pattern Detection
    report.append("-" * 60)
    report.append("SECTION 2: PATTERN DETECTION")
    report.append("-" * 60)
    report.append(pattern_detect.generate_report())

    # Section 3: Goal Alignment
    report.append("-" * 60)
    report.append("SECTION 3: GOAL ALIGNMENT")
    report.append("-" * 60)
    report.append(goal_alignment.generate_report())

    # Section 4: Actionable Insights
    report.append("-" * 60)
    report.append("SECTION 4: ACTIONABLE INSIGHTS")
    report.append("-" * 60)
    report.append("")

    actions = generate_action_items()
    if actions:
        report.append("Priority actions based on analysis:")
        for i, action in enumerate(actions, 1):
            report.append(f"\n  {i}. [{action['priority'].upper()}] {action['action']}")
            if action.get('reason'):
                report.append(f"     Why: {action['reason']}")
    else:
        report.append("  No immediate actions identified.")
        report.append("  (Import LinkedIn data to enable full analysis)")

    report.append("")
    report.append("=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)

    return "\n".join(report)


def generate_action_items() -> list[dict]:
    """Generate prioritized action items from all analyses."""
    actions = []

    # Get network insights
    network = network_intel.load_network()

    # Check if network is populated
    connections = network.get("connections", [])
    if not connections:
        actions.append({
            "priority": "high",
            "action": "Import LinkedIn data to populate network",
            "reason": "Network intelligence requires connection data",
        })
        return actions

    # Stale relationships
    stale = network_intel.stale_relationships(network)
    for s in stale[:3]:  # Top 3
        if s.priority == "high":
            actions.append({
                "priority": "high",
                "action": f"Reconnect with {s.connections[0] if s.connections else 'stale contact'}",
                "reason": s.message,
            })

    # Network gaps
    gaps = network_intel.network_gaps(network)
    for g in gaps[:2]:
        if g.priority == "high":
            actions.append({
                "priority": "medium",
                "action": "Build network in " + g.message.split(": ")[-1].strip('"'),
                "reason": "Gap in important domain",
            })

    # Draining relationships
    energy = network_intel.energizing_connections(network)
    for e in energy:
        if e.type == "draining" and len(e.connections) > 3:
            actions.append({
                "priority": "low",
                "action": "Review draining relationships",
                "reason": f"{len(e.connections)} connections flagged as draining",
            })

    # Blind spots
    blind_spots = pattern_detect.blind_spot_detection(network)
    for b in blind_spots[:2]:
        if "undocumented" in b.type or "echo" in b.type:
            actions.append({
                "priority": "medium",
                "action": b.suggestion or b.description,
                "reason": b.description,
            })

    # Goal alignment
    goals = goal_alignment.load_goals()
    alignment = goal_alignment.stated_vs_revealed(goals)
    for a in alignment:
        if a.type == "misaligned":
            actions.append({
                "priority": "high",
                "action": f"Address goal misalignment: {a.description[:50]}",
                "reason": f"Stated: {a.stated}, Actual: {a.actual}",
            })

    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    actions.sort(key=lambda x: priority_order.get(x["priority"], 3))

    return actions[:10]  # Top 10 actions


def quick_summary() -> dict:
    """Generate a quick summary for session start."""
    network = network_intel.load_network()
    connections = network.get("connections", [])

    if not connections:
        return {
            "status": "unpopulated",
            "message": "Network not populated. Import LinkedIn data to enable intelligence.",
        }

    summary = network_intel.network_summary(network)

    # Count key metrics
    high_trust = summary.get("high_trust_count", 0)
    energizing = summary.get("energizing_count", 0)
    draining = summary.get("draining_count", 0)
    stale = summary.get("stale_count", 0)

    return {
        "status": "active",
        "total_connections": summary.get("total_connections", 0),
        "close": summary.get("close", 0),
        "warm": summary.get("warm", 0),
        "cold": summary.get("cold", 0),
        "high_trust": high_trust,
        "energizing": energizing,
        "draining": draining,
        "stale_relationships": stale,
        "needs_attention": stale > 0 or draining > 3,
    }


def before_meeting(connection_id: str) -> str:
    """Generate a quick brief before meeting someone."""
    network = network_intel.load_network()
    assessment = network_intel.connection_assessment(connection_id, network)

    if "error" in assessment:
        return f"Connection not found: {connection_id}"

    brief = []
    brief.append(f"MEETING BRIEF: {assessment['name']}")
    brief.append("-" * 40)
    brief.append(f"Company: {assessment.get('company', 'Unknown')}")
    brief.append(f"Position: {assessment.get('position', 'Unknown')}")
    brief.append(f"Relationship: {assessment.get('relationship_strength', 'Unknown')}")
    brief.append(f"Trust: {assessment.get('trust_level', 'Unknown')}")
    brief.append(f"Energy: {assessment.get('energy', 'Unknown')}")
    brief.append("")

    if assessment.get("positives"):
        brief.append("POSITIVES:")
        for p in assessment["positives"]:
            brief.append(f"  + {p}")
        brief.append("")

    if assessment.get("negatives"):
        brief.append("WATCH-OUTS:")
        for n in assessment["negatives"]:
            brief.append(f"  ! {n}")
        brief.append("")

    if assessment.get("can_ask_for"):
        brief.append("CAN ASK FOR:")
        for c in assessment["can_ask_for"]:
            brief.append(f"  - {c}")
        brief.append("")

    if assessment.get("notes"):
        brief.append(f"NOTES: {assessment['notes']}")

    return "\n".join(brief)


def main():
    """CLI entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "brief" and len(sys.argv) > 2:
            print(before_meeting(sys.argv[2]))
        elif command == "summary":
            import json
            print(json.dumps(quick_summary(), indent=2))
        elif command == "actions":
            actions = generate_action_items()
            for i, a in enumerate(actions, 1):
                print(f"{i}. [{a['priority'].upper()}] {a['action']}")
        else:
            print(f"Unknown command: {command}")
            print("Usage:")
            print("  python -m context._brain.human.analysis.run_all")
            print("  python -m context._brain.human.analysis.run_all summary")
            print("  python -m context._brain.human.analysis.run_all actions")
            print("  python -m context._brain.human.analysis.run_all brief conn.john-smith")
    else:
        print(generate_full_report())


if __name__ == "__main__":
    main()
