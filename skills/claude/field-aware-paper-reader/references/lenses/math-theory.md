# Lens: Mathematics and theoretical computer science

**How this community reads.** Math papers are not stories and are not read linearly; what you read depends on your goal. A common progression: first the structure and big picture, then the definitions and main notions, then the main statements with small examples, then the ideas behind the proofs, and only then the full proofs. Experienced readers often map the dependencies between lemmas and theorems instead of reading proofs in order.

## Reading order
1. Abstract and introduction: the main theorem(s), stated informally, and why they matter (what was open, what was known).
2. Definitions and notation: make sure every object is understood; build a tiny example and a non-example for each key definition.
3. Main theorem statements: hypotheses vs conclusions; check them on the small examples.
4. Proof overview / proof strategy section (if present), then the dependency map: which lemmas feed which theorem.
5. The key lemma or the step the authors call new — read that proof carefully. Other proofs only in deep mode.

## For each main result
- Restate it formally (LaTeX), then in plain words.
- Which hypotheses are essential, and which are for convenience? Is there a counterexample showing a hypothesis is needed?
- What is the proof technique (induction, probabilistic method, compactness, reduction, potential function, ...) and the one main idea?
- Where exactly is each hypothesis used?
- How does it compare to the previous best result (strengthens, generalizes, unifies, gives the first proof, improves a bound)?

## For algorithms/complexity papers
Model of computation, input/output, running time or approximation ratio, lower bounds, and whether it is practical or only asymptotic.

## Red flags
- "It is easy to see" at the crucial step.
- Main result depends on an unpublished or conjectural result.
- Hypotheses so strong that no interesting example satisfies them.

## Write in the "Field lens" section
Definitions (with tiny examples) → main results formal + plain → dependency map (lemma → theorem) → the key new idea → where the hypotheses bite → comparison with prior bounds/results.
