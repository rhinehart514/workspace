"""
Goal Alignment Analysis
Compares stated goals against revealed preferences and network fit.

Functions:
- stated_vs_revealed: Gaps between what you say and what you do
- network_goal_fit: Does your network support your goals
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class AlignmentInsight:
    """An insight about goal alignment."""
    type: str  # aligned, misaligned, gap
    description: str
    stated: str
    actual: str
    suggestion: Optional[str] = None


def load_goals(path: Optional[Path] = None) -> dict:
    """Load goals.yaml."""
    if path is None:
        path = Path(__file__).parent.parent / "goals.yaml"
    if not path.exists():
        return {}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def load_network(path: Optional[Path] = None) -> dict:
    """Load network.yaml."""
    if path is None:
        path = Path(__file__).parent.parent / "network.yaml"
    if not path.exists():
        return {"connections": []}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {"connections": []}


def load_interactions(path: Optional[Path] = None) -> dict:
    """Load interactions.yaml."""
    if path is None:
        path = Path(__file__).parent.parent / "interactions.yaml"
    if not path.exists():
        return {"interactions": []}
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {"interactions": []}


def stated_vs_revealed(goals: Optional[dict] = None) -> list[AlignmentInsight]:
    """
    Analyze gaps between stated goals and revealed preferences.

    Looks at:
    - Time allocation vs stated priorities
    - Avoided actions vs stated goals
    - Explicit misalignments in goals.yaml
    """
    if goals is None:
        goals = load_goals()

    insights = []

    # Check explicit misalignments
    delta = goals.get("delta", {})
    misalignments = delta.get("misalignments", [])

    for m in misalignments:
        insights.append(AlignmentInsight(
            type="misaligned",
            description=m.get("gap", "Unspecified gap"),
            stated=m.get("stated", ""),
            actual=m.get("actual", ""),
            suggestion=", ".join(m.get("possible_reasons", [])) or None,
        ))

    # Check revealed preferences
    revealed = goals.get("revealed", {})
    avoided = revealed.get("avoided_actions", [])

    if avoided:
        insights.append(AlignmentInsight(
            type="avoidance",
            description="Actions you keep avoiding despite saying they're important",
            stated="(various)",
            actual=", ".join(avoided[:5]),
            suggestion="Consider why these are being avoided",
        ))

    # If no data, note it
    if not insights and not goals:
        insights.append(AlignmentInsight(
            type="no_data",
            description="Goals not populated",
            stated="Unknown",
            actual="Unknown",
            suggestion="Populate goals.yaml to enable alignment analysis",
        ))

    return insights


def network_goal_fit(
    goals: Optional[dict] = None,
    network: Optional[dict] = None,
) -> list[AlignmentInsight]:
    """
    Analyze whether your network supports your stated goals.

    Cross-references:
    - Stated goals with network domains
    - Goal keywords with connection expertise
    """
    if goals is None:
        goals = load_goals()
    if network is None:
        network = load_network()

    insights = []

    # Get stated goals
    stated = goals.get("stated", {})
    primary = stated.get("primary", "")
    secondary = stated.get("secondary", [])

    all_goals = [primary] + secondary if primary else secondary
    all_goals = [g for g in all_goals if g]  # Filter empty

    if not all_goals:
        return [AlignmentInsight(
            type="no_goals",
            description="No stated goals to analyze",
            stated="None",
            actual="N/A",
            suggestion="Add goals to goals.yaml",
        )]

    # Collect all domains and expertise in network
    network_domains = set()
    for conn in network.get("connections", []):
        for domain in conn.get("domains", []):
            network_domains.add(domain.lower())
        for skill in conn.get("can_ask_for", []):
            network_domains.add(skill.lower())

    # Check each goal for network support
    for goal in all_goals:
        goal_lower = goal.lower()
        goal_words = set(goal_lower.split())

        # Find overlapping domains
        matching_domains = [d for d in network_domains if any(w in d for w in goal_words)]

        if matching_domains:
            # Find specific people
            relevant_people = []
            for conn in network.get("connections", []):
                conn_domains = [d.lower() for d in conn.get("domains", [])]
                if any(d in conn_domains for d in matching_domains):
                    relevant_people.append(conn.get("name"))

            insights.append(AlignmentInsight(
                type="aligned",
                description=f"Network supports goal: {goal[:50]}",
                stated=goal,
                actual=f"{len(relevant_people)} relevant connections",
                suggestion=f"Talk to: {', '.join(relevant_people[:3])}" if relevant_people else None,
            ))
        else:
            insights.append(AlignmentInsight(
                type="gap",
                description=f"Network gap for goal: {goal[:50]}",
                stated=goal,
                actual="No connections in relevant domains",
                suggestion="Build relationships in this area",
            ))

    return insights


def generate_report(
    goals: Optional[dict] = None,
    network: Optional[dict] = None,
) -> str:
    """Generate a text report of goal alignment analysis."""
    report = []
    report.append("=" * 50)
    report.append("GOAL ALIGNMENT REPORT")
    report.append("=" * 50)
    report.append("")

    # Stated vs revealed
    alignment = stated_vs_revealed(goals)
    if alignment:
        report.append("STATED VS REVEALED:")
        for insight in alignment:
            report.append(f"\n  [{insight.type.upper()}] {insight.description}")
            if insight.stated:
                report.append(f"    Stated: {insight.stated}")
            if insight.actual:
                report.append(f"    Actual: {insight.actual}")
            if insight.suggestion:
                report.append(f"    >> {insight.suggestion}")
        report.append("")

    # Network-goal fit
    fit = network_goal_fit(goals, network)
    if fit:
        report.append("NETWORK-GOAL FIT:")
        for insight in fit:
            report.append(f"\n  [{insight.type.upper()}] {insight.description}")
            if insight.actual and insight.type == "aligned":
                report.append(f"    {insight.actual}")
            if insight.suggestion:
                report.append(f"    >> {insight.suggestion}")
        report.append("")

    return "\n".join(report)


def main():
    """CLI entry point."""
    print(generate_report())


if __name__ == "__main__":
    main()
