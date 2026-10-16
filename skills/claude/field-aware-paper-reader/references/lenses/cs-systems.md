# Lens: Computer systems, networking, software engineering, quantitative HCI

**How this community reads.** Systems papers are read with the three-pass approach: a quick first pass on title, abstract, introduction, headings and conclusions to get the gist; a second pass on figures and the main argument while skipping details; and a third pass that virtually re-implements the work to find hidden assumptions. The evaluation is judged on realistic workloads, strong baselines, out-of-sample testing, and whether ablations separate the new idea from the engineering around it.

## Reading order
1. Problem and setting: what system, what bottleneck or failure, why existing systems fall short.
2. Key insight: the one idea the design rests on.
3. Design: architecture diagram, main mechanisms, assumptions about the environment (workload, hardware, failure model, threat model).
4. Evaluation: setup, workloads, baselines, metrics, main graphs.
5. Discussion, limitations, related work.

## Questions to answer
- Is the key insight stated clearly, and is it really new or a known technique in a new setting?
- What does the design assume about workload, scale, hardware or failures — and what happens when those change?
- Evaluation: realistic or production workloads vs microbenchmarks? Strong, well-configured baselines? Tail latency as well as averages? Repeated runs with variance? Tested on workloads not used to design or tune it?
- Ablations: which component gives which gain?
- Costs: complexity, resources, compatibility, deployment effort.
- For HCI/user studies: participants, task realism, measures, statistics, and novelty effects.

## Figures
For each evaluation graph: axes, workload, which line is which system, what the gap is and under which load/scale it appears or disappears.

## Red flags
- Only microbenchmarks; only the operating point the system was tuned for.
- Baselines misconfigured or old versions.
- Averages without tails or variance.
- Threat or failure model narrower than the claims.

## Write in the "Field lens" section
Key insight → design and its environmental assumptions → evaluation critique (workloads, baselines, variance, out-of-sample) → ablation map → when it would not help.
