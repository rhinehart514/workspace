"use strict";
/**
 * Brain SDK Loaders
 * Functions to load YAML/JSON brain data
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadYaml = loadYaml;
exports.loadJson = loadJson;
exports.loadEntities = loadEntities;
exports.loadRelationships = loadRelationships;
exports.loadPredictions = loadPredictions;
exports.loadAgenda = loadAgenda;
exports.loadNetwork = loadNetwork;
exports.loadState = loadState;
exports.getBrainRoot = getBrainRoot;
const tslib_1 = require("tslib");
const fs = tslib_1.__importStar(require("fs"));
const path = tslib_1.__importStar(require("path"));
const yaml = tslib_1.__importStar(require("js-yaml"));
// Find brain root (go up from sdk/typescript/src to brain/)
const BRAIN_ROOT = path.resolve(__dirname, '..', '..', '..');
function loadYaml(relativePath) {
    const fullPath = path.join(BRAIN_ROOT, relativePath);
    if (!fs.existsSync(fullPath)) {
        throw new Error(`Brain file not found: ${fullPath}`);
    }
    const content = fs.readFileSync(fullPath, 'utf-8');
    return yaml.load(content);
}
function loadJson(relativePath) {
    const fullPath = path.join(BRAIN_ROOT, relativePath);
    if (!fs.existsSync(fullPath)) {
        throw new Error(`Brain file not found: ${fullPath}`);
    }
    const content = fs.readFileSync(fullPath, 'utf-8');
    return JSON.parse(content);
}
function loadEntities() {
    return loadYaml('graph/entities.yaml')?.entities || [];
}
function loadRelationships() {
    return loadYaml('graph/relationships.yaml')?.relationships || [];
}
function loadPredictions() {
    return loadYaml('graph/predictions.yaml')?.predictions || [];
}
function loadAgenda() {
    return loadYaml('agenda.yaml');
}
function loadNetwork() {
    return loadYaml('human/network.yaml');
}
function loadState() {
    return loadJson('state.json');
}
function getBrainRoot() {
    return BRAIN_ROOT;
}
//# sourceMappingURL=loaders.js.map