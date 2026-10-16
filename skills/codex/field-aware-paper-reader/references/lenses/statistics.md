# Lens: Statistics and statistical methodology

**How this community reads.** Statisticians read a methods paper as a dependency chain: motivating problem → model and assumptions → estimator or procedure → theoretical properties → simulations → real-data application. The assumptions do most of the intellectual work, so they get the most scrutiny. A common way to judge understanding is: "could I reimplement this and predict when it fails?"

## Reading order
1. Problem formulation: what is the estimand or inferential target? (parameter, function, distribution, causal effect, test, prediction)
2. The model and **every assumption** — explicit ones in the text and implicit ones hidden in notation (independence, identical distribution, linearity, Gaussian or sub-Gaussian noise, sparsity, low rank, smoothness, stationarity, missing-at-random, positivity, correct specification, known variance).
3. The estimator or algorithm: objective function, penalty/prior, tuning parameters and how they are chosen, computational cost.
4. Main theorems: consistency, rates, asymptotic distribution, finite-sample bounds, coverage, identifiability, optimality. Read the conditions before the conclusion.
5. Simulations, then the real-data application.
6. Supplement: proofs and extra simulations often contain the real conditions.

## Equations to interpret (pick the key 2–6)
- The model equation (data-generating process) — what each term represents in the application.
- The estimator's objective — what it trades off and why.
- The main theorem — what the rate or guarantee means in practice (how much data is needed, how the error scales with dimension).
- Any variance or uncertainty formula used for inference.
For each: define every symbol, state what it computes, and **point to the assumption each step depends on**.

## Questions to answer
- Are the assumptions realistic for the data the method is meant for? Which one is most fragile at realistic sample sizes?
- Is the theory about the estimator actually used in practice (e.g. with tuning chosen by cross-validation), or an idealized version?
- What happens when an assumption is violated — does the paper test this?
- Is uncertainty quantified (standard errors, intervals, posterior), and is it valid after model selection / tuning?
- Compared with the closest existing methods, which assumption is relaxed, and what is the price (computation, extra tuning, stronger assumption elsewhere)?

## Simulation checklist (ADEMP: Aims, Data-generating mechanisms, Estimands, Methods, Performance measures)
- Do the data-generating scenarios include cases where the method's assumptions are **violated**, and a regime that favours the competitors? Or only the method's preferred regime?
- Are competitors tuned fairly and up to date?
- Are performance measures appropriate (bias, variance/MSE, coverage, power, type I error) and reported with Monte Carlo error?
- Are the sample sizes and dimensions realistic for the intended application?

## Red flags
- Simulations generated from exactly the proposed model, with no misspecification.
- Theorems whose conditions are never discussed in relation to real data.
- Inference after data-driven selection without adjustment.
- Real-data analysis with no ground truth and no way to tell whether the method helped.
- "Outperforms" claims based on one simulation setting or one dataset.

## Write in the "Field lens" section
Model + assumptions table (assumption | where used | realistic? | consequence if violated) → key equations explained → what the theory guarantees in plain words → simulation critique → real-data critique.
