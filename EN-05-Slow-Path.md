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
