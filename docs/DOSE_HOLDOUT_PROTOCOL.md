# Held-middle dose prediction protocol

## Question

The formal dose run established non-decreasing target-router response at three predeclared strengths. This
integrity-bound post-hoc analysis asks a stricter question: for the same image, can the low and high observations
predict the held middle response when interpolation is weighted by the middle condition's actual RGB input
distance?

The parent data already exist, so this is a retrospectively specified held-level analysis, not a prospective blind
experiment. The protocol is committed before inspecting per-image residuals. It does not measure learned behavior,
accuracy or causal response.

## Locked method

- Parent: exact manifest of `p2q-20260906-dose-response-v1`
- Unit: image after equal averaging over seeds 0/1/2; 32 images per family
- Families remain separate: brightness, contrast and Gaussian blur
- Held point: the predeclared middle level; only low/high route values and low/middle/high RGB MAE enter prediction
- Predictor: `y_low + ((x_middle-x_low)/(x_high-x_low)) * (y_high-y_low)`
- Baseline: unweighted endpoint midpoint `(y_low+y_high)/2`
- Primary endpoint: target raw-grid probability MAE
- Secondary endpoint: dominant-expert switch fraction
- Error: absolute residual for all images; span-normalized residual only when `|y_high-y_low|>0`
- Uncertainty: 10,000 image bootstrap draws for absolute error, signed error and paired baseline improvement
- Initialization check: pairwise Spearman association of low-to-high per-image response slopes across three seeds

No transform family is pooled. A zero endpoint span is retained with null normalized error. Correlation is retained
as undefined when a seed-slope vector is constant. Undefined bootstrap resamples and leave-one-image-out estimates
are counted; a bootstrap interval is emitted only when at least 95% of predeclared draws are defined.

## Pass contract

PASS requires a clean committed analyzer, exact parent path/hash/size verification, the complete
3-family×3-level×32-image×3-seed matrix, strict low<middle<high RGB distances for every image, finite predictions,
all residuals regardless of direction, deterministic image-level resampling, evidence below 8 MiB and an exact
SHA-256 manifest. Predictive error, improvement over baseline and correlation sign are observations, not PASS
criteria.
