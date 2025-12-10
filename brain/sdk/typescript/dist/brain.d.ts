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
import { BrainState, Entity, Belief, Thread, Relationship, Prediction, Agenda, Network, Connection, ConfidenceLevel, RelationshipStrength } from './types';
export declare class Brain {
    private _state;
    private _entities;
    private _relationships;
    private _predictions;
    private _agenda;
    private _network;
    private constructor();
    /**
     * Load the brain from disk
     */
    static load(): Brain;
    get state(): BrainState;
    get version(): string;
    get capabilities(): Record<string, boolean>;
    hasCapability(name: string): boolean;
    get entities(): Entity[];
    get beliefs(): Belief[];
    get threads(): Thread[];
    entity(id: string): Entity | undefined;
    /**
     * Check if the brain holds a belief
     */
    believes(beliefId: string): boolean;
    /**
     * Get belief confidence level
     */
    beliefConfidence(beliefId: string): ConfidenceLevel | undefined;
    /**
     * Get entities by type
     */
    entitiesByType(type: Entity['type']): Entity[];
    /**
     * Get entities by confidence level
     */
    entitiesByConfidence(confidence: ConfidenceLevel): Entity[];
    get relationships(): Relationship[];
    /**
     * Get relationships for an entity
     */
    relationshipsFor(entityId: string): Relationship[];
    /**
     * Get what supports an entity
     */
    supports(entityId: string): Relationship[];
    /**
     * Get what contradicts an entity
     */
    contradicts(entityId: string): Relationship[];
    get predictions(): Prediction[];
    /**
     * Get pending predictions
     */
    pendingPredictions(): Prediction[];
    /**
     * Get predictions due soon
     */
    predictionsDueBefore(date: Date): Prediction[];
    get agenda(): Agenda;
    /**
     * Get high-priority agenda items
     */
    urgentAgendaItems(): Agenda['immediate'];
    get network(): NetworkAccessor;
    /**
     * Get attention items that need immediate focus
     */
    get pendingAttention(): string[];
    /**
     * Get recent changes to the brain
     */
    get recentChanges(): string[];
}
/**
 * Network accessor for convenient querying
 */
declare class NetworkAccessor {
    private _network;
    constructor(network: Network);
    get connections(): Connection[];
    get stats(): Network['stats'];
    /**
     * Find connections in a domain
     */
    domainMatches(domain: string): Connection[];
    /**
     * Find connections by relationship strength
     */
    byStrength(strength: RelationshipStrength): Connection[];
    /**
     * Get high-trust connections
     */
    highTrust(): Connection[];
    /**
     * Get energizing connections
     */
    energizing(): Connection[];
    /**
     * Get draining connections
     */
    draining(): Connection[];
    /**
     * Get a specific connection
     */
    get(id: string): Connection | undefined;
    /**
     * Search connections by name
     */
    search(query: string): Connection[];
}
export {};
