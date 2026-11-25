# Model & Task Optimization Blueprints (`tarik-prompt`)

Use these structural patterns internally when building the final prompt. Never output theory—only apply the right structure cleanly.

---

## 1. Model-Specific Architectures

### A. ChatGPT (`Structured Instructions` + `Context Layering`)
Best practices:
- Layer context from top to bottom: **Role & Objective -> Background Context -> Core Instructions -> Strict Constraints -> Output Format**.
- Use crisp Markdown headings (`#`, `##`) and numbered action rules.
- Explicitly define edge-case handling ("If input X is missing, ask or state clearly rather than guessing").

```markdown
# Role & Objective
...

# Context
...

# Execution Instructions
1. ...
2. ...

# Constraints & Guardrails
- Do NOT ...
- Ensure ...

# Output Format
...
```

### B. Claude (`XML Long-Context` + `Reasoning Structure`)
Best practices:
- Separate data/inputs from instructions using clean XML tags (`<context>`, `<input>`, `<instructions>`, `<constraints>`, `<thinking_steps>`, `<output_format>`).
- For complex or analytical tasks, instruct Claude to reason systematically through edge cases and tradeoffs before producing the final deliverable.

```xml
<role>
...
</role>

<context>
...
</context>

<instructions>
1. Analyze ...
2. Structure ...
3. Verify against constraints ...
</instructions>

<constraints>
- ...
</constraints>

<output_format>
...
</output_format>
```

### C. Gemini (`Multimodal Integration` + `Creative-Analytical Balance`)
Best practices:
- Explicitly reference attached or expected modalities when relevant (`[الصورة المرفقة / الفيديو / المستند / البيانات]`) and specify what to extract or cross-reference across them.
- Combine clear structural anchors (goal, audience, tone) with precise output schemas (tables, bullet hierarchies, JSON, or scripted beats) to balance synthesis and creativity.

```markdown
**الهدف والمهمة الأساسية:**
...

**المدخلات والسياق (النص / الوسائط المرفقة):**
...

**خطوات التحليل والتنفيذ:**
1. ...
2. ...

**ضوابط الجودة والأسلوب:**
- ...

**تنسيق المخرج النهائي:**
...
```

---

## 2. Task-Type Optimization Checklists

### 1. Creative Tasks (المهام الإبداعية)
- **Tone & Voice:** Specify exact register (e.g., سينمائي، ساخر ذكي، رسمي رصين، دارجة/فصحى عصرية).
- **Target Audience:** Define who reads/watches it, their pain point, and desired emotional reaction.
- **Anti-Cliché Guardrail:** Explicitly ban generic AI openings, filler adjectives, and repetitive phrasing.

### 2. Technical & Coding Tasks (المهام التقنية)
- **Exact Stack & Environment:** Language, framework versions, runtime constraints.
- **Anti-Hallucination Rule:** Forbid inventing undocumented APIs, flags, or libraries; require explicit uncertainty flagging if a detail cannot be verified.
- **Quality Gates:** Edge cases, error handling, time/space complexity or security constraints, and runnable output format.

### 3. Educational Tasks (المهام التعليمية)
- **Learner Level:** Beginner, intermediate, or specialist.
- **Progressive Scaffolding:** Concept intuition -> clear breakdown -> concrete `Few-shot` examples -> quick diagnostic check or practical exercise.

### 4. Complex / Multi-Goal Tasks (المهام المعقدة)
- **Task Decomposition:** Break monolithic goals into sequential phases (`Phase 1 -> Phase 2 -> Phase 3`).
- **Logical Chain:** Make each step's output feed directly into the next step, ending with a self-verification checklist against all constraints.
