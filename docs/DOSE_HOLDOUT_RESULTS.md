# Held-middle dose prediction result

## Verdict

Run `p2h-20260907-dose-holdout-v1` passed its locked parent-integrity, completeness, finite-value, resampling and
manifest gates. Using only each image's low/high route values and its actual low/middle/high RGB distances,
linear interpolation predicted the held middle probability response with median span-normalized absolute error
of `0.115%` for brightness, `0.161%` for contrast and `2.647%` for Gaussian blur.

For all three families, input-distance-weighted interpolation had lower absolute error than the naive low/high
arithmetic midpoint, and the paired image-bootstrap improvement interval remained above zero. This strengthens
the earlier monotonicity result into evidence of an approximately input-distance-proportional continuous response
over these three fixed levels. It is retrospectively specified validation on existing random-initialization data,
not a blind experiment, trained robustness result or accuracy curve.

## Evidence contract

- Parent manifest: `c1917ad0d254b01d33ce9883c33d7d085c3147633915c2cab6213dde95ecaafe`
- Parent verification: 82/82 files, exact path set and zero hash or size mismatches
- Analysis units: 32 images × 3 families = 96 held-middle records, after equal averaging over 3 seeds
- Prediction: linear interpolation in each image's measured RGB MAE using only low/high route endpoints
- Baseline: unweighted arithmetic midpoint of the same low/high endpoints
- Uncertainty: 10,000 image bootstrap draws for errors and paired improvement
- Initialization evidence: 18 predeclared pairwise seed-slope associations, including undefined-draw accounting
- Formal tool source: local commit `9e3cec7615a2817c40b1162ccd3673c07bacbce8`; publication-equivalent
  GitHub commit `0d12bc12d557e5b08fadd2b56b7c5873180f3318`; exact tree
  `52e99d29d82dd24cb390c1132490125104b2f79b`
- Tests/lint: 66 passed / Ruff passed
- Evidence manifest: SHA-256 `1beeb20bf31d2ad153ecfde466cbd8f66e9e45dd322f13c6c66e57eae82b2b2e`,
  8 non-manifest files, exact set and zero mismatches

## Primary probability result

| Family | Weighted absolute error | Naive midpoint error | Naive−weighted improvement | Improvement 95% interval | Normalized median / P90 |
| --- | ---: | ---: | ---: | ---: | ---: |
| brightness | 7.725e-10 | 1.087e-7 | 1.080e-7 | 9.992e-8–1.161e-7 | 0.115% / 0.206% |
| contrast | 6.613e-10 | 5.616e-8 | 5.550e-8 | 5.112e-8–5.980e-8 | 0.161% / 0.422% |
| Gaussian blur | 1.639e-9 | 1.449e-8 | 1.285e-8 | 1.045e-8–1.544e-8 | 2.647% / 5.331% |

The observed middle value lies between the low/high values for 32/32 images in every family. All brightness and
contrast images have normalized error at or below 10%; blur has 30/32 at or below 10% and 32/32 at or below 20%.
Blur is therefore still well ordered but less nearly linear in raw RGB distance than brightness or contrast.

## Secondary switch result

| Family | Weighted absolute error | Naive midpoint error | Improvement 95% interval | Normalized median | ≤10% / ≤20% |
| --- | ---: | ---: | ---: | ---: | ---: |
| brightness | 0.00376 | 0.01319 | 0.00742–0.01134 | 6.02% | 71.9% / 96.9% |
| contrast | 0.00287 | 0.00653 | 0.00231–0.00483 | 6.90% | 71.9% / 93.8% |
| Gaussian blur | 0.00200 | 0.00309 | 0.00013–0.00199 | 22.53% | 21.9% / 46.9% |

Input weighting also improves the switch prediction on average, but the normalized blur error is much larger.
This is consistent with the earlier margin evidence: an `argmax` transition is a threshold event and need not
follow the continuous probability displacement linearly.

## Cross-initialization slope stability

| Family | Probability slope pairwise rho range | Switch slope pairwise rho range |
| --- | ---: | ---: |
| brightness | 0.267–0.628 | -0.067–0.482 |
| contrast | 0.130–0.563 | 0.060–0.202 |
| Gaussian blur | 0.695–0.861 | -0.154–0.097 |

The image-averaged interpolation result does not imply that every initialization ranks image sensitivity the same
way. Probability slope ranking is strongest for blur and mixed for brightness/contrast; switch-slope ranking is
weak or inconsistent. All pairwise coefficients, bootstrap undefined-draw counts and leave-one-image-out records
remain available in the formal JSON.

## Reproduction

```bat
run_tests.cmd
run_dose_holdout.cmd --run-id another-dose-holdout-run
```

The complete ledger is in
[`artifacts/p2/p2h-20260907-dose-holdout-v1`](../artifacts/p2/p2h-20260907-dose-holdout-v1/).
