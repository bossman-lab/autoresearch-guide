# 先快后慢：AI 辅助开发的双路径质量保障体系

Fast/Slow 双路径方案完整文档。80% 的简单任务不浪费 token，20% 的复杂任务不牺牲质量。

## 文档列表

| 文件 | 大小 | 内容 | 适合读者 |
|------|:----:|------|---------|
| [📖 完整方案](00-complete-guide.md) | 48KB | **第一篇就在这里**，15 章全量内容 | 想一次读完的人 |
| [01 概念篇](01-concept.md) | 3KB | 根本矛盾、双路径策略总览 | 所有团队成员快速理解 |
| [02 Fast Path 详解](02-fastpath.md) | 3KB | Hermes SDD 基线方案、三阶段四步走 | 开发工程师 |
| [03 AI 上下文负债](03-ai-context-debt.md) | 7KB | AI Context Debt、Brownfield 策略、SDD 对照 | 技术 Leader |
| [04 Slow Path 详解](04-slowpath.md) | 10KB | 升级条件、AutoResearch 架构、核心机制 | 核心开发者 |
| [05 实现与集成](05-implementation.md) | 4KB | 编排逻辑、Hermes 实现、PR/CI 集成 | 实施工程师 |
| [06 团队落地策略](06-team-rollout.md) | 5KB | SDD 四阶段：筑基→试点→推广→深化 | 团队 Leader |
| [07 扩展模式](07-advanced-patterns.md) | 18KB | 辩论式 / 进化式 / 角色分工 / 交互式 / 自改进 | 架构师 + 高级工程师 |

## 建议阅读顺序

```
新人入门: 01 → 03 → 06
技术实施: 02 → 05 → 07
深度理解: 01 → 03 → 04 → 06
完整阅读: 00-complete-guide.md
```

## 更新记录

- 2026-05-18: 初始发布，15 章完整方案
- 2026-05-18: 整合 AI Context Debt、Brownfield 策略、SDD 对照
- 2026-05-18: 拆分为 7 篇独立文章 + 1 篇完整文档
