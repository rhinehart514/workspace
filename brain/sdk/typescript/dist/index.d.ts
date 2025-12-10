/**
 * Brain SDK
 *
 * Access the shared brain from any project in the monorepo.
 *
 * @example
 * ```typescript
 * import { Brain } from '@workspace/brain';
 *
 * const brain = Brain.load();
 *
 * // Check a belief
 * if (brain.believes('distribution-beats-product')) {
 *   console.log('Focus on distribution!');
 * }
 *
 * // Get belief confidence
 * const confidence = brain.beliefConfidence('small-is-underrated');
 *
 * // Find people who know about sales
 * const salesExperts = brain.network.domainMatches('sales');
 *
 * // Get high-trust connections
 * const trusted = brain.network.highTrust();
 *
 * // Get urgent agenda items
 * const urgent = brain.urgentAgendaItems();
 *
 * // Check pending attention
 * console.log(brain.pendingAttention);
 * ```
 */
export { Brain } from './brain';
export * from './types';
export { getBrainRoot } from './loaders';
