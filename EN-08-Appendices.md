## 13. Monitoring Metrics

After going live, track at least the following metrics:

| Metric | Normal Range | Warning Threshold | Meaning |
|:-------|:------------:|:-----------------:|:--------|
| Fast Path success rate | 70-85% | < 50% | Fast review criteria has issues |
| Fast→Slow upgrade rate | 15-30% | > 40% | Complexity assessment is inaccurate |
| Slow Path average rounds | 3-5 rounds | > 10 rounds | Threshold may be too high |
| Slow Path pass rate | 60-80% | < 40% | 9.0 threshold is too high |
| Manual intervention rate | < 10% | > 20% | Automated process needs checking |
| Average token consumption per task | — | Continuously rising | Check for over-iteration |

---

---

## 14. FAQ

**Q: What if we only have one model?**
A: Cross-review effectiveness will be reduced, but it's still better than nothing. It's recommended to configure at least two models from different providers.

**Q: Is the 9.0 threshold too high or too low?**
A: Start at 9.0, run for 2 weeks, then adjust based on data. If the pass rate is > 80%, increase it; if < 40%, decrease it.

**Q: Will 42 maximum iterations be too many?**
A: 42 is the upper limit; actual average is 3-5 rounds. 42 rounds is a safety net to prevent extreme cases from getting stuck.

**Q: Who should maintain Program.md?**
A: The technical lead is responsible, updating it periodically as the project evolves. Notify the full team with every change.

**Q: What if an audit finds that manual changes are better than AI?**
A: Let the scoring data speak. If manually modified code scores significantly higher than AI-automated code, it means the scoring dimensions have biases that need adjustment.

**Q: When should we bypass the automated process and go fully manual?**
A: High-frequency changes, emergency hotfixes, experimental features — these scenarios prioritize speed over process.

---

## References

Key external sources cited in this document, organized by chapter:

### AI-Assisted Development Efficiency and Bottlenecks

| Source | Author/Organization | Year | Referenced In |
|--------|--------------------|:----:|:-------------:|
| **METR Paradox** — RCT controlled experiment: AI perceived speedup vs actual completion rate | METR Research Team | 2026 | [metr.org](https://metr.org/blog/2026-02-24-uplift-update/) |
| **Faros Paradox** — AI code leading to +91% PR review time | Faros Engineering Report | 2026 | [faros.ai](https://www.faros.ai/blog/ai-acceleration-whiplash-takeaways) |
| **DORA Mirror** — AI amplifies existing team quality gaps | Djimit (N=906 survey) | 2026 | [djimit.nl](https://djimit.nl/ai-tooling-for-software-engineers-in-2026/) |
| **DORA 2025 Research Report** — Impact of AI-assisted coding on delivery speed | DORA / CodeRabbit | 2025-2026 | [dora.dev](https://dora.dev/guides/dora-metrics/) |
| **95% of enterprises not receiving meaningful returns from AI investment** | MIT Survey | 2025 | §4 cited in text |

### AI Context Debt and Context Engineering

| Source | Author/Organization | Year | Referenced In |
|--------|--------------------|:----:|:-------------:|
| **AI Context Debt** concept original | Abbas Raza | 2026.04 | [LinkedIn](https://www.linkedin.com/posts/abbasraza_most-engineering-teams-deploying-ai-tools-activity-7449869888673718272-Kw6O) |
| **InfoQ Deep Dive: AI Context Debt** | InfoQ | 2026 | [infoq.cn](https://www.infoq.cn/article/K7hpIOogPsLlPQz4lwXu) |
| **Context Engineering Best Practices Guide** | Laurent Py / Packmind | 2026 | [packmind.com](https://packmind.com/context-engineering-ai-coding/context-engineering-best-practices/) |
| **ACE Research: Incremental context updates reduce drift by 86%** | Stanford / SambaNova | 2025.10 | [packmind.com](https://packmind.com/context-engineering-ai-coding/context-engineering-playbook/) |
| **GitClear Report: Code duplication rate grows 4x in AI era** | GitClear | 2024 | [gitclear.com](https://www.gitclear.com/ai_assistant_code_quality_2025_research) |
| **Index.dev Report: 41% of code is AI-generated** | Index.dev | 2026 | §4 |

### AutoResearch and Multi-Agent Patterns

| Source | Author/Organization | Year | Referenced In |
|--------|--------------------|:----:|:-------------:|
| **AutoResearch** methodology and open-source implementation | Andrej Karpathy | 2026 | [github.com/karpathy](https://github.com/karpathy/autoresearch) |
| **Generalizing AutoResearch to non-ML tasks** | Udit Goenka | 2026 | [github.com/uditgoenka](http://github.com/uditgoenka/autoresearch) |
| **5 Hidden Technical Debts from AI** | Ajay Mudettula / DEV | 2026 | [dev.to](https://dev.to/ajay_mudettula/5-hidden-technical-debts-ai-is-adding-to-your-codebase-2026-5g3c) |

### Methodology and Tools

| Source | Author/Organization | Year | Referenced In |
|--------|--------------------|:----:|:-------------:|
| **Specification-Driven Development** (spec-kit, OpenSpec) | GitHub / Community | 2026 | [github.com/github](https://github.com/github/spec-kit) |
| **Claude Code Agent patterns and /goal system** | Anthropic | 2025-2026 | [docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code/overview) |
| **Hermes Agent Subagent-Driven-Development** | Hermes Agent Community | 2026 | [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/docs) |

For deeper understanding of any of these sources, search for the original text at the corresponding URL (some sources are paid/closed reports; abstracts can be obtained through public channels).

---

## 15. Summary

The core insight of "Fast first, Slow second" in three sentences:

1. **Don't waste on simple tasks** — Fast Path passes in one go; 80% of tasks complete in under 5 minutes
2. **Don't sacrifice on complex tasks** — Slow Path automatically catches you; cross-review + quantitative scoring + iterative loop
3. **No human judgment needed** — The upgrade logic is code-level, not gut-feel

The end result:

```
Simple tasks don't waste tokens
Complex tasks don't sacrifice quality
Automatic upgrades don't need human judgment
```
