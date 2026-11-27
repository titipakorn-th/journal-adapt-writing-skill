# journal-adapt skill

This folder contains the executable skill instructions for journal-adapt.

journal-adapt builds a **dynamic academic writing skill** from:

1. an optional static base writing skill,
2. a primary target-journal corpus,
3. optional field-top or topic-similar reference papers,
4. optional user/lab exemplars,
5. the manuscript section being revised.

The generated rules are reviewable before any manuscript revision starts.

---

## Install

For Claude Code:

```bash
mkdir -p ~/.claude/skills
ln -s "$PWD/skill" ~/.claude/skills/journal-adapt   # run from the repository root; git pull updates it
```

For Codex:

- If your Codex setup supports custom skills, install this folder as `journal-adapt`.
- If not, keep this repository open and ask Codex to follow `skill/SKILL.md` directly.

See the repository's `docs/INSTALLATION.md` for PDF conversion and `docs/STATIC_SKILL_RECOMMENDATIONS.md` for static base skill recommendations.

---

## Inputs

Quickest start: `/journal-adapt manuscript.tex corpus/ JEEM`. The skill asks only for what it cannot infer: manuscript, target journal, corpus folder, and optionally field papers, lab samples, your own writing guide, and which sections to revise.

Markdown, LaTeX, and plain-text inputs work without any converter. PDF inputs need a PDF-to-text converter. An existing `dynamic_writing_skill.md` can be loaded directly to skip corpus analysis.

---

## Included Base Rules

```text
base_rules/
├── economics.md
├── ml_cv_nlp.md
├── cs_engineering.md
└── general_academic.md
scripts/
└── check_preserved.py   # flags citations, refs, math, footnotes, numbers lost or added in a revision
```

Run `python3 scripts/check_preserved.py --selftest` to verify the checker (Python 3 stdlib only).

You may replace these with any static writing skill or skip the base layer entirely.

---

## Output

The skill writes Markdown outputs next to the manuscript:

```text
[manuscript_name]_revised/
├── dynamic_writing_skill.md
├── style_profile.md
├── [section]_original.[ext]
├── [section]_revised.[ext]
├── [section]_revision_log.md
└── revision_summary.md
```

No facts, equations, citations, variables, or numerical claims should be changed unless the user explicitly approves that change.
