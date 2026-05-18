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