"""
Network Intelligence
Analyzes network.yaml and provides proactive suggestions.

Functions:
- stale_relationships: Find connections going cold
- domain_matches: Find people who know about a topic
- reconnection_suggestions: Match threads to people who could help
- network_gaps: Identify missing network areas
- intro_paths: Find who can intro you to whom
- high_trust_connections: Find your most trusted people
- energizing_connections: Find people who give you energy
- watch_outs: Surface connections with known negatives
- network_summary: Generate network overview
"""

import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class NetworkInsight:
    """A single insight from network analysis."""
    type: str  # stale, domain_match, gap, intro_path
    priority: str  # high, medium, low
    message: str
    connections: list
    action: Optional[str] = None


def load_network(path: Optional[Path] = None) -> dict:
    """Load network.yaml."""
    if path is None:
        path = Path(__file__).parent.parent / "network.yaml"

    if not path.exists():
        return {"connections": [], "stats": {}}

    with open(path, 'r') as f:
        return yaml.safe_load(f) or {"connections": [], "stats": {}}


def load_threads(path: Optional[Path] = None) -> list:
    """Load active threads from context library."""
    if path is None:
        path = Path(__file__).parent.parent.parent.parent / "threads"

    threads = []
    if path.exists():
        for thread_file in path.glob("*.md"):
            if thread_file.name.startswith("_"):
                continue
            threads.append({
                "id": f"thread.{thread_file.stem}",
                "name": thread_file.stem,
            })
    return threads


def stale_relationships(
    network: Optional[dict] = None,
    threshold_days: int = 180
) -> list[NetworkInsight]:
    """
    Find relationships that are going cold.

    Returns connections that:
    - Were warm/close (had messages)
    - Haven't been contacted in threshold_days
    """
    if network is None:
        network = load_network()

    insights = []
    cutoff = (datetime.now() - timedelta(days=threshold_days)).strftime("%Y-%m-%d")

    for conn in network.get("connections", []):
        strength = conn.get("relationship_strength", "cold")
        last_message = conn.get("last_message")
        last_contact = conn.get("last_contact")

        # Check if relationship is going stale
        if strength in ("warm", "close"):
            last_touch = last_contact or last_message
            if last_touch and last_touch < cutoff:
                days_ago = (datetime.now() - datetime.strptime(last_touch, "%Y-%m-%d")).days

                insights.append(NetworkInsight(
                    type="stale",
                    priority="high" if strength == "close" else "medium",
                    message=f"{conn['name']} ({conn.get('company', 'Unknown')}) - {strength} relationship, no contact in {days_ago} days",
                    connections=[conn['id']],
                    action=f"Consider reaching out. Last topic: {conn.get('notes', 'N/A')}",
                ))

    return sorted(insights, key=lambda x: x.priority == "high", reverse=True)


def domain_matches(
    topic: str,
    network: Optional[dict] = None,
    min_strength: str = "cold"
) -> list[NetworkInsight]:
    """
    Find people who know about a specific topic.

    Searches:
    - domains field
    - position/title
    - company
    - notes
    """
    if network is None:
        network = load_network()

    topic_lower = topic.lower()
    strength_order = {"close": 3, "warm": 2, "cold": 1}
    min_order = strength_order.get(min_strength, 1)

    matches = []

    for conn in network.get("connections", []):
        conn_strength = strength_order.get(conn.get("relationship_strength", "cold"), 1)
        if conn_strength < min_order:
            continue

        # Search in various fields
        searchable = [
            " ".join(conn.get("domains", [])),
            conn.get("position", ""),
            conn.get("company", ""),
            conn.get("notes", ""),
            " ".join(conn.get("can_ask_for", [])),
        ]

        if any(topic_lower in field.lower() for field in searchable):
            matches.append(conn)

    if matches:
        return [NetworkInsight(
            type="domain_match",
            priority="high",
            message=f"Found {len(matches)} connections related to '{topic}'",
            connections=[m['id'] for m in matches],
            action=f"People to talk to: {', '.join(m['name'] for m in matches[:5])}",
        )]

    return []


def reconnection_suggestions(
    network: Optional[dict] = None,
    threads: Optional[list] = None,
) -> list[NetworkInsight]:
    """
    Match current threads to people who could help.

    Cross-references:
    - Active threads (what you're thinking about)
    - Network domains (what people know)
    """
    if network is None:
        network = load_network()

    if threads is None:
        threads = load_threads()

    insights = []

    for thread in threads:
        # Use thread name as topic
        topic = thread['name'].replace('-', ' ')
        matches = domain_matches(topic, network, min_strength="warm")

        if matches:
            insights.append(NetworkInsight(
                type="reconnection",
                priority="medium",
                message=f"Thread '{thread['id']}' - you know people who might help",
                connections=matches[0].connections,
                action=matches[0].action,
            ))

    return insights


def network_gaps(
    network: Optional[dict] = None,
    target_domains: Optional[list] = None,
) -> list[NetworkInsight]:
    """
    Identify domains where you lack connections.

    If target_domains provided, checks against those.
    Otherwise, suggests based on common needs.
    """
    if network is None:
        network = load_network()

    # Default domains to check if none provided
    if target_domains is None:
        target_domains = [
            "distribution",
            "sales",
            "marketing",
            "fundraising",
            "technical",
            "product",
            "design",
            "operations",
        ]

    # Count connections per domain
    domain_counts = {}
    for conn in network.get("connections", []):
        for domain in conn.get("domains", []):
            domain_lower = domain.lower()
            domain_counts[domain_lower] = domain_counts.get(domain_lower, 0) + 1

    insights = []
    for domain in target_domains:
        count = domain_counts.get(domain.lower(), 0)
        if count == 0:
            insights.append(NetworkInsight(
                type="gap",
                priority="high",
                message=f"Network gap: No connections in '{domain}'",
                connections=[],
                action=f"Consider building relationships in {domain}",
            ))
        elif count < 3:
            insights.append(NetworkInsight(
                type="gap",
                priority="medium",
                message=f"Thin coverage: Only {count} connections in '{domain}'",
                connections=[],
                action=f"Could strengthen {domain} network",
            ))

    return insights


def intro_paths(
    target_domain: str,
    network: Optional[dict] = None,
) -> list[NetworkInsight]:
    """
    Find who might be able to introduce you to people in target_domain.

    Looks at:
    - introduces_to field
    - Position/company that suggests access
    """
    if network is None:
        network = load_network()

    paths = []
    target_lower = target_domain.lower()

    for conn in network.get("connections", []):
        # Check explicit intro list
        intros = conn.get("introduces_to", [])
        if any(target_lower in intro.lower() for intro in intros):
            paths.append(conn)
            continue

        # Check if position suggests they know people in domain
        position = conn.get("position", "").lower()
        company = conn.get("company", "").lower()

        # Heuristics: certain roles know certain people
        if target_lower in ("vc", "fundraising", "investors"):
            if any(term in position for term in ["partner", "principal", "investor", "founder"]):
                paths.append(conn)
        elif target_lower in ("sales", "distribution"):
            if any(term in position for term in ["sales", "growth", "marketing", "bd"]):
                paths.append(conn)

    if paths:
        return [NetworkInsight(
            type="intro_path",
            priority="medium",
            message=f"Potential intros to '{target_domain}': {len(paths)} connections might help",
            connections=[p['id'] for p in paths],
            action=f"Ask: {', '.join(p['name'] for p in paths[:3])}",
        )]

    return []


def high_trust_connections(
    network: Optional[dict] = None,
    for_domain: Optional[str] = None,
) -> list[NetworkInsight]:
    """
    Find your most trusted connections.

    Optionally filter by domain if you need trusted people in a specific area.
    """
    if network is None:
        network = load_network()

    trusted = []
    for conn in network.get("connections", []):
        trust = conn.get("trust_level")
        if trust == "high":
            # If filtering by domain, check match
            if for_domain:
                domains = [d.lower() for d in conn.get("domains", [])]
                if not any(for_domain.lower() in d for d in domains):
                    continue
            trusted.append(conn)

    if trusted:
        domain_msg = f" in '{for_domain}'" if for_domain else ""
        return [NetworkInsight(
            type="high_trust",
            priority="high",
            message=f"High-trust connections{domain_msg}: {len(trusted)} people",
            connections=[t['id'] for t in trusted],
            action=f"Your trusted circle: {', '.join(t['name'] for t in trusted[:5])}",
        )]
    return []


def energizing_connections(
    network: Optional[dict] = None,
) -> list[NetworkInsight]:
    """
    Find people who give you energy.

    These are good people to reach out to when you need a boost,
    or to prioritize when scheduling meetings.
    """
    if network is None:
        network = load_network()

    energizing = []
    draining = []

    for conn in network.get("connections", []):
        energy = conn.get("energy")
        if energy == "energizing":
            energizing.append(conn)
        elif energy == "draining":
            draining.append(conn)

    insights = []

    if energizing:
        insights.append(NetworkInsight(
            type="energizing",
            priority="medium",
            message=f"Energizing connections: {len(energizing)} people who boost you",
            connections=[e['id'] for e in energizing],
            action=f"Reach out when you need energy: {', '.join(e['name'] for e in energizing[:5])}",
        ))

    if draining:
        insights.append(NetworkInsight(
            type="draining",
            priority="low",
            message=f"Draining connections: {len(draining)} people (be mindful of scheduling)",
            connections=[d['id'] for d in draining],
            action="Consider limiting exposure or having shorter meetings",
        ))

    return insights


def watch_outs(
    network: Optional[dict] = None,
    for_connections: Optional[list] = None,
) -> list[NetworkInsight]:
    """
    Surface connections with known negatives.

    Useful when about to meet someone or make an introduction.
    If for_connections provided, only checks those specific people.
    """
    if network is None:
        network = load_network()

    insights = []

    for conn in network.get("connections", []):
        # Filter if specific connections requested
        if for_connections and conn['id'] not in for_connections:
            continue

        negatives = conn.get("negatives", [])
        if negatives:
            insights.append(NetworkInsight(
                type="watch_out",
                priority="medium",
                message=f"Watch-out for {conn['name']}: {len(negatives)} pattern(s) noted",
                connections=[conn['id']],
                action=f"Remember: {'; '.join(negatives[:2])}",
            ))

    return insights


def connection_assessment(
    connection_id: str,
    network: Optional[dict] = None,
) -> dict:
    """
    Get a full assessment of a specific connection.

    Returns positives, negatives, trust level, energy, and suggestions.
    """
    if network is None:
        network = load_network()

    for conn in network.get("connections", []):
        if conn['id'] == connection_id:
            return {
                "name": conn.get("name"),
                "company": conn.get("company"),
                "position": conn.get("position"),
                "relationship_strength": conn.get("relationship_strength"),
                "trust_level": conn.get("trust_level", "unknown"),
                "energy": conn.get("energy", "neutral"),
                "positives": conn.get("positives", []),
                "negatives": conn.get("negatives", []),
                "domains": conn.get("domains", []),
                "can_ask_for": conn.get("can_ask_for", []),
                "last_contact": conn.get("last_contact") or conn.get("last_message"),
                "notes": conn.get("notes"),
            }

    return {"error": f"Connection {connection_id} not found"}


def network_summary(network: Optional[dict] = None) -> dict:
    """
    Generate a summary of the network for display.
    """
    if network is None:
        network = load_network()

    connections = network.get("connections", [])
    stats = network.get("stats", {})

    # Compute if not present
    if not stats.get("total"):
        stats = {
            "total": len(connections),
            "by_relationship": {"close": 0, "warm": 0, "cold": 0},
            "by_domain": {},
        }
        for conn in connections:
            strength = conn.get("relationship_strength", "cold")
            stats["by_relationship"][strength] = stats["by_relationship"].get(strength, 0) + 1
            for domain in conn.get("domains", []):
                stats["by_domain"][domain] = stats["by_domain"].get(domain, 0) + 1

    # Compute trust and energy stats
    trust_stats = {"high": 0, "medium": 0, "low": 0, "unknown": 0}
    energy_stats = {"energizing": 0, "neutral": 0, "draining": 0}
    with_positives = 0
    with_negatives = 0

    for conn in connections:
        trust = conn.get("trust_level", "unknown")
        trust_stats[trust] = trust_stats.get(trust, 0) + 1

        energy = conn.get("energy", "neutral")
        energy_stats[energy] = energy_stats.get(energy, 0) + 1

        if conn.get("positives"):
            with_positives += 1
        if conn.get("negatives"):
            with_negatives += 1

    stale = stale_relationships(network)
    gaps = network_gaps(network)
    energy_insights = energizing_connections(network)

    return {
        "total_connections": stats.get("total", len(connections)),
        "close": stats.get("by_relationship", {}).get("close", 0),
        "warm": stats.get("by_relationship", {}).get("warm", 0),
        "cold": stats.get("by_relationship", {}).get("cold", 0),
        "top_domains": sorted(
            stats.get("by_domain", {}).items(),
            key=lambda x: x[1],
            reverse=True
        )[:5],
        "stale_count": len(stale),
        "stale_high_priority": [s for s in stale if s.priority == "high"],
        "gaps": [g.message for g in gaps if g.priority == "high"],
        # Trust & Energy
        "trust": trust_stats,
        "energy": energy_stats,
        "with_positives": with_positives,
        "with_negatives": with_negatives,
        "high_trust_count": trust_stats["high"],
        "energizing_count": energy_stats["energizing"],
        "draining_count": energy_stats["draining"],
    }


def generate_report(network: Optional[dict] = None) -> str:
    """Generate a text report of network intelligence."""
    summary = network_summary(network)

    report = []
    report.append("=" * 50)
    report.append("NETWORK INTELLIGENCE REPORT")
    report.append("=" * 50)
    report.append("")

    report.append(f"Total connections: {summary['total_connections']}")
    report.append(f"  Close: {summary['close']}")
    report.append(f"  Warm: {summary['warm']}")
    report.append(f"  Cold: {summary['cold']}")
    report.append("")

    if summary['top_domains']:
        report.append("Top domains in network:")
        for domain, count in summary['top_domains']:
            report.append(f"  - {domain}: {count}")
        report.append("")

    if summary['stale_count'] > 0:
        report.append(f"ATTENTION: {summary['stale_count']} relationships going stale")
        for insight in summary['stale_high_priority'][:5]:
            report.append(f"  - {insight.message}")
        report.append("")

    if summary['gaps']:
        report.append("Network gaps:")
        for gap in summary['gaps']:
            report.append(f"  - {gap}")
        report.append("")

    # Trust & Energy section
    trust = summary.get('trust', {})
    energy = summary.get('energy', {})

    if trust.get('high', 0) > 0 or trust.get('low', 0) > 0:
        report.append("Trust levels:")
        report.append(f"  High trust: {trust.get('high', 0)}")
        report.append(f"  Medium trust: {trust.get('medium', 0)}")
        report.append(f"  Low trust: {trust.get('low', 0)}")
        report.append(f"  Unknown: {trust.get('unknown', 0)}")
        report.append("")

    if energy.get('energizing', 0) > 0 or energy.get('draining', 0) > 0:
        report.append("Energy dynamics:")
        report.append(f"  Energizing: {energy.get('energizing', 0)} people who boost you")
        report.append(f"  Draining: {energy.get('draining', 0)} people to be mindful of")
        report.append("")

    # Enrichment status
    with_positives = summary.get('with_positives', 0)
    with_negatives = summary.get('with_negatives', 0)
    total = summary.get('total_connections', 0)

    if total > 0:
        enrichment_pct = round((with_positives + with_negatives) / total * 100, 1)
        if enrichment_pct < 100:
            report.append(f"Enrichment: {enrichment_pct}% of connections have notes")
            if enrichment_pct < 20:
                report.append("  >> Consider adding positives/negatives for key connections")
            report.append("")

    return "\n".join(report)


def main():
    """CLI entry point."""
    print(generate_report())


if __name__ == "__main__":
    main()
