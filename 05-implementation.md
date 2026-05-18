---
title: "实现与集成：编排逻辑 + Hermes 实现步骤 + PR/CI 工作流集成"
date: 2026-05-18
author: "提灯人"
tags: [AI, Agent, AutoResearch, 质量工程, FastSlow, Hermes]
---

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

---
