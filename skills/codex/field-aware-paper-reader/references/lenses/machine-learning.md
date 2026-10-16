# Lens: Machine learning and AI

**How this community reads.** Experienced ML readers do not read linearly: they skim the abstract, introduction and conclusion, then often read the **experiments before the method**, because the evaluation decides whether the method matters. Reviewers focus on whether the baselines are current and fairly tuned, whether ablations isolate the claimed contribution, and whether results are reproducible.

## Reading order
1. Claim: what task, what metric, what improvement, over what.
2. Experiments: datasets/benchmarks, baselines, metrics, main results table, variance across seeds.
3. Ablations: which components were removed or replaced, and how much each contributes.
4. Method: architecture or algorithm, training objective, data, compute.
5. Analysis sections, failure cases, limitations, appendix (hyperparameters, compute budget, data details).

## Equations to interpret
- The training objective / loss — what is optimized and what each term encourages.
- The core architectural or algorithmic change, written as the minimal equation that differs from the closest prior method.
- Any theoretical result (bound, convergence) — what it assumes and whether it explains the empirical gains.

## Questions to answer
- **Baselines**: Are they the current state of the art, or outdated? Same data, compute and tuning budget? Are numbers re-run or copied from other papers under different settings?
- **Ablations**: Does each claimed component have an ablation? Could the gain come from something bundled with it (more data, bigger model, better tuning, longer training)? Which obvious ablation was not run?
- **Statistics**: Mean ± std over several seeds? Are differences larger than seed-to-seed noise? Any significance or confidence intervals?
- **Generalization**: Out-of-distribution or held-out evaluation? Test-set contamination risk (especially for pretrained models)? Was the test set used for model selection?
- **Cost**: training/inference compute, memory, data requirements — is the improvement worth it?
- **Mechanism**: Does the paper explain *why* it works (analysis, probing, controlled experiments), or only *that* it works?

## Red flags
- Bold numbers with no variance; single seed.
- Baselines several years old, or under-tuned.
- Gains within noise, or only on one benchmark.
- Complexity not justified by ablations.
- Evaluation only on the authors' own new benchmark.
- No code, no hyperparameters, no compute reported.

## Reporting standard
NeurIPS/ICML-style paper checklists (claims, limitations, reproducibility, compute, data, code). Use them to spot what is missing.

## Write in the "Field lens" section
Main results in one sentence → baseline fairness → ablation map (component | evidence it matters) → the key equation(s) explained → cost → what would convince a sceptical reviewer that is missing.
