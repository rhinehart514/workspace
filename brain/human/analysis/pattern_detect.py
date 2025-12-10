"""
Pattern Detection
Analyzes communication patterns, domain clusters, and relationship trajectories.

Functions:
- communication_patterns: Who you talk to, how often
- domain_clusters: Where your network is strong/weak
- relationship_trajectory: Warming/cooling connections
- trust_patterns: What correlates with trust
- energy_patterns: Who drains vs energizes you
- positive_negative_insights: Patterns in your assessments
- blind_spot_detection: Potential blind spots in how you see people
"""

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import yaml


@dataclass
class Pattern:
    """A detected pattern in behavior or network."""
    type: str
    description: str
    evidence: list
    suggestion: Optional[str] = None


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


def communication_patterns(
    network: Optional[dict] = None,
    interactions: Optional[dict] = None,
) -> list[Pattern]:
    """
    Analyze who you communicate with and how often.

    Returns patterns about:
    - Most frequent contacts
    - Communication gaps
    - Medium preferences
    """
    if network is None:
        network = load_network()
    if interactions is None:
        interactions = load_interactions()

    patterns = []

    # Count interactions by person
    contact_counts = defaultdict(int)
    medium_counts = defaultdict(int)

    for interaction in interactions.get("interactions", []):
        contact = interaction.get("with", "")
        medium = interaction.get("medium", "unknown")

        if contact:
            contact_counts[contact] += 1
        medium_counts[medium] += 1

    # Also use message counts from network
    for conn in network.get("connections", []):
        name = conn.get("name", "")
        msg_count = conn.get("message_count", 0)
        if msg_count > 0:
            contact_counts[name] += msg_count

    # Find top contacts
    if contact_counts:
        top_contacts = sorted(contact_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        patterns.append(Pattern(
            type="high_frequency",
            description="Most frequent contacts",
            evidence=[f"{name}: {count} interactions" for name, count in top_contacts],
        ))

    # Find preferred mediums
    if medium_counts:
        sorted_mediums = sorted(medium_counts.items(), key=lambda x: x[1], reverse=True)
        patterns.append(Pattern(
            type="medium_preference",
            description="Preferred communication mediums",
            evidence=[f"{medium}: {count}" for medium, count in sorted_mediums],
        ))

    # Find people you connected with but never talked to
    silent_connections = []
    for conn in network.get("connections", []):
        if conn.get("message_count", 0) == 0:
            silent_connections.append(conn.get("name"))

    if silent_connections:
        patterns.append(Pattern(
            type="silent_connections",
            description=f"{len(silent_connections)} connections with no recorded interaction",
            evidence=silent_connections[:10] + (["...and more"] if len(silent_connections) > 10 else []),
            suggestion="Consider which of these might be worth reaching out to",
        ))

    return patterns


def domain_clusters(network: Optional[dict] = None) -> list[Pattern]:
    """
    Analyze domain distribution in network.

    Returns patterns about:
    - Domain concentrations
    - Underrepresented areas
    - Domain/strength correlations
    """
    if network is None:
        network = load_network()

    patterns = []

    # Count domains
    domain_counts = defaultdict(int)
    domain_by_strength = defaultdict(lambda: {"close": 0, "warm": 0, "cold": 0})

    for conn in network.get("connections", []):
        strength = conn.get("relationship_strength", "cold")
        for domain in conn.get("domains", []):
            domain_counts[domain] += 1
            domain_by_strength[domain][strength] += 1

    if not domain_counts:
        patterns.append(Pattern(
            type="no_domains",
            description="No domain tags on connections",
            evidence=[],
            suggestion="Add domains to connections for better intelligence",
        ))
        return patterns

    # Find strongest domains
    sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)

    patterns.append(Pattern(
        type="domain_concentration",
        description="Top domains in network",
        evidence=[f"{domain}: {count}" for domain, count in sorted_domains[:5]],
    ))

    # Find domains where you have close relationships
    strong_domains = []
    for domain, strengths in domain_by_strength.items():
        if strengths["close"] > 0:
            strong_domains.append((domain, strengths["close"]))

    if strong_domains:
        sorted_strong = sorted(strong_domains, key=lambda x: x[1], reverse=True)
        patterns.append(Pattern(
            type="strong_domain_relationships",
            description="Domains where you have close relationships",
            evidence=[f"{domain}: {count} close" for domain, count in sorted_strong[:5]],
        ))

    return patterns


def relationship_trajectory(
    network: Optional[dict] = None,
    lookback_days: int = 90,
) -> list[Pattern]:
    """
    Analyze which relationships are warming or cooling.

    Based on:
    - Message recency vs historical frequency
    - Explicit contact tracking
    """
    if network is None:
        network = load_network()

    patterns = []
    cutoff = (datetime.now() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")

    warming = []
    cooling = []

    for conn in network.get("connections", []):
        name = conn.get("name", "Unknown")
        strength = conn.get("relationship_strength", "cold")
        last_message = conn.get("last_message")
        message_count = conn.get("message_count", 0)

        # Cooling: was warm/close but no recent contact
        if strength in ("warm", "close") and last_message:
            if last_message < cutoff:
                cooling.append({
                    "name": name,
                    "strength": strength,
                    "last": last_message,
                })

        # Warming: cold but has recent messages
        if strength == "cold" and last_message:
            if last_message >= cutoff and message_count >= 2:
                warming.append({
                    "name": name,
                    "messages": message_count,
                    "last": last_message,
                })

    if cooling:
        patterns.append(Pattern(
            type="cooling",
            description=f"{len(cooling)} relationships cooling off",
            evidence=[f"{c['name']} ({c['strength']}) - last contact {c['last']}" for c in cooling[:5]],
            suggestion="Consider re-engaging with these contacts",
        ))

    if warming:
        patterns.append(Pattern(
            type="warming",
            description=f"{len(warming)} relationships warming up",
            evidence=[f"{w['name']} - {w['messages']} messages, last {w['last']}" for w in warming[:5]],
            suggestion="Continue building these relationships",
        ))

    return patterns


def trust_patterns(network: Optional[dict] = None) -> list[Pattern]:
    """
    Analyze what correlates with trust in your network.

    Looks for patterns like:
    - Do you trust people from certain companies more?
    - Do you trust people you've known longer?
    - Is trust correlated with relationship strength?
    """
    if network is None:
        network = load_network()

    patterns = []

    # Gather trust data
    high_trust = []
    low_trust = []
    trust_by_company = defaultdict(lambda: {"high": 0, "low": 0, "total": 0})
    trust_by_strength = defaultdict(lambda: {"high": 0, "low": 0, "total": 0})

    for conn in network.get("connections", []):
        trust = conn.get("trust_level")
        company = conn.get("company", "Unknown")
        strength = conn.get("relationship_strength", "cold")

        if trust == "high":
            high_trust.append(conn)
            trust_by_company[company]["high"] += 1
        elif trust == "low":
            low_trust.append(conn)
            trust_by_company[company]["low"] += 1

        trust_by_company[company]["total"] += 1
        trust_by_strength[strength]["total"] += 1
        if trust:
            trust_by_strength[strength][trust] = trust_by_strength[strength].get(trust, 0) + 1

    # Pattern: Companies with high trust concentration
    high_trust_companies = []
    for company, stats in trust_by_company.items():
        if stats["high"] >= 2 and stats["total"] >= 3:
            ratio = stats["high"] / stats["total"]
            if ratio >= 0.5:
                high_trust_companies.append((company, stats["high"], stats["total"]))

    if high_trust_companies:
        patterns.append(Pattern(
            type="trust_by_company",
            description="Companies where you trust many people",
            evidence=[f"{c}: {h}/{t} high trust" for c, h, t in sorted(high_trust_companies, key=lambda x: x[1], reverse=True)[:5]],
            suggestion="Your trust may correlate with company culture or hiring quality",
        ))

    # Pattern: Trust vs relationship strength correlation
    close_high_trust = trust_by_strength["close"].get("high", 0)
    close_total = trust_by_strength["close"]["total"]
    cold_high_trust = trust_by_strength["cold"].get("high", 0)
    cold_total = trust_by_strength["cold"]["total"]

    if close_total > 0 and cold_total > 0:
        close_ratio = close_high_trust / close_total if close_total else 0
        cold_ratio = cold_high_trust / cold_total if cold_total else 0

        if close_ratio > cold_ratio * 2:
            patterns.append(Pattern(
                type="trust_strength_correlation",
                description="Trust correlates with relationship closeness",
                evidence=[
                    f"Close relationships: {close_high_trust}/{close_total} high trust ({round(close_ratio*100)}%)",
                    f"Cold relationships: {cold_high_trust}/{cold_total} high trust ({round(cold_ratio*100)}%)",
                ],
                suggestion="You build trust through interaction (expected pattern)",
            ))

    # Pattern: Low trust signals
    if low_trust:
        low_trust_reasons = []
        for conn in low_trust:
            negatives = conn.get("negatives", [])
            if negatives:
                low_trust_reasons.extend(negatives)

        if low_trust_reasons:
            # Find common patterns in negatives
            from collections import Counter
            word_counts = Counter()
            for reason in low_trust_reasons:
                words = reason.lower().split()
                word_counts.update(words)

            common_words = [w for w, c in word_counts.most_common(10) if c >= 2 and len(w) > 3]
            if common_words:
                patterns.append(Pattern(
                    type="low_trust_patterns",
                    description="Common themes in low-trust connections",
                    evidence=[f"Recurring terms: {', '.join(common_words[:5])}"],
                    suggestion="These might be your trust dealbreakers",
                ))

    return patterns


def energy_patterns(network: Optional[dict] = None) -> list[Pattern]:
    """
    Analyze what correlates with energy in your network.

    Looks for patterns like:
    - Do certain domains energize or drain you?
    - Is energy correlated with trust?
    - Time-based patterns in draining relationships
    """
    if network is None:
        network = load_network()

    patterns = []

    energizing = []
    draining = []
    energy_by_domain = defaultdict(lambda: {"energizing": 0, "draining": 0, "total": 0})
    energy_by_trust = defaultdict(lambda: {"energizing": 0, "draining": 0})

    for conn in network.get("connections", []):
        energy = conn.get("energy")
        trust = conn.get("trust_level", "unknown")

        for domain in conn.get("domains", []):
            energy_by_domain[domain]["total"] += 1
            if energy:
                energy_by_domain[domain][energy] = energy_by_domain[domain].get(energy, 0) + 1

        if energy == "energizing":
            energizing.append(conn)
            energy_by_trust[trust]["energizing"] += 1
        elif energy == "draining":
            draining.append(conn)
            energy_by_trust[trust]["draining"] += 1

    # Pattern: Domains that energize
    energizing_domains = []
    for domain, stats in energy_by_domain.items():
        if stats.get("energizing", 0) >= 2:
            energizing_domains.append((domain, stats["energizing"]))

    if energizing_domains:
        patterns.append(Pattern(
            type="energizing_domains",
            description="Domains that tend to energize you",
            evidence=[f"{d}: {c} energizing connections" for d, c in sorted(energizing_domains, key=lambda x: x[1], reverse=True)[:5]],
            suggestion="Consider seeking more relationships in these areas",
        ))

    # Pattern: Domains that drain
    draining_domains = []
    for domain, stats in energy_by_domain.items():
        if stats.get("draining", 0) >= 2:
            draining_domains.append((domain, stats["draining"]))

    if draining_domains:
        patterns.append(Pattern(
            type="draining_domains",
            description="Domains that tend to drain you",
            evidence=[f"{d}: {c} draining connections" for d, c in sorted(draining_domains, key=lambda x: x[1], reverse=True)[:5]],
            suggestion="Be mindful when engaging in these areas",
        ))

    # Pattern: Trust-energy correlation
    high_trust_energizing = energy_by_trust.get("high", {}).get("energizing", 0)
    high_trust_draining = energy_by_trust.get("high", {}).get("draining", 0)
    low_trust_draining = energy_by_trust.get("low", {}).get("draining", 0)

    if high_trust_draining > 0:
        patterns.append(Pattern(
            type="trust_energy_mismatch",
            description=f"You have {high_trust_draining} high-trust but draining connections",
            evidence=["These relationships may be worth examining"],
            suggestion="High trust + draining = possible obligation or guilt dynamic",
        ))

    if low_trust_draining > 2:
        patterns.append(Pattern(
            type="low_trust_draining",
            description=f"{low_trust_draining} low-trust draining connections",
            evidence=["Consider whether these relationships are necessary"],
            suggestion="Low trust + draining = candidates for reducing exposure",
        ))

    return patterns


def positive_negative_insights(network: Optional[dict] = None) -> list[Pattern]:
    """
    Analyze patterns in how you assess people.

    Looks for:
    - Balance of positives vs negatives
    - Common positive traits you value
    - Common negative traits you notice
    - Assessment blind spots
    """
    if network is None:
        network = load_network()

    patterns = []

    all_positives = []
    all_negatives = []
    only_positive = 0
    only_negative = 0
    balanced = 0

    for conn in network.get("connections", []):
        positives = conn.get("positives", [])
        negatives = conn.get("negatives", [])

        all_positives.extend(positives)
        all_negatives.extend(negatives)

        if positives and not negatives:
            only_positive += 1
        elif negatives and not positives:
            only_negative += 1
        elif positives and negatives:
            balanced += 1

    # Pattern: Assessment balance
    total_assessed = only_positive + only_negative + balanced
    if total_assessed > 0:
        if only_positive > balanced * 2:
            patterns.append(Pattern(
                type="overly_positive",
                description="You tend to only note positives",
                evidence=[f"{only_positive} only positive, {only_negative} only negative, {balanced} balanced"],
                suggestion="Consider: what are you not seeing about people?",
            ))
        elif only_negative > balanced * 2:
            patterns.append(Pattern(
                type="overly_negative",
                description="You tend to only note negatives",
                evidence=[f"{only_positive} only positive, {only_negative} only negative, {balanced} balanced"],
                suggestion="Consider: what strengths are you overlooking?",
            ))

    # Pattern: Common positive traits
    if all_positives:
        from collections import Counter
        positive_words = Counter()
        for p in all_positives:
            words = [w.lower() for w in p.split() if len(w) > 3]
            positive_words.update(words)

        top_positive = positive_words.most_common(10)
        if top_positive:
            patterns.append(Pattern(
                type="valued_traits",
                description="Traits you frequently value",
                evidence=[f"{w}: {c}x" for w, c in top_positive[:5] if c >= 2],
                suggestion="These reveal what you prioritize in people",
            ))

    # Pattern: Common negative traits
    if all_negatives:
        from collections import Counter
        negative_words = Counter()
        for n in all_negatives:
            words = [w.lower() for w in n.split() if len(w) > 3]
            negative_words.update(words)

        top_negative = negative_words.most_common(10)
        if top_negative:
            patterns.append(Pattern(
                type="watched_traits",
                description="Traits you frequently watch for",
                evidence=[f"{w}: {c}x" for w, c in top_negative[:5] if c >= 2],
                suggestion="These reveal your dealbreakers or sensitivities",
            ))

    return patterns


def blind_spot_detection(network: Optional[dict] = None) -> list[Pattern]:
    """
    Detect potential blind spots in how you see your network.

    Looks for:
    - High trust without documented reasons
    - Long relationships without assessment
    - Potential echo chambers
    """
    if network is None:
        network = load_network()

    patterns = []

    # Blind spot: High trust without positives documented
    undocumented_trust = []
    for conn in network.get("connections", []):
        trust = conn.get("trust_level")
        positives = conn.get("positives", [])

        if trust == "high" and not positives:
            undocumented_trust.append(conn.get("name"))

    if undocumented_trust:
        patterns.append(Pattern(
            type="undocumented_trust",
            description=f"{len(undocumented_trust)} high-trust connections without documented reasons",
            evidence=undocumented_trust[:5],
            suggestion="Why do you trust them? Making it explicit helps validate",
        ))

    # Blind spot: Long relationships without assessment
    old_unassessed = []
    one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    for conn in network.get("connections", []):
        connected = conn.get("connected_date")
        trust = conn.get("trust_level")
        positives = conn.get("positives", [])
        negatives = conn.get("negatives", [])

        if connected and connected < one_year_ago:
            if not trust and not positives and not negatives:
                old_unassessed.append(conn.get("name"))

    if old_unassessed:
        patterns.append(Pattern(
            type="old_unassessed",
            description=f"{len(old_unassessed)} long-term connections without assessment",
            evidence=old_unassessed[:5] + (["...and more"] if len(old_unassessed) > 5 else []),
            suggestion="Do you actually know these people? Consider assessing or archiving",
        ))

    # Blind spot: Echo chamber detection
    domain_counts = defaultdict(int)
    for conn in network.get("connections", []):
        for domain in conn.get("domains", []):
            domain_counts[domain] += 1

    total = sum(domain_counts.values())
    if total > 0:
        dominant_domains = [(d, c) for d, c in domain_counts.items() if c / total > 0.4]
        if dominant_domains:
            patterns.append(Pattern(
                type="potential_echo_chamber",
                description="Your network may be concentrated in few domains",
                evidence=[f"{d}: {c}/{total} ({round(c/total*100)}%)" for d, c in dominant_domains],
                suggestion="Diverse perspectives come from diverse networks",
            ))

    return patterns


def generate_report(
    network: Optional[dict] = None,
    interactions: Optional[dict] = None,
) -> str:
    """Generate a text report of pattern analysis."""
    report = []
    report.append("=" * 50)
    report.append("PATTERN DETECTION REPORT")
    report.append("=" * 50)
    report.append("")

    # Communication patterns
    comm = communication_patterns(network, interactions)
    if comm:
        report.append("COMMUNICATION PATTERNS:")
        for pattern in comm:
            report.append(f"\n  {pattern.description}:")
            for evidence in pattern.evidence[:5]:
                report.append(f"    - {evidence}")
            if pattern.suggestion:
                report.append(f"    >> {pattern.suggestion}")
        report.append("")

    # Domain clusters
    domains = domain_clusters(network)
    if domains:
        report.append("DOMAIN CLUSTERS:")
        for pattern in domains:
            report.append(f"\n  {pattern.description}:")
            for evidence in pattern.evidence[:5]:
                report.append(f"    - {evidence}")
            if pattern.suggestion:
                report.append(f"    >> {pattern.suggestion}")
        report.append("")

    # Relationship trajectory
    trajectory = relationship_trajectory(network)
    if trajectory:
        report.append("RELATIONSHIP TRAJECTORY:")
        for pattern in trajectory:
            report.append(f"\n  {pattern.description}:")
            for evidence in pattern.evidence[:5]:
                report.append(f"    - {evidence}")
            if pattern.suggestion:
                report.append(f"    >> {pattern.suggestion}")
        report.append("")

    # Trust patterns
    trust = trust_patterns(network)
    if trust:
        report.append("TRUST PATTERNS:")
        for pattern in trust:
            report.append(f"\n  {pattern.description}:")
            for evidence in pattern.evidence[:5]:
                report.append(f"    - {evidence}")
            if pattern.suggestion:
                report.append(f"    >> {pattern.suggestion}")
        report.append("")

    # Energy patterns
    energy = energy_patterns(network)
    if energy:
        report.append("ENERGY PATTERNS:")
        for pattern in energy:
            report.append(f"\n  {pattern.description}:")
            for evidence in pattern.evidence[:5]:
                report.append(f"    - {evidence}")
            if pattern.suggestion:
                report.append(f"    >> {pattern.suggestion}")
        report.append("")

    # Positive/negative insights
    assessments = positive_negative_insights(network)
    if assessments:
        report.append("ASSESSMENT PATTERNS:")
        for pattern in assessments:
            report.append(f"\n  {pattern.description}:")
            for evidence in pattern.evidence[:5]:
                report.append(f"    - {evidence}")
            if pattern.suggestion:
                report.append(f"    >> {pattern.suggestion}")
        report.append("")

    # Blind spots
    blind_spots = blind_spot_detection(network)
    if blind_spots:
        report.append("POTENTIAL BLIND SPOTS:")
        for pattern in blind_spots:
            report.append(f"\n  {pattern.description}:")
            for evidence in pattern.evidence[:5]:
                report.append(f"    - {evidence}")
            if pattern.suggestion:
                report.append(f"    >> {pattern.suggestion}")
        report.append("")

    return "\n".join(report)


def main():
    """CLI entry point."""
    print(generate_report())


if __name__ == "__main__":
    main()
