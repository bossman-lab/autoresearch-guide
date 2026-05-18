---
title: "先快后慢：AI 辅助开发的双路径质量保障体系"
date: 2026-05-18
author: "提灯人"
tags: [AI, Agent, AutoResearch, 质量工程, FastSlow, Hermes]
---

> **一句话摘要**：80% 的简单任务不要浪费 token 做多轮迭代，20% 的复杂任务不要牺牲质量走一次通过——先快后慢，分级兜底。

---

# 第一部分：问题与策略

## 一、我们面对的根本矛盾

在 AI 辅助开发中，效率和质量是一对矛盾：

| 目标 | 做法 | 对简单任务的代价 | 对复杂任务的代价 |
|------|------|:---:|:---:|
| **效率优先** | 一次通过，不迭代 | ✅ 快，省 token | ❌ 容易翻车 |
| **质量优先** | 多轮迭代，交叉审核 | ❌ 严重浪费 | ✅ 质量有保障 |

**关键洞察**：两个目标不冲突——前提是系统能自动判断当前任务该走哪条路。

### AutoResearch 的启示

2026 年，Karpathy 的 AutoResearch 方法论被迁移到软件开发领域，带来了三个核心改进：

1. **多模型交叉审核** — Codex 和 Claude 轮流担任实现者和审核者，消除单模型盲区
2. **5维量化评分** — 正确性(35%) + 测试(25%) + 代码质量(20%) + 安全(10%) + 性能(10%)，达标线 9.0/10
3. **反馈驱动迭代** — 审核意见直接注入下一轮 prompt，Agent 看到问题后针对性改进

但这套模式对所有任务一刀切，80% 的简单任务会浪费 3-8 倍的 token。

**我们的方案**：先快后慢，分级兜底。

---

## 二、先快后慢：双路径策略总览

### 核心思想

```
每个任务进来，默认走快通道（Fast Path）。
     │
     ├── 简单任务 → 一次通过 → ✅ 交付（~2-5分钟）
     │
     └── 复杂任务 / 快通道失败 → 自动升级到慢通道（Slow Path）
                               ├── 双模型交叉实施+审核
                               ├── 5维量化评分
                               ├── 反馈驱动迭代
                               └── ✅ 交付（~10-30分钟）
```

### 分档矩阵

| 维度 | Fast Path | Slow Path |
|------|-----------|-----------|
| **适用场景** | 增删字段、改配置、单文件改动、简单 bug fix | 跨模块 feature、架构改动、安全敏感、新系统 |
| **实施模型** | 1 个（deepseek 或已配模型） | 2 个交叉（如 deepseek + claude） |
| **审核方式** | 二元通过/不通过 | 5 维加权评分 ≥ 9.0 |
| **迭代机制** | 一次通过，不迭代 | 反馈驱动循环，最多 42 轮 |
| **典型耗时** | 2-5 分钟 | 10-30 分钟 |
| **Token 消耗** | 1× | 3-8× |
| **预期成功率** | ~80% | ~95%+（经过迭代） |

### 核心价值

```
不浪费：80% 的简单任务走 Fast，省时间省 token
不遗漏：20% 的复杂任务走 Slow 兜底，质量有保障
```

---

# 第二部分：Fast Path — Hermes Subagent-Driven-Development

## 三、Fast Path 的架构

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

## 四、什么时候升级到 Slow Path？

Fast Path 不通过不一定升级，**只有特定条件才升级**。

### 升级触发条件

| # | 条件 | 行为 |
|:-:|------|------|
| 1 | 审核发现**架构级问题**（"这个设计可能不太对"） | 🔺 立刻升级 |
| 2 | 审核列出 **3+ 个严重问题** | 🔺 立刻升级 |
| 3 | 同一任务 **连续 2 次** Fast 审核不通过 | 🔺 升级 |
| 4 | 任务涉及支付/安全/用户数据 | 🔺 直接走 Slow |
| 5 | 任务改动 **3+ 个文件** 且跨模块 | 🔺 直接走 Slow |
| 6 | 实施 Subagent **主动报告** "需要多次迭代" | 🔺 尊重 agent 判断 |
| 7 | 上述条件都不满足，审核不通过 | ⟳ 小幅度修复后重审 |

### 核心判断函数

```python
def should_upgrade(task, review_result, failure_count):
    # 条件 4/5：复杂度预先评估
    if "security" in task.get("tags", []) or task.get("cross_module"):
        return True
    
    # 条件 1/2：审核结果严重
    if review_result.contains("架构") or count_serious_issues(review_result) >= 3:
        return True
    
    # 条件 3：连续失败
    if failure_count >= 2:
        return True
    
    # 条件 6：Agent 自述
    if "多次迭代" in str(review_result):
        return True
    
    return False  # 保持 Fast Path，修复后重审
```

---

# 第三部分：Slow Path — AutoResearch 增强方案

## 五、Slow Path 的架构

Slow Path 在 Fast Path 的基础上增加了三层增强：

```
Fast Path 架构
    +
    ├── ① 宪法注入（Program.md）
    ├── ② 双模型交叉（A写B审/B写A审）
    ├── ③ 5维量化评分（达标线 9.0）
    └── ④ 反馈驱动循环（直至达标或终止）
```

### 整体流程

```
任务进入 Slow Path
    │
    ▼
[Step 0] 注入 Program.md 宪法规则
    │
    ▼
┌── 迭代循环 ──────────────────────────────────┐
│                                               │
│  [Step 1] 角色分配                             │
│    奇数轮: Agent A 实施 → Agent B 审核          │
│    偶数轮: Agent B 实施 → Agent A 审核          │
│                                               │
│  [Step 2] 实施                                 │
│    接收: 任务描述 + 上一轮反馈 + 评分历史         │
│    产出: 代码 + 通过测试                        │
│                                               │
│  [Step 3] 5 维评分                             │
│    维度: 正确性35% 测试25% 质量20% 安全10% 性能10%│
│    达标: ≥ 9.0                                 │
│                                               │
│  [Step 4] 判断                                 │
│    ├─ 达标 → ✅ 自动合并                        │
│    ├─ 评分停滞 → ⛑️ 人工介入                    │
│    ├─ 超时 → ⛑️ 人工介入                        │
│    └─ 未达标 → 收集反馈 → 进入下一轮              │
│                                               │
└───────────────────────────────────────────────┘
```

### 迭代引擎伪代码

```python
def slow_path(task, program_md):
    models = ["deepseek", "claude"]  # 两个不同的模型
    scores = []
    max_rounds = 42
    
    for round in range(1, max_rounds + 1):
        # 轮换角色
        impl_idx = 0 if round % 2 == 1 else 1  # 实施者索引
        rev_idx = 1 if round % 2 == 1 else 0    # 审核者索引
        
        # Step 1: 实施
        implementation = delegate_task(
            goal=f"第 {round} 轮 - {models[impl_idx]} 实施",
            context=f"""
            ## Program.md 宪法
            {program_md}
            
            ## 上一轮反馈（注入本轮）
            {json.dumps(scores[-1]["issues"]) if scores else "首次实施，无历史反馈"}
            
            ## 评分历史
            {json.dumps([s["weighted_total"] for s in scores])}
            
            ## 任务
            {task.full_text}
            """
        )
        
        # Step 2: 审核 + 5维评分
        review = delegate_task(
            goal=f"第 {round} 轮 - {models[rev_idx]} 审核评分",
            context=f"""
            按以下维度评分（1-10）:
            - 正确性 × 0.35
            - 测试覆盖 × 0.25
            - 代码质量 × 0.20
            - 安全 × 0.10
            - 性能 × 0.10
            
            达标: 加权总分 ≥ 9.0
            
            输出 JSON:
            {{"scores": {{...}}, "weighted_total": N,
              "issues": [...], "verdict": "PASS|NEEDS_WORK"}}
            """
        )
        
        review_data = json.loads(review)
        scores.append(review_data)
        
        # 达标？
        if review_data["weighted_total"] >= 9.0:
            return {"status": "approved", "rounds": round, "scores": scores}
        
        # 动态终止：连续 3 轮评分不提高
        if round >= 4 and not is_improving([s["weighted_total"] for s in scores[-4:]]):
            return {"status": "escalate", "reason": "评分停滞", "scores": scores}
    
    return {"status": "escalate", "reason": "超最大轮次", "scores": scores}
```

---

## 六、核心机制详解

### 6.1 Program.md — Agent 宪法

Program.md 是所有 Agent 的行为准绳，每次 Slow Path 启动时注入。

```markdown
# Program.md

## 权限边界
- 允许: 修改 src/, internal/, cmd/
- 禁止: 修改 .github/, CI/CD, program.md 本身

## 代码规范
- 函数 ≤ 50 行，文件 ≤ 500 行
- 所有 public 方法必须有文档注释
- 禁止魔法数字，提取为常量
- 错误必须处理（禁止 `_` 忽略）

## 测试规范
- 覆盖率 ≥ 70%
- 表格驱动测试
- 测试命名: Test<Function>_<Scenario>
- 禁止: time.Sleep, 外部HTTP依赖

## 评分维度
| 维度 | 权重 | 评估内容 |
|------|------|---------|
| 正确性 | 35% | 功能是否完全正确 |
| 测试 | 25% | 覆盖率、边界情况 |
| 代码质量 | 20% | 可读性、可维护性 |
| 安全 | 10% | 输入校验、权限 |
| 性能 | 10% | 时间复杂度、资源使用 |

达标线: 加权总分 ≥ 9.0/10
```

**为什么需要一个宪法文件？**
- 消除歧义：每个 Agent 读到同一套规则
- 权限边界：防止 Agent 做它不该做的事
- 统一标准：不同模型的评估尺度一致
- 可审计：所有决策规则可追溯

### 6.2 多模型交叉审核

```
传统方式:  同一模型写 + 同一模型审 → 盲区重叠
AutoResearch: Model A 写 → Model B 审 → 盲区互补
               Model B 写 → Model A 审 → 盲区互补
```

**为什么不同模型交叉有效？**

| 模型特性 | Codex / GPT 系 | Claude 系 |
|---------|---------------|-----------|
| 训练数据侧重 | 更大的代码语料占比 | 更注重推理和逻辑一致 |
| 盲区 | 偶尔跳过安全检查 | 可能在性能优化上不够激进 |
| 审核特长 | 发现 API 用法错误 | 发现逻辑漏洞和边界条件 |

**轮换策略**：

```
轮次 1: Codex 实施 → Claude 审核 → 修复 → 评分
轮次 2: Claude 实施 → Codex 审核 → 修复 → 评分
轮次 3: Codex 实施 → Claude 审核 → 修复 → 评分
...
```

两个模型的错误分布是独立的——**交集（两者都漏掉的问题）远小于并集（各自漏掉的问题）**。

> **注意**：如果只有一种模型可用（比如只有 deepseek），交叉审核退化为"同模型交叉"，效果有限。尽量配置两个不同厂商的模型。

### 6.3 5 维评分体系

#### 评分规则

| 分数 | 含义 | 行为 |
|:---:|------|------|
| 10 | 完美 | 无需任何修改 |
| 9 | 有建议改进项，非必要 | 可接受 |
| 7 | 一般问题，应该修复 | 需处理 |
| 4 | 严重问题 | 必须修复 |
| 1 | 致命问题，设计错误 | 重做 |

#### 权重设定原理

```
正确性 35% — 功能是底线，权重最高
测试    25% — 没有测试保护的代码是不可维护的
代码质量 20% — 影响长期维护成本
安全    10% — 大多数业务场景非高危
性能    10% — 大多数场景非性能敏感
```

> 团队可以根据自身业务调整权重。比如金融项目可以调高"安全"权重，基础设施项目可以调高"性能"权重。

#### 示例评分

```
正确性: 9 × 0.35 = 3.15
测试:    7 × 0.25 = 1.75  ← 薄弱项
质量:    8 × 0.20 = 1.60
安全:    8 × 0.10 = 0.80
性能:   10 × 0.10 = 1.00
────────────────────
总分:              8.30

❌ 未达标（< 9.0）
   → 问题定位：测试覆盖不足，质量有提升空间
   → 下一轮重点：提升测试和技术质量
```

### 6.4 反馈驱动迭代

迭代的精髓不是重试，而是**带着上一轮的问题清单有针对性地改进**。

```
❌ 盲目重试：
   第 N+1 轮 Agent 的 prompt 和 N 轮一模一样
   → Agent 不知道自己上一轮哪里做得不好

✅ 反馈驱动：
   第 N+1 轮 Agent 的 prompt 包含：
   "上一轮你得了 8.3 分，具体问题有：
    1. [测试 - 严重] 边界情况遗漏：空数组未测试
    2. [质量 - 重要] processData() 80 行，拆分为 3 个子函数
    3. [安全 - 重要] 用户输入未做长度校验
    本轮请优先修复上述问题。"
   → Agent 知道方向，改得准
```

#### 终止条件

| 条件 | 动作 |
|:---:|:----:|
| 评分 ≥ 9.0 | ✅ 自动提交 + 合并 |
| 连续 3 轮评分未提高 | ⛑️ 标记为需人工介入 |
| 达到最大轮次（42） | ⛑️ 停止，存档全量日志 |
| 连续 3 次测试失败 | ⛑️ 停止，记录环境问题 |

---

# 第四部分：落地实现

## 七、完整编排逻辑

整合 Fast Path 和 Slow Path 的完整流程：

```python
def auto_research_dispatch(plan_path, issue_number):
    """
    Fast/Slow 双路径编排器
    """
    # 1. 读取计划
    plan = read_plan(plan_path)
    tasks = parse_tasks(plan)
    
    # 2. 评估复杂度（是否直接走 Slow）
    complexity_score = assess_complexity(plan)
    program_md = load_program_md()
    
    for task in tasks:
        task_result = None
        
        # 3. 决策：Fast or Slow
        if complexity_score >= 8 or "security" in task.get("tags", []):
            # 直接走 Slow Path
            task_result = slow_path(task, program_md)
        else:
            # 走 Fast Path
            task_result = fast_path(task)
            
            # Fast 不通过？判断是否升级
            if task_result["status"] == "failed":
                if should_upgrade(task, task_result["review"], task_result.get("fail_count", 0)):
                    print(f"⏫ 升级到 Slow Path: {task['description'][:40]}...")
                    task_result = slow_path(task, program_md)
        
        # 4. 处理结果
        handle_result(task_result, issue_number)
        
        # 5. 日志
        log_to_tsv(task, task_result, issue_number)
```

---

## 八、Hermes Agent 上的实现步骤

### Step 1: 创建 Program.md

```bash
mkdir -p ~/.hermes/autoresearch
cat > ~/.hermes/autoresearch/program.md << 'EOF'
# Program.md — 开发宪法

## 权限边界
- 允许: 修改 src/ internal/ cmd/
- 禁止: 修改 .github/ CI/CD 配置

## 代码规范
- 函数 ≤ 50 行
- 无魔法数字
- 所有错误必须处理

## 测试规范
- 覆盖率 ≥ 70%
- 表格驱动测试
- 边界 case 全覆盖

## 评分标准
- 正确性(35%) + 测试(25%) + 代码质量(20%) + 安全(10%) + 性能(10%)
- 达标线: 9.0/10
EOF
```

### Step 2: Fast Path（复用现有 subagent-driven-development）

Fast Path 直接使用 Hermes 现有的 `subagent-driven-development` skill。无需额外配置。

### Step 3: Slow Path 入口

Slow Path 的核心是修改 `subagent-driven-development` skill 中的审核环节：

```python
# 原审核（Fast）:
delegate_task(goal="Spec review（二元判断）")

# 改为（Slow）:
if is_slow_path:
    delegate_task(goal="5-dimension scoring review（带评分）")
```

### Step 4: 升级判断

在每次 Fast Path 审核后增加升级判断：

```python
def should_upgrade(review_result, task, fail_count):
    # 是否涉及安全/跨模块？
    if "security" in str(task.get("tags", [])):
        return True
    # 审核是否发现架构问题？
    if any(kw in str(review_result) for kw in ["架构", "设计", "重构", "根本"]):
        return True
    # 是否连续失败？
    if fail_count >= 2:
        return True
    return False
```

---

## 九、与现有工作流的集成

### 9.1 与 PR 工作流

```
开发者创建 PR
    │
    ▼
Fast/Slow 系统自动分析变更
    │
    ├── 简单变更 → Fast Path → 标注 Approved
    │
    └── 复杂变更 → Slow Path → 输出评分报告
```

PR 中显示的审核报告：

```markdown
## 🤖 AI 评审报告

**执行路径**: Slow Path（3轮迭代）

**最终评分**: 9.0 / 10 ✅

| 维度 | 评分 | 说明 |
|------|:---:|------|
| 正确性 | 10 | 全部用例通过 |
| 测试 | 9 | 覆盖率87%，含边界case |
| 代码质量 | 9 | 拆分合理，命名清晰 |
| 安全 | 8 | ⚠️ 建议加参数长度校验 |
| 性能 | 9 | 无性能隐患 |
```

### 9.2 与 CI/CD 集成

```
push / PR
    │
    ▼
CI pipeline
    ├── lint / test（常规检查）
    └── AI 质量评分（非阻塞）
        ├── Fast Path → 直接在 CI 输出评分
        └── Slow Path → 异步执行，webhook 推送结果
```

---

## 十、SDD 团队落地四阶段策略

Fast/Slow 双路径在团队中推广，需要一套完整的组织落地策略。核心原则：**由点及面、先易后难**。

### 第一阶段：筑基 — 团队认知与基础设施搭建（第 1-2 周）

**目标**：让团队理解"S双向路径"的价值，搭好运行环境。

| 动作 | 产出 |
|------|------|
| 内部 Workshop 演示 Fast/Slow 完整流程 | 全员理解核心思想 |
| Code Review 中展示 AI 评分报告 | 看到实际产出 |
| 确定 Program.md 宪法内容 | 团队达成规则共识 |
| 配置 Hermes subagent 运行环境 | 可执行的基础设施 |
| 建立沙盒项目（低风险仓库） | 安全的练习场 |

**里程碑**：团队至少看过一次完整执行过程，Program.md 全员 Review 通过。

### 第二阶段：试点 — 低风险项目验证（第 3-4 周）

**目标**：在真实但低风险的项目上跑通流程，积累数据。

**推荐试点类型**：

| 试点类型 | 示例 | 风险 |
|---------|------|:----:|
| 文档生成/维护 | API 文档翻译、README 更新 | 🟢 极低 |
| 单元测试生成 | 存量模块补测试 | 🟢 极低 |
| 简单 bug fix | 单文件小修小补 | 🟢 低 |
| 配置变更 | 环境参数、依赖升级 | 🟢 低 |

**检查清单**：
- [ ] 至少完成 3 个完整 Fast Path 任务
- [ ] 至少触发 1 次 Fast→Slow 升级
- [ ] 收集了评分数据和升级原因
- [ ] 验证了人工审核与 AI 评分的一致性

**关注指标**：
- Fast Path 成功率（正常 70-85%）
- Fast→Slow 升级率（正常 15-30%）
- 审核评分与人工判断的一致性

**里程碑**：3 个以上任务跑通，数据说明方案可行。

### 第三阶段：推广 — 规模化与标准化（第 5-8 周）

**目标**：扩展到全团队日常开发流程。

| 动作 | 说明 |
|------|------|
| 纳入 Code Review 流程 | 每个 PR 自动触发 Fast Path 审核 |
| 建立 Subagent Market | 团队共享最佳实践 prompt 模板 |
| 设立 Agent Owner 角色 | 负责 Program.md 维护和规则更新 |
| 内部 Benchmark | 对比引入前后的交付效率和质量指标 |
| 激励机制 | 季度最佳 Agent 协作奖（质量提升最明显的团队） |

**推进策略**：

```python
# 推广路径：从最配合的团队开始
pilot_team = select_most_willing_team()
pilot_team.run_for_2_weeks()

if pilot_team.metrics.improvement > 15%:
    expand_to(team_2, team_3)       # 效果好 → 快速铺开
else:
    investigate_and_fix(pilot_team)  # 效果不佳 → 根因分析后调整
```

**里程碑**：50% 以上的 PR 经过 Fast Path，团队满意度 > 70%。

### 第四阶段：深化 — 组织文化融合（第 9 周起）

**目标**：让双路径策略成为团队的默认工作方式。

| 维度 | 具体做法 |
|------|---------|
| **流程** | 将 AI 评分纳入质量门禁，不达标不放行 |
| **角色** | 设立 AI 工程教练，负责最佳实践推广 |
| **文化** | 将"与 AI 协作的能力"纳入绩效考核维度 |
| **创新** | 探索新协作模式：Master-Slave Agent、多 Agent 辩论 |
| **开源** | 将打磨好的 Program.md 和 Prompt 库开源 |

**里程碑**：90%+ PR 经 AI 辅助审核，人工介入率 < 10%。

---

### 四个阶段的节奏总览

```
第 1-2 周    第 3-4 周     第 5-8 周      第 9 周起
  筑基         试点          推广            深化
   │           │            │              │
   ▼           ▼            ▼              ▼
┌──────┐   ┌──────┐    ┌──────┐       ┌──────┐
│认知  │ → │验证  │ →  │铺开  │ →    │内化  │
│环境  │   │数据  │    │标准  │       │文化  │
└──────┘   └──────┘    └──────┘       └──────┘
   │           │            │              │
   ├ Workshop  ├ 3+ 任务    ├ 50%+ PR     ├ 90%+ PR
   ├ Program.md├ 1+ 升级    ├ Benchmark   ├ <10% 介入
   └ 沙盒环境  └ 评分一致   └ 激励机制    └ 文化融合
```

### 与 Fast/Slow 阶段 0-1-2-3 的对照

| SDD 四阶段 | Fast/Slow 自动化等级 | 人工参与度 |
|:---------:|:-------------------:|:---------:|
| 筑基 | 阶段 0（纯学习） | 100% 人工检查 |
| 试点 | 阶段 1（辅助审核） | 人工审核每次输出 |
| 推广 | 阶段 2（半自动） | 人工抽查 20% |
| 深化 | 阶段 3（全自动） | 仅处理异常 |

每个阶段至少跑 2 周，用数据说话，不靠感觉推进。

---

## 十一、监控指标体系

上线后至少跟踪以下指标：

| 指标 | 正常范围 | 告警阈值 | 含义 |
|:----|:-------:|:--------:|:----|
| Fast Path 成功率 | 70-85% | < 50% | Fast 审核标准有问题 |
| Fast→Slow 升级率 | 15-30% | > 40% | 复杂度评估不准确 |
| Slow Path 平均轮次 | 3-5 轮 | > 10 轮 | 阈值可能过高 |
| Slow Path 达标率 | 60-80% | < 40% | 9.0 阈值太高 |
| 人工介入率 | < 10% | > 20% | 自动流程需检查 |
| 平均每任务 token 消耗 | — | 持续上升 | 检查是否过度迭代 |

---

## 十二、FAQ

**Q: 只有一种模型怎么办？**
A: 交叉审核效果会打折扣，但仍比没有好。建议配置至少两个不同厂商的模型。

**Q: 阈值 9.0 太高/太低？**
A: 从 9.0 开始，运行 2 周后根据数据调整。达标率 > 80% 就调高，< 40% 就调低。

**Q: 42 轮最大迭代会不会太多？**
A: 42 是上限，实际平均 3-5 轮。42 轮是安全网，防止极端情况卡死。

**Q: Program.md 应该谁维护？**
A: 技术 Leader 负责，随着项目演进定期更新。每次改动通知全员。

**Q: 审计发现人工修改比 AI 好怎么办？**
A: 用评分数据说话。如果人工修改后的评分显著高于 AI 自动，说明评分维度有偏差，需要调整。

**Q: 什么情况下应该绕过自动流程，走纯人工？**
A: 高频改动、紧急 hotfix、实验性功能——这些场景追求速度胜于流程。

---

## 十三、总结

先快后慢的核心洞察三句话：

1. **不浪费在简单任务上** — Fast Path 一次通过，80% 的任务在 5 分钟内完成
2. **不牺牲在复杂任务上** — Slow Path 自动兜底，交叉审核 + 量化评分 + 迭代闭环
3. **不需要人来判断** — 升级逻辑是代码级的，不是靠直觉

最终效果：

```
简单任务不浪费 token
复杂任务不牺牲质量
自动升级不需要人判断
```