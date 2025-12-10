# Protocol: Evaluate Codebase

Systematic evaluation of any codebase against the brain's beliefs and principles. Produces a formal judgment with tangible qualities and predictions.

---

## Trigger

- User says "evaluate [path]" or "judge [path]"
- User shares a codebase for analysis
- Brain suggests evaluation of a project

---

## Prerequisites

- Path to codebase (local) or repo URL
- Brief context on what it's supposed to do

---

## Process

### Phase 1: Technical Scan

**Objective:** Understand what this codebase IS, technically.

1. **Stack identification**
   - Language(s)
   - Framework(s)
   - Architecture pattern

2. **Structure analysis**
   - Directory layout
   - Key entry points
   - Package/module organization

3. **Scale assessment**
   - Lines of code (rough)
   - Number of components/modules
   - Test coverage presence

4. **AI integration** (if applicable)
   - Where is AI used?
   - Is it load-bearing or decorative?
   - What happens if AI is removed?

**Output:** Technical summary (3-5 bullet points)

---

### Phase 2: Business Model Scan

**Objective:** Understand what this codebase is TRYING to do.

1. **Value proposition**
   - What problem does it solve?
   - For whom?
   - How urgent is the problem?

2. **Distribution strategy**
   - How do users find this?
   - What's the acquisition channel?
   - Is distribution built-in or bolted-on?

3. **Moat assessment**
   - What type? (context, distribution, network, expertise, none)
   - Is there value accumulation through use?
   - What's defensible vs. replicable?

4. **Revenue model** (if identifiable)
   - How does money flow?
   - Per-user? Usage-based? Enterprise?

**Output:** Business summary (3-5 bullet points)

---

### Phase 3: Principle Check

**Objective:** Evaluate against the brain's criteria.

Run through each principle:

| Principle | Status | Notes |
|-----------|--------|-------|
| Real problem, real urgency | ✓/✗/? | |
| Structural advantage | ✓/✗/? | |
| Clear value capture | ✓/✗/? | |
| AI is load-bearing | ✓/✗/? | |

Run through anti-patterns:

| Anti-pattern | Present? | Evidence |
|--------------|----------|----------|
| Thin wrapper | Y/N | |
| Feature hunting | Y/N | |
| Premature scaling | Y/N | |
| Complexity theater | Y/N | |
| AI decoration | Y/N | |
| Model dependency | Y/N | |

**Output:** Principle assessment table

---

### Phase 4: Tangible Qualities

**Objective:** Find concrete, specific qualities — the actual insights.

For each finding:
- **Quality name:** Short label
- **Finding:** What specifically did you observe?
- **Significance:** high/medium/low
- **Evidence:** Where in the codebase?

Aim for 3-5 tangible qualities.

**Output:** List of tangible qualities

---

### Phase 5: Unresolved Questions

**Objective:** Acknowledge what you couldn't determine.

- What would you need to validate this further?
- What assumptions are you making?
- What's outside the codebase that matters?

**Output:** List of unresolved items

---

### Phase 6: Stance

**Objective:** Take a position.

Choose one:
- **Bullish:** This will likely succeed, I'd bet on it
- **Cautiously optimistic:** Good signs, real concerns
- **Neutral:** Could go either way, insufficient signal
- **Skeptical:** Significant issues, unlikely to succeed as-is
- **Bearish:** Fundamental problems, would bet against

State confidence: speculative / tentative / grounded

**Output:** Stance with reasoning

---

### Phase 7: Predictions

**Objective:** Make falsifiable claims.

For each prediction:
- **Statement:** Specific, observable outcome
- **Check by:** Date to evaluate
- **Confidence:** How sure?

Make 1-3 predictions. These go into the prediction registry.

**Output:** Prediction list

---

## Output Format

```yaml
# Judgment: [target]

judgment:
  target: ""
  date: ""
  context: ""

  technical_summary:
    - ""

  business_summary:
    - ""

  principle_check:
    real_problem:
    structural_advantage:
    clear_value_capture:
    ai_load_bearing:

  antipattern_check:
    thin_wrapper:
    feature_hunting:
    premature_scaling:
    complexity_theater:
    ai_decoration:
    model_dependency:

  tangible_qualities:
    - quality: ""
      finding: ""
      significance:
      evidence: ""

  unresolved:
    - ""

  stance:
  stance_confidence:
  stance_reasoning: ""

  predictions:
    - statement: ""
      check_by: ""
      confidence:
```

---

## Post-Evaluation

1. Add judgment to `_graph/judgments.yaml`
2. Add predictions to `_graph/predictions.yaml`
3. Create project file in `_brain/projects/`
4. Update entities and relationships if new concepts emerged
5. Log evaluation in `_brain/logs/`

---

## Quality Criteria

A good evaluation:
- Finds at least 2-3 tangible qualities (not generic observations)
- Acknowledges what couldn't be resolved
- Takes a stance (even if uncertain)
- Makes at least one falsifiable prediction
- References which beliefs/principles drove the assessment
