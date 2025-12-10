# Workspace Brain — Session Instructions

This is a monorepo with a **shared brain** that provides intelligence to all projects. The brain lives at `/brain/` and can be accessed by any project.

---

## Session Start: Load Brain Context

At session start:

1. Check `brain/state.json` for brain status
2. Check `brain/agenda.yaml` for pending actions
3. Detect current project (from working directory)
4. Load project overlay if exists (`.brain.yaml`)

Surface a brief summary:
```
Brain v[version]
Working in: [project name or "root"]
Pending attention: [count]
```

---

## Brain Architecture

```
workspace/
├── brain/                    # SHARED INTELLIGENCE
│   ├── context/              # Beliefs, principles, vocabulary
│   ├── graph/                # Entities, relationships, predictions
│   ├── human/                # Network, profile, patterns
│   ├── agents/               # Reflection, exploration, synthesis
│   ├── sdk/                  # TypeScript + Python access
│   ├── state.json            # Brain state
│   └── agenda.yaml           # Proactive actions
│
├── apps/                     # Deployable applications
├── libs/                     # Shared libraries
└── projects/                 # Independent projects
    └── [project]/
        └── .brain.yaml       # Project-specific overlay
```

---

## Accessing the Brain

### From TypeScript
```typescript
import { Brain } from '@workspace/brain';

const brain = Brain.load();

// Check beliefs
if (brain.believes('distribution-beats-product')) {
  // Apply strategy
}

// Get network
const experts = brain.network.domainMatches('sales');

// Get urgent items
const urgent = brain.urgentAgendaItems();
```

### From Python
```python
from brain import Brain

brain = Brain.load()

# Same interface
if brain.believes('distribution-beats-product'):
    ...

experts = brain.network.domain_matches('sales')
```

---

## Core Beliefs (Hardened)

These are load-bearing — they guide decisions:

- **distribution-beats-product**: Great distribution with good product beats great product with no distribution
- **context-compounds**: Value grows through accumulation, not just creation
- **small-is-underrated**: Lean teams with focus beat bloated teams with resources

---

## Project Context

When working in a project directory:
1. Global brain context loads first
2. Project `.brain.yaml` overlay loads on top
3. Project-specific decisions, conventions, and focus are available

To see current project context:
```bash
cat .brain.yaml
```

---

## Running Brain Agents

```bash
# From workspace root
nx run brain:reflect     # Run reflection agent
nx run brain:explore     # Run exploration agent
nx run brain:synthesize  # Run synthesis agent
nx run brain:curate      # Run curator agent

# Network intelligence report
nx run brain:network-report
```

---

## Adding New Projects

1. Create project in `apps/`, `libs/`, or `projects/`
2. Add `.brain.yaml` with project-specific context
3. Import brain SDK: `import { Brain } from '@workspace/brain'`
4. Project automatically has access to all brain intelligence

---

## Brain Principles

- **Single source of truth**: One brain serves all projects
- **Append-only for hardened**: Never overwrite hardened beliefs
- **Contradictions flagged**: Don't auto-resolve, surface for human decision
- **Evidence-based confidence**: Beliefs move between speculative → tentative → grounded → hardened
- **Network awareness**: Brain knows your people, not just your ideas

---

## Human Layer

The brain knows:
- **Network**: Your connections with positives/negatives, trust levels, energy
- **Patterns**: Your behavioral patterns, blind spots
- **Goals**: Stated vs revealed preferences

Access via:
```python
brain.network.high_trust()
brain.network.domain_matches('sales')
brain.network.draining()  # Connections to be mindful of
```

---

## Proactive Behaviors

At session start, the brain may surface:
- Beliefs that have new counter-evidence
- Stale threads needing attention
- Predictions due for resolution
- Network connections relevant to current work
- Agenda items that need action

The brain speaks first when it has something to say.
