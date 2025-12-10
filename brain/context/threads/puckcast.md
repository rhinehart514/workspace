---
entity_id: thread.puckcast
entity_type: thread
created: 2024-12-06
last_explored: 2024-12-06
status: active
graph_synced: true

# Momentum tracking
last_touched: 2024-12-06
touch_count: 1
staleness_threshold_days: 7
stale: true
stale_since: 2024-12-13
---

# Puckcast: NHL Prediction Product

## The Pitch

AI-powered NHL predictions with 60% accuracy. Outputs for each game: winner prediction with probability, confidence level, recommended bet type, key factors summary.

**Current claims:**
- 60% accuracy on historical test data
- Calibrated probability outputs (not just picks)
- Game-by-game explanation of key factors

---

## First Pass: Taxonomy

### Actors
- **NHL bettors** (casual fans who wager occasionally)
- **Sharp bettors** (professionals seeking edge)
- **Hockey fans** (engagement, not betting)
- **Sportsbooks** (DraftKings, FanDuel, BetMGM — the house)
- **Sports media** (ESPN, The Athletic — free alternatives)
- **Data providers** (sell feeds to books, some public)

### Objects
- Game predictions (the core output)
- Probability calibration (60% means 60%)
- Historical track record (proof of performance)
- Betting recommendations (which bet type)
- NHL game data (publicly available)
- Sportsbook odds/lines (efficient, sharp)

### Processes
- Pre-game analysis → prediction generation
- User consumption → betting decision
- Outcome tracking → credibility building
- Community discussion → engagement/retention

### Constraints
- **NHL is niche.** 36.58% of betting is football. NHL is smaller.
- **Sportsbook lines are sharp.** Set by sophisticated algorithms + sharp money.
- **60% accuracy ≠ 60% profit.** After 5% vig, need ~52.4% just to break even.
- **Seasonality.** Oct-June only. Dead 4 months.
- **Free alternatives.** ESPN, The Athletic, social media tipsters.
- **Live betting dominates.** 59.58% of online betting is live. Pre-game predictions miss this.

---

## Second Pass: Topology

### Layers

```
Layer 4: User Decision (bet or not)
        ↑
Layer 3: Prediction Consumption (daily email, app, Discord)
        ↑
Layer 2: Prediction Generation (the AI model)
        ↑
Layer 1: Data (game stats, odds, weather, injuries)
```

### Where Value Could Accumulate

**Option A: User context accumulation**
- Track user's betting history, risk tolerance, bankroll
- Personalize recommendations over time
- Problem: Most prediction products don't do this. Why?

**Option B: Model improvement flywheel**
- Outcomes feed back → model gets better
- Public models can do this too
- No defensibility unless data is proprietary

**Option C: Community/social layer**
- Discord discussions, shared picks, social proof
- Retention through belonging, not just accuracy
- Example: Private sports betting discords are thriving

**Option D: Distribution through output**
- Shareable prediction cards for social
- "I called this" screenshots → viral loop
- Requires memorable format + correct calls

### Key Flows

1. **Attention → Trust → Subscription**
   - Free content hooks (social posts, previews)
   - Track record builds trust
   - Paid tier for full access

2. **Correct prediction → Social proof → Distribution**
   - User shares winning call
   - New users discover
   - Works only if predictions are publicly verifiable

3. **Usage → Context → Better recommendations** (not currently present)
   - Would need to track user preferences
   - Personalization could differentiate

---

## Third Pass: Concept Generation & Reality Check

### The Hard Truth (Post-Research)

Applying domain knowledge from sports-betting-2025.md, ai-landscape-2025.md, distribution-2025.md:

**1. The Accuracy Problem**
- 60% sounds good. But:
- Sportsbooks take ~5% juice (vig)
- Need ~52.4% to break even against the spread
- 60% sounds like 7.6% edge over breakeven
- But: Are we measuring against the spread or moneyline?
- Against efficient closing lines, 60% is exceptional and likely won't hold
- Most public models regress toward ~50-52% over large samples

**2. The Market Position Problem**
- NHL = niche within niche
- Football is 36.58% of market, NHL much smaller
- Smaller market = smaller addressable revenue
- But: Less competition in prediction space

**3. The Distribution Problem**
- How do bettors find this before they've already bet?
- Timing: Predictions need to reach users before game time
- Channel: Email works (daily predictions), but need list first
- Social: TikTok/Instagram for awareness, but prediction content isn't viral
- Community: Discord could work for retention

**4. The Competition Problem**
- Free alternatives: ESPN, The Athletic, Twitter tipsters
- Sharp alternatives: Professional touts, Unabated, PlusEV
- Why pay for Puckcast specifically?

**5. What AI Landscape Winners Have That Puckcast Might Lack**
- Cursor: Clear productivity gain (10x faster coding)
- Midjourney: Visible output, shareable, viral
- ElevenLabs: Creates something new (voice)
- Puckcast: Accuracy claim without clear UX advantage

---

## Strategic Options

### Option 1: Pivot to B2B
Sell predictions/data to sportsbooks or media companies rather than individual bettors.

**Pro:** B2B has budgets, clearer sales motion
**Con:** Sportsbooks have their own models; media wants free content

### Option 2: Entertainment-First, Betting-Second
Position as engagement tool for hockey fans, not betting edge.

**Pro:** Larger audience (fans > bettors), no vig problem
**Con:** Harder to monetize, commoditized space

### Option 3: Double Down on Niche + Community
Build the best NHL betting community. Predictions are the hook, community is the product.

**Pro:** Retention through belonging, word-of-mouth distribution
**Con:** Community building is slow, requires active management

### Option 4: Prove ROI Over Vig
Track and publicize actual betting ROI (after vig), not just accuracy.

**Pro:** Real differentiator if it works
**Con:** If ROI doesn't hold, whole thesis collapses

---

## Questions Raised

1. What's the actual ROI after accounting for vig? (Not accuracy — profit)
2. Is there a distribution wedge we're missing? (Partnership, integration, format)
3. Would the model perform better on specific bet types (totals, props)?
4. Is the real product community + identity, not predictions?
5. Should this be free-with-ads rather than subscription?

---

## Assessment Against Beliefs

| Belief | Application | Implication |
|--------|-------------|-------------|
| belief.small-is-underrated | NHL niche is small | Could be advantage (less competition) or disadvantage (limited TAM) |
| belief.distribution-beats-product | No clear distribution edge | Major weakness; accuracy alone won't distribute |
| belief.context-is-moat | No user context accumulation | Missing the flywheel that would differentiate |
| belief.markets-smaller | Niche of niche | Be realistic about ceiling |
| belief.b2b-underrated | B2B pivot worth exploring | Who would actually pay for this data? |

---

## Verdict: Cautious Skepticism

**What's good:**
- 60% accuracy is meaningful if it holds
- NHL is underserved vs. NFL/NBA
- Calibrated probabilities + transparency could differentiate

**What's concerning:**
- No distribution strategy
- No context flywheel
- Accuracy may not survive vig after large sample
- Seasonality limits revenue
- No clear answer to "why not free alternatives?"

**Hardest question:**
Can you prove positive ROI after vig, consistently, over 500+ bets? If yes, product sells itself. If no, you're selling entertainment, not edge.

---

*Thread status: Explored with enriched 2025 context. Pending: user validation of accuracy claims, distribution strategy discussion.*
