---
title: "Fast/Slow Dual-Path: A Tiered Quality Assurance System for AI-Assisted Development"
date: 2026-05-18
author: "Lantern Keeper"
tags: [AI, Agent, AutoResearch, Quality Engineering, FastSlow, Hermes]
---

> **One-sentence summary**: Don't waste tokens on 80% simple tasks with multi-round iteration; don't sacrifice quality on 20% complex tasks with a single pass.


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


## 2. The Third Paradigm Shift in Quality Engineering

### The Three Stages of Software Quality

Software quality assurance has undergone two complete paradigm shifts over the past thirty years, and a third is unfolding before our eyes.

**First Paradigm (1990s–2000s): The Era of Manual Testing.**

Quality was the QA team's job. Developers would "throw code over the wall," and testing teams manually executed test cases, wrote test reports, and organized release reviews. A typical enterprise application release cycle was 6–18 months. Quality was measured by defect density (defects/KLOC), and QA teams were typically 1/3 to 1/2 the size of development teams. The 1999 Standish Group report showed that only 28% of projects were delivered on time and on budget, with quality issues being the number one cause.

The core assumption of this paradigm was: *"Writing code is slow; testing can be even slower."*

**Second Paradigm (2000s–2020s): The Era of Automated Testing.**

Practices such as Continuous Integration (CI), Test-Driven Development (TDD), Behavior-Driven Development (BDD), and shift-left testing emerged. DORA metrics (Deployment Frequency, Lead Time for Changes, Change Failure Rate, Time to Restore Service) became industry standards. Quality shifted from "QA's responsibility" to "everyone's responsibility" — developers wrote their own unit tests, and CI pipelines automatically ran thousands of test cases. Release cycles compressed from months to days or even hours.

The core assumption of this paradigm was: *"Automation can keep up with the speed of writing code."*

**Third Paradigm (2020s–): Quality in the AI Era.**

The fundamental question has shifted entirely — it is no longer *"how to write correct code"* but *"how to verify that AI-generated code is correct."* When AI coding assistants generate code at 5–10x human speed, the bottleneck shifts from *generation* to *verification*. Your team can produce in one hour what would have taken a week to write, but if you're still using manual line-by-line review and manual test execution, release cycles will increase rather than decrease.

The core dilemma of this paradigm is: *"Generation is too fast, verification is too slow, and old tools have failed."*

### Echoes from History: Microsoft's Vista Lesson and the AI Transformation of Today

In 2001, Microsoft's Windows team had approximately 5,000 developers and 3,000 testers. The development cycle for Windows XP was 18 months, with manual testing processes consuming about 60% of that time. Quality was acceptable.

Then Microsoft launched the Windows Vista (codenamed Longhorn) project. Between 2002 and 2006, the Windows codebase ballooned to over 50 million lines of code. But the quality assurance process barely changed — still relying on manual test plan execution and QA team final verification. The result is well-known: Vista was delayed two years, shipped with a record number of bugs, and became the biggest commercial and reputational disaster in Microsoft's history.

Vista's failure directly triggered a quality revolution inside Microsoft. In 2004, Microsoft Research began promoting "Spec Explorer" — a model-based automated testing tool. By 2006, the Windows team had converted thousands of manual test cases into automated tests. The 2008 Windows 7 project adopted "Quality-First Development," pushing automated test coverage from less than 20% to over 70%. Windows 7's release quality far exceeded Vista's, with a bug-fix rate 40% higher than Vista's during the same period.

This inflection pattern is strikingly similar to today's AI transformation:

| Phase | 2000s Microsoft | 2020s AI Coding |
|-------|----------------|-----------------|
| Speed Multiplication | XP→Vista code explosion | AI-generated code 5–10x speedup |
| Bottleneck Failure | Manual testing couldn't keep up with code volume | Manual review can't keep up with AI generation |
| Catalyzing Event | Vista quality disaster | Not yet arrived (but approaching) |
| Solution | Large-scale migration to automated testing | Unknown (AI-driven verification?) |

History doesn't repeat itself exactly, but it rhymes. When generation speed crosses a critical threshold, the verification system must evolve in response, or quality collapse is inevitable.

### TDD's Failure in the AI Era

**Story:** In early 2024, the engineering team at a mid-sized SaaS company decided to strictly adhere to Test-Driven Development even after introducing GitHub Copilot and Cursor. The team lead was a devout TDD believer — "write tests first, then write code, ensure every behavior has test coverage."

The first two weeks went smoothly. In the third week, anomalies emerged: developers found that Copilot generated code so fast they couldn't keep up writing tests in advance. Worse, Copilot sometimes produced unexpected implementation approaches — not "wrong," but "another correct way" — causing already-written tests to fail. Developers started "writing code first, then backfilling tests, pretending they wrote tests first." By the sixth week, the team's actual TDD compliance rate had plummeted from 92% to 18%.

**Why does TDD fail in the AI era?**

TDD's underlying assumption is: *"You wrote the code, you know what the code should do."* When a developer writes a test, they already have a precise behavioral expectation in mind. The conversational workflow of AI coding assistants breaks this assumption — AI may produce implementations you didn't think of, use libraries you hadn't considered, or even refactor parts you're unfamiliar with.

The correct stance in the AI era is not Test-Driven, but **Test-Everywhere**:

- **Don't presuppose the implementation path.** Instead of writing tests in advance to "dictate" what AI should do, generate the code first, then write tests that verify its actual behavior.
- **Verification over drive.** Shift focus from "driving design" to "verifying results." The role of tests changes from a *design tool* to a *quality guardrail*.
- **AI-assisted test generation.** Let AI help you generate test cases — not derived from code, but from requirements documentation and boundary conditions.

### Failure Case: A Team Locked in the Old Paradigm

In 2024, an e-commerce platform team discovered a counter-intuitive result after fully adopting AI coding tools (Copilot + Claude).

Team structure: 40 developers, 12 QA engineers. Process: developers use AI for coding, submit PR after completion → QA manually executes functional tests → regression testing → release approval. This was exactly the same process they had established in 2019 — only the development side had been swapped to AI.

**Three-month data comparison:**

| Metric | Before AI (2023 Q4) | After AI (2024 Q1) | Change |
|--------|---------------------|--------------------|--------|
| Average daily lines of code per developer | 120 lines | 680 lines | +467% |
| Average daily PR submissions | 8 | 47 | +488% |
| Average PRs processed per QA per day | 6 | 6 (unchanged) | 0% |
| Average PR wait time for review | 4 hours | 31 hours | +675% |
| Feature release cycle | 5.2 days | 7.3 days | **+40%** |
| Production defect rate | 3.1% | 4.8% | +55% |
| QA team overtime rate | 12% | 67% | +458% |

**Diagnosis:** Development speed increased 5x, but the quality verification process remained unchanged. The QA team became the bottleneck, and the release cycle actually lengthened by 40%. More ironically, due to increased release pressure and review fatigue, the production defect rate also rose.

**Lesson:** Accelerating only the "generation" side without upgrading the "verification" side results in decreased rather than increased overall delivery speed. This trap is identical to what the Windows Vista team experienced in 2006 — code volume increased while testing processes stayed in place.

### Which Paradigm Is Your Team In?

The following 8 questions will help you self-diagnose which quality paradigm your team's practices belong to. For each question, choose the description that best fits your team (1–3 points).

| # | Question | First Paradigm (1 point) | Second Paradigm (2 points) | Third Paradigm (3 points) |
|---|---------|-------------------------|---------------------------|--------------------------|
| 1 | Who executes most tests? | Dedicated QA team manually | Developers write automated tests, CI runs them automatically | AI-assisted test generation, strategy auto-orchestrated by verification framework |
| 2 | How is code review done? | In-person meetings, line-by-line | Asynchronous PR review with checklist | AI performs initial review, humans spot-check disputed parts |
| 3 | How frequent are releases? | Every 1–6 months | Daily to weekly | Multiple times per day, on-demand |
| 4 | What metrics define quality? | Defect density (defects/KLOC) | DORA metrics + test coverage | Production validation (canary, blue-green, chaos engineering) |
| 5 | How are requirement changes handled? | Change control board approval, freeze periods | CI/CD pipeline, feature flags | Real-time A/B testing, auto-rollback |
| 6 | When are defects typically discovered? | System testing or UAT phase | Development phase (unit/integration tests) | During coding or minutes before release (AI review + production validation) |
| 7 | How is test data managed? | Manually constructed static datasets | Scripted generation + database snapshots | AI-generated boundary cases + production traffic replay |
| 8 | What is the team's perception of "quality"? | "Quality is QA's job" | "Quality is everyone's job" | "Quality is the system's job" (AI + automation + observability) |

**Scoring Reference:**
- **8–12 points:** Your team is still in the First Paradigm. Introducing AI coding tools will create a serious quality bottleneck. Prioritize automating core manual tests.
- **13–20 points:** Your team is in the Second Paradigm. This is where most mature engineering teams currently sit. Start experimenting with AI-assisted verification processes.
- **21–24 points:** Your team has entered the early stages of the Third Paradigm. The verification system's evolution has kept pace with code generation speed.

---

**Core Thesis:** Every paradigm shift in quality engineering is, at its heart, the process of verification speed catching up to generation speed. From manual to automated, from automated to AI-driven verification, the underlying logic has never changed — *generation acceleration inevitably demands verification acceleration, or quality will collapse.* Microsoft's Vista story is not history — it is being replayed in every team that adopts AI coding tools while neglecting quality infrastructure.


## 3. Fast Path Architecture

Fast Path is the existing `subagent-driven-development` skill (SDD) in Hermes Agent.

It is a **three-phase, four-step** pipeline:

### A Typical Fast Path Work Log

> Real case: Adding filter conditions to the order list for an e-commerce backend.

**Task Description:** Add `status` and `date_range` filters to the Order List API, returning paginated results.

**Step 1 — Implementation Subagent Work Log (excerpt):**
```
Subagent starts → reads API docs → writes tests (test_filter_by_status, test_filter_by_date_range)
→ first test FAIL (expected) → writes implementation (modifies ListOrders handler)
→ second test PASS → runs full test suite → all pass
→ git commit -m "feat: add status and date_range filters to ListOrders"
Time elapsed: 4 min 23 sec
```

**Step 2 — Spec Review:**
```
✅ All requirements implemented
✅ No scope creep
✅ Interface signature conforms to project REST conventions
```

**Step 3 — Quality Review:**
```
✅ Code style consistent, follows project error handling patterns
✅ Test coverage includes happy path + edge cases (empty results, invalid status values)
⚠️ Suggestion: date_range format validation could be stricter (currently only checks for non-empty)
→ Fixed and re-reviewed — PASSED
Total time: 6 min 47 sec
```

This task would normally take 30–60 minutes with manual coding + manual review. Fast Path compressed it to under 7 minutes. The key point: **it's not that humans are slower — it's that the AI is constrained to a sufficiently narrow scope and doesn't need to repeatedly confirm upstream intent.**

```
Task enters
    │
    ▼
┌───────────────────────────────────┐
│ Phase 1: Single Task Execution     │
│                                   │
│ Step 1: Implementation Subagent   │
│   • Read task → TDD (write test → implement) │
│   • pytest verification — all pass │
│   • git commit                     │
└─────────────────┬─────────────────┘
                  ▼
┌───────────────────────────────────┐
│ Phase 2: Two-Stage Review         │
│                                   │
│ Step 2: Spec Review               │
│   • Are all requirements implemented? │
│   • Any scope creep?              │
│   └── Pass → continue             │
│       └── Fail → fix and re-review │
│                                   │
│ Step 3: Quality Review            │
│   • Code style / error handling / tests │
│   └── Pass → mark complete        │
│       └── Fail → fix and re-review │
└─────────────────┬─────────────────┘
                  ▼
Next task / ✅ Complete
```

### Three Design Principles

**Principle 1: One Dedicated Subagent Per Task**

```
❌ Wrong: One Subagent handles all tasks
   → Context keeps piling up, Agent starts getting confused

✅ Correct: A new Subagent for each task
   → Each Subagent only sees the information it needs
   → Clean context = fewer hallucinations
```

**Principle 2: Two-Stage Review Separates Concerns**

Spec review checks "did you build the right thing," quality review checks "did you build it well" — different reviewers focus on different aspects.

**Principle 3: Review Feedback Must Be Closed-Loop**

```
Issue found → Fix → Re-review → APPROVED
                  ↑           │
                  └── Still broken ┘
```

No "fix it later" allowed.

### Fast Path Implementation Code

```python
# Step 1: Implementation
result = delegate_task(
    goal=task.description,
    context=f"""
    Follow the TDD workflow:
    1. Write tests → pytest verifies FAIL
    2. Write implementation → pytest verifies PASS
    3. Run full test suite
    """,
    toolsets=['terminal', 'file']
)

# Step 2: Spec Review
spec_review = delegate_task(
    goal="Spec compliance review",
    context=f"""
    Original task requirements: {task.full_text}
    Check:
    - [ ] Are all requirements implemented?
    - [ ] Any scope creep?
    - [ ] Do the interfaces/signatures match expectations?
    """
)

# Step 3: Quality Review
quality_review = delegate_task(
    goal="Code quality review",
    context=f"""
    Check:
    - [ ] Does code style match project conventions?
    - [ ] Is error handling thorough?
    - [ ] Is test coverage ≥ 70%?
    - [ ] No security concerns?
    """
)
```

### ⚠️ Anti-Pattern: One Subagent Doing Everything

A startup had a single Subagent process 8 related tasks consecutively. By the 5th task, the Subagent began showing "hallucination decay":

- Confused the requirement boundaries between different tasks (wrote logic from Task A into Task B's code)
- Re-introduced utility functions that already existed (too much information in the context — it couldn't "see" them anymore)
- Code review for the 7th task found 5 issues, 3 of which had already been resolved earlier

**Root Cause:** Each Subagent's context window is limited. When one Subagent carries the context of 8 tasks, its effective attention allocated to the "new instructions" shrinks progressively.

**Lesson:**
- One new Subagent per task → clean context
- Don't reuse a Subagent unless there is a clear sequential dependency
- "Saving the cost of spinning up one Subagent" is not worth bug-ridden code

### 👐 Hands-On: Task Decomposition Exercise

**Give your team a real task and try breaking it down into "Fast Path granularity":**

**Original Task:** `Add a "batch import" feature to the user module, supporting CSV upload, data validation, and failed-record export.`

**Decomposition Principles:**
- Each subtask: modifies ≤ 2 files, does not cross module boundaries
- Each subtask: can be completed independently by a Subagent in under 10 minutes
- Each subtask: review focuses on one clear area of concern

**Exercise: Break the above task into 4–6 Fast Path subtasks**

| Subtask | Scope | Est. Time | Review Focus |
|---------|-------|:---------:|--------------|
| _Example: CSV Parser_ | `parser.py` + tests | 5 min | Format compatibility, invalid character handling |
| 1. ________________ | __________ | __ min | ________________ |
| 2. ________________ | __________ | __ min | ________________ |
| 3. ________________ | __________ | __ min | ________________ |
| 4. ________________ | __________ | __ min | ________________ |

**Reference Answer (check after filling yours in):**

| Subtask | Scope | Est. Time | Review Focus |
|---------|-------|:---------:|--------------|
| CSV Parser | `parser.py` + tests | 5 min | Field mapping, encoding handling |
| Data Validation Logic | `validator.py` + tests | 5 min | Required-field checks, format validation |
| Batch Database Insert | `importer.py` + tests | 5 min | Transaction handling, performance |
| Failed-Record Export | `exporter.py` + tests | 5 min | Error code output format |
| API Interface Layer | `handler.py` + `router.py` | 8 min | Parameter validation, status codes |
| Frontend Upload UI | `upload.vue` + components | 8 min | File size limits, progress bar |

---


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


## 5. When to Upgrade to Slow Path?

Fast Path failure does not necessarily mean an upgrade — **only specific conditions trigger an upgrade**.

### Upgrade Trigger Conditions

| # | Condition | Action |
|:-:|-----------|--------|
| 1 | Review finds **architecture-level issues** ("this design might not be right") | 🔺 Upgrade immediately |
| 2 | Review lists **3+ serious issues** | 🔺 Upgrade immediately |
| 3 | Same task **fails Fast review 2 times consecutively** | 🔺 Upgrade |
| 4 | Task involves payments/security/user data | 🔺 Directly go Slow |
| 5 | Task modifies **3+ files** and crosses modules | 🔺 Directly go Slow |
| 6 | Implementation Subagent **actively reports** "needs multiple iterations" | 🔺 Respect agent judgment |
| 7 | None of the above conditions are met, review fails | ⟳ Minor fix then re-review |

### Core Decision Function

```python
def should_upgrade(task, review_result, failure_count):
    # Condition 4/5: Pre-assessed complexity
    if "security" in task.get("tags", []) or task.get("cross_module"):
        return True
    
    # Condition 1/2: Severe review results
    if review_result.contains("architecture") or count_serious_issues(review_result) >= 3:
        return True
    
    # Condition 3: Consecutive failures
    if failure_count >= 2:
        return True
    
    # Condition 6: Agent self-report
    if "multiple iterations" in str(review_result):
        return True
    
    return False  # Stay on Fast Path, fix and re-review
```


---

## 6. Slow Path Architecture

Slow Path adds three layers of enhancement on top of Fast Path:

```
Fast Path Architecture
    +
    ├── ① Constitution Injection (Program.md)
    ├── ② Dual-Model Cross-Review (A writes B reviews / B writes A reviews)
    ├── ③ 5-Dimension Quantitative Scoring (Passing threshold: 9.0)
    └── ④ Feedback-Driven Loop (until pass or termination)
```

### Overall Flow

```
Task enters Slow Path
    │
    ▼
[Step 0] Inject Program.md constitutional rules
    │
    ▼
┌── Iteration Loop ──────────────────────────────────┐
│                                                      │
│  [Step 1] Role Assignment                            │
│    Odd rounds: Agent A implements → Agent B reviews  │
│    Even rounds: Agent B implements → Agent A reviews │
│                                                      │
│  [Step 2] Implementation                             │
│    Receives: task description + previous feedback + score history │
│    Produces: code + passing tests                    │
│                                                      │
│  [Step 3] 5-Dimension Scoring                        │
│    Dimensions: Correctness 35% Tests 25% Quality 20% Security 10% Performance 10% │
│    Passing: ≥ 9.0                                    │
│                                                      │
│  [Step 4] Decision                                   │
│    ├─ Pass → ✅ Auto-merge                           │
│    ├─ Score stagnation → ⛑️ Human intervention       │
│    ├─ Timeout → ⛑️ Human intervention                │
│    └─ Not passed → Collect feedback → Next round     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Iteration Engine Pseudocode

```python
def slow_path(task, program_md):
    models = ["deepseek", "claude"]  # Two different models
    scores = []
    max_rounds = 42
    
    for round in range(1, max_rounds + 1):
        # Rotate roles
        impl_idx = 0 if round % 2 == 1 else 1  # Implementer index
        rev_idx = 1 if round % 2 == 1 else 0    # Reviewer index
        
        # Step 1: Implementation
        implementation = delegate_task(
            goal=f"Round {round} - {models[impl_idx]} implement",
            context=f"""
            ## Program.md Constitution
            {program_md}
            
            ## Previous Round Feedback (injected into this round)
            {json.dumps(scores[-1]["issues"]) if scores else "First implementation, no history"}
            
            ## Score History
            {json.dumps([s["weighted_total"] for s in scores])}
            
            ## Task
            {task.full_text}
            """
        )
        
        # Step 2: Review + 5-Dimension Scoring
        review = delegate_task(
            goal=f"Round {round} - {models[rev_idx]} review & score",
            context=f"""
            Score on the following dimensions (1-10):
            - Correctness × 0.35
            - Test Coverage × 0.25
            - Code Quality × 0.20
            - Security × 0.10
            - Performance × 0.10
            
            Passing: Weighted total ≥ 9.0
            
            Output JSON:
            {{"scores": {{...}}, "weighted_total": N,
              "issues": [...], "verdict": "PASS|NEEDS_WORK"}}
            """
        )
        
        review_data = json.loads(review)
        scores.append(review_data)
        
        # Passed?
        if review_data["weighted_total"] >= 9.0:
            return {"status": "approved", "rounds": round, "scores": scores}
        
        # Dynamic termination: 3 consecutive rounds with no improvement
        if round >= 4 and not is_improving([s["weighted_total"] for s in scores[-4:]]):
            return {"status": "escalate", "reason": "Score stagnation", "scores": scores}
    
    return {"status": "escalate", "reason": "Max rounds exceeded", "scores": scores}
```

---

---

## 7. Core Mechanisms Explained

### 7.1 Program.md — Agent Constitution

Program.md is the behavioral code of conduct for all Agents, injected at each Slow Path startup.

```markdown
# Program.md

## Permission Boundaries
- Allowed: Modify src/, internal/, cmd/
- Forbidden: Modify .github/, CI/CD, program.md itself

## Code Standards
- Functions ≤ 50 lines, files ≤ 500 lines
- All public methods must have doc comments
- No magic numbers; extract as constants
- Errors must be handled (no `_` ignore allowed)

## Test Standards
- Coverage ≥ 70%
- Table-driven tests
- Test naming: Test<Function>_<Scenario>
- Forbidden: time.Sleep, external HTTP dependencies

## Scoring Dimensions
| Dimension | Weight | Evaluation Content |
|-----------|--------|-------------------|
| Correctness | 35% | Is functionality completely correct? |
| Tests | 25% | Coverage, edge cases |
| Code Quality | 20% | Readability, maintainability |
| Security | 10% | Input validation, permissions |
| Performance | 10% | Time complexity, resource usage |

Passing threshold: Weighted total ≥ 9.0/10
```

**Why a constitution file?**
- Eliminate ambiguity: Every Agent reads the same set of rules
- Permission boundaries: Prevent Agents from doing things they shouldn't
- Unified standards: Consistent evaluation scales across different models
- Auditability: All decision rules are traceable

### 7.2 Multi-Model Cross-Review

```
Traditional approach:  Same model writes + same model reviews → overlapping blind spots
AutoResearch:          Model A writes → Model B reviews → complementary blind spots
                       Model B writes → Model A reviews → complementary blind spots
```

**Why cross-review with different models works?**

| Model Characteristics | Codex / GPT Family | Claude Family |
|----------------------|--------------------|--------------|
| Training data focus | Larger proportion of code corpus | More emphasis on reasoning and logical consistency |
| Blind spots | Occasionally skips security checks | May not be aggressive enough on performance optimization |
| Review specialty | Finds API usage errors | Finds logic flaws and boundary conditions |

**Rotation strategy**:

```
Round 1: Codex implements → Claude reviews → Fix → Score
Round 2: Claude implements → Codex reviews → Fix → Score
Round 3: Codex implements → Claude reviews → Fix → Score
...
```

The error distributions of the two models are independent — **the intersection (issues both miss) is far smaller than the union (issues each misses)**.

> **Note**: If only one model is available (e.g., only deepseek), cross-review degrades to "same-model cross-review" with limited effectiveness. Try to configure two models from different vendors.

### 7.3 5-Dimension Scoring System

#### Scoring Rules

| Score | Meaning | Action |
|:----:|---------|--------|
| 10 | Perfect | No changes needed |
| 9 | Has suggested improvements, not mandatory | Acceptable |
| 7 | General issues, should be fixed | Needs handling |
| 4 | Serious issues | Must fix |
| 1 | Fatal issue, design error | Redo |

#### Weight Setting Rationale

```
Correctness   35% — Functionality is the baseline, highest weight
Tests        25% — Code without test protection is unmaintainable
Code Quality 20% — Affects long-term maintenance cost
Security     10% — Most business scenarios are not high-risk
Performance  10% — Most scenarios are not performance-sensitive
```

> Teams can adjust weights based on their own business needs. For example, finance projects may increase the "Security" weight, and infrastructure projects may increase the "Performance" weight.

#### Example Score Card

```
Correctness:  9 × 0.35 = 3.15
Tests:        7 × 0.25 = 1.75  ← Weak area
Quality:      8 × 0.20 = 1.60
Security:     8 × 0.10 = 0.80
Performance: 10 × 0.10 = 1.00
────────────────────
Total:                8.30

❌ Not passed (< 9.0)
   → Issue identified: Insufficient test coverage, room for quality improvement
   → Next round focus: Improve tests and code quality
```

### 7.4 Feedback-Driven Iteration

The essence of iteration is not retrying, but **carrying forward the previous round's issue list for targeted improvement**.

```
❌ Blind retry:
   Round N+1 Agent's prompt is identical to Round N
   → Agent doesn't know what it did wrong in the previous round

✅ Feedback-driven:
   Round N+1 Agent's prompt includes:
   "Last round you scored 8.3. Specific issues:
    1. [Tests - Serious] Missing edge cases: empty array not tested
    2. [Quality - Important] processData() is 80 lines; split into 3 sub-functions
    3. [Security - Important] User input missing length validation
    This round, prioritize fixing the above issues."
   → Agent knows the direction, fixes accurately
```

#### Termination Conditions

| Condition | Action |
|:---------:|:------:|
| Score ≥ 9.0 | ✅ Auto-commit + merge |
| 3 consecutive rounds with no score improvement | ⛑️ Flag for human intervention |
| Max rounds reached (42) | ⛑️ Stop, archive full logs |
| 3 consecutive test failures | ⛑️ Stop, record environment issues |

---

## 📖 Case Study: The Cost of a Payment Team Skipping Slow Path

### Background

In March 2025, the **PayCore team (6 people)** at a mid-sized FinTech company needed to refactor the settlement engine's "clearing module." This module handled reconciliation and fund allocation for 2 million daily transactions, involving 12 files, 4 microservices, and directly affecting user funds.

### Team Decision

The tech lead believed "the team has extensive experience, Fast Path is enough" and refused to upgrade to Slow Path. The reasoning was:
- "It's just one module, no architectural changes"
- "Fast Path passed the first two rounds, no need for dual-model hassle"

### What Happened

| Time | Event |
|:----:|-------|
| Round 1 Fast | Implementation complete, review passed ✅ |
| 3 days after production deploy | Found clearing precision deviation: one in a thousand transactions had a 0.01 CNY truncation error |
| Round 2 Fast | Fixed truncation issue, review passed ✅ |
| 1 week after deploy | Found extreme edge case (multiple refunds arriving simultaneously) causing a deadlock — clearing queue backed up for 37 minutes |
| Round 3 Fast | Fixed deadlock, review passed ✅ |
| 2 weeks after deploy | Security audit found: clearing rule engine vulnerable to parameter injection, affecting 8,943 merchant accounts |
| Total | **3 production incidents, affecting 9,000+ merchants, 187 person-hours of fixes, 2 emergency patches** |

### Post-Mortem Analysis

If Slow Path had been used:

- **Dual-model cross-review**: Claude would have found the truncation boundary in Round 1; Codex would have found the deadlock path in Round 2
- **5-dimension scoring**: Only Claude gave Security a 4 (serious), but Fast review had Codex reviewing itself, completely missing it
- **Failure cost comparison**:

| | Fast Path | Slow Path (estimated) |
|------------|-----------|----------------------|
| Total rounds | 3 rounds | 4–5 rounds |
| Development cycle | 6 days | 10–12 days |
| Production incidents | 3 | 0 |
| Fix cost | 187 person-hours | 0 |
| Merchant impact | 9,000+ | 0 |

> **Lesson**: Slow Path's "slowness" happens during development, not during failure recovery. For cross-module + security-sensitive tasks, Fast Path's "speed" is an illusion.

---

## ⚠️ Failure Case: The Iteration Trap of Stagnation at 8.5

### Phenomenon

An AI Agent system ran Slow Path on the same code refactoring task — **6 consecutive rounds** with scores hovering between **8.2–8.5**, never breaking through the 9.0 passing threshold:

```
Round 1: 8.5  → Feedback focus: Increase test coverage
Round 2: 8.3  → Feedback focus: Handle null pointer edge cases
Round 3: 8.4  → Feedback focus: Optimize error handling
Round 4: 8.2  → Feedback focus: Split long functions
Round 5: 8.4  → Feedback focus: Add integration tests
Round 6: 8.3  → Feedback focus: Performance optimization
```

Each time the Agent fixed the previous round's issues as requested, but the total score never reached passing.

### Root Cause Analysis

A manual review of the full logs revealed three deep-seated problems:

**1. Fixing A breaks B — Lack of isolation between scoring dimensions**

Each round, the Agent only focused on the dimensions and issues pointed out in the previous feedback. Fixing one dimension often inadvertently lowered scores in others. For example:
- Round 2: To fix edge cases (Correctness↑), many if-else blocks were added, causing cyclomatic complexity to jump from 12 to 27 (Quality↓)
- Round 4: To split long functions (Quality↑), 5 internal helper functions were introduced but none had tests (Tests↓)

**2. Review model developed anchoring bias toward "improvements"**

The scoring model in cross-review tended to give higher scores when it saw "improvements compared to the previous round," but absolute quality had not reached the threshold. This manifested as:
- Round 1 gave Tests 6 → Round 2 added 2 tests → gave 7 (actual coverage only went from 45% to 52%, far below the 70% requirement)
- The model was "scoring the magnitude of improvement" rather than "scoring absolute quality"

**3. Feedback granularity was too coarse**

```
❌ Vague feedback: "Test coverage is insufficient, please add more tests"
✅ Precise feedback: "Test_CalculateFee is missing edge test for amount=0;
    Test_SplitOrders does not cover multi-merchant scenarios;
    Current coverage 52%, target 70%, needs at least 4 more test cases"
```

### Solutions

| Fix Item | Specific Approach | Effect |
|----------|------------------|:------:|
| Dimension isolation | Each round explicitly marks "this round's focus dimension," other dimensions get only regression checks | Prevents fixing A from breaking B |
| Absolute standard anchoring | Add "absolute quality anchors" in scoring prompts: provide concrete examples for each score level | Scoring consistency improved from 62% to 89% |
| Precise feedback | Implementation Agent outputs unified JSON-format feedback, quantifying each defect | Fix efficiency improved 2.3× |
| Force reset | When stuck for 3 consecutive rounds, clear history and restart from Program.md | After reset at Round 4, passed by Round 2 of the new run |

After applying the above fixes, the same task reached passing (9.1) by Round 3.

---

## 👐 Hands-On Exercise: Scoring Calibration Practice

Below are **3 scoring snippets from real scenarios**, each containing the scorer's errors. Find the problems, then compare with the corrected answers.

### Exercise 1: Test Dimension Scoring Bias

```
Reviewer score output:

{
  "scores": {
    "correctness": 9,
    "tests": 7,
    "code_quality": 8,
    "security": 9,
    "performance": 9
  },
  "weighted_total": 8.55,
  "issues": [],
  "verdict": "NEEDS_WORK"
}
```

**Background**: The reviewed code has 142 lines, 3 unit tests, 38% coverage. Tests cover the happy path but are missing all error paths and edge cases.

**❓ Your question**: What's wrong with this scoring? (Hint: at least 2 issues)

<details>
<summary>Click to reveal answer</summary>

**Issue 1**: Tests scored 7 is unreasonable. Per scoring rules, 7 means "general issues, should be fixed," but 38% coverage, no edge case tests, and no error path tests constitute a **serious issue** — should be scored **4**.

**Issue 2**: Issues is an empty array (`[]`). Even if Tests scored 7 is considered "passing," the reviewer should list specific improvement items, such as:
- Missing edge test for empty input
- Missing exception paths: network timeout, database disconnection
- Coverage far below the 70% required by Program.md

**Corrected score**:
```
Correctness:  8  (missing exception path coverage, deduct 1)
Tests:        4  (38% coverage, no edge/error path tests, serious issue)
Quality:      7  (142-line file, could be split)
Security:     8  (input validation exists but untested)
Performance:  9
──────────────────
Total:      7.15  (should mark as NEEDS_WORK, with specific issues listed)
```
</details>

### Exercise 2: High Scores but Self-Contradictory

```
Reviewer score output:

{
  "scores": {
    "correctness": 10,
    "tests": 10,
    "code_quality": 8,
    "security": 10,
    "performance": 10
  },
  "weighted_total": 9.60,
  "issues": ["Code uses eval() to execute user input", "Some functions exceed 80 lines"],
  "verdict": "PASS"
}
```

**Background**: The reviewer listed 2 issues (`eval` and long functions), yet still gave near-perfect scores and a PASS verdict.

**❓ Your question**: Where is the logical contradiction in this scoring?

<details>
<summary>Click to reveal answer</summary>

**Contradiction 1**: `eval()` on user input is a **fatal security issue** (1 point). Security cannot possibly score 10. Security should be **1** → weighted loss of -0.90.

**Contradiction 2**: Functions exceeding 80 lines violate Program.md's "functions ≤ 50 lines" standard. Code quality should be no higher than **4**.

**Contradiction 3**: Two clearly identified issues exist, yet the verdict is PASS — PASS means "no changes needed." This is an execution error in applying the scoring rules.

**Contradiction 4**: Correctness scored 10 ("Perfect, no changes needed") directly conflicts with the security risk of using eval() — an insecure implementation cannot be "perfect."

**Corrected score**:
```
Correctness:  7  (eval existence casts doubt on correctness)
Tests:        7  (has tests but did not find the eval issue)
Quality:      4  (overly long functions, violates standards)
Security:     1  (eval on user input = fatal issue)
Performance:  8  (eval itself carries performance risk)
──────────────────
Total:      5.55  → verdict: NEEDS_WORK
```
</details>

### Exercise 3: Misjudgment from Ignoring Dimension Weights

```
Reviewer score output:

{
  "scores": {
    "correctness": 6,
    "tests": 9,
    "code_quality": 9,
    "security": 9,
    "performance": 9
  },
  "weighted_total": 8.25,
  "issues": ["Core algorithm has a logic deviation: negative amounts not rejected"],
  "verdict": "NEEDS_WORK"
}
```

**Background**: Correctness scored 6 indicates a **serious issue** (a core logic boundary like negative amounts not handled).

**❓ Your question**: What evaluation-level error exists in this scoring?

<details>
<summary>Click to reveal answer</summary>

**Issue 1**: Correctness has a 35% weight — the highest weight dimension. A score of 6 means a weighted loss of 0.35 × 4 = 1.4 points. Even if all other dimensions scored perfectly, the maximum total would be 8.6 — **mathematically impossible to pass**.

**Issue 2**: The reviewer's description of the correctness issue is vague. Negative amounts not being rejected means:
- This is a **boundary condition omission**, a serious issue in the correctness dimension
- It could also be a **security vulnerability** (malicious users could construct negative-amount transactions)
- Test coverage also did not cover this scenario → Tests scored 9 is unreasonable

**Issue 3**: There is a logical contradiction — Tests scored 9 (near perfect), yet the tests did not catch this serious correctness issue. If test coverage were truly adequate, this should have been discovered.

**Corrected score**:
```
Correctness:  4  (core logic boundary omission = serious issue)
Tests:        4  (missing critical boundary test = serious issue)
Quality:      8  (code structure acceptable)
Security:     6  (negative amounts could be a security attack vector)
Performance:  9
──────────────────
Total:      5.70  → verdict: NEEDS_WORK, must fix core logic
```
</details>

### Exercise Summary

| Common Scoring Error | Frequency | Severity |
|---------------------|:---------:|:--------:|
| Test dimension score inflated (ignoring coverage) | ⭐⭐⭐⭐⭐ | High |
| Lists issues but gives PASS | ⭐⭐⭐⭐ | Medium |
| Ignores dimension weight differences | ⭐⭐⭐⭐ | High |
| Fixing A lowers B, not caught | ⭐⭐⭐ | Medium |
| Scoring contradicts issue content | ⭐⭐⭐⭐ | High |

**Purpose of the calibration exercise**: To make scorers (human or Agent) realize — scores are not a numbers game. Each dimension's score must be strictly consistent with the issue content and rule standards.

---


## 8. Complete Orchestration Logic

Complete flow integrating Fast Path and Slow Path:

```python
def auto_research_dispatch(plan_path, issue_number):
    """
    Fast/Slow Dual-Path Orchestrator
    """
    # 1. Read plan
    plan = read_plan(plan_path)
    tasks = parse_tasks(plan)
    
    # 2. Assess complexity (whether to go directly to Slow)
    complexity_score = assess_complexity(plan)
    program_md = load_program_md()
    
    for task in tasks:
        task_result = None
        
        # 3. Decision: Fast or Slow
        if complexity_score >= 8 or "security" in task.get("tags", []):
            # Go directly to Slow Path
            task_result = slow_path(task, program_md)
        else:
            # Go to Fast Path
            task_result = fast_path(task)
            
            # Fast Path failed? Check whether to upgrade
            if task_result["status"] == "failed":
                if should_upgrade(task, task_result["review"], task_result.get("fail_count", 0)):
                    print(f"⏫ Upgrading to Slow Path: {task['description'][:40]}...")
                    task_result = slow_path(task, program_md)
        
        # 4. Handle result
        handle_result(task_result, issue_number)
        
        # 5. Log
        log_to_tsv(task, task_result, issue_number)
```

---

## 9. Implementation Steps on Hermes Agent

### Step 1: Create Program.md

```bash
mkdir -p ~/.hermes/autoresearch
cat > ~/.hermes/autoresearch/program.md << 'EOF'
# Program.md — Development Constitution

## Permission Boundaries
- Allowed: modify src/ internal/ cmd/
- Prohibited: modify .github/ CI/CD configuration

## Code Standards
- Functions ≤ 50 lines
- No magic numbers
- All errors must be handled

## Testing Standards
- Coverage ≥ 70%
- Table-driven tests
- Full boundary case coverage

## Scoring Criteria
- Correctness(35%) + Testing(25%) + Code Quality(20%) + Security(10%) + Performance(10%)
- Passing threshold: 9.0/10
EOF
```

### Step 2: Fast Path (Reuse existing subagent-driven-development)

Fast Path directly uses Hermes' existing `subagent-driven-development` skill. No additional configuration required.

### Step 3: Slow Path Entry Point

The core of Slow Path is modifying the review phase in the `subagent-driven-development` skill:

```python
# Original review (Fast):
delegate_task(goal="Spec review (binary judgment)")

# Changed to (Slow):
if is_slow_path:
    delegate_task(goal="5-dimension scoring review (with scoring)")
```

### Step 4: Upgrade Decision

Add an upgrade decision after each Fast Path review:

```python
def should_upgrade(review_result, task, fail_count):
    # Involves security/cross-module?
    if "security" in str(task.get("tags", [])):
        return True
    # Review found architectural issues?
    if any(kw in str(review_result) for kw in ["architecture", "design", "refactor", "root cause"]):
        return True
    # Consecutive failures?
    if fail_count >= 2:
        return True
    return False
```

---

---

## 10. Integration with Existing Workflows

### 10.1 PR Workflow Integration

```
Developer creates PR
    │
    ▼
Fast/Slow system automatically analyzes changes
    │
    ├── Simple changes → Fast Path → Labeled Approved
    │
    └── Complex changes → Slow Path → Output scoring report
```

Review report displayed in PR:

```markdown
## 🤖 AI Review Report

**Execution Path**: Slow Path (3 iterations)

**Final Score**: 9.0 / 10 ✅

| Dimension | Score | Notes |
|-----------|:-----:|-------|
| Correctness | 10 | All test cases passed |
| Testing | 9 | 87% coverage, includes boundary cases |
| Code Quality | 9 | Well-structured, clear naming |
| Security | 8 | ⚠️ Recommend adding parameter length validation |
| Performance | 9 | No performance concerns |
```

### 10.2 CI/CD Integration

```
push / PR
    │
    ▼
CI pipeline
    ├── lint / test (standard checks)
    └── AI quality scoring (non-blocking)
        ├── Fast Path → Output score directly in CI
        └── Slow Path → Execute asynchronously, push results via webhook
```

### 10.3 Risk-Graded Review — Solving the AI-Induced Review Bottleneck

The Faros Paradox (2026 Engineering Report) reveals a harsh reality: **AI increases code generation speed by 3-5x, but PR review time has increased by 91%**. Without solving the review bottleneck, the "speed" of Fast Path is meaningless.

**Solution**: Automatically score the risk level of each change and handle it by tier:

```python
def risk_score(pr):
    score = 0
    score += len(pr.files_changed) * 0.5          # More files changed = higher score
    score += sum(1 for f in pr.files if "security" in f or "auth" in f) * 3  # Security files weighted
    score += pr.insertions / 100                   # Code volume
    score += len(pr.dependency_changes) * 5        # Dependency changes are high-risk
    return score

risk = risk_score(pr)
if risk < 5:
    auto_merge = True      # 🟢 Low risk → Fast Path → Auto-merge
elif risk < 15:
    need_review = True     # 🟡 Medium risk → Fast Path + Manual spot-check
else:
    slow_path = True       # 🔴 High risk → Go directly to Slow Path
```

**Risk Score Panel in CI:**

| Scoring Dimension | Low Risk (🟢) | Medium Risk (🟡) | High Risk (🔴) |
|-------------------|:-------------:|:----------------:|:--------------:|
| Files Changed | 1-2 files | 3-5 files | 6+ files |
| Security Impact | No security relevance | Involves non-critical data | Involves user data/payments |
| Dependency Changes | None | Minor version upgrades | New dependencies/major versions |
| Logic Complexity | Single-file internal changes | Cross-module calls | Architectural changes |
| **Handling Method** | Fast Path + Auto-merge | Fast Path + Manual spot-check | Slow Path + Cross-review |

This solves the Faros Paradox: not by making human review catch up to AI generation speed, but by **letting AI review handle 80% of the evaluation work, leaving only the most critical 20% for humans**. This is the natural extension of our Fast/Slow tiered thinking.

---

## 11. SDD Team Adoption Four-Stage Strategy

Promoting the Fast/Slow dual-path system within a team requires a complete organizational rollout strategy. Core principle: **Start from one point, expand to others; tackle the easy first, then the hard**.

### Stage 1: Foundation Building — Team Awareness & Infrastructure Setup (Weeks 1-2)

**Goal**: Help the team understand the value of the "dual-path" system and set up the runtime environment.

| Action | Output |
|--------|--------|
| Internal workshop demonstrating Fast/Slow complete flow | Full team understands core concepts |
| Show AI scoring reports in Code Reviews | See actual output |
| Finalize Program.md constitution content | Team reaches consensus on rules |
| Configure Hermes subagent runtime environment | Executable infrastructure |
| Set up sandbox project (low-risk repository) | Safe practice ground |

**Milestone**: Team has seen at least one complete execution process; Program.md reviewed and approved by all team members.

### Stage 2: Pilot — Low-Risk Project Validation (Weeks 3-4)

**Goal**: Run the full flow on real but low-risk projects to accumulate data.

**Recommended Pilot Types**:

| Pilot Type | Example | Risk |
|------------|---------|:----:|
| Documentation generation/maintenance | API doc translation, README updates | 🟢 Very Low |
| Unit test generation | Adding tests to existing modules | 🟢 Very Low |
| Simple bug fixes | Single-file minor fixes | 🟢 Low |
| Configuration changes | Environment parameters, dependency upgrades | 🟢 Low |

**Checklist**:
- [ ] At least 3 complete Fast Path tasks completed
- [ ] At least 1 Fast→Slow upgrade triggered
- [ ] Scoring data and upgrade reasons collected
- [ ] Verified consistency between human review and AI scoring

**Metrics to Track**:
- Fast Path success rate (expected 70-85%)
- Fast→Slow upgrade rate (expected 15-30%)
- Consistency between review scores and human judgment

**Milestone**: 3+ tasks completed successfully, data shows the approach is viable.

### Stage 3: Rollout — Scaling & Standardization (Weeks 5-8)

**Goal**: Expand to the full team's daily development workflow.

| Action | Description |
|--------|-------------|
| Integrate into Code Review process | Each PR automatically triggers Fast Path review |
| Establish a Subagent Market | Team shares best practice prompt templates |
| Create Agent Owner role | Responsible for Program.md maintenance and rule updates |
| Internal Benchmark | Compare delivery efficiency and quality metrics before and after |
| Incentive program | Quarterly Best Agent Collaboration award (team with most quality improvement) |

**Rollout Strategy**:

```python
# Rollout path: start with the most willing team
pilot_team = select_most_willing_team()
pilot_team.run_for_2_weeks()

if pilot_team.metrics.improvement > 15%:
    expand_to(team_2, team_3)       # Good results → rapid rollout
else:
    investigate_and_fix(pilot_team)  # Poor results → root cause analysis, then adjust
```

**Milestone**: 50%+ of PRs go through Fast Path; team satisfaction > 70%.

### Stage 4: Deepening — Organizational Culture Integration (Week 9 onward)

**Goal**: Make the dual-path strategy the team's default way of working.

| Dimension | Specific Approach |
|-----------|-------------------|
| **Process** | Integrate AI scoring into quality gates — don't pass if below threshold |
| **Roles** | Establish AI Engineering Coach role responsible for best practice promotion |
| **Culture** | Include "ability to collaborate with AI" in performance evaluation |
| **Innovation** | Explore new collaboration modes: Master-Slave Agent, Multi-Agent Debate |
| **Open Source** | Open-source refined Program.md and Prompt libraries |

**Milestone**: 90%+ PRs reviewed with AI assistance; manual intervention rate < 10%.

---

### Four Stages Overview Timeline

```
Weeks 1-2      Weeks 3-4       Weeks 5-8        Week 9 onward
Foundation     Pilot           Rollout          Deepening
   │             │                │                 │
   ▼             ▼                ▼                 ▼
┌──────┐      ┌──────┐        ┌──────┐          ┌──────┐
│Aware │  →  │Verify │  →    │Scale  │  →      │Internalize│
│Env   │      │Data   │       │Standard│         │Culture│
└──────┘      └──────┘        └──────┘          └──────┘
   │             │                │                 │
   ├ Workshop    ├ 3+ tasks       ├ 50%+ PR        ├ 90%+ PR
   ├ Program.md  ├ 1+ upgrade     ├ Benchmark      ├ <10% intervention
   └ Sandbox     └ Score aligned  └ Incentives     └ Culture integration
```

### Comparison with Fast/Slow Stages 0-1-2-3

| SDD Four Stages | Fast/Slow Automation Level | Human Involvement |
|:---------------:|:--------------------------:|:-----------------:|
| Foundation | Stage 0 (Pure learning) | 100% manual checking |
| Pilot | Stage 1 (Assisted review) | Human reviews every output |
| Rollout | Stage 2 (Semi-automated) | 20% manual spot-check |
| Deepening | Stage 3 (Full automation) | Handle exceptions only |

Each stage should run for at least 2 weeks; use data to guide decisions, not gut feelings.

---

## 📖 Story: The Cost of Skipping Foundation Building — A Company's Lesson

### Background

A mid-sized internet company (200+ R&D staff) decided to roll out the Fast/Slow dual-path system in Q4 2025. The VP of Engineering got excited after hearing about the concept at KubeCon and demanded the team "go live in two weeks."

### What They Did

The team skipped the "Foundation Building" stage and jumped directly to "Pilot":

1. **No Workshop** — Only sent a document in the company chat
2. **No Consensus on Program.md** — The architect wrote Program.md alone without team review
3. **No Sandbox Environment** — Ran directly on the target branch of the production repo
4. **No Score Calibration** — Used 9.0 threshold directly, without verifying whether AI scoring was reasonable

Week 1 Data:

| Metric | Expected | Actual |
|:------:|:--------:|:------:|
| Fast Path tasks executed | 10+ | 32 |
| Fast Path success rate | 70-85% | **43%** |
| Fast→Slow upgrade rate | 15-30% | **57%** |
| Code rollback rate | <5% | **22%** |
| Team trust (anonymous survey) | >70% | **28%** |

### What Happened

Skipping the foundation phase led to three cascading problems:

**Problem 1: Program.md became a "castle in the air."** The scoring standards set by the architect gave security only 10% weight, but a senior engineer with a security background pointed out that the company's payment module accounted for 30% of the codebase. Applying "universal code standards" to "code with strong security constraints" caused Fast Path to frequently pass security changes that should have been upgraded.

**Problem 2: Uncalibrated scoring became "random grading."** Without the manual review calibration of the foundation phase, AI scoring biases went undetected. Sampling showed: AI gave code that was "superficially neat but logically flawed" an average score of 8.7, while human reviewers gave only 5.3 — a deviation of 3.4 points.

**Problem 3: Team became polarized between "AI blind trust" and "AI resistance."** Junior engineers fully trusted AI scoring results, directly merging code scored 9.2 that had concurrency bugs, causing production incidents. Senior engineers completely rejected the system, believing "AI doesn't understand our business logic at all."

### Fix and Turnaround

In Week 3, the VP of Engineering halted the full rollout and fell back to the foundation phase:

1. **Held Workshops Retroactively** — Used the rollback incidents as case studies, had the whole team discuss what Program.md should look like
2. **Recalibrated** — Organized 3 rounds of human vs AI score alignment meetings, identified and fixed 7 types of systematic bias
3. **Sandbox Trial** — Ran 20 tasks in an isolated environment before returning to production
4. **Tiered Trust** — First 2 weeks: AI scores were "suggestions only," mandatory human review; starting Week 3: gradual delegation

After foundation remediation, data returned to normal:

| Metric | Before Foundation | After Foundation |
|:------:|:-----------------:|:----------------:|
| Fast Path success rate | 43% | 78% |
| Fast→Slow upgrade rate | 57% | 22% |
| Code rollback rate | 22% | 3% |
| Team trust | 28% | 74% |

**Core Lesson**: Foundation building is not "going through the motions" — it's the process of calibrating the trust benchmark. Skipping foundation and going straight to Fast Path is like running on a track without checking your vision — you either hit a wall or run off course.

---

## ⚠️ Failure Case: 9.0 Threshold Setting Mistake — When 90% of Tasks Went to Slow Path

### Scenario

A fintech team (50 R&D staff) set the scoring threshold to **9.5/10** (higher than the default 9.0) when implementing the Fast/Slow system, expecting "only the highest quality code should go through Fast Path."

### Data Performance

Week 1 results (47 total tasks):

| Score Range | Tasks | Percentage | Processing Path |
|:-----------:|:-----:|:----------:|:---------------:|
| 9.5 - 10 | 2 | 4% | Fast Path (auto-pass) |
| 9.0 - 9.4 | 8 | 17% | ❌ Should be Fast, blocked by threshold → Slow Path |
| 8.0 - 8.9 | 21 | 45% | Slow Path |
| < 8.0 | 16 | 34% | Slow Path |

**Result**: Only 4% of tasks used Fast Path; 96% went to Slow Path. Fast Path was effectively useless, and the team actually increased workload — running both the AI Slow Path review and waiting for manual review.

### Root Cause Analysis

1. **Threshold lacked calibration** — Setting 9.5 was a "gut feel" decision with zero data support. The team didn't first run a threshold-free observation period to understand the score distribution.

2. **Program.md scoring criteria didn't match task types** — The team primarily maintained internal tool libraries and generated documentation, which naturally scored high (simple + easy test coverage). But compliance code for fintech naturally scored low (many security constraints + high change impact). Using a uniform threshold ignored this difference.

3. **Didn't distinguish between "quality gate" and "path selection gate"** — 9.5 as a "can this code go to production?" quality threshold is reasonable, but as a "Fast vs Slow" path selection threshold it's too high. Path selection thresholds should focus on "how risky is this?" not "how high quality is this?"

### Adjustment Plan

The team redesigned the decision logic in Week 3:

```python
# Wrong approach: single threshold decides everything
if score >= 9.5:   # ← This is a quality gate, not a path selection gate
    fast_path()

# Correct approach: two-dimensional decision
def path_decision(score, risk_tags, complexity):
    # Path selection: based on risk, not quality
    if risk_tags or complexity >= 8:
        slow_path()            # High risk → Force Slow
    elif score >= 7.5:
        fast_path()            # Low risk and quality meets threshold → Fast
    else:
        slow_path()            # Low risk but insufficient quality → Rework

# Quality gate retained separately, checked before merge
def merge_gate(score, has_human_review):
    if score < 9.0 and not has_human_review:
        block_merge("Score below 9.0, requires manual review before merging")
```

**Key Distinctions**:
- **Path Selection Gate** (Fast vs Slow) = 7.5 score, focuses on risk
- **Merge Release Gate** (can go to production) = 9.0 score, focuses on quality
- Fast Path is just "AI fully automated processing," not "release without review"
- Code that passes Fast Path still needs to go through the merge quality gate

### Adjusted Data

| Metric | Before Adjustment (9.5 single threshold) | After Adjustment (two-dimensional decision) |
|:------:|:----------------------------------------:|:------------------------------------------:|
| Fast Path share | 4% | 71% |
| Slow Path share | 96% | 29% |
| Manual intervention rate | 100% (waiting for review) | 29% (high-risk/low-quality only) |
| Average PR merge cycle | 4.7 hours | 22 minutes |
| Production defect rate | 0.8% | 0.9% (no significant change) |

**Core Lesson**: Threshold setting must be data-driven. Run for 2 weeks without thresholds first to see the distribution, then set reasonable cutoffs based on actual data. Path selection looks at risk; quality gates look at scores — don't conflate the two gates.

---

## 👐 Hands-on Exercise: Promotion Pitch Practice

In the following scenarios, you are the promoter of the Fast/Slow system and need to persuade different stakeholders. Practice method: first read the scenario description, try to organize your own pitch, then compare with the provided dialogue script.

### Scenario 1: Convincing the CTO — Answering "Why should we trust AI?"

**Background**: The CTO is pragmatic and has seen too many AI adoption "storms in a teacup." You need data and logic to convince them to invest resources.

**Your pitch (think for 2 minutes, write down key points):**

↓

**Reference Dialogue Script**:

> **You**: Wang, I understand your concern. When we tried that AI code generation tool last year, it did increase test coverage from 40% to 65%, but maintenance costs went up by 30% — that's because we only used "generation" without pairing it with "review."
>
> **CTO**: Right, so how do I know this isn't another numbers game?
>
> **You**: The difference is that the Fast/Slow dual-path core isn't "using AI to do the work" — it's "using AI for tiered review." Here's our pilot data:
>
> | Metric | Pure Manual | AI Fast Path | Fast + Slow Tiered |
> |:------:|:-----------:|:------------:|:------------------:|
> | Single PR review time | 45 min | 3 min ↓93% | 8 min (incl. upgrades) ↓82% |
> | Defect miss rate | 2.1% | 3.8% ↑ | **1.9%** ↓ |
> | Engineer AI trust score | — | 52% | **81%** |
>
> **CTO**: Fast Path's defect miss rate is 3.8%, higher than manual. What about that?
>
> **You**: That's exactly the value of the "dual-path" approach. Fast Path's 3.8% is indeed higher than manual's 2.1%, but Fast Path only handles low-risk changes — even if defects slip through, the blast radius is limited. All high-risk changes are escalated to Slow Path (human + AI cross-review), where the defect miss rate drops to 0.7%. **Overall, the tiered system's total defect rate is 10% lower than pure manual, while being 5x faster.**
>
> This isn't about replacing humans — it's about focusing human effort on the truly important 20%.
>
> **CTO**: How much investment is needed?
>
> **You**: Two weeks of foundation building plus two weeks of pilot, with three people working part-time. By the fourth week, we'll have data to decide whether to continue or cut losses. **Using two weeks of investment to validate a solution that could improve efficiency 5x — the ROI is extremely high.**

### Scenario 2: Convincing a Senior Engineer — Answering "AI review my code? What does it know?"

**Background**: Senior Engineer Zhang, 10 years of experience, the team's technical authority. He believes code review is a "craft" that AI can never replace.

**Your pitch (think for 2 minutes, write down key points):**

↓

**Reference Dialogue Script**:

> **You**: Zhang, you're right. AI really doesn't understand business logic. That's why we never intended AI to replace your code review.
>
> **Zhang**: Then what's this Fast/Slow thing for? Isn't it still AI doing reviews?
>
> **You**: Let me break it down. How much time do you spend on Code Review every day?
>
> **Zhang**: About two hours on average, sometimes up to four.
>
> **You**: Of those two hours, how much is on things like "tool library version upgrades, README translations, log format standardization"?
>
> **Zhang**: ...At least an hour.
>
> **You**: Exactly. Fast Path is meant to eat that hour for you. Those low-risk, non-business-logic changes can be reviewed directly by AI. You just glance at the scoring report on the results panel, confirm it's fine — 30 seconds, done.
>
> **Zhang**: What if AI misses something?
>
> **You**: Great question. Our rule is — whenever a change involves security, architecture, or core business logic, it's forced to upgrade to Slow Path, which requires your review. Fast Path only handles changes that you could "approve with your eyes closed." **We're not using AI to replace your judgment — we're using AI to replace your repetitive labor.**
>
> That hour you save, you can use to review core modules that actually need your expertise, or to write architecture documentation. Isn't that better?
>
> **Zhang**: When you put it that way... it kind of makes sense. But how do we ensure the scoring is reliable?
>
> **You**: During the foundation phase, we run human vs AI scoring alignment sessions, calibrating until the deviation is < 0.5 points before going live. You'll be the scoring judge — what you say goes.

### Scenario 3: Guiding a Junior Engineer — Answering "Letting AI write my code? That sounds awesome!"

**Background**: Junior engineer Li, 6 months on the job, enthusiastic about AI but lacking in judgment. They plan to use Fast Path as a "no-review fast-track to production."

**Your pitch (think for 2 minutes, write down key points):**

↓

**Reference Dialogue Script**:

> **You**: Li, I see you've been trying Fast Path. How's it going?
>
> **Li**: It's amazing! I wrote a utility function, AI reviewed it and merged it directly — no waiting for human review, my efficiency doubled!
>
> **You**: Well, the efficiency improvement is real. But let me ask you something — last time your utility function scored 9.2 from AI. Do you know where the points were deducted?
>
> **Li**: Uh... I didn't look closely. It passed anyway.
>
> **You**: I read that report. 0.8 points were deducted on the security dimension — because the function accepts user input but doesn't do length validation. A 9.2 score did pass Fast Path, but that doesn't mean this code is ready for production. It just means "this change is low risk, AI can do the initial review." Before merging, the quality gate checks security-related warnings.
>
> **Li**: Wait — passing Fast Path doesn't mean it's done?
>
> **You**: This is the most important concept — **Fast Path pass ≠ code is production-ready**. Fast Path just lets AI replace the "manual initial review of low-risk changes." There's still a quality gate to clear before merging. And if this function gets modified later to involve security logic, the system will automatically upgrade to Slow Path.
>
> **Li**: Got it... but how do I know when my code should go Fast vs Slow?
>
> **You**: Three simple criteria:
>
> 1. **If you're not sure the code is correct** → Actively request Slow Path
> 2. **If the module you're modifying you've only read, not written** → Actively request Slow Path
> 3. **If you fully understand the change and it doesn't involve business logic** → Go Fast Path confidently
>
> **Remember this mantra**: `Fast is fast, Slow is steady; when unsure, upgrade — no shame.`

---

**Promotion Checklist**: After each communication, confirm the other person understands these three core points for the communication to count as effective:

- [ ] Fast/Slow is a **path selection**, not a quality gate
- [ ] AI is **sharing the repetitive workload**, not replacing judgment
- [ ] Foundation building is the **prerequisite** for all trust


## 12. More AI-Assisted Development Patterns

Fast/Slow dual-path covers 90% of daily development scenarios. But some scenarios — architectural decisions, performance optimization, high-risk modules, large projects — require other patterns to supplement. These patterns **do not replace** Fast/Slow but are **on-demand add-on** enhancement layers.

### 12.1 Debate Pattern (Multi-Agent Debate)

Applicable when **design decisions** need to be made, not implementation written.

#### Core Idea

```
Design Plan A: Agent X independently conceives and outputs
Design Plan B: Agent Y independently conceives and outputs

    Each lists pros and cons

Both sides critique each other (discovering each other's blind spots)

    Synthesize optimal plan or vote for winner
```

#### Differences from Slow Path

| Dimension | Slow Path (Iterative Scoring) | Debate Pattern |
|-----------|:----------------------------:|:--------------:|
| **Direction** | Sequential (modify → review → re-modify) | Parallel (multiple plans produced simultaneously) |
| **Goal** | Improve implementation quality | Validate design correctness |
| **Output** | A piece of code | A decision |
| **Applicable** | "How to implement" | "Which plan to choose" |

#### Typical Scenarios

| Scenario | Debate Question | Participants |
|----------|----------------|-------------|
| Database selection | MySQL vs PostgreSQL vs Custom | Each Agent represents one option |
| API style | REST vs GraphQL vs gRPC | Each Agent represents one style |
| Architecture pattern | Microservices vs Modular Monolith vs Event-Driven | Each Agent represents one architecture |
| Cache strategy | Redis vs Local Cache vs CDN | Each Agent represents one strategy |

#### Engineering Implementation

```python
def debate(question, candidates, rounds=3):
    """
    question: "Should the user system use MySQL or PostgreSQL?"
    candidates: [Agent_MySQL, Agent_PostgreSQL, Agent_Neutral]
    """
    arguments = {}
    
    for round in range(rounds):
        for agent in candidates:
            # Each Agent sees others' arguments, then rebuts or improves
            context = format_debate_context(question, arguments, agent.stance)
            response = agent.argue(context)
            arguments[agent.name] = response
    
    # Neutral Agent makes final judgment
    verdict = Agent_Neutral.judge(question, arguments)
    return verdict
```

#### Integration with Fast/Slow

```
Need to make a design decision?
  ├── Simple decision (Redis vs Memcached?)
  │   └── Single Agent direct judgment → Go Fast Path
  │
  └── Complex decision (Cloud vs Self-hosted datacenter?)
      └── Debate Pattern → Output decision → Go Fast/Slow for implementation
```

**Recommended Tool**: Hermes' `delegate_task` can dispatch multiple Subagents in parallel to each output their own plan.

---

### 12.2 Evolutionary Pattern (Evolutionary / Genetic)

Applicable when **optimizing existing code** (performance, memory, latency) rather than implementing from scratch.

#### Core Idea

Inspired by evolutionary algorithms: make small modifications to code (mutation), run tests to evaluate (selection), retain high-scoring solutions (heredity).

```
┌─────────────────────────────────────────────┐
│ Generation 1: Generate 3-5 different plans    │
│  ┌──────┐  ┌──────┐  ┌──────┐               │
│  │Plan A│  │Plan B│  │Plan C│               │
│  └──────┘  └──────┘  └──────┘               │
│         ↓                                    │
│  Evaluate: test pass rate + performance metrics│
│         ↓                                    │
│  Eliminate lowest score, keep best plan       │
│         ↓                                    │
│  Generation 2: Mutate + crossover best plans  │
│         ↓                                    │
│  Repeat until performance target met or max gen│
└─────────────────────────────────────────────┘
```

#### Differences from Slow Path

| Dimension | Slow Path (Iterative Scoring) | Evolutionary Pattern |
|-----------|:----------------------------:|:--------------------:|
| **Improvement direction** | Review feedback **tells** Agent what to change | Mutation + testing **discovers** which changes work |
| **Exploration** | Low (Agent changes per feedback) | High (random mutations may find unexpected optimizations) |
| **Determinism** | Stable (done when score meets threshold) | Uncertain (may have degenerate mutations) |
| **Applicable** | Feature implementation quality | Performance/memory/latency optimization |

#### Typical Scenarios

| Scenario | Example | Mutation Operation |
|----------|---------|-------------------|
| Performance optimization | Convert O(n²) loop to O(n log n) | Replace data structures, cache intermediate results |
| Memory optimization | Reduce unnecessary object allocation | Object pooling, buffer reuse |
| Latency optimization | Reduce database query count | Batch queries, lazy loading, connection reuse |
| Code compression | Reduce duplicate code | Extract common functions, simplify conditional logic |

#### Engineering Implementation

```python
def evolution(base_code, test_cmd, metric_extractor, generations=10, population=5):
    """
    base_code: original code to optimize
    test_cmd: test command (e.g., "pytest tests/")
    metric_extractor: function to extract performance metrics from test output
    """
    # Generation 0: original code
    population = [base_code] * population
    
    for gen in range(generations):
        scores = []
        for code in population:
            # Mutation
            mutated = mutate(code)
            # Testing
            test_output = run(test_cmd, mutated)
            score = metric_extractor(test_output)
            scores.append((score, mutated))
        
        # Selection: keep top 50%
        scores.sort(reverse=True, key=lambda x: x[0])
        survivors = [s[1] for s in scores[:population//2]]
        
        # Breeding: crossover to generate next generation
        population = survivors + [crossover(survivors) for _ in range(population - len(survivors))]
        
        # Check if significantly better than baseline
        if scores[0][0] >= target_metric:
            return scores[0][1]
    
    return scores[0][1]  # Return best individual
```

> **Safety mechanism**: Must enforce git revert protection — if mutated code causes test failures, automatically roll back to the previous generation. No degradation allowed.

#### Integration with Fast/Slow

```
Need performance optimization?
  └── Evolutionary pattern explores mutation space
      └── After finding optimal code
          └── Go through Fast Path review to confirm (prevent side effects)
```

---

### 12.3 Role-Based Pattern

Applicable when **multiple specialized roles** need to collaborate on a large task.

#### Core Idea

Simulate a software company organizational structure, each Agent with a clear role and deliverables.

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  PM        │ → │ Architect  │ → │ Engineer   │ → │ Tester     │
│            │   │            │   │            │   │            │
│ Output: PRD│   │ Output:    │   │ Output:    │   │ Output:    │
│            │   │ Design Doc │   │ Code       │   │ Test Report│
└────────────┘   └────────────┘   └────────────┘   └────────────┘
     │                │                │                │
     └── Upstream ────┴── As input ────┴── Downstream ──┘
         output                            validation
```

#### Roles & Outputs

| Role | Responsibility | Deliverable | Dependency |
|:----:|---------------|-------------|:----------:|
| **PM** | Understand requirements, break into executable tasks | PRD, User Stories | — |
| **Architect** | Design system structure, interfaces, data flow | Architecture doc, API design | PM's PRD |
| **Engineer** | Implement code, unit tests | Feature code, tests | Architecture design |
| **Tester** | Integration testing, boundary validation | Test report, Bug List | Implementation code |
| **Ops** | Deployment config, monitoring, alerting | Deployment scripts, Dockerfile | Tested code |

#### Differences from Fast/Slow

| Dimension | Fast/Slow Dual-Path | Role-Based Pattern |
|-----------|:------------------:|:------------------:|
| **Split dimension** | By **task granularity** (complexity) | By **role responsibility** (specialization) |
| **Subtask relationship** | Parallel or sequential | **Strictly progressive** (upstream output is downstream input) |
| **Quality assurance** | Cross-review + scoring | **Role validation** (downstream verifies upstream) |
| **Applicable** | Quality of a single feature | End-to-end delivery of a complete project |

#### Typical Scenarios

| Scenario | Why Role-Based Is Needed |
|----------|-------------------------|
| Building a new service from scratch | Needs sequential requirements, architecture, coding, testing |
| Large-scale refactoring | Needs architect to design transition plan, engineers to execute in batches |
| API design | PM defines features, architect defines interfaces, engineer implements, test validates |
| Multi-client development | Frontend, backend, test each with their own responsibilities |

#### Engineering Implementation

```python
def role_based_workflow(task):
    # Step 1: PM produces requirements
    prd = delegate_task(
        goal="As a product manager, transform the following requirements into a PRD",
        context=task.description,
        toolsets=['file']
    )
    
    # Step 2: Architect produces design based on PRD
    design = delegate_task(
        goal="As an architect, output a technical design document based on the PRD",
        context=f"PRD: {prd}",
        toolsets=['file']
    )
    
    # Step 3: Engineer implements based on design
    code = delegate_task(
        goal="As an engineer, implement code based on the design document",
        context=f"Design: {design}",
        toolsets=['terminal', 'file']
    )
    
    # Step 4: Tester validates
    test_report = delegate_task(
        goal="As a tester, verify the implementation meets the PRD",
        context=f"PRD: {prd}\nImplementation: {code}",
        toolsets=['terminal', 'file']
    )
```

#### Integration with Fast/Slow

```
Large project → Role-Based Pattern (define each role's deliverables first)
              │
              ├── Each role's sub-tasks → Fast/Slow dual-path
              │     (PM tasks use Fast, Engineer tasks evaluate complexity)
              │
              └── Cross-role validation → Slow Path review
                    (Architect validates Engineer's output)
```

---

### 12.4 Interactive Pattern (Human-in-the-Loop)

Applicable when tasks are **high risk** or require **human experience and judgment**.

#### Core Idea

The Agent doesn't make decisions at critical steps on its own — it pauses and asks a human.

```
Agent: "I plan to use PostgreSQL. Is that okay?"
  ⏸️ Waiting for reply
Human: "Okay, but watch the connection pool limit."
  ▶️ Continue
Agent: "Got it. Here's the table structure design: ..."
  ⏸️ Waiting for confirmation
Human: "Add a unique index on users.email"
  ▶️ Continue
Agent: "Starting implementation..."
```

#### Pause Point Types

| Pause Point | Trigger Condition | Pause Content |
|:-----------:|------------------|---------------|
| Design Decision | Involves technology selection, architecture plan | "Suggest X vs Y, which to choose?" |
| Security Confirmation | Involves data access, permission changes | "The following changes involve user data. Allow?" |
| Resource Change | Involves cost, infrastructure | "New cloud resources required. Approve?" |
| Boundary Judgment | Business rules are unclear | "How to handle this edge case?" |
| Merge Confirmation | Slow Path abnormal termination | "Score below threshold but max rounds reached. Force merge?" |

#### Differences from Fast/Slow

| Dimension | Fast/Slow (Fully Automated) | Interactive Pattern |
|-----------|:--------------------------:|:-------------------:|
| **Automation level** | High (auto-upgrade, auto-merge) | Low (pauses at critical nodes for confirmation) |
| **Applicable risk** | Low-to-medium risk daily development | High risk, high uncertainty |
| **Speed** | Fast (minutes) | Slow (depends on human response time) |
| **Applicable scenarios** | 80% of routine tasks | 20% requiring human experience and judgment |

#### Implementation Position

Interactive is not a standalone pattern but a **pause layer stacked on top of other patterns**:

```
Fast / Slow / Debate / Evolution
         │
         ▼
    ┌────────────┐
    │ Interactive │ ─── Condition met → Pause, wait for human
    │  Pause Point│
    └────────────┘
         │
         ▼
    Continue execution
```

#### Integration with Fast/Slow

```python
def run_with_human_checkpoints(mode, task):
    if mode == "slow" or mode == "debate":
        # Design decisions need human confirmation
        answer = ask_human(
            question="Architecture plan suggestion: ... Do you agree?",
            choices=["Agree and continue", "Modify plan", "Abort"]
        )
        if answer == "Abort":
            return
    
    # Continue execution
    result = execute(mode, task)
    
    # Slow Path abnormal termination
    if result["status"] == "escalate":
        answer = ask_human(
            question=f"Task {task.id} score stagnated. Force merge?\n"
                     f"Score history: {result['scores']}",
            choices=["Force merge", "Hand off for manual fix", "Abandon"]
        )
```

---

### 12.5 Self-Improving Pattern

Applicable when **repetitive work** occurs frequently — the Agent should learn to build tools to speed itself up.

#### Core Idea

```
Agent detects repetitive work pattern
  → Automatically generates a skill/script/tool
  → Injects it into its own workflow
  → Next time it encounters a similar task, calls it directly
```

#### Differences from Fast/Slow

| Dimension | Fast/Slow (Execution) | Self-Improving (Meta-Learning) |
|-----------|:---------------------:|:-----------------------------:|
| **Focus** | Quality of the current task | Efficiency of future tasks |
| **Output** | Complete one task | Produce one tool/template |
| **Timeline** | Short-term (minutes~hours) | Long-term (continuous accumulation) |
| **Applicable** | Quality of individual tasks | Efficiency improvement for the whole team |

#### Typical Patterns

| Pattern | Example |
|---------|---------|
| Auto-generate skill | "This company's API style is very consistent — generate a skill for reuse next time" |
| Template extraction | "This CRUD pattern has appeared 5 times — extract as a template" |
| Knowledge consolidation | "10 common project conventions — auto-update Program.md" |
| Toolchain optimization | "Each deployment requires modifying 3 files — write a script to do it in one click" |

#### Integration with Fast/Slow

Self-Improving is the **upper layer of all patterns** — whether going through Fast or Slow, if a repetitive pattern is detected, it automatically generates a tool:

```
Fast Path executes task
  → Detects that code structure is similar to last time
  → Automatically extracts as a skill
  → Next similar task calls the skill directly

Slow Path executes task
  → Review finds 3 files changed with the same type of content
  → Automatically generates batch modification script
  → Next time, execute with one click
```

---

### 12.6 Pattern Selection Decision Tree

```
What type of task is this?
  │
  ├── Implement a feature / Fix a bug
  │   └── Go Fast/Slow dual-path (default)
  │
  ├── Make a design decision (choose database, choose architecture)
  │   └── Fast/Slow + Debate pattern enhancement
  │
  ├── Optimize existing code performance
  │   └── Evolutionary pattern (explore optimal solution)
  │
  ├── Build a complete system from scratch
  │   └── Role-Based pattern (PM → Architect → Dev → Test)
  │
  └── Task is high risk / rules are unclear
      └── Any pattern + Interactive pause points
          └── Detect repetitive patterns → Self-Improving extracts a skill
```

### 12.7 Pattern Comparison Table

| Pattern | Applicable Scenario | Automation Level | Exploration Level | Best For |
|:-------:|--------------------|:----------------:|:-----------------:|----------|
| Review (Fast) | Daily development | ⭐⭐⭐⭐⭐ | ⭐ | All team members |
| Iterative Scoring (Slow) | Complex implementation | ⭐⭐⭐⭐ | ⭐⭐ | Core developers |
| Debate | Design decisions | ⭐⭐⭐ | ⭐⭐⭐⭐ | Architects |
| Evolutionary | Performance optimization | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Senior engineers |
| Role-Based | Large projects | ⭐⭐⭐ | ⭐ | Full team collaboration |
| Interactive | High-risk scenarios | ⭐⭐ | ⭐ | All + human confirmation |
| Self-Improving | Repetitive work | ⭐⭐⭐⭐ | ⭐⭐⭐ | Toolchain maintainers |

---

## Case Study: Patterns in Practice

The following cases are all adapted from real projects, showing when and under what conditions each pattern is triggered, and what effects were achieved.

### Debate Case Study: Startup Backend Architecture Selection

A startup team needed to build a SaaS platform targeting small-to-medium businesses. The technical lead was torn between two directions: **Microservices architecture** (flexible, independent deployment) and **Modular Monolith** (fast development, simple operations). The team debated for two weeks without reaching a conclusion.

The lead decided to activate the Debate pattern. They dispatched two Agents: one as the microservices advocate, the other as the modular monolith advocate. Each Agent received the same requirements document (launch within 3 months, initial team of 3 developers, target fewer than 500 customers), but independently produced their plans.

After the first round of debate, the microservices side emphasized independent scalability and team division flexibility, while the modular monolith side pointed out the startup's limited ops capability, the time cost of debugging across services, and the fact that initial traffic would never need independent scaling. After critiquing each other, both sides proposed improvements targeting each other's weaknesses in the second round: the microservices side agreed to start with modular internal structure reserving split interfaces, and the modular side acknowledged they could package modules as containers for future migration.

The final verdict: choose **Modular Monolith + clear module boundaries and interface contracts**, then gradually split after user count exceeds 2000. The entire debate took 3 rounds and 40 minutes, while the team had debated for two weeks. In retrospect, the team believed the Debate pattern's greatest value wasn't having AI "make decisions," but having both viewpoints presented completely and structurally, eliminating information asymmetry.

### Evolutionary Case Study: Data Pipeline Performance Optimization

A financial risk control system processed 5 million transactions daily. The core pipeline was a Python script: Read Kafka → Rule Matching → Write Results Table. As business grew, processing latency ballooned from 2 seconds to 35 seconds, severely slowing down the downstream real-time alerting system.

The engineer handed this core logic to the Evolutionary pattern. The baseline code was approximately 200 lines, with a clearly defined fitness function: **processing time for 100K records + peak memory usage**, weighted 50% each. The initial population generated 5 mutation variants containing different changes: switching to DataFrame batch processing instead of row-by-row loops, introducing an LRU cache to reduce redundant computation, using multi-process parallelism instead of serial processing, etc.

After 6 generations of evolution, the optimal solution reduced processing latency from 35 seconds to 4.2 seconds (88% improvement), and memory usage from 1.8GB to 540MB. The most brilliant mutation came from Generation 4 — the Agent inadvertently swapped the order of two rule matching operations, discovering that filtering high-frequency rules first could skip 70% of records early. This optimization direction was something the engineer had never considered. This is the unique value of the Evolutionary pattern: it doesn't depend on human prior knowledge and can explore counterintuitive but effective optimization paths through random mutation.

### Role-Based Case Study: Building an Order Service from Scratch

An e-commerce platform decided to split its order module into an independent service, involving payment integration, inventory deduction, logistics status synchronization, and 10+ external systems. This was a classic "large project requiring multi-role collaboration" scenario.

The team used the Role-Based pattern to start this project. First, the PM Agent produced a complete requirements document with priority ordering based on the PRD (containing 23 user stories). The Architect Agent, after receiving the PRD, designed a layered architecture: API layer (RESTful), Business layer (state-machine driven), Infrastructure layer (database + message queue), and drew the core state transition diagram (Pending Payment → Paid → Shipped → Completed).

The Engineer Agent implemented all interfaces and business logic by module according to the architecture document, including idempotency handling, distributed transaction compensation (Saga pattern), and inventory pre-deduction with rollback. The Test Agent not only validated end-to-end flows for all 23 user stories but also discovered 3 edge-case omissions (concurrent inventory overselling, duplicate payment callback processing, logistics state jumping). The final delivered order service had zero incidents in production.

The key was the **upstream-downstream validation** between roles: the Architect found that two user stories in the PM's requirements conflicted ("Cancel order should refund immediately" vs "Refund requires manual review") and corrected them before development began. The Test Agent also discovered an exception handling gap in one of the Engineer's state paths. This kind of layered quality control is very difficult to achieve with a single developer.

### Interactive Case Study: Core Database Migration

A company's user database (MySQL 5.7, single table with 210 million rows) needed migration to TiDB to solve the query complexity from sharding. The migration risk was extremely high — 800GB of data, a maintenance window of only 4 hours, and corrupting even one user data row could trigger customer complaints.

The engineer added Interactive pause points on top of the migration script. The Agent automatically performed full data export, incremental binlog sync, row count and checksum validation, but paused at the following nodes to wait for human confirmation: ① Source DB load assessment before export (Agent suggested 2 AM execution, please confirm), ② Handling strategy when data validation finds 0.003% row inconsistency (Agent suggested re-running validation, please confirm), ③ Final consistency snapshot confirmation before switching read/write traffic.

On the night of migration, the Agent detected a consistency issue at the second pause point — 3,247 rows had primary key conflicts during the incremental sync. The Agent's analysis concluded that an application had performed data repair on the source database during sync, causing primary key changes. After the engineer confirmed online, the Agent automatically executed the "overwrite target with source" strategy and re-validated successfully. Without the Interactive pause points, the Agent might have overwritten with its default strategy, causing data loss. The migration completed in 3 hours 20 minutes with zero data loss.

> The core principle of Interactive: **Let humans make judgments; let Agents execute.** Each judgment pause point should have a clear question and optional solutions — don't make humans start from a blank page.

### Self-Improving Case Study: CRUD Template Auto-Generation

A team maintained 12 microservices using Hermes Agent, each with a similar structure: Controller → Service → Repository → Model. Team members noticed that every time they created a new resource (like `User`, `Order`, `Product`), the code the Agent wrote was highly structurally consistent — only field names and business rules differed.

On the 5th similar resource creation, the Agent proactively detected this repetitive pattern: it noticed the newly created file structure was highly similar to the previous 4 times (filename patterns like `*Controller.java`, `*Service.java`), and the diff type was the same each time (adding/removing fields, modifying query conditions, replacing business validation logic). The Agent automatically generated a **CRUD generation skill**, extracting file structure, standard comments, and basic test code as template variables.

The effect was immediate: creating a new resource went from 12-15 steps taking 8 minutes down to a single skill call taking 1.5 minutes, and the generated code fully complied with the team's conventions — no more inconsistencies like "last Controller used `@RestController`, this one used `@Controller`." Six months later, this skill had been used 40+ times, saving approximately 5 person-days of development time cumulatively.

The core insight of Self-Improving: **Any manual pattern repeated 3+ times should be automated.** The Agent doesn't need to wait until the 10th time — seeing a similar structure on the 3rd occurrence, it should proactively ask whether to create a skill.

---

## 👐 Pattern Selection Exercise

For the following 5 scenarios, determine which extended pattern is most suitable (Debate / Evolutionary / Role-Based / Interactive / Self-Improving), and briefly explain why. Answers provided at the end.

### Scenario 1: Log System Selection

Your team needs to choose a log collection solution for a high-concurrency system (1 billion log entries per day). Candidate solutions include: ELK Stack, Loki + Grafana, a custom lightweight solution. Each has pros and cons; team members disagree and have been debating for three days.

**Question**: Which pattern should be used? Why?

### Scenario 2: Image Processing Service Performance Bottleneck

An image thumbnail generation service, implemented in Python. When a user uploads a 10MB image, thumbnail generation takes 1.8 seconds, but the business requirement is < 200ms. The code uses Pillow's `resize` method — the logic is clear but very slow. You suspect the bottleneck is in I/O and algorithm selection, but aren't sure of the specific optimization direction.

**Question**: Which pattern should be used? Why?

### Scenario 3: Building a Notification Center from Scratch

The company needs a new notification center microservice supporting email, SMS, and App Push channels, integrating with 5 third-party services, and depending on existing user service and template service. Project timeline: 3 weeks.

**Question**: Which pattern should be used? Why?

### Scenario 4: Batch Deletion of Production User Data

Operations needs to batch delete a batch of anomalous accounts (~200K records), involving three tables: user, order, payment. The operation is high risk — deleting one wrong record could affect financial reconciliation. Business rules are complex ("accounts with orders in the last 30 days cannot be deleted," "accounts with non-zero balance need to go through refund process").

**Question**: Which pattern should be used? Why?

### Scenario 5: Team Habit — Standardizing API Response Format

Your team has 6 backend developers, each writing API responses in different formats: some use `{code, data, msg}`, some use `{status, result, message}`, some directly use `{success, data}`. You repeatedly flag this in code reviews, but every new endpoint still brings a new format.

**Question**: Which pattern should be used? Why?

---

### Recommended Answers

**Scenario 1 (Log System Selection) → Debate Pattern**

This is a classic design decision problem with clear multiple candidate options and a divided team. The Debate pattern can output complete analysis of each option in parallel (performance, cost, operational complexity), expose each option's blind spots through mutual critique, and finally produce a structured recommendation. Compared to three days of team debate, the Debate pattern can produce decision rationale in 30-60 minutes.

**Scenario 2 (Image Processing Performance Bottleneck) → Evolutionary Pattern**

There's already clear baseline code and a quantifiable optimization goal (1.8s → 200ms), but it's unclear which specific changes will be effective. The Evolutionary pattern automatically explores the optimization space through random mutation (replacing algorithm libraries, adjusting parameters, adding caching, multi-threaded processing) and may discover optimization directions the engineer never thought of (e.g., switching from Pillow to libvips, reducing resolution before compression, etc.). Fitness function = processing time + memory usage + image quality score.

**Scenario 3 (Notification Center Development) → Role-Based Pattern**

This is a complete system built from scratch, involving requirements analysis, architecture design, multi-client implementation, and external integration. The Role-Based pattern simulates progressive collaboration: PM (output requirements document and channel priorities), Architect (design unified notification model, channel adapter pattern), Engineer (implement each channel adapter, retry mechanism, template rendering), Tester (verify end-to-end sending for each channel). The upstream-downstream validation mechanism can catch requirement conflicts and design omissions early.

**Scenario 4 (Batch User Data Deletion) → Interactive Pattern (stacked on any implementation pattern)**

This operation involves user data and financial data — extremely high risk. The Interactive pattern can pause at critical nodes for human confirmation: pre-deletion check (which accounts meet deletion criteria? Any overlooked business rules?), mid-deletion confirmation (100K records deleted, verifying consistency — continue?), post-deletion verification (is financial reconciliation normal?). The Agent handles executing precise SQL and validation scripts; the human makes judgments and provides safety net at critical nodes.

**Scenario 5 (API Response Format Inconsistency) → Self-Improving Pattern**

This is a classic repetitive work pattern — every code review flags the same type of issue. Self-Improving can automatically detect the "API response format" repetitive pattern, generate a standardized response format skill (or lint rule, code snippet template), and inject it into the team's CI pipeline or Agent's workflow. The Agent can further create a git hook to automatically check whether new API endpoint response formats comply with standards, completely eliminating manual review omissions.

**Scoring Criteria**

- Correct pattern identification: 4 points / question
- Adequate explanation: 1 point / question
- Maximum: 25 points

**20-25 points**: You have deep understanding of the extended patterns and can apply them flexibly in real projects.
**12-19 points**: Basic mastery achieved. Suggest reviewing the core ideas of each pattern against the case studies.
**0-11 points**: Suggest returning to the beginning of the chapter to re-understand each pattern's "applicable scenarios" and "differences from Fast/Slow."

---


## 13. Monitoring Metrics

After going live, track at least the following metrics:

| Metric | Normal Range | Warning Threshold | Meaning |
|:-------|:------------:|:-----------------:|:--------|
| Fast Path success rate | 70-85% | < 50% | Fast review criteria has issues |
| Fast→Slow upgrade rate | 15-30% | > 40% | Complexity assessment is inaccurate |
| Slow Path average rounds | 3-5 rounds | > 10 rounds | Threshold may be too high |
| Slow Path pass rate | 60-80% | < 40% | 9.0 threshold is too high |
| Manual intervention rate | < 10% | > 20% | Automated process needs checking |
| Average token consumption per task | — | Continuously rising | Check for over-iteration |

---

---

## 14. FAQ

**Q: What if we only have one model?**
A: Cross-review effectiveness will be reduced, but it's still better than nothing. It's recommended to configure at least two models from different providers.

**Q: Is the 9.0 threshold too high or too low?**
A: Start at 9.0, run for 2 weeks, then adjust based on data. If the pass rate is > 80%, increase it; if < 40%, decrease it.

**Q: Will 42 maximum iterations be too many?**
A: 42 is the upper limit; actual average is 3-5 rounds. 42 rounds is a safety net to prevent extreme cases from getting stuck.

**Q: Who should maintain Program.md?**
A: The technical lead is responsible, updating it periodically as the project evolves. Notify the full team with every change.

**Q: What if an audit finds that manual changes are better than AI?**
A: Let the scoring data speak. If manually modified code scores significantly higher than AI-automated code, it means the scoring dimensions have biases that need adjustment.

**Q: When should we bypass the automated process and go fully manual?**
A: High-frequency changes, emergency hotfixes, experimental features — these scenarios prioritize speed over process.

---

## References

Key external sources cited in this document, organized by chapter:

### AI-Assisted Development Efficiency and Bottlenecks

| Source | Author/Organization | Year | Referenced In |
|--------|--------------------|:----:|:-------------:|
| **METR Paradox** — RCT controlled experiment: AI perceived speedup vs actual completion rate | METR Research Team | 2026 | [metr.org](https://metr.org/blog/2026-02-24-uplift-update/) |
| **Faros Paradox** — AI code leading to +91% PR review time | Faros Engineering Report | 2026 | [faros.ai](https://www.faros.ai/blog/ai-acceleration-whiplash-takeaways) |
| **DORA Mirror** — AI amplifies existing team quality gaps | Djimit (N=906 survey) | 2026 | [djimit.nl](https://djimit.nl/ai-tooling-for-software-engineers-in-2026/) |
| **DORA 2025 Research Report** — Impact of AI-assisted coding on delivery speed | DORA / CodeRabbit | 2025-2026 | [dora.dev](https://dora.dev/guides/dora-metrics/) |
| **95% of enterprises not receiving meaningful returns from AI investment** | MIT Survey | 2025 | §4 cited in text |

### AI Context Debt and Context Engineering

| Source | Author/Organization | Year | Referenced In |
|--------|--------------------|:----:|:-------------:|
| **AI Context Debt** concept original | Abbas Raza | 2026.04 | [LinkedIn](https://www.linkedin.com/posts/abbasraza_most-engineering-teams-deploying-ai-tools-activity-7449869888673718272-Kw6O) |
| **InfoQ Deep Dive: AI Context Debt** | InfoQ | 2026 | [infoq.cn](https://www.infoq.cn/article/K7hpIOogPsLlPQz4lwXu) |
| **Context Engineering Best Practices Guide** | Laurent Py / Packmind | 2026 | [packmind.com](https://packmind.com/context-engineering-ai-coding/context-engineering-best-practices/) |
| **ACE Research: Incremental context updates reduce drift by 86%** | Stanford / SambaNova | 2025.10 | [packmind.com](https://packmind.com/context-engineering-ai-coding/context-engineering-playbook/) |
| **GitClear Report: Code duplication rate grows 4x in AI era** | GitClear | 2024 | [gitclear.com](https://www.gitclear.com/ai_assistant_code_quality_2025_research) |
| **Index.dev Report: 41% of code is AI-generated** | Index.dev | 2026 | §4 |

### AutoResearch and Multi-Agent Patterns

| Source | Author/Organization | Year | Referenced In |
|--------|--------------------|:----:|:-------------:|
| **AutoResearch** methodology and open-source implementation | Andrej Karpathy | 2026 | [github.com/karpathy](https://github.com/karpathy/autoresearch) |
| **Generalizing AutoResearch to non-ML tasks** | Udit Goenka | 2026 | [github.com/uditgoenka](http://github.com/uditgoenka/autoresearch) |
| **5 Hidden Technical Debts from AI** | Ajay Mudettula / DEV | 2026 | [dev.to](https://dev.to/ajay_mudettula/5-hidden-technical-debts-ai-is-adding-to-your-codebase-2026-5g3c) |

### Methodology and Tools

| Source | Author/Organization | Year | Referenced In |
|--------|--------------------|:----:|:-------------:|
| **Specification-Driven Development** (spec-kit, OpenSpec) | GitHub / Community | 2026 | [github.com/github](https://github.com/github/spec-kit) |
| **Claude Code Agent patterns and /goal system** | Anthropic | 2025-2026 | [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/overview) |
| **Hermes Agent Subagent-Driven-Development** | Hermes Agent Community | 2026 | [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs) |

For deeper understanding of any of these sources, search for the original text at the corresponding URL (some sources are paid/closed reports; abstracts can be obtained through public channels).

---

## 15. Summary

The core insight of "Fast first, Slow second" in three sentences:

1. **Don't waste on simple tasks** — Fast Path passes in one go; 80% of tasks complete in under 5 minutes
2. **Don't sacrifice on complex tasks** — Slow Path automatically catches you; cross-review + quantitative scoring + iterative loop
3. **No human judgment needed** — The upgrade logic is code-level, not gut-feel

The end result:

```
Simple tasks don't waste tokens
Complex tasks don't sacrifice quality
Automatic upgrades don't need human judgment
```