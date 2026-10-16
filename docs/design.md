# Design notes

## Two layers

Every reading combines:

1. **Core questions** that matter for every paper: the research question, the approach, inputs and outputs, the contribution relative to prior work, the evidence for each claim, later work, and limitations.
2. **A field lens**: what the paper's own community looks at most closely. A lens is chosen by how the paper argues, not by where it was published; a methods paper in a biology journal still needs a methods lens.

Interdisciplinary papers get at most two lenses: one for the method and one for the application. Where the two disagree (for example, a method that is statistically sound but rests on a measurement step the application field considers fragile), the reading says so.

## Why the lenses are built in

The lenses were written once from published reading guides and reporting standards rather than searched for at every reading. This makes readings faster and more consistent. If a paper falls outside all 11 lenses, the skill adapts the nearest one and, where search is available, can briefly look up how that field reads papers to build a temporary lens.

## Calibration rules

The skill is designed to avoid two common failure modes of automated critique: inventing problems and overstating them.

- Limitations are labelled by source: **[authors]**, **[later work]** or **[inferred]**.
- An inferred issue must state its mechanism and the conditions under which it matters.
- A demonstrated error, a plausible concern and an unreported detail are kept separate. "Not specified in the material inspected" is different from "not done".
- Statistical claims are judged on the experimental unit, selection reuse, null construction, sample-size matching, dependence, multiple comparisons and calibration — not dismissed wholesale.
- The skill does not demand a simulation, theorem or intervention from every paper; it explains when missing evidence matters for the paper's actual claim.
- The verdict is given per claim, because computational and biological evidence, for example, can differ in strength within one paper.

## Grounding in the source

- The full extracted text is kept alongside heuristic navigation aids; claims of absence are checked against the raw text and page images.
- Figures and key equations are described only after their pages have been viewed. A rendered image that was not looked at does not count.
- Exact equations are kept separate from the reader's interpretation, and a corrupted extraction is never reconstructed as though it were transcribed.

## Bounded forward look

Follow-up work is useful context for a single paper, but an unbounded search turns a reading into a literature review. The skill therefore:

- checks both journal and preprint versions, because citations are often attached to the preprint;
- uses citation indexes (Semantic Scholar, OpenAlex) plus a few targeted web searches, then stops;
- keeps zero to five successors whose relationship to the paper is verified from primary text;
- reports failed channels, result caps and dates, and never presents a capped list as exhaustive.

## Sources behind the lenses

The lenses summarise widely used reading and appraisal guidance, including:

- S. Keshav, "How to Read a Paper" (the three-pass method).
- Critical Appraisal Skills Programme (CASP) checklists; CONSORT, STROBE, STARD, TRIPOD, PRISMA and related reporting guidelines.
- OHBM Committee on Best Practices in Data Analysis and Sharing (COBIDAS) report.
- COREQ (Consolidated criteria for reporting qualitative research).
- Morris, White and Crowther, "Using simulation studies to evaluate statistical methods" (the ADEMP framework).
- Machine-learning conference paper checklists (NeurIPS/ICML style).
- Published guidance on reading mathematics, empirical economics and experimental biology papers.

This project is not affiliated with any of these authors or organisations.
