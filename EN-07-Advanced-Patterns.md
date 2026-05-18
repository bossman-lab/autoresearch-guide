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
