---
title: "先快后慢：AI 辅助开发的双路径质量保障体系"
date: 2026-05-18
author: "提灯人"
tags: [AI, Agent, AutoResearch, 质量工程, FastSlow, Hermes]
---

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

### 2026 年的三组反直觉数据

2026 年的实证研究揭示了一个深层问题：**AI 不是快慢的问题，而是好与不好的问题被转移了。**

**① METR Paradox（METR RCT 随机对照实验）**

> 使用 Claude 的开发者**主观感觉快了 20%**，但实际在测试时间内**正确完成的任务少了 19%**——主客观差距达 39 个百分点。

原因：AI **减少了首次产出时间，但增加了验证时间**。开发者花更多时间理解、验证和修复 AI 生成的代码。感知提速 ≠ 实际提速。

**② Faros Paradox（Faros 工程报告，2026）**

> AI 生成的代码导致 **PR 审核时间延长 91%**。

当生成速度提升 3-5 倍，但审核能力没有同步提升时，瓶颈从"编码"转移到了"审核"。代码写作变快了，但系统没有变快。

**③ DORA Mirror——AI 放大现有质量**

> AI 工具的效果高度依赖代码库健康度。Staff+ 工程师采用 Agent 的比例是初级工程师的 2.3 倍。**AI 放大现有能力差距**——好团队用 AI 更好，差团队用 AI 更差。

这三组数据指向同一个结论：**不解决审核和验证问题，AI 带来的不是效率提升，而是幻觉提速。** 简单任务走一次通过能减轻验证负担，复杂任务走多轮交叉审核能保证质量不失守。

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


## 四、AI 上下文负债：Fast/Slow 必须解决的深层问题

Fast/Slow 双路径解决了"如何执行"的问题，但一个更深层的问题在 2026 年才被清晰定义——**AI 上下文负债（AI Context Debt）**。

### 4.1 什么是 AI 上下文负债？

由科技从业者 Abbas Raza 在 2026 年 4 月提出：

> **AI 上下文负债** = 代码库关于自身的信息 与 AI 工具需要才能生成正确输出所需信息之间的缺口

**具体表现**：

| 你的代码库 | AI 以为的代码库 | 结果 |
|-----------|----------------|------|
| 异常类叫 `AppException` | 抛泛型 `Error` | 代码不符合规范 |
| 依赖带结构化字段的日志封装 | 写了 `console.log` | 破坏运维看板 |
| 40,000 行旧模式 + 8,000 行新模式 | 倾向旧模式 | 生成不符合新技术栈 |
| 订单状态需查日志表最后一条记录 | 建干净的数据表做标准 CRUD | 审核成本 > 生成节省 |

这些错误**抽象层面正确**，但**具体上下文错误**。传统技术债可追溯，AI 上下文负债出问题前无从察觉。

关键结论：**代码越混乱，AI 效率提升越可疑。**

> MIT 2025 年调查：95% 的企业没有从 AI 投资中获得有意义的回报。原因不是模型不行。DeepSeek V4 在 2026 年 4 月追平了闭源旗舰，模型供给侧瓶颈被打破，**组织知识管理成为唯一瓶颈**。

### 4.2 代码库健康度：决定 Fast/Slow 效果的前提

Fast Path 的成功率直接取决于代码库的健康度：

```
代码库健康度          Fast Path 成功率         Slow Path 轮次
   ⭐⭐⭐⭐⭐                85%+                   1-2 轮
   ⭐⭐⭐⭐                   70-85%                2-3 轮
   ⭐⭐⭐                     50-70%                3-5 轮
   ⭐⭐                       <50%                   >5 轮
   ⭐                      Fast 失效频繁            根本跑不通
```

**如果代码库不健康，Fast Path 频繁升级到 Slow Path，Slow Path 需要大量轮次才能达标——双路径的"快"就被上下文负债吃掉了。**

### 4.3 应对 AI 上下文负债的五项基础工作

Raza 提出五条必须在 Fast/Slow 运行之前或同期完成的任务：

| # | 工作 | 内容 | 由谁负责 | 优先级 |
|:-:|------|------|---------|:-----:|
| 1 | **架构规则文件** | 告诉 AI 代码库不可逾越的边界（模块依赖方向、分层约定、禁止使用的 API） | 架构师 | 🔴 最高 |
| 2 | **系统行为文档** | 运行时依赖、故障模式、启动顺序、配置项含义 | 运维/DevOps | 🔴 高 |
| 3 | **领域知识文档** | 代码表面读不出的业务概念——"退款必须同时写三张表"、"发货超30天走人工" | 业务方/PM | 🔴 高 |
| 4 | **实战验证的提示模板库** | 针对项目常见任务的标准化 prompt，减少每次重复试错 | 技术 Leader | 🟡 中 |
| 5 | **PR 审查标准** | 要求 AI 辅助生成的代码注明所用上下文和参考文件——强制 Agent 说明"我基于什么做出了这个判断" | 全部 | 🟡 中 |

这五项工作直接对应到我们的方案中：

| 方案中的组件 | 对应哪项基础工作 |
|------------|----------------|
| **Program.md** | ① 架构规则 + ② 系统行为（部分） |
| **5 维评分中的"正确性"维度** | ⑤ 强制 Agent 说明上下文来源 |
| **SDD 团队落地筑基阶段** | ①②③④ 全部在筑基期完成 |
| **信息检索增强** | ③ 领域知识需要被 Agent 检索到才能引用 |

### 4.4 Brownfield（棕地项目）的渐进策略

文章指出了一个残酷现实：**老旧项目只能蚕食，不能推倒重来。**

```
新功能 / 重构模块 → 写 spec → 走 Fast/Slow
         │
         ├── 新代码有 spec ───────────────── ✔️ 质量可控
         │
         └── 旧代码无 spec ───────────────── ❌ 接口不规整
                     │                      状态转换条件藏在旧代码中
                     ▼
              集成时可能崩溃
              （新加校验 → 老代码依赖校验不存在时的默认行为）
```

**策略**：不追求全量覆盖，而是**增量蚕食**：

1. 每个**新功能**都写 spec（从 0% 到 x%）
2. 每个**重构模块**都补 spec（从 x% 到 y%）
3. 每条**线上故障**都补文档（防止同类问题再次被 AI 误判）
4. 当 spec 覆盖率达到某个临界点时——**真正的效率回报才会出现**

> 文章引用的朋友公司总结很精辟："我们现在用 AI，其实就是在用一个放大器。代码库是干净的，它就放大效率和创造力；代码库一团乱麻，它就放大混乱。"

### 4.5 与 Fast/Slow 的结合

```
┌─────────────────────────────────────────┐
│    运行 Fast/Slow 之前必须先做            │
│                                         │
│  Step 0: 评估代码库健康度                  │
│  ├── 有架构规则文件吗？                    │
│  ├── 关键业务逻辑有文档吗？                │
│  └── 模块依赖关系清晰吗？                  │
│                                         │
│  如果三答都是"否"：                         │
│  └── 筑基阶段延长 1-2 周，先补文档再跑流程  │
│                                         │
│  如果部分有：                              │
│  └── 用 Program.md 兜底缺失的部分          │
│      Fast 不通过 → 说明上下文不够 →        │
│      补文档 → 重试                        │
└─────────────────────────────────────────┘
```

### 4.6 关于 Spec-Driven Development（SDD）

文章中提到的 **Specification-Driven Development**（不是我们的 Subagent-Driven Development，但缩写相同）是一个互补概念：

> 规格从属于代码 → 代码从属于规格

GitHub 的 spec-kit 和 OpenSpec 两个项目推动"先写规格再写代码"。规格文件与代码一起版本化，AI 在生成时以规格为唯一依据。

**与我们方案的对照**：

| SDD（Spec-Driven） | 我们的 Fast/Slow |
|:-----------------:|:----------------:|
| 聚焦**写什么** | 聚焦**怎么写好** |
| 规格文件是输入 | Program.md 是约束 |
| 适合新项目/新功能 | 棕地项目也适用 |
| 鼓励先思后写 | 鼓励先试后审 |

两者不冲突，可以串联使用：

```
需求 → SDD（写规格）→ Fast/Slow（实现）→ 审核 → 交付
```

### 4.7 Context Engineering：从提示词工程到上下文工程

2026 年，"Prompt Engineering（提示词工程）"正在被 **Context Engineering（上下文工程）** 所取代。Packmind 的 Context Engineering 指南是一个实质性进展：

**两者的本质区别：**

| 维度 | Prompt Engineering | Context Engineering |
|------|:-----------------:|:------------------:|
| **关注点** | 单次交互的输入质量 | 整个团队的信息环境 |
| **载体** | 写在聊天框里 | 版本化在代码库中 |
| **维护者** | 个人 | 团队（有 owner） |
| **持久性** | 用完即弃 | 持续演进，与代码同行 |
| **范围** | 一个模型 | 所有工具和 Agent |

**关键数据：** Stanford/SambaNova 2025 年研究（ACE）表明：**增量式结构化上下文更新相比静态 prompt 可减少 86% 的漂移和延迟**。Context 而非模型大小，才是真实的性能前沿。

#### 分层上下文文件方案

不推荐一个巨大的 `CLAUDE.md`，而是按目录分层：

```
/CLAUDE.md              → 项目总览、全局约定
/backend/CLAUDE.md      → 后端技术栈、模式、反模式
/frontend/CLAUDE.md     → 组件约定、状态管理
/infrastructure/CLAUDE.md → 部署、环境、工具链
```

每个文件包含清晰的 H2 章节（## Architecture、## Conventions、## Testing、## Commands），每条规则附带 exact 的构建/测试命令。

**原则：** 一份专注于 400 token 的上下文文件，效果优于一份 4000 token 的大杂烩。

#### 上下文治理（ContextOps）

> "上下文工程将在未来 12-18 个月内从创新差异化因素转变为企业 AI 基础设施。" — Neeraj Abhyankar, R Systems VP of Data and AI

**ContextOps 的四个实践：**

| 实践 | 做法 |
|------|------|
| **作为代码管理** | 上下文文件进 Git，随代码变更一起更新，在 PR 中审查 |
| **指定 owner** | 每个上下文文件有明确的维护者，月度 review 有效性 |
| **metadata 标注** | 文件头标注 `last_updated`、`owner`、`scope`、`reviewed_by` |
| **PR 模板联动** | 新增 check：变更是否影响编码规范？如是，上下文文件更新了吗？ |

#### 在我们的方案中的集成

目前我们的方案使用单个 **Program.md** 作为宪法文件。Context Engineering 的启示是：

1. **Program.md 可以分层** — 根目录的全局宪法 + 各模块的子上下文
2. **每条规则最好附带 exact 命令** — 不只是"测试覆盖率 ≥ 70%"，而是"运行 `pytest --cov=src --cov-fail-under=70`"
3. **上下文文件需要版本历史和 owner** — 不是写完就忘了
4. **Architecture Decision Record（ADR）应作为上下文注入** — 关键架构决策的历史背景比代码本身更能指导 AI

这不会替代现有的 Program.md 概念，而是完善它——从"一份宪法"进化到"一套上下文体系"。


## 五、什么时候升级到 Slow Path？

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

## 六、Slow Path 的架构

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

---

## 七、核心机制详解

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


## 八、完整编排逻辑

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

## 九、Hermes Agent 上的实现步骤

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

---

## 十、与现有工作流的集成

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

### 9.3 风险分级审核——解决 AI 带来的 Review 瓶颈

Faros Paradox（2026 年工程报告）揭示了一个残酷事实：**AI 让代码生成速度提升 3-5 倍，但 PR 审核时间延长了 91%**。如果不解决审核瓶颈，Fast Path 的"快"毫无意义。

**方案**：对每个变更自动评分风险级别，分级处理：

```python
def risk_score(pr):
    score = 0
    score += len(pr.files_changed) * 0.5          # 改动文件越多分越高
    score += sum(1 for f in pr.files if "security" in f or "auth" in f) * 3  # 安全文件加权
    score += pr.insertions / 100                   # 代码量
    score += len(pr.dependency_changes) * 5        # 依赖变更高风险
    return score

risk = risk_score(pr)
if risk < 5:
    auto_merge = True      # 🟢 低风险 → Fast Path → 自动合并
elif risk < 15:
    need_review = True     # 🟡 中风险 → Fast Path + 人工抽查
else:
    slow_path = True       # 🔴 高风险 → 直接走 Slow Path
```

**CI 中的风险评分面板：**

| 评分维度 | 低风险（🟢） | 中风险（🟡） | 高风险（🔴） |
|---------|:----------:|:----------:|:----------:|
| 文件改动 | 1-2 个文件 | 3-5 个文件 | 6+ 个文件 |
| 安全影响 | 无安全相关 | 涉及非关键数据 | 涉及用户数据/支付 |
| 依赖变更 | 无 | 小版本升级 | 新依赖/大版本 |
| 逻辑复杂度 | 单文件内部修改 | 跨模块调用 | 架构性变更 |
| **处理方式** | Fast Path + 自动合并 | Fast Path + 人工抽查 | Slow Path + 交叉审核 |

这解决了 Faros Paradox：不是让人力审核追上 AI 生成速度，而是**让 AI 审核承担 80% 的评审工作，只把最关键的 20% 留给人工**。这正是我们 Fast/Slow 分级思想的自然延伸。

---

## 十一、SDD 团队落地四阶段策略

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


## 十二、更多 AI 辅助开发模式

Fast/Slow 双路径覆盖了日常开发的 90% 场景。但还有一些场景——架构决策、性能优化、高风险模块、大型项目——需要其他模式来补充。这些模式**不是替代** Fast/Slow，而是**按需叠加**的增强层。

### 11.1 辩论式（Multi-Agent Debate）

当需要做出**设计决策**而非写实现时适用。

#### 核心思想

```
设计方案 A: Agent X 独立构思并输出
设计方案 B: Agent Y 独立构思并输出

    各自列出优缺点

双方互相 critique（发现对方盲区）

    合成最优方案 或 投票选出胜者
```

#### 与 Slow Path 的区别

| 维度 | Slow Path（迭代评分式） | 辩论式 |
|------|:---------------------:|:------:|
| **方向** | 串行（改→审→再改） | 并行（多方案同时产出） |
| **目标** | 提高实现质量 | 验证设计正确性 |
| **产出** | 一段代码 | 一个决策 |
| **适用** | "怎么实现" | "该选哪个方案" |

#### 典型场景

| 场景 | 辩论问题 | 参与者 |
|------|---------|--------|
| 数据库选型 | MySQL vs PostgreSQL vs 自研 | 各 Agent 代表一种方案 |
| API 风格 | REST vs GraphQL vs gRPC | 各 Agent 代表一种风格 |
| 架构模式 | 微服务 vs 模块化单体 vs 事件驱动 | 各 Agent 代表一种架构 |
| 缓存策略 | Redis vs 本地缓存 vs CDN | 各 Agent 代表一种策略 |

#### 工程实现

```python
def debate(question, candidates, rounds=3):
    """
    question: "用户系统应该用 MySQL 还是 PostgreSQL?"
    candidates: [Agent_MySQL, Agent_PostgreSQL, Agent_Neutral]
    """
    arguments = {}
    
    for round in range(rounds):
        for agent in candidates:
            # 每位 Agent 看到其他人的论点后就反驳或改进
            context = format_debate_context(question, arguments, agent.stance)
            response = agent.argue(context)
            arguments[agent.name] = response
    
    # 中立 Agent 做最终裁决
    verdict = Agent_Neutral.judge(question, arguments)
    return verdict
```

#### 与 Fast/Slow 的结合

```
需要做设计决策？
  ├── 简单决策（用 Redis 还是 Memcached？）
  │   └── 单 Agent 直接判断 → 走 Fast Path
  │
  └── 复杂决策（上云还是自建机房？）
      └── 辩论式 → 产出决策 → 走 Fast/Slow 实现
```

**推荐工具**：Hermes 的 `delegate_task` 可以并行派多个 Subagent 各自输出方案。

---

### 11.2 进化式（Evolutionary / Genetic）

当需要**优化已有代码**（性能、内存、延迟）而非从零实现时适用。

#### 核心思想

借鉴进化算法：对代码做微小修改（变异），跑测试评估（选择），保留高分方案（遗传）。

```
┌────────────────────────────────────┐
│ 第 1 代：生成 3-5 个不同实现方案     │
│  ┌──────┐ ┌──────┐ ┌──────┐       │
│  │方案 A│ │方案 B│ │方案 C│       │
│  └──────┘ └──────┘ └──────┘       │
│         ↓                          │
│ 评估：测试通过率 + 性能指标           │
│         ↓                          │
│ 淘汰最低分，保留最优方案               │
│         ↓                          │
│ 第 2 代：对最优方案做变异 + 交叉      │
│         ↓                          │
│ 重复直到性能达标或达到最大代数          │
└────────────────────────────────────┘
```

#### 与 Slow Path 的区别

| 维度 | Slow Path（迭代评分式） | 进化式 |
|------|:---------------------:|:------:|
| **改进方向** | 审核反馈**告诉**Agent 改哪里 | 变异+测试**发现**哪些改动有效 |
| **探索性** | 低（Agent 按 feedback 改） | 高（随机变异可能发现意外优化） |
| **确定性** | 稳定（评分达标即完成） | 不确定（可能有退化变异） |
| **适用** | 功能实现质量 | 性能/内存/延迟优化 |

#### 典型场景

| 场景 | 例子 | 变异操作 |
|------|------|---------|
| 性能优化 | 将 O(n²) 循环改成 O(n log n) | 替换数据结构、缓存中间结果 |
| 内存优化 | 减少不必要的对象分配 | 对象池化、复用缓冲区 |
| 延迟优化 | 减少数据库查询次数 | 批量查询、懒加载、连接复用 |
| 代码压缩 | 减少重复代码 | 提取公共函数、简化条件逻辑 |

#### 工程实现

```python
def evolution(base_code, test_cmd, metric_extractor, generations=10, population=5):
    """
    base_code: 要优化的原始代码
    test_cmd: 测试命令（如 "pytest tests/"）
    metric_extractor: 从测试输出中提取性能指标的函数
    """
    # 第 0 代：原始代码
    population = [base_code] * population
    
    for gen in range(generations):
        scores = []
        for code in population:
            # 变异
            mutated = mutate(code)
            # 测试
            test_output = run(test_cmd, mutated)
            score = metric_extractor(test_output)
            scores.append((score, mutated))
        
        # 选择：保留前 50%
        scores.sort(reverse=True, key=lambda x: x[0])
        survivors = [s[1] for s in scores[:population//2]]
        
        # 繁殖：交叉生成下一代
        population = survivors + [crossover(survivors) for _ in range(population - len(survivors))]
        
        # 检查是否显著优于基线
        if scores[0][0] >= target_metric:
            return scores[0][1]
    
    return scores[0][1]  # 返回最优个体
```

> **安全机制**：必须强制 git revert 保护——如果变异后的代码导致测试失败，自动回滚到上一代。不允许退化。

#### 与 Fast/Slow 的结合

```
需要性能优化？
  └── 进化式探索变异空间
      └── 找到最优代码后
          └── 走 Fast Path 审核确认（防止副作用）
```

---

### 11.3 角色分工式（Role-Based）

当需要**多个专业角色协作**完成一个大型任务时适用。

#### 核心思想

模拟软件公司组织结构，每个 Agent 有明确的角色和交付物。

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  产品经理   │ → │   架构师   │ → │   工程师   │ → │   测试员   │
│            │   │            │   │            │   │            │
│ 输出: PRD  │   │ 输出: 设计 │   │ 输出: 代码 │   │ 输出: 测试 │
│            │   │ 文档       │   │            │   │ 报告       │
└────────────┘   └────────────┘   └────────────┘   └────────────┘
     │                │                │                │
     └──── 上游产出 ──┴── 作为输入 ────┴── 下游验证 ────┘
```

#### 角色与输出

| 角色 | 职责 | 交付物 | 依赖 |
|:----:|------|--------|:----:|
| **PM** | 理解需求，拆解为可执行任务 | PRD、用户故事 | — |
| **架构师** | 设计系统结构、接口、数据流 | 架构文档、API 设计 | PM 的 PRD |
| **工程师** | 实现代码、单元测试 | 功能代码、测试 | 架构设计 |
| **测试员** | 集成测试、边界验证 | 测试报告、Bug List | 实现代码 |
| **运维** | 部署配置、监控告警 | 部署脚本、Dockerfile | 测试通过代码 |

#### 与 Fast/Slow 的区别

| 维度 | Fast/Slow 双路径 | 角色分工式 |
|------|:--------------:|:----------:|
| **拆分维度** | 按**任务粒度**（复杂度） | 按**角色职责**（专业度） |
| **子任务关系** | 并行或顺序 | **严格递进**（上游输出是下游输入） |
| **质量保证** | 交叉审核 + 评分 | **角色校验**（下游验证上游） |
| **适用** | 单个 feature 的质量 | 完整项目的端到端交付 |

#### 典型场景

| 场景 | 为什么需要角色分工 |
|------|-----------------|
| 从零搭建新服务 | 需要先后做需求、架构、编码、测试 |
| 大型重构 | 需要架构师设计过渡方案，工程师分批执行 |
| API 设计 | PM 定功能，架构师定接口，工程师实现，测试验证 |
| 多端开发 | 前端、后端、测试各司其职 |

#### 工程实现

```python
def role_based_workflow(task):
    # Step 1: PM 产出需求
    prd = delegate_task(
        goal="作为产品经理，将以下需求转化为 PRD",
        context=task.description,
        toolsets=['file']
    )
    
    # Step 2: 架构师根据 PRD 出设计
    design = delegate_task(
        goal="作为架构师，根据 PRD 输出技术设计文档",
        context=f"PRD: {prd}",
        toolsets=['file']
    )
    
    # Step 3: 工程师根据设计实现
    code = delegate_task(
        goal="作为工程师，根据设计文档实现代码",
        context=f"设计: {design}",
        toolsets=['terminal', 'file']
    )
    
    # Step 4: 测试员验证
    test_report = delegate_task(
        goal="作为测试员，验证实现是否符合 PRD",
        context=f"PRD: {prd}\n实现: {code}",
        toolsets=['terminal', 'file']
    )
```

#### 与 Fast/Slow 的结合

```
大型项目 → 角色分工式（先确定各角色交付物）
              │
              ├── 每个角色的子任务 → Fast/Slow 双路径
              │     （PM 任务用 Fast，工程师任务评估复杂度）
              │
              └── 角色间校验 → Slow Path 审核
                    （架构师校验工程师产出）
```

---

### 11.4 交互式（Human-in-the-Loop）

当任务**风险高**或**需要人的经验判断**时适用。

#### 核心思想

Agent 不在关键步骤上自己做决定，而是停下来问人。

```
Agent: "我打算用 PostgreSQL，可以吗？"
  ⏸️ 等回复
人: "可以，但注意连接池上限"
  ▶️ 继续
Agent: "好的。表结构设计好了：..."
  ⏸️ 等确认
人: "users.email 加唯一索引"
  ▶️ 继续
Agent: "开始实现..."
```

#### 暂停点类型

| 暂停点 | 触发条件 | 暂停内容 |
|:------:|---------|---------|
| 设计决策 | 涉及技术选型、架构方案 | "建议 X vs Y，选哪个？" |
| 安全确认 | 涉及数据访问、权限变更 | "以下修改涉及用户数据，是否允许？" |
| 资源变更 | 涉及成本、基础设施 | "需要申请新的云资源，是否批准？" |
| 边界判断 | 业务规则不明确 | "这个边界 case 怎么处理？" |
| 合并确认 | Slow Path 异常终止 | "评分不达标但超过最大轮次，是否强制合并？" |

#### 与 Fast/Slow 的区别

| 维度 | Fast/Slow（全自动） | 交互式 |
|------|:-----------------:|:------:|
| **自动化程度** | 高（自动升级、自动合并） | 低（关键节点等确认） |
| **适用风险** | 中低风险日常开发 | 高风险、高不确定性 |
| **速度** | 快（分钟级） | 慢（取决于人回复速度） |
| **适用场景** | 80% 的常规任务 | 20% 需要人的经验判断 |

#### 实现位置

交互式不是独立模式，而是**在其他模式上叠加的暂停层**：

```
Fast / Slow / 辩论 / 进化
         │
         ▼
    ┌────────────┐
    │ 交互式暂停点 │ ─── 满足条件 → 暂停等人
    └────────────┘
         │
         ▼
    继续执行
```

#### 与 Fast/Slow 的结合

```python
def run_with_human_checkpoints(mode, task):
    if mode == "slow" or mode == "debate":
        # 设计决策需要人确认
        answer = ask_human(
            question="架构方案建议：... 是否同意？",
            choices=["同意并继续", "修改方案", "终止"]
        )
        if answer == "终止":
            return
    
    # 继续执行
    result = execute(mode, task)
    
    # Slow Path 异常终止时
    if result["status"] == "escalate":
        answer = ask_human(
            question=f"任务 {task.id} 评分停滞，是否强制合并？\n"
                     f"历史评分：{result['scores']}",
            choices=["强制合并", "交给人工修改", "放弃"]
        )
```

---

### 11.5 自改进式（Self-Improving）

当**重复性工作**频繁出现，Agent 应该学会自己写工具来加速。

#### 核心思想

```
Agent 发现重复性工作模式
  → 自动生成一个 skill/脚本/工具
  → 注入自己的工作流
  → 下次遇到同类任务直接调用
```

#### 与 Fast/Slow 的区别

| 维度 | Fast/Slow（执行） | 自改进式（元学习） |
|------|:--------------:|:----------------:|
| **关注点** | 当前任务的完成质量 | 未来任务的执行效率 |
| **产出** | 完成一次任务 | 生产一个工具/模板 |
| **时间线** | 短期（分钟~小时） | 长期（持续积累） |
| **适用** | 单个任务的质量 | 整个团队的效率提升 |

#### 典型模式

| 模式 | 例子 |
|------|------|
| skill 自动生成 | "这个公司的 API 风格很一致，生成一个 skill 下次复用" |
| 模板提取 | "这个 CRUD 模式出现了 5 次，提取为模板" |
| 知识固化 | "项目常用的 10 条规范，自动更新到 Program.md" |
| 工具链优化 | "每次部署都要改 3 个文件，写个脚本一键搞定" |

#### 与 Fast/Slow 的结合

自改进式是**所有模式的上层**——不管走 Fast 还是 Slow，只要发现重复模式，就自动生成工具：

```
Fast Path 执行任务
  → 发现某段代码结构和上次类似
  → 自动提取为 skill
  → 下次类似任务直接调用 skill

Slow Path 执行任务
  → 审核发现 3 个文件改了同一类内容
  → 自动生成批量修改脚本
  → 下次一键执行
```

---

### 11.6 模式选择决策树

```
这个任务是什么类型？
  │
  ├── 实现一个功能 / 修一个 bug
  │   └── 走 Fast/Slow 双路径（默认）
  │
  ├── 做设计决策（选数据库、选架构）
  │   └── Fast/Slow + 辩论式增强
  │
  ├── 优化已有代码的性能
  │   └── 进化式（探索最优解）
  │
  ├── 从零搭建一个完整系统
  │   └── 角色分工式（PM→架构→开发→测试）
  │
  └── 任务风险高 / 规则不明确
      └── 任何模式 + 交互式暂停点
          └── 发现重复模式 → 自改进式提取 skill
```

### 11.7 模式对比总表

| 模式 | 适用场景 | 自动化程度 | 探索性 | 适合谁用 |
|:----:|---------|:---------:|:-----:|---------|
| 审核式（Fast） | 日常开发 | ⭐⭐⭐⭐⭐ | ⭐ | 所有团队成员 |
| 迭代评分式（Slow） | 复杂实现 | ⭐⭐⭐⭐ | ⭐⭐ | 核心开发者 |
| 辩论式 | 设计决策 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 架构师 |
| 进化式 | 性能优化 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 高级工程师 |
| 角色分工式 | 大型项目 | ⭐⭐⭐ | ⭐ | 全团队协作 |
| 交互式 | 高风险场景 | ⭐⭐ | ⭐ | 所有 + 人工确认 |
| 自改进式 | 重复工作 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 工具链维护者 |

---


## 十三、监控指标体系

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

---

## 十四、FAQ

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

## 文献参考

本文引用的关键外部来源，按使用章节排列：

### AI 辅助开发效率与瓶颈

| 来源 | 作者/机构 | 年份 | 本文引用位置 |
|------|----------|:----:|:----------:|
| **METR Paradox** — RCT 对照实验：AI 感知提速 vs 实际完成率 | METR 研究团队 | 2026 | [metr.org](https://metr.org/blog/2026-02-24-uplift-update/) |
| **Faros Paradox** — AI 代码导致 PR 审核时间 +91% | Faros Engineering Report | 2026 | [faros.ai](https://www.faros.ai/blog/ai-acceleration-whiplash-takeaways) |
| **DORA Mirror** — AI 放大现有团队质量差距 | Djimit（N=906 调查） | 2026 | [djimit.nl](https://djimit.nl/ai-tooling-for-software-engineers-in-2026/) |
| **DORA 2025 研究报告** — AI 辅助编码对交付速度的影响 | DORA / CodeRabbit | 2025-2026 | [dora.dev](https://dora.dev/guides/dora-metrics/) |
| **95% 企业未从 AI 投资获得有意义的回报** | MIT 调查 | 2025 | §四 文中引用 |

### AI Context Debt 与上下文工程

| 来源 | 作者/机构 | 年份 | 本文引用位置 |
|------|----------|:----:|:----------:|
| **AI Context Debt** 概念原创 | Abbas Raza | 2026.04 | [LinkedIn](https://www.linkedin.com/posts/abbasraza_most-engineering-teams-deploying-ai-tools-activity-7449869888673718272-Kw6O) |
| **InfoQ 深度解析：AI 上下文负债** | InfoQ | 2026 | [infoq.cn](https://www.infoq.cn/article/K7hpIOogPsLlPQz4lwXu) |
| **Context Engineering 最佳实践指南** | Laurent Py / Packmind | 2026 | [packmind.com](https://packmind.com/context-engineering-ai-coding/context-engineering-best-practices/) |
| **ACE 研究：增量上下文更新减少 86% 漂移** | Stanford / SambaNova | 2025.10 | [packmind.com](https://packmind.com/context-engineering-ai-coding/context-engineering-playbook/) |
| **GitClear 报告：AI 时代代码重复率 4 倍增长** | GitClear | 2024 | [gitclear.com](https://www.gitclear.com/ai_assistant_code_quality_2025_research) |
| **Index.dev 报告：41% 代码为 AI 生成** | Index.dev | 2026 | §四 |

### AutoResearch 与多 Agent 模式

| 来源 | 作者/机构 | 年份 | 本文引用位置 |
|------|----------|:----:|:----------:|
| **AutoResearch** 方法论与开源实现 | Andrej Karpathy | 2026 | [github.com/karpathy](https://github.com/karpathy/autoresearch) |
| **通用化 AutoResearch 到非 ML 任务** | Udit Goenka | 2026 | [github.com/uditgoenka](http://github.com/uditgoenka/autoresearch) |
| **5 种 AI 隐藏技术债** | Ajay Mudettula / DEV | 2026 | [dev.to](https://dev.to/ajay_mudettula/5-hidden-technical-debts-ai-is-adding-to-your-codebase-2026-5g3c) |

### 方法论与工具

| 来源 | 作者/机构 | 年份 | 本文引用位置 |
|------|----------|:----:|:----------:|
| **Specification-Driven Development**（spec-kit, OpenSpec） | GitHub / 社区 | 2026 | [github.com/github](https://github.com/github/spec-kit) |
| **Claude Code Agent 模式与 /goal 系统** | Anthropic | 2025-2026 | [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/overview) |
| **Hermes Agent Subagent-Driven-Development** | Hermes Agent 社区 | 2026 | [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs) |

如需深入了解其中任一来源，可在对应 URL 搜索原文（部分来源为付费/闭源报告，摘要可通过公开渠道获取）。

---

## 十五、总结

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