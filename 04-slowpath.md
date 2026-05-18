---
title: "Slow Path 详解：AutoResearch 增强方案 — 升级条件、架构、核心机制"
date: 2026-05-18
author: "提灯人"
tags: [AI, Agent, AutoResearch, 质量工程, FastSlow, Hermes]
---

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
