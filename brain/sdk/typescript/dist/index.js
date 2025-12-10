"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
exports.getBrainRoot = exports.Brain = void 0;
const tslib_1 = require("tslib");
var brain_1 = require("./brain");
Object.defineProperty(exports, "Brain", { enumerable: true, get: function () { return brain_1.Brain; } });
tslib_1.__exportStar(require("./types"), exports);
var loaders_1 = require("./loaders");
Object.defineProperty(exports, "getBrainRoot", { enumerable: true, get: function () { return loaders_1.getBrainRoot; } });
//# sourceMappingURL=index.js.map