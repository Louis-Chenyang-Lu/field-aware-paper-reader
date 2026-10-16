# Usage guide

## When to use it

Use this skill when you want to understand, explain or critically appraise **one** research paper:

- deciding whether a paper is worth reading in full;
- understanding a method, its equations or its figures before using it;
- preparing a journal club or a lab-meeting presentation;
- reviewing or appraising a paper's evidence.

It is not designed for a literature review across many papers. Its forward look finds a small number of verified follow-up papers to put the reading in context; tracing how an idea evolved across a field is a separate task.

## How to prompt

Give the agent the paper and, ideally, three pieces of context:

1. **The paper.** Attach the PDF, or give a DOI, arXiv ID or exact title. An attached PDF gives the best results, because the agent can view the actual figure and equation pages.
2. **Depth.** Quick, standard (default) or deep.
3. **Purpose.** Why you are reading it changes what is stressed: using the method, replicating it, reviewing it, comparing it with alternatives, or presenting it.

Optional:

- **Focus.** "Concentrate on the statistical method" or "explain Figures 2–4 in detail".
- **Lens.** The agent chooses the field lens(es) itself, but you can ask for one, for example "read the method with the statistics lens".
- **Output.** The default is a reading in chat. Ask for a document if you want something to keep or share.
- **Language.** The agent answers in the language you write in; titles, method names, symbols and technical terms stay in the original.

See [examples/prompts.md](../examples/prompts.md) for templates.

## What you get

A standard reading follows this order (headings adapt to your request):

1. **Source and coverage line.** Paper version, depth, lenses, and what was read, viewed or unavailable.
2. **One-sentence summary.**
3. **Research question.**
4. **Approach, inputs and outputs.** Plain words first, technical detail second.
5. **Contribution.** What changes relative to prior work, with the authors' novelty claim kept separate from what the comparisons establish.
6. **Field-lens explanation.** Key equations with every symbol defined; every main-figure panel; design, identification or bias checks, depending on the lens.
7. **Follow-up work.** Zero to five verified successors, each with what it changed and its own limitations, plus the search channels used.
8. **Limitations.** Each labelled by source.
9. **Verdict.** How far each major claim is supported, when the result is useful, and which sections deserve close reading.
10. **References.** With what was actually read for each.

## How to read the output

- **[authors]** — a limitation the authors state themselves.
- **[later work]** — shown or argued by a citing paper.
- **[inferred]** — the agent's own reasoning. It should explain the mechanism and when it matters. Treat these as hypotheses to check, not findings.
- **Demonstrated error / plausible concern / unreported detail.** "Not specified in the material inspected" means the agent could not find it, not that the authors did not do it.
- **Coverage note.** Check it first. A reading based on the abstract only, or on unviewed figures, is weaker, and it should say so.

## Following up

Useful next questions after a reading:

- "Walk me through the derivation of equation <n> step by step."
- "Explain Figure <n> again, assuming no background in <field>."
- "What would I need to check before applying this method to my own data?"
- "Compare this method with <other method> on the assumptions each one makes."
- "Turn this reading into a short journal-club outline."

## FAQ

**The agent says it could not find any follow-up work.**
Recent papers often have few indexed citations, and sandboxed hosts can block the citation APIs. The reading reports which channels worked and which failed. A failed channel does not mean nothing cites the paper. Check again later, or search the preprint version.

**Do I need to install the Python helpers' dependencies?**
No. The helpers are optional. Without them the agent uses the host's own PDF and web tools. With them, it gets a full-text extraction, a page map and rendered pages. For rendering you need PyMuPDF or Poppler.

**My paper's field is not one of the 11 lenses.**
The agent uses the nearest lens, adapts it, and says so. Where search is available, it can also look up how researchers in that field read or review papers and build a temporary lens.

**The paper's key evidence is in the supplementary material.**
Attach the supplementary file as well, or tell the agent where it is. Otherwise the reading will state which claims rest on material it could not access.

**Can it read scanned PDFs?**
Image-only pages need the host's own image viewing or OCR. The helper flags low-text pages but does not perform OCR.
