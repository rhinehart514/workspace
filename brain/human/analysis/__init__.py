"""
Human Layer Analysis Package
Intelligence functions for analyzing the human layer data.

Quick usage:
    from context._brain.human.analysis import run_all
    run_all.generate_full_report()  # Full report
    run_all.quick_summary()         # Session start summary
    run_all.before_meeting("conn.john-smith")  # Meeting prep
    run_all.generate_action_items() # Priority actions
"""

from .network_intel import (
    stale_relationships,
    domain_matches,
    reconnection_suggestions,
    network_gaps,
    intro_paths,
    network_summary,
    # New trust/energy functions
    high_trust_connections,
    energizing_connections,
    watch_outs,
    connection_assessment,
)
from .pattern_detect import (
    communication_patterns,
    domain_clusters,
    relationship_trajectory,
    # New pattern functions
    trust_patterns,
    energy_patterns,
    positive_negative_insights,
    blind_spot_detection,
)
from .goal_alignment import (
    stated_vs_revealed,
    network_goal_fit,
)

__all__ = [
    # Network intelligence
    "stale_relationships",
    "domain_matches",
    "reconnection_suggestions",
    "network_gaps",
    "intro_paths",
    "network_summary",
    # Trust & energy
    "high_trust_connections",
    "energizing_connections",
    "watch_outs",
    "connection_assessment",
    # Pattern detection
    "communication_patterns",
    "domain_clusters",
    "relationship_trajectory",
    "trust_patterns",
    "energy_patterns",
    "positive_negative_insights",
    "blind_spot_detection",
    # Goal alignment
    "stated_vs_revealed",
    "network_goal_fit",
]
