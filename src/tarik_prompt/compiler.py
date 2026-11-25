"""Model-specific prompt blueprint compiler for Claude (XML), ChatGPT (Markdown), and Gemini."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field

TASK_GUARDRAILS: dict[str, list[str]] = {
    "technical": [
        "Do not invent undocumented APIs, flags, or third-party packages; flag uncertainty explicitly.",
        "Address edge cases, input validation, and failure modes explicitly.",
        "Deliver runnable, self-contained code without placeholder stubs unless requested.",
    ],
    "creative": [
        "Match the specified audience register and emotional tone consistently.",
        "Avoid generic AI openings, filler adjectives, and repetitive clichés.",
    ],
    "educational": [
        "Scaffold concepts progressively from core intuition to concrete examples.",
        "Include a concise diagnostic check or practical exercise at the end.",
    ],
    "complex": [
        "Decompose the objective into sequential phases where each phase feeds the next.",
        "Verify the final output against all stated constraints before responding.",
    ],
}


@dataclass
class PromptSpec:
    goal: str
    role: str = "Senior Domain Specialist"
    context: str = "[Insert relevant project or domain context]"
    model: str = "claude"  # claude | chatgpt | gemini
    task_type: str = "technical"  # technical | creative | educational | complex
    output_format: str = "Structured, copy-paste-ready deliverable"
    constraints: list[str] = field(default_factory=list)


def diagnose_draft(raw_idea: str) -> dict[str, object]:
    """Check whether a raw user draft should trigger DETAIL mode clarification questions."""
    words = raw_idea.strip().split()
    missing: list[str] = []
    if len(words) < 8:
        missing.append("Target outcome is underspecified (< 8 words).")
    low = raw_idea.lower()
    if not any(k in low for k in ("json", "markdown", "code", "table", "script", "list", "جدول", "كود", "قائمة", "ملف")):
        missing.append("No explicit output format detected.")
    mode = "DETAIL" if missing else "BASIC"
    return {"recommended_mode": mode, "word_count": len(words), "gaps": missing}


def compile_prompt(spec: PromptSpec) -> str:
    """Compile a PromptSpec into a model-optimized prompt architecture."""
    model = spec.model.strip().lower()
    task_type = spec.task_type.strip().lower()
    if task_type not in TASK_GUARDRAILS:
        raise ValueError(f"Unsupported task_type '{spec.task_type}'. Choose from: {', '.join(TASK_GUARDRAILS)}")

    merged_constraints = list(TASK_GUARDRAILS[task_type]) + list(spec.constraints)
    bullet_constraints = "\n".join(f"- {c}" for c in merged_constraints)

    if model == "claude":
        return (
            f"<role>\n{spec.role}\n</role>\n\n"
            f"<context>\n{spec.context}\n</context>\n\n"
            f"<instructions>\n"
            f"1. Analyze the objective and constraints carefully.\n"
            f"2. Execute the following primary goal: {spec.goal}\n"
            f"3. Validate the draft against every guardrail in <constraints> before emitting the final response.\n"
            f"</instructions>\n\n"
            f"<constraints>\n{bullet_constraints}\n</constraints>\n\n"
            f"<output_format>\n{spec.output_format}\n</output_format>"
        )

    if model == "chatgpt":
        return (
            f"# Role & Objective\n{spec.role} — {spec.goal}\n\n"
            f"# Context\n{spec.context}\n\n"
            f"# Execution Instructions\n"
            f"1. Break down the core requirements from the context.\n"
            f"2. Fulfill the objective: {spec.goal}\n"
            f"3. Double-check edge cases and formatting rules.\n\n"
            f"# Constraints & Guardrails\n{bullet_constraints}\n\n"
            f"# Output Format\n{spec.output_format}"
        )

    if model == "gemini":
        return (
            f"**Objective:** {spec.goal}\n"
            f"**Role:** {spec.role}\n\n"
            f"**Context & Inputs (Text / Attached Media):**\n{spec.context}\n\n"
            f"**Execution Steps:**\n"
            f"1. Synthesize all provided text and multimodal inputs.\n"
            f"2. Deliver {spec.goal} with high analytical precision.\n\n"
            f"**Quality Guardrails:**\n{bullet_constraints}\n\n"
            f"**Required Output Schema:**\n{spec.output_format}"
        )

    raise ValueError(f"Unsupported model '{spec.model}'. Choose from: claude, chatgpt, gemini")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tarik-prompt",
        description="Compile raw ideas into model-optimized prompts for Claude, ChatGPT, and Gemini.",
    )
    parser.add_argument("goal", help="Raw idea or primary task objective.")
    parser.add_argument("--model", choices=["claude", "chatgpt", "gemini"], default="claude")
    parser.add_argument(
        "--task",
        choices=["technical", "creative", "educational", "complex"],
        default="technical",
    )
    parser.add_argument("--role", default="Senior Specialist")
    parser.add_argument("--context", default="[Insert relevant context]")
    parser.add_argument("--format", dest="output_format", default="Clean, actionable deliverable")
    parser.add_argument("--constraint", action="append", default=[], help="Additional constraint (repeatable).")
    parser.add_argument("--diagnose", action="store_true", help="Run BASIC/DETAIL ambiguity diagnosis as JSON.")

    args = parser.parse_args(argv)
    if sys.stdout and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if args.diagnose:
        print(json.dumps(diagnose_draft(args.goal), ensure_ascii=False, indent=2))
        return 0

    spec = PromptSpec(
        goal=args.goal,
        role=args.role,
        context=args.context,
        model=args.model,
        task_type=args.task,
        output_format=args.output_format,
        constraints=args.constraint,
    )
    print(compile_prompt(spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
