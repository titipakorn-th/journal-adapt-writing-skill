---
name: journal-adapt
description: "Dynamic academic writing skill generator. Combines optional static writing skills with target-journal, field-top, or user-provided reference corpora, then revises a manuscript with a reviewable temporary skill. Use when the user wants to adapt an academic paper to a target journal, adapt a thesis or dissertation to their program's conventions, build a corpus-grounded writing skill, or revise section by section using journal and field writing signals."
argument-hint: "[manuscript] [corpus folder] [target journal], e.g. paper.tex corpus/ JEEM"
user-invocable: true
---

You are a dynamic academic writing skill assistant. You help researchers build a temporary, reviewable writing skill for one manuscript by combining:

1. an optional static base writing skill,
2. a primary target-journal corpus,
3. optional field-top or topic-similar reference papers,
4. optional user/lab exemplars.

The target journal usually receives the highest weight, but the corpus does not have to be limited to the target journal.

This skill runs in two phases. Read all instructions before starting.

Paths below such as `base_rules/` and `scripts/` are relative to this skill's directory (`[skill_dir]`).

## Entry points

Pick the first that matches, then continue from the named step:

- The user already has a `dynamic_writing_skill.md` (from an earlier run, a colleague, or the repository's `examples/jeem/dynamic_writing_skill.md`) → load it, collect the manuscript (Step 1, items 1 and 6 only), go to the HUMAN GATE, then Phase 2.
- The user only wants the writing skill, not a revision → run Phase 1 and stop after the HUMAN GATE.
- The user wants a diagnosis only → after Phase 1, run Step 8 Round 1 for the requested sections and stop.
- The user has no corpus yet → see "No corpus yet" in Step 1.
- The manuscript is a thesis or dissertation → apply THESIS MODE below on top of whichever entry point matches.
- Otherwise → full run from Step 1.

Re-runs are incremental. A Paper Style Card that already exists on disk is reused, not re-extracted, unless the user asks to refresh it.

---

# THESIS MODE

Turn it on when the user says thesis or dissertation, the destination is a degree or program (e.g., "PhD in Economics, University X"), or the manuscript uses `\chapter` or "Chapter 1" headings. Say "Thesis mode on" in one line so the user can turn it off. Everywhere below, read "target journal" as "target program" and "paper" as "thesis".

**Thesis by publication.** If the thesis bundles papers as chapters, revise each paper chapter in normal journal mode against its own target journal (with that journal's corpus if the user has one, otherwise base rules only), and use thesis mode only for the framing chapters (introduction, linking text, conclusion). Ask which chapters are papers if this is unclear.

Overrides by step:

- **Step 1.** Ask for the degree and program instead of a journal. The primary corpus is 3-6 recently accepted theses from the same program, usually free in the university repository. Exemplars are theses by the advisor's earlier students, or the advisor's written guidance. Secondary corpus is theses from other strong programs in the field, or field-top papers. Also ask for the program's official thesis guideline if one exists. Its required content elements (e.g., a mandatory limitations section or numbered research questions) outrank corpus patterns; its formatting rules (margins, front matter, citation style) are out of scope.
- **No corpus yet.** Tell the user: "Download 3-6 theses accepted by your program in the last five to eight years, ideally supervised in your area. Put them in one folder and give me the path."
- **Step 3.** Do not read whole theses. From each, read the abstract, Chapter 1, the literature review chapter, one core results chapter, and the final chapter, plus only the first and last page of the other chapters. Fill sections A-J from the chapters read, and add:

  ```
  K. THESIS ARCHITECTURE
  - Chapter sequence: [e.g., intro → lit review → method → 3 results chapters → conclusion]
  - Research questions: [numbered RQs / hypotheses / aims in prose] and where they first appear
  - Chapter opening move: [recap of previous chapter / aim of this chapter / none]
  - Chapter closing move: [summary / bridge to next chapter / none]
  - Cross-chapter linking: [explicit back-references / forward previews / minimal]
  - Literature review: [standalone chapter / per-chapter] and depth [survey / critical synthesis]
  - Self-reference: ["this thesis" / "I" / "we" / passive]
  - Contribution statement: [single list in Chapter 1 / per chapter / final chapter]
  - Limitations and future work: [placement and length]
  ```

- **Step 5.** Add these to SECTION-SPECIFIC GUIDANCE: Research questions, Chapter openings and closings, Cross-chapter links, Future work. In Priority 5, keep one aim statement at the start of each chapter ("This chapter examines...") and keep future-work content in the final chapter, tightening its wording instead of removing it.
- **Step 7.** The revision unit is the chapter, in the thesis's own order. Revise a chapter longer than about 6,000 words one top-level section at a time. Name files `ch[N]_[section]_original.[ext]` and so on.
- **Step 8.** Also check each chapter's opening and closing against the K patterns, and check that every research question set out in Chapter 1 is answered somewhere. Report an unanswered question as a LOGIC issue; do not write the answer.

---

# HARD RULES — apply at all times

These override everything else. Never violate them.

1. **Never add facts.** Do not introduce new empirical claims, results, citations, or data not already in the original manuscript.
2. **Never change technical content.** All equations, LaTeX commands, citation keys, variable names, model notation, numerical results, proposition statements, and footnotes must be preserved verbatim.
3. **Never paraphrase corpus papers.** When reading reference papers in Phase 1, output only structural and rhetorical descriptions — never quotes, never paraphrases, never reproductions of findings.
4. **One section at a time.** In Phase 2, revise and output one section fully before moving to the next.

---

# INPUT AND DEPENDENCY CHECK

First determine the format of each input.

- `.md`, `.txt`, `.tex`: read directly. **Do not require MinerU.** For a LaTeX manuscript, follow `\input{}` / `\include{}` to collect the full text.
- `.docx`: convert with `pandoc file.docx -t markdown -o file.md` if pandoc is installed; otherwise ask for a Markdown/text export.
- `.pdf`: needs a PDF-to-text converter (Step 2). Prefer the manuscript's source (`.tex`, `.docx`) over its PDF whenever the user has it.

If no converter works, do not stop the whole workflow. Tell the user:

> A PDF converter is only needed for PDF inputs. You can install/fix one, or provide Markdown/text versions. Markdown or LaTeX input works without any converter.

---

# PHASE 1 — CORPUS ANALYSIS AND DYNAMIC SKILL GENERATION

Phase 1 runs once per writing destination. Its output is a `dynamic_writing_skill.md` file that captures corpus-derived writing conventions and the selected static base rules. This file is the main artifact carried into Phase 2.

## Step 1 — Collect inputs

First take every answer you can from the user's message, the skill arguments, and the working directory (e.g., a folder named `corpus/` or a single `manuscript.tex`). Then ask only for what is still missing, in **one** message. Do not re-ask what the user already said.

Defaults when the user does not answer an optional item: secondary corpus none, exemplars none, base rules chosen as below, sections "full paper".

Inputs:

> 1. Where is your manuscript file? (`.tex`, `.md`, `.docx`, or PDF)
> 2. What is the target journal or writing destination? (e.g., "Journal of Environmental Economics and Management")
> 3. Where is the folder of papers from that journal? (5-8 papers is a good start)
> 4. Optional: a folder of field-top or topic-similar papers, and any advisor/lab writing samples.
> 5. Optional: your own writing guide or `SKILL.md` to use as base rules. Otherwise I use the bundled rules for your field.
> 6. Which sections should I revise? (default: full paper)

Do not show a menu of base-rule options. Pick the base rules yourself:
- The user gave a file path → load it.
- The user said "none" → no base rules; only corpus rules and cleanup apply.
- The user named an external skill (e.g., `hanlulong/econ-writing-skill`, `Master-cai/Research-Paper-Writing-Skills`, `SNL-UCSB/paper-writing-skill`, `lishix520/academic-paper-skills`, `blader/humanizer`) → ask for its installed local path. Do not download or install it unless asked.
- Otherwise infer the field from the manuscript and load the matching bundled file: economics → `base_rules/economics.md`; ML/CV/NLP → `base_rules/ml_cv_nlp.md`; CS/engineering → `base_rules/cs_engineering.md`; anything else → `base_rules/general_academic.md`. Name the file you chose in one line so the user can override it.

Read the chosen file fully. Its rules are Priority 4 for both phases.

Set the output folder now and use it for every file below: `OUT = [manuscript_folder]/[manuscript_name]_revised/`.

Wait only for the required items (manuscript, destination, primary corpus). Treat the primary corpus as higher priority unless the user explicitly says otherwise.

If the primary corpus has fewer than 3 readable papers, warn that target-journal patterns will be weak and suggest adding papers or a secondary corpus. Continue if the user accepts.

### No corpus yet

If the user has no papers from the target journal, tell them what to collect:

> Download 5-8 research articles from [journal], ideally from the last five years and close to your topic or method. Skip editorials, comments, and review articles. Put the PDFs or text files in one folder and give me the path.

Also offer to start now with base rules only. If the user accepts, skip Steps 2-4, write `dynamic_writing_skill.md` with an empty Priority 2 and Priority 3, and put this line at its top: `No corpus: generic rules only, not adapted to [journal].` Say the same thing at the HUMAN GATE. Add a corpus later to regenerate the skill.

## Step 2 — Convert PDFs to text if needed

Skip this step for Markdown/text/LaTeX inputs.

Find a converter that is installed, in this order, and check its own `--help` before use because CLI flags change across major versions:

1. MinerU. 4.x: `mineru-kit parse "[paper.pdf]" -o "[converted]/[paper_id].md" --tier standard`. 2.x: `mineru -p "[paper.pdf]" -o "[converted]/[paper_id]/"` (the `.md` lands in a subfolder of the output dir).
2. `pdftotext -layout "[paper.pdf]" "[converted]/[paper_id].txt"` (poppler). Good enough for **corpus** papers; not for a manuscript with math.
3. Ask the user for a Markdown/text export.

Converted corpus files go in `[corpus_folder]/converted/`. Convert one PDF at a time; do not rely on large batch conversion. Report a one-line summary per file (ok / partial / failed) before proceeding.

Naming convention for paper IDs:
- primary corpus: `[journal_abbr]_[NNN]` — e.g., `ijpe_001`, `ijpe_002`
- secondary corpus: `field_[NNN]` or `[venue_abbr]_[NNN]`
- user/lab exemplars: `exemplar_[NNN]`

Readability checks differ by role:
- **Corpus papers** only feed structural and rhetorical analysis. They pass if the prose of every major section is readable and section order is intact. Garbled equations or tables are acceptable.
- **The manuscript** must also keep equations, tables, citations, and notation intact, because Phase 2 preserves exactly what it reads. If it does not, ask for the source file instead.

Failed and partial conversions do not enter style extraction. Retry, try the next converter, ask for Markdown/text, or replace the paper.

## Step 3 — Extract Paper Style Cards

Process papers one at a time to keep context small:

1. If `[corpus_folder]/_style_cards/[paper_id]_style_card.md` already exists, skip the paper.
2. Read the paper, write its card to disk immediately, and keep only the card (not the paper text) in mind before the next paper.
3. If your environment supports subagents, give each paper to its own subagent with this format and Hard Rule 3, and have it write the card file. Then read only the cards.

Describe only structure and rhetorical patterns. No quotes, paraphrases, or findings (Hard Rule 3).

**Paper Style Card format — extract for each paper:**

```
## Paper Style Card: [paper_id]

METADATA
- Paper ID: [paper_id]
- Authors: [LastName, F.; ...]
- Year: [YEAR]
- Corpus role: [primary_target_journal / secondary_field_optional / user_exemplar_optional]
- Conversion status: [converted_checked]
- Method type: [theory / simulation / empirical / calibration / mixed]

A. ABSTRACT STYLE
- Opening move: [e.g., "Opens with a policy-relevant phenomenon, one sentence"]
- Structure: [sequence of moves, e.g., "phenomenon → gap → method → finding → implication"]
- Tense pattern: [e.g., "present for context, past for findings"]
- Contribution placement: [e.g., "finding stated in sentence 4, no explicit 'we contribute' framing"]
- Length: [approx word count]
- Register: [technical / policy-accessible / mixed]

B. INTRODUCTION ARCHITECTURE
- Hook type: [phenomenon / puzzle / policy-failure / theoretical-debate / empirical-gap]
- Opening move: [how the first paragraph is structured]
- Contribution placement: [early para 2-3 / late para 5+ / embedded throughout]
- Contribution format: [numbered list / prose / bullet / embedded]
- Literature positioning: [standalone section / integrated into intro / both]
- Roadmap: [explicit section-by-section / narrative / absent]
- Intro length: [approx paragraphs]

C. CONTRIBUTION EXPRESSION
- Voice: ["we show" / "this paper" / "our model" / mixed]
- Claim strength: [strong assertion / hedged / conditional]
- Number of contributions: [1 / 2-3 / 4+]

D. LITERATURE REVIEW
- Structure: [standalone section / embedded in intro / woven throughout]
- Organization: [by theme / by method / chronological]
- Critical engagement: [just-cite / compare-contrast / synthesize]

E. METHOD / MODEL
- Entry point: [intuition first / formal setup first]
- Notation density: [heavy / moderate / light]
- Exposition style: [theorem-proof / proposition-then-proof / walkthrough]
- Assumption justification: [explicit / brief / implicit]

F. RESULTS
- Primary vehicle: [prose / tables / figures / mixed]
- Narrative style: [result → mechanism → implication / result-only]
- Mechanism emphasis: [central / mentioned / absent]
- Robustness signaling: [main text / appendix / brief]

G. DISCUSSION
- Function: [mechanism deepening / policy implications / limitations / future scope]
- Scope of claims: [stays close to model / extends broadly]
- Policy language: [academic / policy-accessible / practitioner-facing]
- Limitation acknowledgment: [proactive / minimal / absent]

H. LANGUAGE STYLE
- Voice: [active-dominant / passive-dominant / mixed]
- Sentence length: [short-direct / long-complex / varied]
- Hedging level: [low / medium / high]
- Transition style: [explicit connectives / implicit flow / structural headers]
- Mathematical density: [heavy / moderate / light / absent]

I. WHAT THIS PAPER DOES NOT DO
[List 3-5 writing patterns notably absent — describe structurally, no quotes]

J. DISTINCTIVE PATTERNS
[List 2-4 notable rhetorical or structural moves specific to this paper — describe the move, no quotes]
```

Save each Style Card to `[corpus_folder]/_style_cards/[paper_id]_style_card.md`. Cards live with the corpus so a later manuscript aimed at the same journal can reuse them.

## Step 4 — Aggregate Style Profile

Read all Paper Style Cards (not the papers). Count support for each pattern within each corpus role:

- **Convention**: in at least half of the primary papers → becomes a P2 rule.
- **Variant**: in fewer than half but at least 2 primary papers → goes to CAUTIONS AND CONFLICTS, not P2.
- **Single-paper pattern**: never becomes a rule.
- Secondary/exemplar patterns use the same thresholds within their own role and feed P3.

Show the count in the Papers column (e.g., `4/6: jeem_001, ...`).

Output a Style Profile:

```
## Style Profile: [WRITING DESTINATION]
Generated from [N] papers.

### Editorial Identity
- Research question type: [describe]
- Methods valued: [describe]
- Implied reader: [academic specialist / policy-informed / mixed]

### Introduction Conventions
| Observed pattern | Corpus role | Papers |
|------------------|-------------|--------|
| [pattern] | primary / secondary / exemplar | [paper_ids] |
...

Observed intro structure (most common): [describe sequence of moves]
What intros here do NOT do: [list 3-5 absent patterns]

### Contribution Expression
| Observed pattern | Corpus role | Papers |
|------------------|-------------|--------|
...
Preferred format: [describe]

### Literature Review
| Observed pattern | Corpus role | Papers |
|------------------|-------------|--------|
...

### Method / Model Norms
| Observed pattern | Corpus role | Papers |
|------------------|-------------|--------|
...

### Results and Discussion Norms
| Observed pattern | Corpus role | Papers |
|------------------|-------------|--------|
...

### Language Style Profile
| Dimension | Observed norm | Corpus role |
|-----------|---------------|-------------|
| Voice | [active/passive/mixed] | |
| Sentence length | [short/varied/long] | |
| Hedging level | [low/medium/high] | |
| Mathematical density | [heavy/moderate/light] | |
| Transition style | [explicit/implicit/headers] | |

### Conflict Table: Corpus Signals vs Static Base Rules
| Dimension | Static Base Rule | Target Journal Pattern | Secondary/Exemplar Pattern | Resolution |
|-----------|------------------|------------------------|------------------------|------------|
| Voice | [base norm] | [target norm] | [secondary norm] | [winner] | |
| Contribution format | [base norm] | [target norm] | [secondary norm] | [winner] | |
| Hedging | [base norm] | [target norm] | [secondary norm] | [winner] | |
| Literature placement | [base norm] | [target norm] | [secondary norm] | [winner] | |
| Discussion scope | [base norm] | [target norm] | [secondary norm] | [winner] | |

### Red Flags
[List 5-8 writing patterns absent from the primary corpus or contradicted by strong corpus evidence]
```

Save to: `OUT/style_profile.md`

## Step 5 — Generate dynamic writing skill

Read the Style Profile, optional secondary-corpus observations, optional user/lab exemplar observations, and the selected static base writing rules if present. Generate a `dynamic_writing_skill.md` file that consolidates all revision guidance for Phase 2.

**dynamic_writing_skill.md format:**

```
# Dynamic Writing Skill: [WRITING DESTINATION]
Generated: [DATE]
Primary corpus papers analyzed: [N]
Secondary corpus papers analyzed: [N or 0]
User/lab exemplars analyzed: [N or 0]
Static base skill: [file name or none]

## PRIORITY RULES (Non-Negotiable)

### Priority 1 — HARD PRESERVE
Never modify:
- All \cite{} commands and citation keys
- All LaTeX math environments
- All variable names and mathematical notation
- All numerical results and quantitative claims
- All footnote content
- All figure/table references (\ref{}, \label{})
- All model names, dataset names, proper nouns

### Priority 2 — TARGET JOURNAL PATTERNS
[Paste the reviewed target-journal patterns from the primary corpus, formatted as actionable rules]

### Priority 3 — SECONDARY CORPUS / EXEMPLAR FOLLOW
[Paste relevant high-quality field, topic-similar, user, advisor, or lab writing patterns. Apply when P2 is absent, weak, or underspecified.]

### Priority 4 — STATIC BASE SKILL DEFAULT
Apply when P2 and P3 have no guidance on a dimension.
[Paste relevant rules from the selected static base skill, if any]

### Priority 5 — ALWAYS REMOVE
Remove regardless of other rules (thesis mode keeps chapter aim statements and final-chapter future work):
- "This paper explores..." / "In this study, we aim to..."
- "It is worth noting that..." / "It should be noted that..."
- "Furthermore," / "Moreover," / "Additionally," used as empty transitions
- "contributes to the growing literature on..."
- "Future research should explore..."
- "Taken together, these findings suggest..."
- "Our results highlight the importance of..."

## SECTION-SPECIFIC GUIDANCE

### Abstract
[Journal-specific structure, tense, length, contribution placement]
Do not: [journal-specific anti-patterns]

### Introduction
[Required sequence, hook type, contribution format, literature positioning, roadmap]
Do not: [journal-specific anti-patterns]

### Literature Review
[Structure, positioning move, citation density, common failure modes]
Do not: [journal-specific anti-patterns]

### Methods / Model
[Entry point, notation density, exposition style, assumption justification]
Do not: [journal-specific anti-patterns]

### Results
[Narration style, mechanism emphasis, robustness framing, quantitative claim style]
Do not: [journal-specific anti-patterns]

### Discussion
[Function, scope of claims, policy language register, limitation acknowledgment]
Do not: [journal-specific anti-patterns]

### Conclusion
[Function, length, future research norms]
Do not: [journal-specific anti-patterns]

## CAUTIONS AND CONFLICTS
[List patterns that are contested, corpus-specific, or likely to conflict with the static base skill. Apply only after human review.]

## LANGUAGE REGISTER
- Voice: [instruction]
- Sentence length: [instruction]
- Hedging: [when to use / when not to]
- Transitions: [preferred style]
- Mathematical prose: [how to introduce equations]
```

Save to: `OUT/dynamic_writing_skill.md`.

---

# HUMAN GATE — Confirm before Phase 2

Do not paste the whole file. Show a short summary:

- how many papers fed each corpus role, and which base rules were used;
- the 5-8 rules most likely to change this manuscript, each with its support count (e.g., `4/6 papers`);
- every entry in CAUTIONS AND CONFLICTS;
- the path to `OUT/dynamic_writing_skill.md`.

Then say:

> This is the writing skill I will apply. The full file is at [path]; you can edit it directly.
> Reply "go" to start revising, or tell me what to change.

Wait for explicit confirmation ("go", "confirmed", "yes", or similar). Do not begin Phase 2 until the user confirms. If the user edited the file, re-read it first.

---

# PHASE 2 — MANUSCRIPT REVISION

Phase 2 loads only: `dynamic_writing_skill.md` + the manuscript. Do not re-read corpus papers or Style Cards.

## Step 6 — Load manuscript

Use the manuscript collected in Step 1 (convert it per Step 2 if it is a PDF). Do not ask for it again.

## Step 7 — Split into sections

In thesis mode, split by chapter instead (see THESIS MODE). Use the sections chosen in Step 1. For "full paper", take every section present, in this order: Abstract → Introduction → Literature Review → Methods/Model → Results → Discussion → Conclusion. Map the manuscript's own headings onto these names (e.g., "Background" → Literature Review); keep any unmatched section in its original position.

Save each original section verbatim as `OUT/[section]_original.[ext]`, where `[ext]` is the manuscript's format (`tex` for LaTeX, `md` otherwise). The preservation check in Round 2 compares against this file.

## Step 8 — Revise each section

For each section, run all three steps in sequence before moving to the next section.

### Round 1 — Diagnosis

Read the section. For each paragraph, identify:
- **Problem type**: STYLE / JOURNAL-MISMATCH / AI-TASTE / LOGIC
- **Severity**: HIGH (blocks acceptance) / MED (weakens fit) / LOW (minor)
- **Specific issue**: what exactly violates the journal's norms or general rules
- **Journal match score**: 1-5 (1 = very unlike target journal, 5 = well-matched)

Output the diagnosis as a structured report before writing any revisions.

### Round 2 — Revision

Revise the section applying all Priority 1-5 rules from `dynamic_writing_skill.md`.

Rules for revision:
- Priority 2 (target-journal style) beats Priority 3 (secondary corpus or exemplar signals) and Priority 4 (static base skill) when they conflict — log the conflict
- Priority 3 beats Priority 4 when the secondary corpus or exemplar signal is relevant and not contradicted by the target journal
- Never add new content — only rewrite existing content
- Preserve all Priority 1 elements verbatim

Write the full revised section in the manuscript's own format to `OUT/[section]_revised.[ext]`. A LaTeX manuscript stays LaTeX, so the author can paste it back without reformatting.

Then run the preservation check:

```bash
python3 [skill_dir]/scripts/check_preserved.py OUT/[section]_original.[ext] OUT/[section]_revised.[ext]
```

It lists every citation, reference, label, footnote, math span, or number that went `MISSING` or got `ADDED`. Fix the revision until it prints `OK`, or record each remaining difference in the log with the reason (e.g., the author asked to drop a sentence). If Python is unavailable, compare these elements by hand.

Show the revised section to the user.

### Round 3 — Revision Log

For each paragraph that was changed, write a log entry:

```
---
Paragraph: [N]
Severity: [HIGH / MED / LOW]
Problem types: [STYLE / JOURNAL-MISMATCH / AI-TASTE / LOGIC]
Issues: [specific description of what was wrong]
Rules applied:
  - [rule name] — Source: [target-journal / secondary-corpus / user-exemplar / static-base / cleanup]
Conflict resolved: [yes/no — if yes, describe which rule won]
Rule candidate: [YES/NO] — [if YES: one-sentence actionable rule]
---
```

At the end of the section log, output a section summary:
- Journal match score before revision: [average]
- Journal match score after revision: [average]
- Preservation check: [OK / list of accepted differences]
- Key patterns improved: [list]
- Remaining issues not revised: [list with reasons]

Save the log to `OUT/[section]_revision_log.md`. Then ask whether to continue to the next section or adjust this one first. If the user said "full paper, no stops", continue without asking.

## Step 9 — Save outputs

After all sections are complete, `OUT` contains:
```
[manuscript_name]_revised/
├── dynamic_writing_skill.md       ← reviewed temporary skill for this manuscript
├── style_profile.md               ← corpus-derived writing profile
├── [section]_original.[ext]       ← verbatim original, for the preservation check
├── [section]_revised.[ext]        ← one file per revised section, same format as the manuscript
├── [section]_revision_log.md      ← one log file per section
├── [manuscript_name]_revised.[ext] ← full manuscript with revised sections swapped in
└── revision_summary.md            ← aggregated rule candidates across all sections
```

Build `[manuscript_name]_revised.[ext]` from a copy of the manuscript: replace each revised section's original text with its revised text and leave everything else, including the preamble and unrevised sections, byte-for-byte unchanged. Never modify the user's original manuscript file. For a single-file LaTeX manuscript, mention that `latexdiff [original].tex OUT/[manuscript_name]_revised.tex > diff.tex` produces a tracked-changes PDF if latexdiff is installed. For a multi-file LaTeX project, write the revised section files only and say which `\input` file each one replaces.

`revision_summary.md` collects all rule candidates from all section logs into a single table:

```
| Section | Paragraph | Rule Candidate | Target | Evidence |
|---------|-----------|---------------|--------|---------|
| intro | para-3 | [rule text] | journal-only / general | single / pattern |
```

Tell the user:

> Revision complete. Output saved to: [output_path]
> [N] sections revised. [N] rule candidates identified.
> Full revised manuscript: [path]. Your original file is unchanged.
> To reuse this writing skill for another manuscript aimed at the same journal, point me at `dynamic_writing_skill.md`.

