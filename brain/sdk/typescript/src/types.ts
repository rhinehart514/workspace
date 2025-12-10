/**
 * Brain SDK Types
 * Defines the shape of all brain data structures
 */

export type ConfidenceLevel = 'speculative' | 'tentative' | 'grounded' | 'hardened';
export type RelationshipStrength = 'cold' | 'warm' | 'close';
export type TrustLevel = 'high' | 'medium' | 'low' | 'unknown';
export type EnergyLevel = 'energizing' | 'neutral' | 'draining';
export type Priority = 'high' | 'medium' | 'low';

// === ENTITIES ===

export interface Entity {
  id: string;
  type: 'belief' | 'term' | 'thread' | 'principle' | 'antipattern' | 'prediction' | 'judgment';
  name: string;
  confidence: ConfidenceLevel;
  created: string;
  last_updated: string;
  description?: string;
  tags?: string[];
}

export interface Belief extends Entity {
  type: 'belief';
  hardened_date?: string;
  can_be_wrong?: boolean;
}

export interface Thread extends Entity {
  type: 'thread';
  status: 'active' | 'parked' | 'resolved' | 'stale';
  momentum: 'accelerating' | 'steady' | 'slowing' | 'stalled';
  last_activity?: string;
}

export interface Prediction extends Entity {
  type: 'prediction';
  claim: string;
  resolution_date: string;
  status: 'pending' | 'validated' | 'invalidated' | 'partially_validated';
  evidence?: string[];
}

// === RELATIONSHIPS ===

export interface Relationship {
  id: string;
  type: 'supports' | 'contradicts' | 'suggests' | 'validates' | 'challenges' | 'depends_on';
  from: string;
  to: string;
  strength: number; // 1-10
  created: string;
  notes?: string;
}

// === HUMAN LAYER ===

export interface Connection {
  id: string;
  name: string;
  email?: string;
  company?: string;
  position?: string;
  connected_date?: string;
  relationship_strength: RelationshipStrength;
  message_count: number;
  last_message?: string;
  context?: string;
  domains: string[];
  can_ask_for: string[];
  has_asked_you: string[];
  introduces_to: string[];
  notes?: string;
  last_contact?: string;
  contact_frequency?: string;
  positives: string[];
  negatives: string[];
  trust_level?: TrustLevel;
  energy?: EnergyLevel;
}

export interface Network {
  connections: Connection[];
  stats: {
    total: number;
    by_relationship: Record<RelationshipStrength, number>;
    by_domain: Record<string, number>;
    stale_relationships: string[];
  };
  network_gaps: Array<{
    domain: string;
    have: number;
    need: string;
    priority: Priority;
  }>;
}

// === AGENDA ===

export interface AgendaItem {
  id: string;
  action: 'challenge' | 'surface' | 'ask' | 'remind' | 'propose' | 'check';
  target: string;
  reason: string;
  prompt: string;
  priority: Priority;
  added: string;
  source: string;
}

export interface Agenda {
  immediate: AgendaItem[];
  scheduled: Array<{
    id: string;
    type: string;
    target: string;
    check_date: string;
    description: string;
    status: string;
  }>;
  watching: Array<{
    id: string;
    pattern: string;
    target: string;
    reason: string;
    last_evidence?: string;
  }>;
  suggestions: Array<{
    id: string;
    type: string;
    description: string;
    rationale: string;
    thread?: string;
    priority: Priority;
  }>;
}

// === BRAIN STATE ===

export interface BrainState {
  version: string;
  initialized: string;
  last_activity: string;
  architecture: string;
  agents: Record<string, {
    last_run: string;
    runs_total: number;
    mode: string;
  }>;
  capabilities: Record<string, boolean>;
  pending_attention: string[];
  recent_changes: string[];
}

// === FULL BRAIN CONTEXT ===

export interface BrainContext {
  state: BrainState;
  entities: Entity[];
  relationships: Relationship[];
  predictions: Prediction[];
  agenda: Agenda;
  network: Network;

  // Convenience accessors
  beliefs: Belief[];
  threads: Thread[];
}
