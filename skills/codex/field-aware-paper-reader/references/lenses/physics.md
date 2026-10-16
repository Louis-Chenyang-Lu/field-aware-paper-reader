# Lens: Physics, astronomy and engineering physics

**How this community reads.** Physicists ask what approximation or model the result rests on, in which regime it is valid, and whether it behaves correctly in known limits. For experiments, the question is whether the signal is real: statistical and systematic uncertainties, calibration, and alternative explanations. On first reading, formulas that are not essential can be skipped; the numbered core equations carry the argument.

## Theoretical / computational papers
- What is the model (Hamiltonian, Lagrangian, field equations, effective theory, simulation setup)? Which degrees of freedom are kept and which are dropped?
- Which approximations are made (perturbative order, mean field, continuum limit, adiabatic, non-relativistic, ...) and in which parameter regime are they valid?
- **Key equations**: write them out, define every symbol with units, check dimensions, and check limiting cases (does it reduce to the known result when a parameter → 0 or ∞?).
- For simulations: resolution, convergence tests, finite-size effects, boundary conditions, validation against known solutions.
- What is the physical prediction, and how could it be tested?

## Experimental / observational papers
- What is measured, with which apparatus/instrument, how calibrated?
- Signal vs background; statistical significance (e.g. in σ); look-elsewhere effect.
- Systematic uncertainties: which sources, how estimated, how they compare to statistical uncertainty.
- Figures: axes and units, error bars (what they include), fits and what is fitted; data vs model comparison and residuals.
- Independent confirmation or consistency with other measurements.

## Red flags
- Approximations used outside their stated regime.
- No convergence or finite-size checks in simulations.
- Systematics hand-waved or smaller than seems plausible.
- Fits with many free parameters presented as confirmation.

## Write in the "Field lens" section
Model and approximations (with regime of validity) → key equations explained with units and limiting checks → for experiments: signal, uncertainties, systematics → figure walk-through → testable predictions.
