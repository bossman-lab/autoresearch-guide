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