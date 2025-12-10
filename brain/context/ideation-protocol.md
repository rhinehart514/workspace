# The Ideation Protocol

This document defines how ideation works in this workspace. It applies to any request for ideas, concepts, or exploration of a domain.

---

## Why This Protocol Exists

The default behavior of LLMs when asked for ideas is to generate plausible-sounding concepts quickly. This tends to produce:
- Ideas detached from how domains actually work
- Assumptions carried over from other contexts
- Solutions looking for problems
- Vibes over mechanics

The protocol below forces structure before generation. It keeps ideation grounded in the actual topology of a domain rather than floating in abstraction.

---

## The Sequence

### 1. Taxonomy Pass

Before proposing anything, map the space.

Identify the fundamental elements:
- **Actors**: Who operates here? What are their roles, incentives, and constraints? Not demographics — actual agents with actual motivations.
- **Objects**: What things exist? Products, artifacts, data types, assets, documents, resources.
- **Processes**: What activities matter? Workflows, transactions, cycles, rituals, sequences.
- **Environments**: What contexts or settings shape work? Physical, digital, organizational, temporal.
- **Constraints**: What limits apply? Regulations, costs, technical limitations, cultural norms, structural forces.

Name these pieces explicitly in prose. Don't skip to ideas. The naming itself reveals the domain's shape.

### 2. Topology Pass

After naming elements, map relationships.

- **Layers**: What are the levels of the system? Where does ground-level work happen vs. coordination vs. strategy?
- **Flows**: How does information move? How does value move? How do decisions propagate?
- **Feedback loops**: Where do outputs become inputs? What reinforces itself? What dampens?
- **Bottlenecks**: Where does the system slow down, clog, or fail? What's scarce?
- **Tensions**: Where do competing forces create pressure? What tradeoffs define the space?

This pass produces a structural picture — a map of how the domain actually works mechanically, not how people talk about it.

### 3. Concept Generation

Only after taxonomy and topology are clear, generate ideas.

For each concept:
- **Name**: A clear label
- **Category**: What kind of thing is this? Tool, platform, layer, module, marketplace, portal, workflow system, intelligence layer — be specific
- **Scope**: Micro-tool (days to build), feature (weeks), product (months), platform (ongoing)
- **Mechanism**: What does it actually do? How does it work? If AI is involved, describe what the AI does mechanically — not "AI-powered" but the specific function
- **Defensibility**: What makes this hard to replicate? Data accumulation, network effects, integration depth, expertise, speed — or nothing
- **Concerns**: What's weak about this? What avoidance patterns does it risk?

Ideas are framed by the structure that precedes them. They point to specific elements and relationships from the taxonomy and topology.

---

## Operating Rules

**Reset assumptions**. Every new ideation request starts from zero unless explicitly anchored. Past contexts don't apply unless invoked. Frameworks from other domains don't transfer unless the user says so.

**Describe AI as mechanism**. When AI appears in a concept, explain what it does: reduces cost of X, speeds up Y, improves accuracy of Z, enables decision quality at scale. Not magic — mechanics.

**Preserve optionality**. Multiple framings. Multiple directions. Multiple interpretations. The user picks; the LLM deepens. No prescribing, no pigeonholing, no premature narrowing.

**Prose by default**. Respond in clean prose unless the user asks for lists or structured output. Prose forces precision.

**No hype**. Analytical tone. No promotional language. No enthusiasm where analysis belongs. Neutral and direct.

---

## When the Protocol Applies

Any request that involves:
- "What could we build in [domain]?"
- "Explore [space] for opportunities"
- "Generate ideas for [problem area]"
- "What's possible in [vertical]?"
- Variations of "help me think through [topic]"

If in doubt, run the protocol. The taxonomy and topology passes are never wasted — they either reveal opportunity or reveal that there isn't one.
