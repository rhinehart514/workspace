/**
 * Brain SDK - Main Brain Class
 *
 * Usage:
 *   import { Brain } from '@workspace/brain';
 *   const brain = Brain.load();
 *
 *   // Query beliefs
 *   if (brain.believes('distribution-beats-product')) { ... }
 *
 *   // Get network
 *   const experts = brain.network.domainMatches('sales');
 */

import {
  BrainContext,
  BrainState,
  Entity,
  Belief,
  Thread,
  Relationship,
  Prediction,
  Agenda,
  Network,
  Connection,
  ConfidenceLevel,
  RelationshipStrength,
} from './types';

import {
  loadEntities,
  loadRelationships,
  loadPredictions,
  loadAgenda,
  loadNetwork,
  loadState,
} from './loaders';

export class Brain {
  private _state: BrainState;
  private _entities: Entity[];
  private _relationships: Relationship[];
  private _predictions: Prediction[];
  private _agenda: Agenda;
  private _network: Network;

  private constructor(
    state: BrainState,
    entities: Entity[],
    relationships: Relationship[],
    predictions: Prediction[],
    agenda: Agenda,
    network: Network,
  ) {
    this._state = state;
    this._entities = entities;
    this._relationships = relationships;
    this._predictions = predictions;
    this._agenda = agenda;
    this._network = network;
  }

  /**
   * Load the brain from disk
   */
  static load(): Brain {
    const state = loadState();
    const entities = loadEntities();
    const relationships = loadRelationships();
    const predictions = loadPredictions();
    const agenda = loadAgenda();
    const network = loadNetwork();

    return new Brain(state, entities, relationships, predictions, agenda, network);
  }

  // === STATE ===

  get state(): BrainState {
    return this._state;
  }

  get version(): string {
    return this._state.version;
  }

  get capabilities(): Record<string, boolean> {
    return this._state.capabilities;
  }

  hasCapability(name: string): boolean {
    return this._state.capabilities[name] === true;
  }

  // === ENTITIES ===

  get entities(): Entity[] {
    return this._entities;
  }

  get beliefs(): Belief[] {
    return this._entities.filter(e => e.type === 'belief') as Belief[];
  }

  get threads(): Thread[] {
    return this._entities.filter(e => e.type === 'thread') as Thread[];
  }

  entity(id: string): Entity | undefined {
    return this._entities.find(e => e.id === id);
  }

  /**
   * Check if the brain holds a belief
   */
  believes(beliefId: string): boolean {
    const belief = this.entity(`belief.${beliefId}`) || this.entity(beliefId);
    return belief !== undefined;
  }

  /**
   * Get belief confidence level
   */
  beliefConfidence(beliefId: string): ConfidenceLevel | undefined {
    const belief = this.entity(`belief.${beliefId}`) || this.entity(beliefId);
    return belief?.confidence;
  }

  /**
   * Get entities by type
   */
  entitiesByType(type: Entity['type']): Entity[] {
    return this._entities.filter(e => e.type === type);
  }

  /**
   * Get entities by confidence level
   */
  entitiesByConfidence(confidence: ConfidenceLevel): Entity[] {
    return this._entities.filter(e => e.confidence === confidence);
  }

  // === RELATIONSHIPS ===

  get relationships(): Relationship[] {
    return this._relationships;
  }

  /**
   * Get relationships for an entity
   */
  relationshipsFor(entityId: string): Relationship[] {
    return this._relationships.filter(r => r.from === entityId || r.to === entityId);
  }

  /**
   * Get what supports an entity
   */
  supports(entityId: string): Relationship[] {
    return this._relationships.filter(r => r.to === entityId && r.type === 'supports');
  }

  /**
   * Get what contradicts an entity
   */
  contradicts(entityId: string): Relationship[] {
    return this._relationships.filter(r => r.to === entityId && r.type === 'contradicts');
  }

  // === PREDICTIONS ===

  get predictions(): Prediction[] {
    return this._predictions;
  }

  /**
   * Get pending predictions
   */
  pendingPredictions(): Prediction[] {
    return this._predictions.filter(p => p.status === 'pending');
  }

  /**
   * Get predictions due soon
   */
  predictionsDueBefore(date: Date): Prediction[] {
    const dateStr = date.toISOString().split('T')[0];
    return this._predictions.filter(p =>
      p.status === 'pending' && p.resolution_date <= dateStr
    );
  }

  // === AGENDA ===

  get agenda(): Agenda {
    return this._agenda;
  }

  /**
   * Get high-priority agenda items
   */
  urgentAgendaItems(): Agenda['immediate'] {
    return this._agenda.immediate.filter(item => item.priority === 'high');
  }

  // === NETWORK ===

  get network(): NetworkAccessor {
    return new NetworkAccessor(this._network);
  }

  // === CONVENIENCE ===

  /**
   * Get attention items that need immediate focus
   */
  get pendingAttention(): string[] {
    return this._state.pending_attention || [];
  }

  /**
   * Get recent changes to the brain
   */
  get recentChanges(): string[] {
    return this._state.recent_changes || [];
  }
}

/**
 * Network accessor for convenient querying
 */
class NetworkAccessor {
  private _network: Network;

  constructor(network: Network) {
    this._network = network;
  }

  get connections(): Connection[] {
    return this._network.connections || [];
  }

  get stats(): Network['stats'] {
    return this._network.stats;
  }

  /**
   * Find connections in a domain
   */
  domainMatches(domain: string): Connection[] {
    const domainLower = domain.toLowerCase();
    return this.connections.filter(c =>
      c.domains?.some(d => d.toLowerCase().includes(domainLower))
    );
  }

  /**
   * Find connections by relationship strength
   */
  byStrength(strength: RelationshipStrength): Connection[] {
    return this.connections.filter(c => c.relationship_strength === strength);
  }

  /**
   * Get high-trust connections
   */
  highTrust(): Connection[] {
    return this.connections.filter(c => c.trust_level === 'high');
  }

  /**
   * Get energizing connections
   */
  energizing(): Connection[] {
    return this.connections.filter(c => c.energy === 'energizing');
  }

  /**
   * Get draining connections
   */
  draining(): Connection[] {
    return this.connections.filter(c => c.energy === 'draining');
  }

  /**
   * Get a specific connection
   */
  get(id: string): Connection | undefined {
    return this.connections.find(c => c.id === id);
  }

  /**
   * Search connections by name
   */
  search(query: string): Connection[] {
    const queryLower = query.toLowerCase();
    return this.connections.filter(c =>
      c.name.toLowerCase().includes(queryLower) ||
      c.company?.toLowerCase().includes(queryLower)
    );
  }
}
