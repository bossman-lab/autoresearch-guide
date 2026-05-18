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
