@AGENTS.md

# Claude Code entry

Use `/writing-skill`, `/manuscript-reviewer`, `/citation-verifier`, or `/style-profiler` according to the shared task routing. `writing-agent` executes assigned manuscript work; `corpus-analyst` reads sources. Both inherit the selected Claude model.

The optional Manuscript Writer output style governs presentation, not permissions or task scope. Do not let an output style override the user's requested analysis, editing, or completion boundary.

Run tools with the toolkit's Python environment. Basic prose, terminology and bibliography checks use the standard library. PDF/DOCX ingestion requires PyMuPDF/python-docx; YAML configuration tools require PyYAML. Resolve paths through the shared rules rather than assuming the current directory is the toolkit.
