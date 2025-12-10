"""
Brain SDK Loaders
Functions to load YAML/JSON brain data
"""

import json
from pathlib import Path
from typing import Any, TypeVar

import yaml

T = TypeVar('T')

# Find brain root (go up from sdk/python/brain to brain/)
BRAIN_ROOT = Path(__file__).parent.parent.parent.parent


def get_brain_root() -> Path:
    """Get the brain root directory."""
    return BRAIN_ROOT


def load_yaml(relative_path: str) -> Any:
    """Load a YAML file from the brain directory."""
    full_path = BRAIN_ROOT / relative_path
    if not full_path.exists():
        raise FileNotFoundError(f"Brain file not found: {full_path}")
    with open(full_path, 'r') as f:
        return yaml.safe_load(f)


def load_json(relative_path: str) -> Any:
    """Load a JSON file from the brain directory."""
    full_path = BRAIN_ROOT / relative_path
    if not full_path.exists():
        raise FileNotFoundError(f"Brain file not found: {full_path}")
    with open(full_path, 'r') as f:
        return json.load(f)


def load_entities() -> list:
    """Load all entities from the graph."""
    data = load_yaml('graph/entities.yaml')
    return data.get('entities', []) if data else []


def load_relationships() -> list:
    """Load all relationships from the graph."""
    data = load_yaml('graph/relationships.yaml')
    return data.get('relationships', []) if data else []


def load_predictions() -> list:
    """Load all predictions from the graph."""
    data = load_yaml('graph/predictions.yaml')
    return data.get('predictions', []) if data else []


def load_agenda() -> dict:
    """Load the agenda."""
    return load_yaml('agenda.yaml') or {}


def load_network() -> dict:
    """Load the network."""
    return load_yaml('human/network.yaml') or {'connections': []}


def load_state() -> dict:
    """Load the brain state."""
    return load_json('state.json')
