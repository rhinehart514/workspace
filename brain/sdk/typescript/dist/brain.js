"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.Brain = void 0;
const loaders_1 = require("./loaders");
class Brain {
    _state;
    _entities;
    _relationships;
    _predictions;
    _agenda;
    _network;
    constructor(state, entities, relationships, predictions, agenda, network) {
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
    static load() {
        const state = (0, loaders_1.loadState)();
        const entities = (0, loaders_1.loadEntities)();
        const relationships = (0, loaders_1.loadRelationships)();
        const predictions = (0, loaders_1.loadPredictions)();
        const agenda = (0, loaders_1.loadAgenda)();
        const network = (0, loaders_1.loadNetwork)();
        return new Brain(state, entities, relationships, predictions, agenda, network);
    }
    // === STATE ===
    get state() {
        return this._state;
    }
    get version() {
        return this._state.version;
    }
    get capabilities() {
        return this._state.capabilities;
    }
    hasCapability(name) {
        return this._state.capabilities[name] === true;
    }
    // === ENTITIES ===
    get entities() {
        return this._entities;
    }
    get beliefs() {
        return this._entities.filter(e => e.type === 'belief');
    }
    get threads() {
        return this._entities.filter(e => e.type === 'thread');
    }
    entity(id) {
        return this._entities.find(e => e.id === id);
    }
    /**
     * Check if the brain holds a belief
     */
    believes(beliefId) {
        const belief = this.entity(`belief.${beliefId}`) || this.entity(beliefId);
        return belief !== undefined;
    }
    /**
     * Get belief confidence level
     */
    beliefConfidence(beliefId) {
        const belief = this.entity(`belief.${beliefId}`) || this.entity(beliefId);
        return belief?.confidence;
    }
    /**
     * Get entities by type
     */
    entitiesByType(type) {
        return this._entities.filter(e => e.type === type);
    }
    /**
     * Get entities by confidence level
     */
    entitiesByConfidence(confidence) {
        return this._entities.filter(e => e.confidence === confidence);
    }
    // === RELATIONSHIPS ===
    get relationships() {
        return this._relationships;
    }
    /**
     * Get relationships for an entity
     */
    relationshipsFor(entityId) {
        return this._relationships.filter(r => r.from === entityId || r.to === entityId);
    }
    /**
     * Get what supports an entity
     */
    supports(entityId) {
        return this._relationships.filter(r => r.to === entityId && r.type === 'supports');
    }
    /**
     * Get what contradicts an entity
     */
    contradicts(entityId) {
        return this._relationships.filter(r => r.to === entityId && r.type === 'contradicts');
    }
    // === PREDICTIONS ===
    get predictions() {
        return this._predictions;
    }
    /**
     * Get pending predictions
     */
    pendingPredictions() {
        return this._predictions.filter(p => p.status === 'pending');
    }
    /**
     * Get predictions due soon
     */
    predictionsDueBefore(date) {
        const dateStr = date.toISOString().split('T')[0];
        return this._predictions.filter(p => p.status === 'pending' && p.resolution_date <= dateStr);
    }
    // === AGENDA ===
    get agenda() {
        return this._agenda;
    }
    /**
     * Get high-priority agenda items
     */
    urgentAgendaItems() {
        return this._agenda.immediate.filter(item => item.priority === 'high');
    }
    // === NETWORK ===
    get network() {
        return new NetworkAccessor(this._network);
    }
    // === CONVENIENCE ===
    /**
     * Get attention items that need immediate focus
     */
    get pendingAttention() {
        return this._state.pending_attention || [];
    }
    /**
     * Get recent changes to the brain
     */
    get recentChanges() {
        return this._state.recent_changes || [];
    }
}
exports.Brain = Brain;
/**
 * Network accessor for convenient querying
 */
class NetworkAccessor {
    _network;
    constructor(network) {
        this._network = network;
    }
    get connections() {
        return this._network.connections || [];
    }
    get stats() {
        return this._network.stats;
    }
    /**
     * Find connections in a domain
     */
    domainMatches(domain) {
        const domainLower = domain.toLowerCase();
        return this.connections.filter(c => c.domains?.some(d => d.toLowerCase().includes(domainLower)));
    }
    /**
     * Find connections by relationship strength
     */
    byStrength(strength) {
        return this.connections.filter(c => c.relationship_strength === strength);
    }
    /**
     * Get high-trust connections
     */
    highTrust() {
        return this.connections.filter(c => c.trust_level === 'high');
    }
    /**
     * Get energizing connections
     */
    energizing() {
        return this.connections.filter(c => c.energy === 'energizing');
    }
    /**
     * Get draining connections
     */
    draining() {
        return this.connections.filter(c => c.energy === 'draining');
    }
    /**
     * Get a specific connection
     */
    get(id) {
        return this.connections.find(c => c.id === id);
    }
    /**
     * Search connections by name
     */
    search(query) {
        const queryLower = query.toLowerCase();
        return this.connections.filter(c => c.name.toLowerCase().includes(queryLower) ||
            c.company?.toLowerCase().includes(queryLower));
    }
}
//# sourceMappingURL=brain.js.map