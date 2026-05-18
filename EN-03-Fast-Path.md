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
