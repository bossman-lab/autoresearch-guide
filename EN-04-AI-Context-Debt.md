## 4. AI Context Debt: The Deep Problem Fast/Slow Must Solve

The Fast/Slow dual-path solves the "how to execute" problem, but a deeper problem was only clearly defined in 2026 — **AI Context Debt**.

### 4.1 What is AI Context Debt?

Proposed by tech practitioner Abbas Raza in April 2026:

> **AI Context Debt** = The gap between what a codebase knows about itself and what AI tools need to know to generate correct output

### The Tale of Two Teams

**Team A**: An 8-person backend team with a well-maintained codebase, clear module boundaries, and a CI pipeline pass rate consistently above 95%. They introduced AI-assisted coding in 2025.

Result: **2.5x delivery speed increase**. AI-generated code typically passed review on the first try. Newcomer ramp-up time dropped from 3 months to 3 weeks.

**Team B**: The same company, another 10-person product team. Codebase followed a "ship first, refactor later" pattern — modules were tightly coupled, with no unified error handling conventions. They introduced the same AI tools.

Result: **No change in delivery speed, online bug rate up by 40%**. AI generated a pile of code that "runs" but is "wrong". Code review became the bottleneck — everyone was spending time debating "is this what the AI wrote correct?"

Same tools, same model, wildly different results.

> AI effectiveness is highly dependent on codebase health. Good teams use AI to get better; bad teams use AI to get worse. — DORA Mirror Effect

**Concrete manifestations:**

| Your Codebase | AI's Perceived Codebase | Result |
|---------------|------------------------|--------|
| Exception class is `AppException` | Throws generic `Error` | Code violates conventions |
| Logging wrapper with structured fields | Writes `console.log` | Breaks operations dashboards |
| 40,000 lines of old patterns + 8,000 lines of new patterns | Favors old patterns | Generates code incompatible with new tech stack |
| Order status requires querying last log entry | Builds clean table with standard CRUD | Review costs > generation savings |

These errors are **correct at the abstract level**, but **wrong in concrete context**. Traditional technical debt is traceable; AI Context Debt is undetectable until something breaks.

Key conclusion: **The messier the code, the more questionable the AI efficiency gains.**

> MIT 2025 survey: 95% of enterprises have not seen meaningful returns on their AI investments. The reason is not the model. DeepSeek V4 caught up with closed-source flagships in April 2026 — the model supply-side bottleneck is broken. **Organizational knowledge management is the only remaining bottleneck.**

### 4.2 Codebase Health: The Prerequisite for Fast/Slow Effectiveness

The success rate of Fast Path is directly determined by codebase health:

```
Codebase Health          Fast Path Success Rate        Slow Path Rounds
   ⭐⭐⭐⭐⭐                85%+                      1-2 rounds
   ⭐⭐⭐⭐                   70-85%                   2-3 rounds
   ⭐⭐⭐                     50-70%                   3-5 rounds
   ⭐⭐                       <50%                      >5 rounds
   ⭐                      Fast fails frequently       Can't complete at all
```

**If the codebase is unhealthy, Fast Path frequently escalates to Slow Path, and Slow Path requires many rounds to meet the bar — the "speed" of the dual-path gets consumed by context debt.**

### 4.3 The Five Foundational Tasks for Addressing AI Context Debt

Raza proposes five tasks that must be completed before or in parallel with running Fast/Slow:

| # | Task | Description | Owner | Priority |
|:-:|------|-------------|-------|:--------:|
| 1 | **Architecture Rule File** | Tells AI the non-negotiable boundaries of the codebase (module dependency direction, layering conventions, prohibited APIs) | Architect | 🔴 Highest |
| 2 | **System Behavior Document** | Runtime dependencies, failure modes, startup sequence, configuration item meanings | Ops/DevOps | 🔴 High |
| 3 | **Domain Knowledge Document** | Business concepts not readable from code surface — "refunds must write to three tables simultaneously", "shipments over 30 days old require manual processing" | Business/PM | 🔴 High |
| 4 | **Battle-Tested Prompt Template Library** | Standardized prompts for common project tasks, reducing repeated trial-and-error | Tech Lead | 🟡 Medium |
| 5 | **PR Review Standards** | Require AI-assisted code to cite the context and reference files used — force the Agent to explain "what I based this judgment on" | Everyone | 🟡 Medium |

These five tasks map directly to our approach:

| Component in Our Approach | Corresponding Foundational Task |
|---------------------------|-------------------------------|
| **Program.md** | ① Architecture rules + ② System behavior (partial) |
| **"Correctness" dimension in 5-score evaluation** | ⑤ Force Agent to cite context source |
| **SDD team onboarding foundation phase** | ①②③④ all completed during foundation phase |
| **Information retrieval augmentation** | ③ Domain knowledge must be retrievable by the Agent to be referenced |

### 4.4 Brownfield Project Gradual Strategy

The article points out a harsh reality: **Old projects can only be encroached upon, not torn down and rebuilt.**

```
New feature / Refactored module → write spec → run Fast/Slow
         │
         ├── New code has spec ──────────────── ✔️ Quality controllable
         │
         └── Old code has no spec ───────────── ❌ Interfaces not clean
                     │                         State transition conditions hidden in old code
                     ▼
              May break during integration
              (new validation added → old code depends on default behavior when validation doesn't exist)
```

**Strategy**: Don't pursue full coverage; instead, **incremental encroachment**:

1. Every **new feature** writes a spec (from 0% to x%)
2. Every **refactored module** fills in its spec (from x% to y%)
3. Every **production incident** gets documentation (preventing the same issue from being misjudged by AI again)
4. When spec coverage reaches a certain tipping point — **real efficiency returns appear**

> The article's summary from a friend's company is spot-on: "What we're doing with AI now is essentially using an amplifier. If the codebase is clean, it amplifies efficiency and creativity; if the codebase is a tangled mess, it amplifies the chaos."

### 4.5 Integration with Fast/Slow

```
┌─────────────────────────────────────────────────┐
│    Must be done BEFORE running Fast/Slow          │
│                                                   │
│  Step 0: Evaluate codebase health                  │
│  ├── Is there an architecture rule file?           │
│  ├── Are critical business logics documented?      │
│  └── Are module dependencies clear?                │
│                                                   │
│  If all three are "No":                            │
│  └── Extend foundation phase by 1-2 weeks,         │
│      fill documentation first, then run the flow   │
│                                                   │
│  If partially in place:                            │
│  └── Use Program.md to backfill what's missing     │
│      Fast doesn't pass → insufficient context →    │
│      fill documentation → retry                    │
└─────────────────────────────────────────────────┘
```

### 4.6 On Spec-Driven Development (SDD)

The article mentions **Specification-Driven Development** (not our Subagent-Driven Development, but sharing the same acronym) as a complementary concept:

> Specifications subordinate to code → Code subordinates to specifications

GitHub's spec-kit and OpenSpec projects promote "write the spec first, then write the code." Spec files are versioned alongside code, and AI uses the spec as its sole reference during generation.

**Comparison with our approach:**

| SDD (Spec-Driven) | Our Fast/Slow |
|:-----------------:|:-------------:|
| Focuses on **what to write** | Focuses on **how to write well** |
| Spec file is input | Program.md is constraint |
| Suitable for new projects/features | Also applicable to brownfield projects |
| Encourages think-before-write | Encourages try-then-review |

The two are not conflicting and can be chained together:

```
Requirements → SDD (write spec) → Fast/Slow (implement) → Review → Delivery
```

### 4.7 Context Engineering: From Prompt Engineering to Context Engineering

In 2026, "Prompt Engineering" is being replaced by **Context Engineering**. Packmind's Context Engineering guide represents a substantive advance:

**The essential difference:**

| Dimension | Prompt Engineering | Context Engineering |
|-----------|:-----------------:|:------------------:|
| **Focus** | Input quality for a single interaction | Information environment for the entire team |
| **Medium** | Written in a chat box | Version-controlled in the codebase |
| **Maintainer** | Individual | Team (with an owner) |
| **Persistence** | Used once, discarded | Continuously evolving, kept alongside code |
| **Scope** | One model | All tools and Agents |

**Key Data Point:** Stanford/SambaNova 2025 research (ACE) shows that **incremental structured context updates reduce drift and latency by 86% compared to static prompts**. Context, not model size, is the real performance frontier.

#### Layered Context File Approach

Rather than one giant `CLAUDE.md`, organize context hierarchically by directory:

```
/CLAUDE.md              → Project overview, global conventions
/backend/CLAUDE.md      → Backend tech stack, patterns, anti-patterns
/frontend/CLAUDE.md     → Component conventions, state management
/infrastructure/CLAUDE.md → Deployment, environments, toolchain
```

Each file contains clear H2 sections (## Architecture, ## Conventions, ## Testing, ## Commands), and each rule includes exact build/test commands.

**Principle:** A focused 400-token context file is more effective than a 4000-token mishmash.

#### Context Governance (ContextOps)

> "Context engineering will move from a differentiator for innovation to enterprise AI infrastructure in the next 12-18 months." — Neeraj Abhyankar, R Systems VP of Data and AI

**Four ContextOps practices:**

| Practice | Approach |
|----------|----------|
| **Manage as Code** | Context files go in Git, updated alongside code changes, reviewed in PRs |
| **Assign owner** | Each context file has a clear maintainer, reviewed monthly for effectiveness |
| **Metadata annotation** | File headers include `last_updated`, `owner`, `scope`, `reviewed_by` |
| **PR template linkage** | Add a check: does this change affect coding conventions? If so, has the context file been updated? |

#### Integration into Our Approach

Currently our approach uses a single **Program.md** as the constitutional document. The Context Engineering insights suggest:

1. **Program.md can be layered** — a root-level global constitution + sub-contexts for each module
2. **Each rule should ideally include exact commands** — not just "test coverage ≥ 70%", but "run `pytest --cov=src --cov-fail-under=70`"
3. **Context files need version history and an owner** — not something you write and forget
4. **Architecture Decision Records (ADRs) should be injected as context** — the historical context behind key architectural decisions guides AI better than code alone

This doesn't replace the existing Program.md concept, but refines it — evolving from "one constitution" to "a system of context."

### ⚠️ Cautionary Tale: The Startup That Got "AI First, Clean Up Later" Wrong

A 20-person AI startup, after securing funding, decided to "roll out AI tools first, then gradually clean up the code once efficiency improves." Three months later:

- Codebase ballooned from 50,000 lines to 180,000 lines
- 7 different error handling patterns emerged
- The same utility function was "reimplemented" by AI across different files 5 times
- New engineers couldn't understand the old code, so they kept generating new code with AI

**The final cost:**
- Spent 1.5 months on code refactoring, during which all new feature development was paused
- Deleted 40,000 lines of duplicate code after refactoring
- Total loss: roughly 3 months of development time + severely damaged team morale

**Lesson:** Running AI on a dirty codebase is like using a high-speed vacuum cleaner on a garbage pile — it sucks fast, but it's still sucking up garbage.

### 👐 Hands-On: Codebase Health Self-Assessment

**20 questions to evaluate whether your codebase is ready for AI:**

**Part 1: Architecture & Modules (1 point each)**

| # | Question | Yes/No |
|:-:|----------|:------:|
| 1 | Do modules have clear dependency directions (no circular dependencies)? | ☐ |
| 2 | Is there an architecture rules document (module boundaries, layering conventions)? | ☐ |
| 3 | Is error handling consistent across the entire project? | ☐ |
| 4 | Can new features be added without modifying old code? | ☐ |
| 5 | Is the data flow traceable in code (no implicit state)? | ☐ |

**Part 2: Documentation & Knowledge (1 point each)**

| # | Question | Yes/No |
|:-:|----------|:------:|
| 6 | Is core business logic documented? | ☐ |
| 7 | Are key architecture decisions recorded in ADRs? | ☐ |
| 8 | Do configuration items have explanations of their meaning? | ☐ |
| 9 | Are startup and deployment processes documented? | ☐ |
| 10 | Is there a project-level AI context file (CLAUDE.md / Program.md)? | ☐ |

**Part 3: Testing & Quality (1 point each)**

| # | Question | Yes/No |
|:-:|----------|:------:|
| 11 | Is test coverage ≥ 70%? | ☐ |
| 12 | Do critical paths have integration tests? | ☐ |
| 13 | Is CI pipeline pass rate ≥ 95%? | ☐ |
| 14 | Are there automated lint + formatting checks? | ☐ |
| 15 | Is code duplication within a reasonable range? | ☐ |

**Part 4: Tools & Processes (1 point each)**

| # | Question | Yes/No |
|:-:|----------|:------:|
| 16 | Is there a unified code style guide that is enforced? | ☐ |
| 17 | Do PR reviews have a clear standards checklist? | ☐ |
| 18 | Are there boundary rules for "what code AI must not touch"? | ☐ |
| 19 | Does the team have a validation process for AI output? | ☐ |
| 20 | Is there a periodic review mechanism for context files? | ☐ |

**Score Interpretation:**

| Score | Health | Recommendation |
|:----:|:------:|---------------|
| **16-20** | ⭐⭐⭐⭐⭐ | Go straight to Fast/Slow, estimated success rate 85%+ |
| **11-15** | ⭐⭐⭐⭐ | Can start, but extend foundation phase by 1-2 weeks |
| **6-10** | ⭐⭐⭐ | Fill in context files first, then run the flow |
| **0-5** | ⭐⭐ | Not recommended to introduce AI tools yet; pay down technical debt first |
