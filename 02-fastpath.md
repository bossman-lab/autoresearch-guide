---
title: "Fast Path 详解：Hermes Subagent-Driven-Development 基线方案"
date: 2026-05-18
author: "提灯人"
tags: [AI, Agent, AutoResearch, 质量工程, FastSlow, Hermes]
---

Fast Path 即 Hermes Agent 现有的 `subagent-driven-development` skill（SDD）。

它是一个**三阶段四步走**的流水线：

```
任务进入
    │
    ▼
┌───────────────────────────────┐
│ 阶段一：单任务执行              │
│                               │
│ Step 1: 实施 Subagent          │
│   • 读任务 → TDD(写测试→实现)  │
│   • pytest 验证全部通过         │
│   • git commit                 │
└─────────────┬─────────────────┘
              ▼
┌───────────────────────────────┐
│ 阶段二：双阶段审核              │
│                               │
│ Step 2: 规范审核（Spec Review）│
│   • 需求是否全部实现？          │
│   • 有无 scope creep？         │
│   └── 通过 → 继续              │
│       └── 不通过 → 修复后重审   │
│                               │
│ Step 3: 质量审核（Quality）     │
│   • 代码风格 / 错误处理 / 测试  │
│   └── 通过 → 标记完成           │
│       └── 不通过 → 修复后重审   │
└─────────────┬─────────────────┘
              ▼
下一任务 / ✅ 完成
```

### 三个设计原则

**原则 1：每个任务一个独立的 Subagent**

```
❌ 错误：一个 Subagent 做所有任务
   → context 越堆越多，Agent 开始混淆

✅ 正确：每个任务一个新 Subagent
   → 每个 Subagent 只看到自己需要的信息
   → 干净 context = 更少的幻觉
```

**原则 2：两阶段审核分离关注点**

规范审核查"做对了没有"，质量审核查"做得好不好"——让不同的审核专注不同的方面。

**原则 3：审核反馈必须闭环**

```
发现问题 → 修复 → 重审 → APPROVED
                  ↑          │
                  └── 仍有问题 ┘
```

不允许"下次再改"。

### Fast Path 的实现代码

```python
# Step 1: 实施
result = delegate_task(
    goal=task.description,
    context=f"""
    按 TDD 流程:
    1. 写测试 → pytest 验证 FAIL
    2. 写实现 → pytest 验证 PASS
    3. 运行完整测试套件
    """,
    toolsets=['terminal', 'file']
)

# Step 2: 规范审核
spec_review = delegate_task(
    goal="Spec compliance review",
    context=f"""
    原始任务要求: {task.full_text}
    检查:
    - [ ] 所有需求都实现了？
    - [ ] 有无额外的 scope creep？
    - [ ] 接口/签名是否符合预期？
    """
)

# Step 3: 质量审核
quality_review = delegate_task(
    goal="Code quality review",
    context=f"""
    检查:
    - [ ] 代码风格符合项目规范？
    - [ ] 错误处理完善？
    - [ ] 测试覆盖 ≥ 70%？
    - [ ] 无安全隐患？
    """
)
```

---
