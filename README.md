# Field-Aware Paper Reader

**Read a research paper the way experts in its field read it — with the evidence checks that field cares about, grounded in the actual equations and figures.**
An agent skill compatible with **Claude** (Claude.ai, desktop, Claude Code) and **OpenAI Codex** (CLI, IDE extension, ChatGPT desktop app).

> **中文简介：** 一个帮你精读单篇论文的 Skill：先回答每篇论文都该回答的核心问题，再按论文所属领域的阅读习惯（统计看公式与假设、生命科学逐图逐 panel、ML 看 baseline 与消融……）深入解读，并有限度地查找后续工作。详见下方 [中文摘要](#中文摘要)。

---

## Why this skill

Different research communities read the same kind of document differently. A statistician goes to the assumptions and theorems, a biologist to the figures, an ML reviewer to the baselines and ablations, an economist to the identification strategy, a clinician to the risk of bias. Generic paper summaries miss exactly these field-specific checks.

| Generic AI summary | This skill |
|---|---|
| Paraphrases the abstract | Answers fixed core questions with evidence from the text |
| Same template for every field | Applies one or two field lenses (11 included) |
| Describes figures from captions | Views the rendered figure and equation pages before describing them |
| "Limitations: small sample size" | Labels each limitation **[authors]**, **[later work]** or **[inferred]**, with the mechanism |
| Claims "no follow-up work" after one search | Bounded search across citation indexes and the web, with channel failures reported as failures |

## How it works

```
1. Establish sources and scope   → paper version, depth (quick / standard / deep), 1–2 field lenses
2. Extract and view              → full text + page map; render and inspect key figure and equation pages
3. Read and explain              → core questions + the field lens (equations, every main-figure panel, design)
4. Calibrate the critique        → demonstrated error vs plausible concern vs unreported detail
5. Bounded forward look          → 0–5 verified successors from Semantic Scholar / OpenAlex / web search
6. Deliver                       → summary, explanation, follow-ups, labelled limitations, per-claim verdict, coverage note
```

**Core questions answered for every paper:** the research question; what the authors do; inputs and outputs; what changes relative to prior work; what evidence supports each major claim; what later work builds on it; the limitations of the paper and of its successors.

## Key features

- **11 field lenses.** Statistics, machine learning, life sciences, clinical/epidemiology, economics, neuroimaging/imaging, mathematics/theory, physics, chemistry/materials, qualitative research, computer systems. Interdisciplinary papers get a method lens and an application lens.
- **Source-grounded equations and figures.** Key equations are written out with every symbol defined; exact equations are kept separate from interpretation. Main figures are covered panel by panel, from images the agent has actually viewed.
- **Calibrated critique.** Distinguishes a demonstrated error, a plausible concern and an unreported detail. Checks the experimental unit, selection reuse, null construction, sample-size matching and multiple comparisons before judging a statistical claim.
- **Bounded, honest forward look.** Checks both journal and preprint versions, verifies each successor's relationship from primary text, and never pads the list.
- **Coverage statement.** Every reading says what was read, what was visually inspected and what was unavailable.
- **Optional helpers, standard library only for search.** `extract_paper.py` (full text, navigation aids, page rendering) and `s2_chain.py` (citation search with JSON reports and fallback URLs). The skill still works with the host's native PDF and web tools.

## Reading depths

| Depth | Best for | How to trigger |
|---|---|---|
| Quick | Deciding whether to read a paper | "Give me a quick read of …" |
| Standard (default) | Understanding a paper properly | "Explain this paper" |
| Deep | Journal club, reviewing, replicating | "Do a deep reading of …" |

## Installation

The repository contains two editions of the same skill. They differ only in a short host-specific "Runtime" section; Codex also gets UI metadata in `agents/openai.yaml`. Both use the skill name `field-aware-paper-reader`, so install only the matching edition in each host.

### Claude.ai / Claude desktop app
1. Download `field-aware-paper-reader-claude.zip` from the [Releases page](https://github.com/Louis-Chenyang-Lu/field-aware-paper-reader/releases), or build it yourself:
   ```bash
   git clone https://github.com/Louis-Chenyang-Lu/field-aware-paper-reader.git
   cd field-aware-paper-reader/skills/claude
   zip -r field-aware-paper-reader-claude.zip field-aware-paper-reader
   ```
2. In Claude, go to **Customize → Skills → + → Create skill → Upload a skill** and choose the zip. Code execution must be enabled. See the official guide: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
3. Enable web search so the forward look can run.

### Claude Code
```bash
git clone https://github.com/Louis-Chenyang-Lu/field-aware-paper-reader.git
mkdir -p ~/.claude/skills
cp -r field-aware-paper-reader/skills/claude/field-aware-paper-reader ~/.claude/skills/
```

### OpenAI Codex (CLI / IDE extension / ChatGPT desktop app)
```bash
git clone https://github.com/Louis-Chenyang-Lu/field-aware-paper-reader.git
mkdir -p ~/.agents/skills
cp -r field-aware-paper-reader/skills/codex/field-aware-paper-reader ~/.agents/skills/
```
For a single project, copy it to that repository's `.agents/skills/` instead. Codex detects new skills automatically; restart it if the skill does not appear. Trigger it in natural language or with `$field-aware-paper-reader`. See [Codex skills documentation](https://developers.openai.com/codex/skills) in the Codex documentation.

### Optional helper requirements
Python 3 with one of: **PyMuPDF** (text and rendering), **Poppler** `pdftotext`/`pdftoppm` (text and rendering), or **pypdf** (text only). The citation helper uses only the standard library; optional `S2_API_KEY` / `OPENALEX_API_KEY` environment variables raise rate limits.

## Quick start

```
Use field-aware-paper-reader to explain <paper title, DOI, or the attached PDF> at standard depth.
I am reading it to <purpose, e.g. decide whether to use the method>.
```
More: [Usage guide](docs/usage-guide.md) · [Prompt templates](examples/prompts.md) · [Design notes](docs/design.md)

## Repository structure

```
field-aware-paper-reader/
├── README.md
├── LICENSE
├── docs/
│   ├── usage-guide.md               # when to use, prompting, reading the output, FAQ
│   └── design.md                    # design rationale and sources behind the lenses
├── examples/
│   └── prompts.md                   # copy-paste prompt templates
└── skills/
    ├── claude/field-aware-paper-reader/   # Claude edition
    │   ├── SKILL.md
    │   ├── references/lenses/       # 11 field lenses
    │   └── scripts/                 # extract_paper.py, s2_chain.py
    └── codex/field-aware-paper-reader/    # Codex edition
        ├── SKILL.md
        ├── agents/openai.yaml       # Codex UI metadata
        ├── references/lenses/
        └── scripts/
```

## Limitations

- **One paper at a time.** The forward look is deliberately bounded (zero to five verified successors). For how an idea evolved across many papers, use a dedicated literature-review workflow.
- **Depends on what the agent can access.** Paywalled full text, separate supplementary files and image-only pages can be unavailable; the helper does not perform OCR. The reading states what it could not access.
- **Citation indexes lag.** Very recent papers often have few or no indexed citations, and sandboxed hosts may block the APIs. Failed channels are reported as failures, not as "no citations".
- **Lenses are starting points, not checklists.** They summarise how each community commonly reads papers; a paper outside the 11 lenses gets the nearest lens, adapted.
- **Not a substitute for reading the paper.** The output points you to the sections, figures and derivations worth your own time.

## 中文摘要

**它做什么。** 针对单篇论文：先回答核心问题（研究问题、做了什么、输入输出、相对已有工作的贡献、证据是否支撑结论、后续工作、局限），再按论文领域选 1–2 个"阅读视角"深入解读——统计论文逐个解释关键公式和假设，生命科学论文逐图逐 panel 讲清楚，ML 论文检查 baseline 和消融，经济学看识别策略，临床看偏倚。局限性会标注来源（作者自述 / 后续工作 / 推断），结论按每个主张分别给出可信度。

**安装。** Claude.ai：上传 `field-aware-paper-reader-claude.zip`（Customize → Skills → Upload a skill，需开启代码执行）。Claude Code：复制 `skills/claude/field-aware-paper-reader` 到 `~/.claude/skills/`。Codex：复制 `skills/codex/field-aware-paper-reader` 到 `~/.agents/skills/`。

**语言。** 用你提问的语言回答；论文标题、方法名、符号和术语保留原文。

## Acknowledgements

The field lenses draw on published reading guides and reporting standards, including Keshav's three-pass method, CASP and CONSORT, the OHBM COBIDAS report, COREQ, and the ADEMP framework for simulation studies. See [docs/design.md](docs/design.md). This project is not affiliated with any of these organisations.

## License

MIT. See [LICENSE](LICENSE).
