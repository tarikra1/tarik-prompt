import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from tarik_prompt import PromptSpec, compile_prompt, diagnose_draft


class TestTarikPromptCompiler(unittest.TestCase):
    def test_claude_uses_semantic_xml_tags(self) -> None:
        spec = PromptSpec(
            goal="Design an idempotent webhook processor in Python",
            model="claude",
            task_type="technical",
            constraints=["Use PostgreSQL advisory locks or unique event IDs."],
        )
        out = compile_prompt(spec)
        self.assertIn("<role>", out)
        self.assertIn("<instructions>", out)
        self.assertIn("<constraints>", out)
        self.assertIn("PostgreSQL advisory locks", out)

    def test_chatgpt_uses_markdown_context_layering(self) -> None:
        spec = PromptSpec(goal="Write a product launch email", model="chatgpt", task_type="creative")
        out = compile_prompt(spec)
        self.assertIn("# Role & Objective", out)
        self.assertIn("# Constraints & Guardrails", out)

    def test_gemini_includes_multimodal_anchors(self) -> None:
        spec = PromptSpec(goal="Audit UI screenshot contrast", model="gemini", task_type="complex")
        out = compile_prompt(spec)
        self.assertIn("Context & Inputs (Text / Attached Media):", out)

    def test_diagnose_draft_modes(self) -> None:
        short = diagnose_draft("make an app")
        self.assertEqual(short["recommended_mode"], "DETAIL")
        detailed = diagnose_draft("Build a Python CLI tool that validates JSON config files and outputs a Markdown table")
        self.assertEqual(detailed["recommended_mode"], "BASIC")


if __name__ == "__main__":
    unittest.main()
