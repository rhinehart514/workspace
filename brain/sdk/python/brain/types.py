"""
Brain SDK Types
Pydantic models for all brain data structures
"""

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ConfidenceLevel(str, Enum):
    SPECULATIVE = "speculative"
    TENTATIVE = "tentative"
    GROUNDED = "grounded"
    HARDENED = "hardened"


class RelationshipStrength(str, Enum):
    COLD = "cold"
    WARM = "warm"
    CLOSE = "close"


class TrustLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class EnergyLevel(str, Enum):
    ENERGIZING = "energizing"
    NEUTRAL = "neutral"
    DRAINING = "draining"


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class EntityType(str, Enum):
    BELIEF = "belief"
    TERM = "term"
    THREAD = "thread"
    PRINCIPLE = "principle"
    ANTIPATTERN = "antipattern"
    PREDICTION = "prediction"
    JUDGMENT = "judgment"


class Entity(BaseModel):
    id: str
    type: EntityType
    name: str
    confidence: ConfidenceLevel
    created: str
    last_updated: str
    description: Optional[str] = None
    tags: list[str] = []


class Belief(Entity):
    type: EntityType = EntityType.BELIEF
    hardened_date: Optional[str] = None
    can_be_wrong: bool = True


class Thread(Entity):
    type: EntityType = EntityType.THREAD
    status: str = "active"
    momentum: str = "steady"
    last_activity: Optional[str] = None


class Prediction(Entity):
    type: EntityType = EntityType.PREDICTION
    claim: str
    resolution_date: str
    status: str = "pending"
    evidence: list[str] = []


class RelationshipType(str, Enum):
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    SUGGESTS = "suggests"
    VALIDATES = "validates"
    CHALLENGES = "challenges"
    DEPENDS_ON = "depends_on"


class Relationship(BaseModel):
    id: str
    type: RelationshipType
    from_entity: str  # 'from' is reserved in Python
    to: str
    strength: int  # 1-10
    created: str
    notes: Optional[str] = None

    class Config:
        # Allow 'from' field in JSON to map to 'from_entity'
        fields = {'from_entity': 'from'}


class Connection(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    connected_date: Optional[str] = None
    relationship_strength: RelationshipStrength = RelationshipStrength.COLD
    message_count: int = 0
    last_message: Optional[str] = None
    context: str = ""
    domains: list[str] = []
    can_ask_for: list[str] = []
    has_asked_you: list[str] = []
    introduces_to: list[str] = []
    notes: str = ""
    last_contact: Optional[str] = None
    contact_frequency: Optional[str] = None
    positives: list[str] = []
    negatives: list[str] = []
    trust_level: Optional[TrustLevel] = None
    energy: Optional[EnergyLevel] = None


class NetworkStats(BaseModel):
    total: int = 0
    by_relationship: dict[str, int] = {}
    by_domain: dict[str, int] = {}
    stale_relationships: list[str] = []


class NetworkGap(BaseModel):
    domain: str
    have: int
    need: str
    priority: Priority


class Network(BaseModel):
    connections: list[Connection] = []
    stats: NetworkStats = NetworkStats()
    network_gaps: list[NetworkGap] = []


class AgendaItem(BaseModel):
    id: str
    action: str
    target: str
    reason: str
    prompt: str
    priority: Priority
    added: str
    source: str


class ScheduledItem(BaseModel):
    id: str
    type: str
    target: str
    check_date: str
    description: str
    status: str


class WatchingItem(BaseModel):
    id: str
    pattern: str
    target: str
    reason: str
    last_evidence: Optional[str] = None


class SuggestionItem(BaseModel):
    id: str
    type: str
    description: str
    rationale: str
    thread: Optional[str] = None
    priority: Priority


class Agenda(BaseModel):
    immediate: list[AgendaItem] = []
    scheduled: list[ScheduledItem] = []
    watching: list[WatchingItem] = []
    suggestions: list[SuggestionItem] = []


class AgentState(BaseModel):
    last_run: str
    runs_total: int
    mode: str


class BrainState(BaseModel):
    version: str
    initialized: str
    last_activity: str
    architecture: str
    agents: dict[str, AgentState] = {}
    capabilities: dict[str, bool] = {}
    pending_attention: list[str] = []
    recent_changes: list[str] = []
