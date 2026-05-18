---
title: "实战指南：如何用 Hermes Agent 搭建 Fast/Slow 双路径开发流水线"
date: 2026-05-18
author: "提灯人"
tags: [Hermes Agent, 实战, FastSlashSlow, Automation, devops]
---

> **一句话摘要**：在 Hermes Agent 框架上一步步搭建 Fast/Slow 双路径质量保障系统，从 plan 解析到自动审核到迭代闭环的完整实现。

---

## 一、前置条件

本文假设你已经在使用 Hermes Agent，并且：

- [x] Hermes Agent 已配置并运行
- [x] 可用的 `delegate_task`（subagent 调度）
- [x] 至少一个代码分析的 API / 语言模型（deepseek / claude / codestral）
- [x] Git 仓库，有 test 命令

---

## 二、快速起步：30 分钟跑通核心流程

### Step 1：创建 Program.md 宪法

```bash
mkdir -p ~/.hermes/autoresearch
cat > ~/.hermes/autoresearch/program.md << 'EOF'
# Program.md — AutoResearch 开发宪法

## 权限边界
- 允许：修改 src/ internal/ cmd/
- 禁止：修改 .github/ CI/CD 配置

## 代码规范
- 遵循项目现有风格
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

### Step 2：创建工作流脚本

创建一个 orchestrator 脚本：

```bash
cat > ~/.hermes/scripts/autoresearch-orchestrator.sh << 'SCRIPT'
#!/bin/bash
# Fast/Slow 双路径编排器
# 用法: ./autoresearch-orchestrator.sh <plan_file> <issue_number>

PLAN_FILE=$1
ISSUE_NUM=$2

echo "📋 加载计划: $PLAN_FILE"
echo "🔢 Issue: #$ISSUE_NUM"

# Step 1: 解析 plan 获取任务列表
# 由 Hermes agent 读取 plan 文件并创建 todo

echo "⚡ 进入 Fast Path — 尝试快速执行..."
echo "  如失败会自动升级到 Slow Path"

# 实际执行由 Hermes 的 subagent 完成
# 这个脚本是 orchestration 框架的入口
SCRIPT
chmod +x ~/.hermes/scripts/autoresearch-orchestrator.sh
```

---

## 三、完整工作流详解

### 3.1 步骤 1：生成 Plan

用 `writing-plans` skill 把需求转成可执行 plan：

```
任务: "为订单系统添加退款功能"
  └── → writing-plans skill
       └── → docs/plans/refund-feature.md
```

Plan 文件结构示例：

```markdown
# 退款功能实现计划

## 任务 1: 数据库迁移
- 文件: db/migrations/20260518_add_refund.sql
- 内容: 创建 refund_requests 表

## 任务 2: Model 层
- 文件: internal/models/refund.go
- 实现 RefundRequest struct + CRUD

## 任务 3: Service 层
- 文件: internal/service/refund.go
- 实现退款业务逻辑

[复杂度评估]
- files_changed: 6
- cross_module: true
- tags: [security, transaction]
- estimated_hours: 4
→ 建议直接走 Slow Path
```

### 3.2 步骤 2：调度入口

```python
# orchestrator 的伪代码逻辑

def dispatch(plan_path):
    plan = read_plan(plan_path)
    tasks = parse_tasks(plan)
    complexity = assess_complexity(plan)
    
    for task in tasks:
        if complexity == "high":
            result = slow_path(task)
        else:
            result = fast_path(task)
            if result == "upgrade":
                result = slow_path(task)
        
        log_result(task, result, plan_path)
```

### 3.3 步骤 3：Fast Path 实现

Fast Path 的核心是**一个 subagent 一次性完成**。

在 Hermes 中，对应的就是现有的 `subagent-driven-development` skill：

```python
result = delegate_task(
    goal=task.description,
    context=f"""
    任务: {task.full_text}
    
    执行步骤:
    1. 写测试 → pytest 验证测试失败
    2. 写实现 → pytest 验证全部通过
    3. 运行完整测试套件
    
    完成前请检查:
    - [ ] 所有测试通过
    - [ ] 无 lint 错误
    - [ ] 无硬编码路径/密钥
    """,
    toolsets=['terminal', 'file']
)
```

### 3.4 步骤 4：Fast Path 审核

```python
review = delegate_task(
    goal="审核 Fast Path 产出",
    context=f"""
    审核以下任务产出是否合格:
    
    任务描述: {task.description}
    变更文件: {get_changed_files()}
    测试结果: {test_output}
    
    审核标准（二元判断）:
    - [ ] 功能正确 → 是否满足任务要求？
    - [ ] 测试完善 → 有无遗漏场景？
    - [ ] 代码可读 → 有无明显质量问题？
    
    输出:
    PASS 或 FAIL + 理由
    
    如果判定 FAIL，请明确说明:
    1. 问题是否可以小幅度修复？(是/否)
    2. 如果不修复，是否涉及架构/逻辑层面的根本问题？
    """,
    toolsets=['file', 'terminal']
)
```

### 3.5 步骤 5：升级决策

```python
def should_upgrade(review_result):
    if review_result == "PASS":
        return False
    
    if "架构" in review_result or "根本问题" in review_result:
        return True  # 架构问题 → 必须走 Slow Path
    
    if count_fast_failures(task_id) >= 2:
        return True  # 连续 2 次失败 → 升级
    
    return False  # 小问题 → 修复后重审
```

### 3.6 步骤 6：Slow Path 实现

慢路径的核心是**双模型交叉 + 反馈驱动迭代**。

在 Hermes 中的实现方式：

```python
def slow_path(task, max_rounds=42):
    # 加载 program.md
    program = read_file("~/.hermes/autoresearch/program.md")
    scores = []
    all_feedback = []
    
    for round in range(1, max_rounds + 1):
        model_A, model_B = ("deepseek", "claude") if round % 2 else ("claude", "deepseek")
        
        # 实施者 A 实现
        implementation = delegate_task(
            goal=f"第 {round} 轮实现: {task.description}",
            context=f"""
            ## 本轮角色
            你担任【实施者】
            
            ## 上一轮反馈（注入本轮）
            {format_feedback(all_feedback)}
            
            ## Program.md 宪法
            {program}
            
            ## 评分历史
            {format_score_history(scores)}
            
            ## 任务
            {task.full_text}
            """,
            toolsets=['terminal', 'file']
        )
        
        # 审核者 B 审核+评分
        review = delegate_task(
            goal=f"第 {round} 轮审核评分",
            context=f"""
            ## 本轮角色
            你担任【审核者】
            
            请按以下 5 个维度对 [实施者 {model_A}] 的产出进行评分:
            
            | 维度 | 权重 | 评分(1-10) | 说明 |
            |------|------|-----------|------|
            | 正确性 | 35% | | 功能正确？|
            | 测试 | 25% | | 覆盖率≥70%？|
            | 代码质量 | 20% | | 可读/可维护？|
            | 安全 | 10% | | 无漏洞？|
            | 性能 | 10% | | 无性能坑？|
            
            达标线: 加权总分 ≥ 9.0
            
            输出 JSON 格式:
            {{
                "scores": {{"correctness": N, "testing": N, "quality": N, "security": N, "performance": N}},
                "weighted_total": N,
                "issues": [{{"dimension": "...", "severity": "critical/important/minor", "description": "..."}}],
                "verdict": "PASS" 或 "NEEDS_WORK"
            }}
            """,
            toolsets=['file']
        )
        
        review_data = parse_review_json(review)
        scores.append(review_data)
        
        if review_data["weighted_total"] >= 9.0:
            return {"status": "approved", "rounds": round, "scores": scores}
        
        all_feedback.append(review_data["issues"])
        
        # 动态终止检查
        if round >= 3 and not is_improving(scores[-3:]):
            return {"status": "escalate", "reason": "评分停滞", "scores": scores}
    
    return {"status": "escalate", "reason": "超最大轮次", "scores": scores}
```

### 3.7 步骤 7：结果处理

```python
def handle_result(result):
    if result["status"] == "approved":
        # 自动 commit + PR
        run("git add -A && git commit -m '...'")
        run("gh pr create --title '...' --body '...'")
        notify_team(f"✅ #{issue_number} 自动完成，评分 {result['scores'][-1]['weighted_total']}")
    
    elif result["status"] == "escalate":
        # 人工介入
        save_report(result)
        notify_developer(f"⛑️ #{issue_number} 需人工介入，原因: {result['reason']}")
        notify_team(f"📊 #{issue_number} 评分报告已生成，请 @owner 查看")
```

---

## 四、最佳实践与避坑指南

### ✅ 要做

1. **小任务起步** — 第一次跑 AutoResearch 模式选一个"改一个文件 + 加几个测试"的 Issue
2. **program.md 要精炼** — 不要超过 200 行，Agent 读不完。关键规则 20 条以内
3. **审核反馈要结构化** — JSON 格式的 issues 列表比自然语言好解析百倍
4. **评分历史要在 context 中保留** — 让 Agent 看到自己是进步还是退步
5. **人工抽查** — 前 10 次 Slow Path 完成的 PR 都要人看一眼评分报告，校准阈值

### ❌ 不要做

1. **不要用同一模型既当实施者又当审核者** — 盲区重叠，交叉审核形同虚设
2. **不要在 Fast Path 启动评分** — Fast Path 就二元判断，评分放在 Slow Path
3. **不要让 Agent 自己编造测试命令** — 测试命令必须硬编码在 program.md 中
4. **不要在 context 中塞无关信息** — 每次 delegate_task 的 context 只放本轮需要的内容
5. **不要跳过 "升级" 判断** — 必须有一个明确的函数判断 "要不要升级"，不要靠感觉

### ⚠️ 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| Agent 反复修同一问题 | 反馈不具体 | 要求审核者输出具体行号+建议 |
| 评分越来越高但代码没变好 | Agent 学会了"高分模板" | 打乱维度的权重，让 Agent 无法预测 |
| Slow Path 跑完人工发现重大问题 | 评分维度覆盖不全 | 检查评分维度是否覆盖团队关注的方面 |
| 升级太频繁 | Fast Path 审核标准过低 | 提高 Fast Path 的通过标准 |

---

## 五、渐进式落地策略

不要第一天就追求全自动化。

| 阶段 | 配置 | 人工参与度 |
|------|------|-----------|
| **阶段 0：纯学习** | 跑一遍完整流程，只看结果，不自动 PR | 100% 人工检查 |
| **阶段 1：辅助评审** | Fast/Slow 都跑，Slow 结果直接出报告，人工决定是否采纳 | 人工合并 |
| **阶段 2：半自动** | Fast 自动合并（阈值 80%），Slow 出报告后自动合并（阈值 90%） | 人工抽查 + 异常处理 |
| **阶段 3：全自动** | Fast 自动合并，Slow 达标自动合并，异常上报 | 仅处理上报 |

每个阶段至少跑 2 周，积累足够的数据调整阈值的信噪比。

---

## 六、监控指标

上线后至少关注以下指标：

| 指标 | 正常范围 | 告警阈值 |
|------|---------|---------|
| Fast Path 成功率 | 70-85% | < 50% 说明 Fast 标准有问题 |
| Fast→Slow 升级率 | 15-30% | > 40% 说明复杂度评估不准 |
| Slow Path 平均轮次 | 3-5 轮 | > 10 轮考虑调整阈值 |
| Slow Path 达标率 | 60-80% | < 40% 说明 9.0 阈值太高 |
| 人工介入率 | < 10% | > 20% 检查自动流程 |
