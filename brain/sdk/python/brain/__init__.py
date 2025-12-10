"""
Brain SDK for Python

Access the shared brain from any Python project in the monorepo.

Usage:
    from brain import Brain

    brain = Brain.load()

    # Check a belief
    if brain.believes('distribution-beats-product'):
        print('Focus on distribution!')

    # Get belief confidence
    confidence = brain.belief_confidence('small-is-underrated')

    # Find people who know about sales
    sales_experts = brain.network.domain_matches('sales')

    # Get high-trust connections
    trusted = brain.network.high_trust()

    # Get urgent agenda items
    urgent = brain.urgent_agenda_items()
"""

from .brain import Brain
from .types import (
    ConfidenceLevel,
    RelationshipStrength,
    TrustLevel,
    EnergyLevel,
    Priority,
    Entity,
    Belief,
    Thread,
    Prediction,
    Relationship,
    Connection,
    Network,
    AgendaItem,
    Agenda,
    BrainState,
)

__all__ = [
    'Brain',
    'ConfidenceLevel',
    'RelationshipStrength',
    'TrustLevel',
    'EnergyLevel',
    'Priority',
    'Entity',
    'Belief',
    'Thread',
    'Prediction',
    'Relationship',
    'Connection',
    'Network',
    'AgendaItem',
    'Agenda',
    'BrainState',
]
