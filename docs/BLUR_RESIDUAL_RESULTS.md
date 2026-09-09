# Gaussian-blur residual diagnosis result

## Verdict

Run `p2x-20260908-blur-residual-v1` passed both locked-parent checks, the 32-image feature matrix contract,
finite-statistic gates and its evidence manifest. None of the three predeclared input-only features passed the
Holm-corrected alpha 0.05 threshold. The larger held-middle blur error is therefore not adequately explained by
source-image mean luminance, square-letterbox content fraction or one global edge-total-variation value on this
fixed subset.

This controlled null result narrows the next hypothesis. It does not show that image content is irrelevant:
localized structure, object scale or nonlinear blur effects were not tested. It is a retrospective diagnostic of
random-initialization evidence, not a mechanism intervention, trained result or accuracy analysis.

## Evidence contract

- Held-middle parent manifest:
  `1beeb20bf31d2ad153ecfde466cbd8f66e9e45dd322f13c6c66e57eae82b2b2e` (8/8 exact files)
- Image-source manifest:
  `c1917ad0d254b01d33ce9883c33d7d085c3147633915c2cab6213dde95ecaafe` (82/82 exact files)
- Selected image-and-label set:
  `80020696759bd2b6a6e68bb645c9c748e90c4b6425489563a746f72fbd161c4f`
- Unit: 32 selected images; no token or seed pseudo-replication
- Endpoint: held-middle Gaussian-blur span-normalized absolute `probability_mae` residual
- Features: letterbox content fraction, mean luminance and continuous edge total variation
- Uncertainty: 10,000 complete-image bootstrap draws per coefficient
- Tests: 20,000 fixed-seed two-sided residual permutations; Holm correction across exactly three tests
- Influence: all 32 leave-one-image-out coefficients
- Formal tool source: commit `efe6763fb5f0e710a0be25a439d672d24eaca232`, tree
  `e528c88e67574ea025e34ef69db936afc249d7bc`
- Tests/lint before formal run: 73 passed / Ruff passed
- Evidence: 10 non-manifest files, 774,725 bytes before manifest
- Evidence manifest SHA-256:
  `4662cecb43174c2e39a415a866c59d07f65c1ee75c87f94d6bf823dd7d527129`

## Predeclared associations

| Input-only feature | Spearman rho | Bootstrap 95% interval | Raw permutation p | Holm p | LOO range |
| --- | ---: | ---: | ---: | ---: | ---: |
| Letterbox content fraction | -0.117 | -0.462 to 0.253 | 0.520 | 1.000 | -0.187 to -0.034 |
| Mean luminance | -0.052 | -0.405 to 0.293 | 0.774 | 1.000 | -0.138 to 0.010 |
| Edge total variation | -0.289 | -0.607 to 0.120 | 0.106 | 0.318 | -0.356 to -0.221 |

Edge total variation had the largest absolute coefficient and remained negative in every leave-one-image-out
sample, but its bootstrap interval crossed zero and its Holm-adjusted p-value was 0.318. It is a follow-up lead,
not a detected effect. The three feature-pair correlations were only `0.04–0.15`, so the null decisions are not
explained by strong collinearity among the predeclared predictors.

## Residual distribution and high-error cases

The normalized blur residual ranged from `0.012%` to `11.308%`; median, P75 and P90 were `2.647%`, `3.525%`
and `5.331%`. Only two images exceeded 10%:

1. sample 17, `000000000370.jpg`: `11.308%`;
2. sample 28, `000000000514.jpg`: `10.390%`.

The published contact sheet keeps the six highest-residual images visible but treats the ranking as descriptive.
No new hypothesis was created from visual inspection of those images.

## What this changes

Before this run, the larger blur interpolation error could be loosely attributed to aspect ratio, brightness or
texture. After predeclared testing, no such single global explanation is supported. The next defensible local
step is a prospective or cross-validated test of a small number of spatially localized features, such as
multi-scale edge loss or object-size distribution. Those must use a new protocol and run ID; this analysis must
not be expanded after observing its null result.

## Boundaries

- The 32 images are a deterministic fixed subset of coco128, not an independent population sample.
- Feature values come from the unperturbed source image; associations are observational and non-causal.
- The model is randomly initialized. These values do not describe learned routing specialization.
- No accuracy, AP, corruption robustness, CUDA latency or GPU memory conclusion is supported.
- Holm non-rejection does not prove zero effect; it says this design did not establish one.
