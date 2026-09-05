# Router-to-detector-output coupling result

## Verdict

Run `p2o-20260906-output-coupling-v2` passed its source, capture, matrix, finite-value and manifest gates. The
predeclared primary detector endpoint, the fixed-grid one-to-one class-score tensor, had exactly zero change for
all 288 seed×image×transform comparisons under this randomly initialized model. Its six primary correlations are
therefore correctly reported as undefined rather than zero or replaced after seeing the data.

The predeclared secondary box endpoint did vary. Within each transform, target-router probability MAE had a strong
positive rank association with one-to-one box-tensor MAE (`rho=0.860–0.930`), with all three image-bootstrap
intervals above zero and all leave-one-image-out values positive. This is a useful end-to-end numerical coupling
observation, but it does not establish route causality, correct detections or an accuracy effect.

## Evidence contract

- Units: 32 deterministic coco128 images after equal averaging over seeds 0/1/2
- Conditions: brightness 0.8, contrast 0.8 and Gaussian blur 1.5, each against identity
- Coverage: 1,536 spatial captures, 1,568 raw arrays, 1,152 layer comparisons, 288 target cases and 288 detector comparisons
- Analysis: 96 image×transform records and 30 predeclared tensor×router-endpoint associations
- Defined/undefined: 12 defined box associations; 18 score/decoded associations undefined because the detector vector is constant
- Formal tool source: local commit `2fb30d82a9a0853d6cc7435a7abae94e46770d52`; publication-equivalent
  GitHub commit `0cd9d70b5f928c4764a7d63c1435732bee7acbfa`; exact tree
  `ff04d282059cb90cdb4f789f2b52eaa2df0943ee`
- Hook/repeat invariants: exact for all three seeds; maximum hooked-output and repeat delta `0`
- Tests/lint: 61 passed / Ruff passed
- Evidence manifest: SHA-256 `2263e40decee2620290c171940aed03f3b0e6b2884f60adf7680fd4edbe9bca4`,
  84 non-manifest files, exact set and zero mismatches

## Primary endpoint: retained null result

| Transform | One-to-one score MAE range across 96 seed-level comparisons | Probability association | Switch association |
| --- | ---: | ---: | ---: |
| brightness 0.8 | exactly 0 | undefined | undefined |
| contrast 0.8 | exactly 0 | undefined | undefined |
| Gaussian blur 1.5 | exactly 0 | undefined | undefined |

The same zero-change result appears in one-to-many scores and decoded Top-300. A constant ranked vector has no
Spearman coefficient; assigning `rho=0` would falsely imply a measured absence of rank association. The analysis
records `null`, unique-value count `1`, and no bootstrap or leave-one-out interval.

## Secondary endpoint: box-tensor association

| Transform | Router predictor | Spearman rho | Image-bootstrap 95% interval | Leave-one-image-out range |
| --- | --- | ---: | ---: | ---: |
| brightness 0.8 | probability MAE | 0.9295 | 0.8218–0.9683 | 0.9225–0.9467 |
| contrast 0.8 | probability MAE | 0.8933 | 0.7472–0.9563 | 0.8827–0.9194 |
| Gaussian blur 1.5 | probability MAE | 0.8604 | 0.6861–0.9451 | 0.8464–0.8882 |
| brightness 0.8 | expert-switch fraction | 0.6295 | 0.3439–0.7843 | 0.5969–0.6812 |
| contrast 0.8 | expert-switch fraction | -0.0264 | -0.3876–0.3346 | -0.1154–0.0440 |
| Gaussian blur 1.5 | expert-switch fraction | 0.5562 | 0.2191–0.7979 | 0.5117–0.6160 |

The continuous probability endpoint is consistently associated with box change. The thresholded switch endpoint
again varies by transformation: contrast is near zero. This agrees with the earlier finding that switch rate also
depends on the reference Top-1 margin, not only on the amount of probability movement.

One-to-one and one-to-many box tensors are numerically identical in this evaluation return contract, so they are
both archived for contract coverage but are not interpreted as independent replications. The observed box MAEs
are extremely small (approximately `7.1e-10–8.2e-8` at seed level), which is another reason not to overstate them.

## Failed-boundary evidence

The first analysis attempt (`p2o-20260906-output-coupling-v1`) completed all forward captures but rejected the
constant score vector because the generic correlation helper requires a defined coefficient. That directory is
retained locally as failed evidence and is not published as a formal PASS. The v2 fix added an explicit
`UNDEFINED_CONSTANT_VECTOR` state, a regression test, and a new run ID; it did not substitute endpoints or alter
the data-generating configuration.

## Reproduction

```bat
run_tests.cmd
run_output_coupling.cmd --run-id another-output-coupling-run
```

The complete ledger is in
[`artifacts/p2/p2o-20260906-output-coupling-v2`](../artifacts/p2/p2o-20260906-output-coupling-v2/).
