# Image-level input-to-routing association protocol

## Question

The 32-image scaling run shows that appearance perturbations change both input pixels and target-layer routing.
This post-hoc analysis asks a narrower question: within one fixed transformation, do images with a larger raw RGB
canvas change also tend to show a larger `model.16.m.0.router` change?

This is an association analysis under random initialization. It is not a causal mediation test, a detector-output
analysis or a population estimate.

## Locked design

- Parent: exact manifest of `p2s-20260905-coco128-32-v1`
- Unit: each of the 32 selected images after equal averaging across seeds 0, 1 and 2
- Predictor: mean absolute RGB difference between candidate and identity 128×128 uint8 canvases, on `[0,255]`
- Endpoints: target-layer probability MAE and dominant-expert switch fraction
- Strata: brightness 0.9, contrast 0.9 and Gaussian blur 0.75 analyzed separately
- Statistic: tie-aware Spearman rank correlation
- Stability: 10,000 image bootstrap draws and 32 leave-one-image-out estimates per endpoint and transform

Cross-transform pooling is forbidden because the units and mechanisms of brightness, contrast and blur differ.
No alternate predictor or endpoint is selected after looking at results. Undefined correlations must be preserved;
the run fails if the observed coefficient, any leave-one-out coefficient or more than 5% of bootstrap draws is
undefined.

## Pass contract

PASS requires exact parent file-set/hash/size verification, clean committed tooling, one input-effect record and
exactly three unique seed cases for all 96 image×transform units, non-no-op inputs, finite image aggregates,
complete within-transform analyses, deterministic bootstrap results, a machine-readable record ledger, a bounded
overview and a new SHA-256 manifest.

The sign and magnitude of the correlations are not pass criteria. Weak, mixed or negative results are valid and
must be reported without switching to a more favorable pooled analysis.
