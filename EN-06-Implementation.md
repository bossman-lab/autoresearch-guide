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
