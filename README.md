# tarik-prompt

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](pyproject.toml)
[![Agent Skill](https://img.shields.io/badge/SKILL.md-Claude%20%7C%20Cursor%20%7C%20Gemini-6E56CF.svg)](SKILL.md)

**Strategic bilingual (English / Arabic) AI prompt engineering skill (`SKILL.md`) and model-aware prompt compiler (`tarik-prompt`) for Claude, ChatGPT, and Gemini.**

Most prompt "optimizers" apply a single generic template to every LLM and inflate good prompts with verbose theory. `tarik-prompt` diagnoses ambiguity first (`BASIC` vs `DETAIL` mode) and compiles task-specific guardrails into the native structural format each frontier model follows best:
- **Claude:** Semantic XML long-context tags (`<role>`, `<context>`, `<instructions>`, `<constraints>`, `<output_format>`) with explicit pre-output validation.
- **ChatGPT:** Top-down Markdown context layering (`Role -> Context -> Instructions -> Constraints -> Output Format`).
- **Gemini:** Multimodal input anchors cross-referencing text, attached media, and strict output schemas.

---

## Install as an AI Agent Skill (`SKILL.md`)

Copy this repository into your agent skills directory (works with **Claude Code**, **Antigravity**, **Cursor**, and `SKILL.md`-compatible runners):

```bash
git clone https://github.com/tarikra1/tarik-prompt.git ~/.claude/skills/tarik-prompt
```

Invoke `/tarik-prompt` (or in Arabic: `حسن البرومبت` / `مهندس أوامر`) in `BASIC` mode for instant optimization, or `DETAIL` mode to answer up to 3 high-leverage diagnostic questions before compilation.

---

## Install & Use the Python CLI

```bash
pip install -e .

# Compile a Claude XML technical prompt
tarik-prompt "Build an async webhook worker with retry backoff" --model claude --task technical

# Diagnose whether a raw draft needs clarifying questions (BASIC vs DETAIL)
tarik-prompt "write code for payments" --diagnose
```

---

## نبذة بالعربية

مهارة وأداة هندسة أوامر احترافية تحوّل الأفكار الخام إلى أوامر محكمة البنية وجاهزة للنسخ والاستخدام المباشر حسب النموذج المستهدف ونوع المهمة:

- تشخيص تلقائي للغموض عبر وضع التنفيذ السريع أو الوضع التفصيلي.
- تخصيص هيكلي دقيق لكل نموذج ذكاء اصطناعي مع قواعد صارمة لتقليل الهلوسة البرمجية.
- دعم كامل للغتين العربية والإنجليزية في المهارة وأداة سطر الأوامر.

---

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## License

Released under the [MIT License](LICENSE).
