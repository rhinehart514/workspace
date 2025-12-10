"""
Brain SDK - Main Brain Class

Usage:
    from brain import Brain

    brain = Brain.load()

    # Check a belief
    if brain.believes('distribution-beats-product'):
        ...

    # Get network
    experts = brain.network.domain_matches('sales')
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .loaders import (
    load_entities,
    load_relationships,
    load_predictions,
    load_agenda,
    load_network,
    load_state,
)
from .types import (
    ConfidenceLevel,
    RelationshipStrength,
    TrustLevel,
    Connection,
)


@dataclass
class NetworkAccessor:
    """Accessor for network queries."""

    _connections: list[dict] = field(default_factory=list)
    _stats: dict = field(default_factory=dict)

    @property
    def connections(self) -> list[dict]:
        return self._connections

    @property
    def stats(self) -> dict:
        return self._stats

    def domain_matches(self, domain: str) -> list[dict]:
        """Find connections in a domain."""
        domain_lower = domain.lower()
        return [
            c for c in self._connections
            if any(domain_lower in d.lower() for d in c.get('domains', []))
        ]

    def by_strength(self, strength: str) -> list[dict]:
        """Find connections by relationship strength."""
        return [
            c for c in self._connections
            if c.get('relationship_strength') == strength
        ]

    def high_trust(self) -> list[dict]:
        """Get high-trust connections."""
        return [c for c in self._connections if c.get('trust_level') == 'high']

    def energizing(self) -> list[dict]:
        """Get energizing connections."""
        return [c for c in self._connections if c.get('energy') == 'energizing']

    def draining(self) -> list[dict]:
        """Get draining connections."""
        return [c for c in self._connections if c.get('energy') == 'draining']

    def get(self, connection_id: str) -> Optional[dict]:
        """Get a specific connection."""
        for c in self._connections:
            if c.get('id') == connection_id:
                return c
        return None

    def search(self, query: str) -> list[dict]:
        """Search connections by name or company."""
        query_lower = query.lower()
        return [
            c for c in self._connections
            if query_lower in c.get('name', '').lower()
            or query_lower in (c.get('company') or '').lower()
        ]


class Brain:
    """
    Main Brain class for accessing shared intelligence.

    Usage:
        brain = Brain.load()
        if brain.believes('distribution-beats-product'):
            ...
    """

    def __init__(
        self,
        state: dict,
        entities: list,
        relationships: list,
        predictions: list,
        agenda: dict,
        network: dict,
    ):
        self._state = state
        self._entities = entities
        self._relationships = relationships
        self._predictions = predictions
        self._agenda = agenda
        self._network_data = network

    @classmethod
    def load(cls) -> Brain:
        """Load the brain from disk."""
        state = load_state()
        entities = load_entities()
        relationships = load_relationships()
        predictions = load_predictions()
        agenda = load_agenda()
        network = load_network()

        return cls(state, entities, relationships, predictions, agenda, network)

    # === STATE ===

    @property
    def state(self) -> dict:
        return self._state

    @property
    def version(self) -> str:
        return self._state.get('version', '')

    @property
    def capabilities(self) -> dict:
        return self._state.get('capabilities', {})

    def has_capability(self, name: str) -> bool:
        """Check if brain has a capability."""
        return self._state.get('capabilities', {}).get(name, False)

    # === ENTITIES ===

    @property
    def entities(self) -> list:
        return self._entities

    @property
    def beliefs(self) -> list:
        return [e for e in self._entities if e.get('type') == 'belief']

    @property
    def threads(self) -> list:
        return [e for e in self._entities if e.get('type') == 'thread']

    def entity(self, entity_id: str) -> Optional[dict]:
        """Get an entity by ID."""
        for e in self._entities:
            if e.get('id') == entity_id:
                return e
        return None

    def believes(self, belief_id: str) -> bool:
        """Check if the brain holds a belief."""
        full_id = f"belief.{belief_id}" if not belief_id.startswith('belief.') else belief_id
        return self.entity(full_id) is not None or self.entity(belief_id) is not None

    def belief_confidence(self, belief_id: str) -> Optional[str]:
        """Get belief confidence level."""
        full_id = f"belief.{belief_id}" if not belief_id.startswith('belief.') else belief_id
        belief = self.entity(full_id) or self.entity(belief_id)
        return belief.get('confidence') if belief else None

    def entities_by_type(self, entity_type: str) -> list:
        """Get entities by type."""
        return [e for e in self._entities if e.get('type') == entity_type]

    def entities_by_confidence(self, confidence: str) -> list:
        """Get entities by confidence level."""
        return [e for e in self._entities if e.get('confidence') == confidence]

    # === RELATIONSHIPS ===

    @property
    def relationships(self) -> list:
        return self._relationships

    def relationships_for(self, entity_id: str) -> list:
        """Get relationships for an entity."""
        return [
            r for r in self._relationships
            if r.get('from') == entity_id or r.get('to') == entity_id
        ]

    def supports(self, entity_id: str) -> list:
        """Get what supports an entity."""
        return [
            r for r in self._relationships
            if r.get('to') == entity_id and r.get('type') == 'supports'
        ]

    def contradicts(self, entity_id: str) -> list:
        """Get what contradicts an entity."""
        return [
            r for r in self._relationships
            if r.get('to') == entity_id and r.get('type') == 'contradicts'
        ]

    # === PREDICTIONS ===

    @property
    def predictions(self) -> list:
        return self._predictions

    def pending_predictions(self) -> list:
        """Get pending predictions."""
        return [p for p in self._predictions if p.get('status') == 'pending']

    def predictions_due_before(self, date_str: str) -> list:
        """Get predictions due before a date."""
        return [
            p for p in self._predictions
            if p.get('status') == 'pending' and p.get('resolution_date', '') <= date_str
        ]

    # === AGENDA ===

    @property
    def agenda(self) -> dict:
        return self._agenda

    def urgent_agenda_items(self) -> list:
        """Get high-priority agenda items."""
        return [
            item for item in self._agenda.get('immediate', [])
            if item.get('priority') == 'high'
        ]

    # === NETWORK ===

    @property
    def network(self) -> NetworkAccessor:
        return NetworkAccessor(
            _connections=self._network_data.get('connections', []),
            _stats=self._network_data.get('stats', {}),
        )

    # === CONVENIENCE ===

    @property
    def pending_attention(self) -> list:
        """Get attention items that need immediate focus."""
        return self._state.get('pending_attention', [])

    @property
    def recent_changes(self) -> list:
        """Get recent changes to the brain."""
        return self._state.get('recent_changes', [])
