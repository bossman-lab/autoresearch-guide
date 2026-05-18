## 1. The Fundamental Contradiction We Face

In AI-assisted development, efficiency and quality are a pair of competing forces:

| Goal | Approach | Cost for Simple Tasks | Cost for Complex Tasks |
|------|----------|:---:|:---:|
| **Efficiency First** | Pass at once, no iteration | ✅ Fast, saves tokens | ❌ Prone to failure |
| **Quality First** | Multiple iterations, cross-review | ❌ Severe waste | ✅ Quality guaranteed |

**Key Insight**: The two goals are not in conflict — provided the system can automatically determine which path each task should take.

### The Beginning of the Story: A CTO's Expensive Lesson

In late 2025, the CTO of a mid-sized SaaS company saw a report — after his engineering team adopted AI-assisted tools, developers "felt 20% faster." Based on this, he cut 30% of the engineering budget and laid off 4 senior engineers.

Six months later, delivery speed had not improved — it had dropped 15%. Production incidents doubled. The remaining engineers spent hours each day reviewing AI-generated code instead of writing new features.

>"We felt faster — but the data never lies."

This is not an isolated case. In 2026, a randomized controlled trial by the METR research team produced an unsettling number: developers using AI **subjectively felt 20% faster**, but actually completed tasks correctly **19% slower**. The gap between subjective and objective was 39 percentage points.

Why do perception and reality diverge? Because AI **reduces initial time-to-output, but increases verification time**. Writing code that "runs" takes only minutes, but confirming it "is correct" takes several times longer. Perception Faster, Reality Slower — this is the first contradiction this book aims to resolve.

### The AutoResearch Revelation

In 2026, Karpathy's AutoResearch methodology was ported to software development, bringing three core improvements:

1. **Multi-model Cross-Review** — Codex and Claude alternate as implementer and reviewer, eliminating single-model blind spots
2. **5-Dimensional Quantitative Scoring** — Correctness (35%) + Testing (25%) + Code Quality (20%) + Security (10%) + Performance (10%), passing threshold 9.0/10
3. **Feedback-Driven Iteration** — Review comments are injected directly into the next prompt; the Agent sees the issues and improves accordingly

But this approach applied the same treatment to all tasks — 80% of simple tasks wasted 3–8x tokens.

### Three Counter-Intuitive Data Points from 2026

Empirical research in 2026 revealed a deeper problem: **The issue isn't whether AI is fast or slow — it's that the question of good vs. bad has been shifted.**

**① METR Paradox (METR RCT Randomized Controlled Trial)**

> Developers using Claude **subjectively felt 20% faster**, but **completed 19% fewer tasks correctly** within the test time — a subjective-objective gap of 39 percentage points.

Cause: AI **reduces initial time-to-output, but increases verification time**. Developers spend more time understanding, verifying, and fixing AI-generated code. Perceived speedup ≠ actual speedup.

**② Faros Paradox (Faros Engineering Report, 2026)**

> AI-generated code leads to **91% longer PR review times**.

When generation speed increases 3–5x but review capacity doesn't keep pace, the bottleneck shifts from "coding" to "reviewing." Code writing became faster, but the system did not.

**③ DORA Mirror — AI Amplifies Existing Quality**

> The effectiveness of AI tools is highly dependent on codebase health. Staff+ engineers adopt Agents at 2.3x the rate of junior engineers. **AI amplifies existing capability gaps** — good teams use AI better, bad teams use AI worse.

All three data points point to the same conclusion: **Without solving the review and verification problem, AI does not bring efficiency gains — it brings illusory speedup.** Simple tasks can use a single-pass approach to reduce verification burden; complex tasks need multi-round cross-review to ensure quality isn't compromised.

**Our solution**: Fast first, slow second, tiered safety net.

---

## 2. Fast First, Slow Second: Dual-Path Strategy Overview

### Core Idea

```
Every task, upon entry, defaults to the Fast Path.
     │
     ├── Simple task → Single pass → ✅ Delivery (~2-5 minutes)
     │
     └── Complex task / Fast Path failure → Automatically escalated to Slow Path
                               ├── Dual-model cross implementation + review
                               ├── 5-dimensional quantitative scoring
                               ├── Feedback-driven iteration
                               └── ✅ Delivery (~10-30 minutes)
```

### Tier Matrix

| Dimension | Fast Path | Slow Path |
|-----------|----------|-----------|
| **Applicable Scenarios** | Adding/removing fields, config changes, single-file changes, simple bug fixes | Cross-module features, architectural changes, security-sensitive, new systems |
| **Implementation Model** | 1 model (deepseek or configured model) | 2 cross-checking models (e.g., deepseek + claude) |
| **Review Method** | Binary pass/fail | 5-dimensional weighted score ≥ 9.0 |
| **Iteration Mechanism** | Single pass, no iteration | Feedback-driven loop, up to 42 rounds |
| **Typical Duration** | 2-5 minutes | 10-30 minutes |
| **Token Consumption** | 1× | 3-8× |
| **Expected Success Rate** | ~80% | ~95%+ (after iteration) |

### Core Value

```
No waste: 80% of simple tasks go through Fast Path, saving time and tokens
No misses: 20% of complex tasks go through Slow Path safety net, quality guaranteed
```

### ⚠️ Cautionary Case: The "Black Swan" of AI Refactoring

A fintech company decided to use AI to fully refactor its core trading module. The reasoning was "AI writes cleaner code with fewer bugs."

**The reality:**
- The AI-refactored code was indeed "cleaner" — but it lacked understanding of the financial business's exception paths
- In the first week after deployment, a date-handling bug was triggered that only appears on February 29th each year (the AI didn't handle leap-year edge cases)
- The incident caused 4 hours of trading outage, with direct losses exceeding $200K

**Lessons:**
1. AI excels at "writing correct" code, not "knowing what can go wrong"
2. Exception handling for core business logic requires human domain knowledge
3. **The core value of Fast/Slow tiering is not "making AI write more code," but "making the things that should go slow, go slow"**

### 👐 Hands-On: Which Stage Is Your Team In?

**10-question self-assessment for your team's AI effectiveness level:**

| # | Question | Yes/No |
|:-:|---------|:-----:|
| 1 | Does your team have a unified set of AI usage guidelines? | ☐ |
| 2 | Has PR review time noticeably increased after introducing AI? | ☐ |
| 3 | Do you distinguish between "simple tasks" and "complex tasks" for AI? | ☐ |
| 4 | Has AI-generated code ever caused a serious issue discovered only after deployment? | ☐ |
| 5 | Do some team members feel AI-generated code is "good enough"? | ☐ |
| 6 | Do you have a codebase health assessment standard? | ☐ |
| 7 | Can new hires use AI to write code that meets your standards? | ☐ |
| 8 | Do you track the ROI of AI-assisted development? | ☐ |
| 9 | Do core module changes go through stronger human review? | ☐ |
| 10 | Do you have clear boundaries for "when not to use AI"? | ☐ |

**Scoring:** 1 point for each "Yes" answer

| Score | Stage | Recommendation |
|:----:|:----:|--------------|
| **0-3** | Exploration Phase | Read Chapter 3 (AI Context Debt) first — set up infrastructure before running |
| **4-6** | Transition Phase | Suitable for piloting Fast/Slow dual-path, start with low-risk projects |
| **7-8** | Growth Phase | Can roll out broadly, focus on Chapter 10's risk-tiered review |
| **9-10** | Maturity Phase | Skip ahead to Chapter 14 to explore extended modes |
