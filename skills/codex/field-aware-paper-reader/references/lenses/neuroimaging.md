# Lens: Neuroimaging and imaging-based measurement science

**How this community reads.** In imaging, the result depends heavily on a long chain of acquisition and processing choices, so readers check the pipeline as carefully as the statistics. The OHBM COBIDAS report organises good practice into seven areas: experimental design, image acquisition, preprocessing, statistical modelling, results reporting, data sharing, and reproducibility. Use these as the reading frame. The same logic applies to other imaging pipelines (EEG/MEG, PET, microscopy, remote sensing): what was measured, how it was turned into numbers, and how those numbers were tested.

## Reading order
1. Question and design: task vs rest vs structural/diffusion; within vs between subjects; sample and inclusion/exclusion criteria.
2. Acquisition: scanner/field strength or instrument, key sequence parameters, resolution, coverage.
3. Preprocessing pipeline: software and versions, motion handling, registration/normalization, denoising, and for derived measures the key modelling choices (e.g. parcellation/atlas, reconstruction or tractography method, network construction, thresholds).
4. Statistical model: what is tested at which level (subject vs group), covariates, multiple-comparison correction, cross-validation for predictive claims.
5. Results figures: brain maps, connectivity matrices, effect sizes; what threshold was used.
6. Data and code availability.

## Questions to answer
- Would a different reasonable pipeline choice (atlas, threshold, preprocessing option) change the result? Did the authors test sensitivity to it?
- How was head motion (or the equivalent nuisance) handled, and could it explain group differences?
- Is multiple-comparison correction appropriate for the number of tests (voxels, edges, regions)?
- Are effect sizes reported, not only significant clusters? Is the sample large enough for the claimed effect (brain–behaviour associations often need large samples)?
- For predictive claims: proper out-of-sample validation, no leakage (e.g. feature selection on all data)?
- Is the interpretation within what the measurement can support (e.g. a derived connectivity estimate is not the same as anatomical ground truth)?

## Figures
For each map or matrix: what quantity is shown, thresholded how, in which space/atlas, what colour means, which contrast or group. Check that the colour scale and threshold do not exaggerate the effect.

## Red flags
- Circular analysis (selecting regions using the same data then testing them).
- Uncorrected or loosely corrected maps presented as findings.
- Small samples with strong brain–behaviour correlations.
- Pipeline details missing or "standard pipeline" without specifics.
- Group differences that could be motion or quality differences.

## Reporting standard
COBIDAS (MRI) and its MEEG counterpart; BIDS for data organisation.

## Write in the "Field lens" section
Pipeline summary (design → acquisition → preprocessing → model) → which choices the result is most sensitive to → statistics critique → figure walk-through of the key maps/matrices → reproducibility.
