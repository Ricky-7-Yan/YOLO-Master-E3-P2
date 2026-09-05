# Appearance-strength dose-response result

## Verdict

Run `p2q-20260906-dose-response-v1` passed every predeclared integrity and completeness gate. For brightness,
contrast and Gaussian blur, stronger perturbations produced a non-decreasing target-router probability response
for all 32 images after equal averaging over three random-initialization seeds. The discrete dominant-expert
switch rate was also monotone for every image-level mean, with a small number of seed-specific reversals retained.

This supports a graded cold-start routing response rather than a one-threshold artifact. It does not establish
trained robustness, detector accuracy, causal mediation or a perceptually equivalent severity scale across the
three transformation families.

## Evidence contract

- Units: 32 deterministic coco128 images, 3 seeds, 3 families and 3 predeclared strengths
- Coverage: 3,840 spatial captures, 3,872 raw arrays, 3,456 aligned comparisons and 864 target-layer cases
- Aggregation: image is primary; seeds are averaged equally before image bootstrap and monotonicity checks
- Stability: 10,000 image-bootstrap draws per level and paired high-minus-low difference
- Hook/repeat invariants: exact for all three seeds; maximum hooked-output and repeat delta `0`
- Restoration: maximum expert-sum error `2.384e-7` before and `1.192e-7` after normalization
- Formal tool source: local commit `0764cbfa107a5666b1356facfe98306da575ca76`; publication-equivalent
  GitHub commit `4b635c824007dd30abdf8bfa953fa62789b55822`; exact tree
  `35377c54fa402ac97c394918c1e8ab4dfbb74e6b`
- Tests/lint at formal run: 56 passed / Ruff passed
- Evidence manifest: SHA-256 `c1917ad0d254b01d33ce9883c33d7d085c3147633915c2cab6213dde95ecaafe`,
  82 non-manifest files, exact set and zero mismatches

## Level response

| Family | Low probability MAE | Medium probability MAE | High probability MAE | Low switch | Medium switch | High switch |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| brightness 0.95/0.90/0.80 | 2.366e-7 | 4.559e-7 | 8.927e-7 | 1.91% | 3.79% | 8.29% |
| contrast 0.95/0.90/0.80 | 1.144e-7 | 2.244e-7 | 4.467e-7 | 1.09% | 2.21% | 4.62% |
| blur 0.25/0.75/1.50 | 8.262e-9 | 2.432e-8 | 6.935e-8 | 0.09% | 0.40% | 1.28% |

The raw input-effect audit independently confirms that every image's RGB MAE increases at every adjacent level.
Its equal-image means increase from `4.220→8.070→15.767` for brightness, `1.805→3.612→7.238` for contrast and
`0.047→0.303→1.034` for blur.

## Monotonicity and paired differences

| Family | Probability monotone images | Probability monotone image×seed | Switch monotone images | Switch monotone image×seed |
| --- | ---: | ---: | ---: | ---: |
| brightness | 32/32 | 96/96 | 32/32 | 96/96 |
| contrast | 32/32 | 96/96 | 32/32 | 95/96 |
| Gaussian blur | 32/32 | 96/96 | 32/32 | 92/96 |

| Family | High−low probability MAE | Image-bootstrap 95% interval | High−low switch | Image-bootstrap 95% interval |
| --- | ---: | ---: | ---: | ---: |
| brightness | 6.561e-7 | 6.055e-7–7.048e-7 | 6.38 pp | 5.43–7.38 pp |
| contrast | 3.323e-7 | 3.066e-7–3.588e-7 | 3.53 pp | 3.17–3.93 pp |
| Gaussian blur | 6.109e-8 | 5.310e-8–6.959e-8 | 1.19 pp | 1.00–1.40 pp |

All paired probability intervals remain above zero. The few seed-specific switch reversals are not removed: the
probability distribution can move continuously while a nearly tied `argmax` switches non-monotonically.

## Reproduction

```bat
run_tests.cmd
run_dose_response.cmd --run-id another-dose-response-run
```

The complete ledger is in
[`artifacts/p2/p2q-20260906-dose-response-v1`](../artifacts/p2/p2q-20260906-dose-response-v1/).
