/**
 * Brain SDK Loaders
 * Functions to load YAML/JSON brain data
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

// Find brain root (go up from sdk/typescript/src to brain/)
const BRAIN_ROOT = path.resolve(__dirname, '..', '..', '..');

export function loadYaml<T>(relativePath: string): T {
  const fullPath = path.join(BRAIN_ROOT, relativePath);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Brain file not found: ${fullPath}`);
  }
  const content = fs.readFileSync(fullPath, 'utf-8');
  return yaml.load(content) as T;
}

export function loadJson<T>(relativePath: string): T {
  const fullPath = path.join(BRAIN_ROOT, relativePath);
  if (!fs.existsSync(fullPath)) {
    throw new Error(`Brain file not found: ${fullPath}`);
  }
  const content = fs.readFileSync(fullPath, 'utf-8');
  return JSON.parse(content) as T;
}

export function loadEntities(): any[] {
  return loadYaml<{ entities: any[] }>('graph/entities.yaml')?.entities || [];
}

export function loadRelationships(): any[] {
  return loadYaml<{ relationships: any[] }>('graph/relationships.yaml')?.relationships || [];
}

export function loadPredictions(): any[] {
  return loadYaml<{ predictions: any[] }>('graph/predictions.yaml')?.predictions || [];
}

export function loadAgenda(): any {
  return loadYaml<any>('agenda.yaml');
}

export function loadNetwork(): any {
  return loadYaml<any>('human/network.yaml');
}

export function loadState(): any {
  return loadJson<any>('state.json');
}

export function getBrainRoot(): string {
  return BRAIN_ROOT;
}
