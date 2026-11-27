# journal-adapt-writing-skill

> **A static + dynamic academic writing skill framework. Start with reusable writing rules, then generate a corpus-grounded dynamic skill for one manuscript and one writing destination.**

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-blueviolet)
![Codex](https://img.shields.io/badge/Codex-compatible-green)
![Version](https://img.shields.io/badge/version-1.1-brightgreen)

There are already many useful **static academic writing skills**: discipline templates, anti-AI phrasing rules, citation/equation safety rules, and general academic style guides. They are valuable, but they usually apply the same rules to every manuscript.

The missing piece is **journal adaptation**. Even for the same manuscript, writing for Journal A and writing for Journal B may require different introduction logic, contribution framing, method exposition, result emphasis, and discussion scope. A strong revision workflow should learn from the actual papers that define the target writing destination.

**journal-adapt adds that dynamic layer on top of optional static skills.**

- **Static skills** are reusable base rules: discipline conventions, general academic writing constraints, anti-AI phrasing cleanup, citation/equation safety, or your own lab/advisor guide.
- **Dynamic skills** are generated for one manuscript and one writing destination from a user-provided corpus: target-journal papers, optional field-top or topic-similar papers, and optional user/lab exemplars.

The result is a visible, editable `dynamic_writing_skill.md`. It does not auto-write a paper; it gives the agent an auditable revision framework for section-by-section academic rewriting.

---

## Static + Dynamic

```mermaid
flowchart TD
    A[Optional Static Skills\nreusable base rules] --> E[Dynamic Writing Skill]
    B[Target Journal Papers\nprimary corpus] --> D[Corpus Style Profile]
    C[Field-top or Topic-similar Papers\noptional] --> D
    U[User / Lab Exemplars\noptional] --> D
    D --> E
    E --> F[Human Review]
    F --> G[Section Revision]
    G --> H[Revision Log]

    style E fill:#e8f5e9,stroke:#4caf50
    style F fill:#f5f0e8,stroke:#999
```

## Optional Static Skills

The static layer is optional. You can choose an existing open-source skill, bring your own, or skip this layer.

| Static option | Field / purpose | Source |
|---------------|-----------------|--------|
| Economics writing | Economics writing and referee-style guidance | [hanlulong/econ-writing-skill](https://github.com/hanlulong/econ-writing-skill) |
| ML / CV / NLP writing | Research paper writing for ML-style papers | [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) |
| CS / research paper writing | Research paper pipeline for CS systems, networking, and ML-adjacent papers | [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) |
| Philosophy / interdisciplinary writing | Academic paper planning and composition | [lishix520/academic-paper-skills](https://github.com/lishix520/academic-paper-skills) |
| General AI-writing cleanup | Generic AI-writing cleanup / humanizing constraints | [blader/humanizer](https://github.com/blader/humanizer) |

More details: [Static Skill Recommendations](docs/STATIC_SKILL_RECOMMENDATIONS.md).

You can also use a custom static skill:

| Custom input | Use when |
|--------------|----------|
| Your own `SKILL.md` | You already have reusable agent instructions. |
| Lab/advisor writing guide | Your group has stable style preferences. |
| Journal or field checklist | You want a lightweight rule sheet instead of a full skill. |
| No static skill | You want the dynamic corpus to drive the workflow on its own. |

## Dynamic Corpus

The dynamic corpus is the main feature. It is broader than "papers from the target journal."

| Corpus role | Required? | What it contributes |
|-------------|-----------|---------------------|
| **Primary corpus: target-journal papers** | Yes | The journal's local writing culture: structure, contribution framing, method/result exposition, discussion scope. |
| **Secondary corpus: field-top or topic-similar papers** | Optional | High-quality field writing when the target-journal corpus is small or when the topic needs extra reference points. |
| **User/lab exemplars** | Optional | Author, advisor, or lab preferences that should be preserved when they do not conflict with the target journal. |

The target journal usually has the highest priority. Optional secondary papers and user/lab exemplars enrich the dynamic skill, but they do not override reviewed target-journal patterns unless the user explicitly chooses that behavior.

## Priority System

| Priority | Source | Rule |
|----------|--------|------|
| P1 | Hard constraints | Preserve facts, citations, equations, notation, numerical results, labels, and author-defined terminology. |
| P2 | Target journal corpus | Follow reviewed target-journal patterns. |
| P3 | Secondary corpus and exemplars | Use high-quality field patterns or user/lab preferences when target-journal evidence is absent or weak. |
| P4 | Static base skill | Apply discipline or general writing rules when corpus signals do not decide. |
| P5 | Cleanup rules | Remove AI-taste phrases, hollow transitions, generic contributions, and unsupported overclaims. |

P1 always wins. P2 usually beats P3 and P4. Any conflict that changes revision behavior should be recorded in the revision log.

---

## Corpus Preparation

Recommended starting point:

| Corpus role | Recommended size |
|-------------|------------------|
| Primary corpus: target-journal papers | 5-8 papers |
| Secondary corpus: field-top or topic-similar papers | 2-5 papers |
| User/lab exemplars | 1-3 documents |

All corpus files should be fully readable Markdown/text before Phase 1. If a PDF conversion is incomplete, retry conversion, use another converter, provide clean Markdown/text, or replace the paper.

---

## Quick Start

### 1. Install

For Claude Code, link the skill so `git pull` keeps it up to date:

```bash
git clone https://github.com/titipakorn-th/journal-adapt-writing-skill.git
mkdir -p ~/.claude/skills
ln -s "$PWD/journal-adapt-writing-skill/skill" ~/.claude/skills/journal-adapt
```

For Codex or other agents, keep this repository open and ask the agent to follow `skill/SKILL.md`. More detail: [Installation and PDF Conversion](docs/INSTALLATION.md).

### 2. Put your files in one place

```text
my_project/
├── corpus/            # 5-8 papers from the target journal (.pdf, .md, or .txt)
└── manuscript.tex     # or .md / .docx / .pdf
```

Use your manuscript's source (`.tex`, `.md`, `.docx`) rather than its PDF when you have it. Corpus PDFs are fine. No corpus yet? Run the skill anyway; it tells you what to collect and can start with generic rules.

### 3. Run it

```text
/journal-adapt manuscript.tex corpus/ JEEM
```

Or in plain words:

```text
Revise the introduction of manuscript.tex for JEEM using the papers in corpus/.
```

The skill asks only for what it cannot find. It shows a short summary of the writing rules it built, waits for your "go", then revises one section at a time.

Other things you can ask for:

| You want | Say |
|----------|-----|
| Only the journal writing rules | "Build the writing skill for JEEM from corpus/, don't revise yet." |
| A diagnosis without rewriting | "Diagnose my introduction against JEEM style." |
| Reuse rules from an earlier run | "Use this dynamic_writing_skill.md to revise my abstract." |
| Your lab's style on top | "Also use lab_samples/ as exemplars." |
| Thesis or dissertation | "Revise chapter 2 of thesis.tex for a PhD in Economics at my university, using the theses in past_theses/." |

**Theses.** Thesis mode turns on automatically for a thesis or dissertation. The corpus becomes 3-6 recently accepted theses from your program, the unit of revision becomes the chapter, and chapter openings, closings, research questions, and future work are handled as a thesis needs them. For a thesis by publication, the paper chapters are revised against their own target journals.

---

## Output

Saved next to the manuscript:

```text
[manuscript_name]_revised/
├── dynamic_writing_skill.md
├── style_profile.md
├── abstract_revised.tex      # same format as your manuscript
├── introduction_revised.tex
├── ...
├── [section]_revision_log.md
└── revision_summary.md
```

The revised files keep your manuscript's format (LaTeX stays LaTeX). Each section is checked by `skill/scripts/check_preserved.py`, which flags any citation, reference, math span, footnote, or number that was lost or added.

---

## Example

`examples/jeem/` shows an anonymized MVP run for the Journal of Environmental Economics and Management:

- corpus-role metadata
- conversion gate report
- aggregated style profile
- generated dynamic writing skill
- sanitized section diagnosis, revision sample, and revision log

Raw PDFs, converted full text, and the private manuscript are not included.

---

## Documentation

- [Installation and PDF Conversion](docs/INSTALLATION.md)
- [Static Skill Recommendations](docs/STATIC_SKILL_RECOMMENDATIONS.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Module Specifications](docs/MODULES.md)
- [Templates](docs/templates/)

---

## Known Limitations

- English-language academic writing only.
- PDF conversion quality depends on the converter. MinerU can fail on some local setups.
- The project extracts writing structure and rhetorical patterns only. It must not quote or paraphrase copyrighted corpus papers.
- The generated dynamic skill needs human review before revision begins.
- The tool does not add facts, citations, results, or claims that are not already in the manuscript.

---

## Contributing

Useful contributions include:

- new static base writing skills for disciplines not covered here
- better installation paths for Claude Code, Codex, and other agent environments
- safer PDF-to-Markdown conversion recipes
- more anonymized example corpora
- improvements to style-card and revision-log templates

One base skill per file is preferred. Keep example corpora free of copyrighted full text and unpublished manuscript details.

---

## License

MIT
