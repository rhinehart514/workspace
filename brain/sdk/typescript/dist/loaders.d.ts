/**
 * Brain SDK Loaders
 * Functions to load YAML/JSON brain data
 */
export declare function loadYaml<T>(relativePath: string): T;
export declare function loadJson<T>(relativePath: string): T;
export declare function loadEntities(): any[];
export declare function loadRelationships(): any[];
export declare function loadPredictions(): any[];
export declare function loadAgenda(): any;
export declare function loadNetwork(): any;
export declare function loadState(): any;
export declare function getBrainRoot(): string;
