# Lens: Economics and causal quantitative social science

**How this community reads.** For empirical work, the **identification strategy** carries the paper: what variation in the data is used to estimate the effect, and why that variation can be treated as if it were random. Readers and referees ask whether the counterfactual is clear and compelling and whether measurement error, simultaneity, omitted variables and selection have been dealt with. For theory papers, the "identification" is the logical structure: which assumptions drive which result.

## First: identify the paper type
Empirical causal (RCT, natural experiment, IV, difference-in-differences, regression discontinuity, synthetic control, event study) · structural estimation · descriptive/measurement · theory · macro / time series.

## Empirical papers — questions
- **Question**: What is the causal effect of what on what, for whom? Is it well defined and falsifiable?
- **Identification**: What is the source of variation? What is the counterfactual? What must be true for the estimate to be causal (parallel trends, exclusion restriction, no manipulation at the cutoff, ...)? Is that assumption tested or argued, and how convincing is it?
- **Data**: Where from, sample, unit of observation, key variables and how they are measured.
- **Estimation**: The main regression/estimating equation — interpret every term, the fixed effects, the clustering of standard errors.
- **Threats**: omitted variables, selection, reverse causality, measurement error, spillovers, anticipation, multiple testing. Which robustness and placebo checks address which threat?
- **Magnitude**: Is the effect economically meaningful (not only statistically significant)? Which population does the estimate apply to (e.g. local effect for compliers)?
- **External validity**: Would it hold in other places, times, scales?

## Theory papers — questions
- The model's primitives and key assumptions; which assumption drives the main result (what breaks if it is relaxed)?
- The main propositions in plain words; intuition for the mechanism.
- How general is the result, and what empirical prediction does it make?

## Red flags
- Identification assumption stated but never defended or tested.
- Weak instruments; pre-trends ignored; bandwidth chosen to get significance.
- Standard errors not clustered at the level of treatment.
- Specification searching; results that disappear in robustness tables.

## Write in the "Field lens" section
Identification in one paragraph (variation → counterfactual → key assumption) → estimating equation explained → threats and which checks address them → magnitude and who it applies to. For theory: assumption → result map.
