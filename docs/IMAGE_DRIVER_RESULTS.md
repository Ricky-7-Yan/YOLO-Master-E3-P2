# Image-level input-to-routing association result

## Verdict

Run `p2i-20260905-image-driver-v1` passed its integrity and completeness contract. Within each transformation,
larger input RGB canvas changes were strongly rank-associated with larger continuous probability changes at
`model.16.m.0.router`. The corresponding relationship with discrete dominant-expert switching was mixed across
transformations.

The result supports separating a continuous route-response measurement from the near-tie-sensitive `argmax`
label. It does not prove causality, detector-output impact, learned behavior or population generalization.

## Evidence contract

- Parent manifest: `42d85cb411ef3776bc03b857025dcb77304b5530c4b4b2b4218d0d773d8d45c1`
- Parent verification: 80/80 files, exact path set, zero hash or size mismatches
- Analysis units: 32 images × 3 transforms = 96 records, each endpoint averaged equally over 3 seeds
- Statistic: tie-aware Spearman rank correlation within transform
- Stability: 10,000 image bootstrap draws and 32 leave-one-image-out estimates for each of 6 analyses
- Tool source: commit `0db9e3db2cdee995dc31120a86783d1b9c2e5364`, tree
  `df4298c76c235f147380306aabaa4597f6e5eae9`
- Tests/lint: 51 passed / Ruff passed
- Evidence manifest: SHA-256 `9d731877eb47b2cd0055ad1e065d00dbc55fac0f3cdcd911494b3316a567a2a3`,
  8 non-manifest files, exact set, zero mismatches

## Continuous probability response

| Transform | Spearman rho | Image-bootstrap 95% percentile interval | Leave-one-image-out range |
| --- | ---: | ---: | ---: |
| brightness 0.9 | 0.8586 | 0.6844–0.9426 | 0.8444–0.8908 |
| contrast 0.9 | 0.8490 | 0.6532–0.9374 | 0.8339–0.9012 |
| Gaussian blur 0.75 | 0.9142 | 0.7710–0.9706 | 0.9056–0.9310 |

All three observed coefficients are strongly positive, all three bootstrap intervals remain above zero, and no
single omitted image changes the direction. Within each fixed transform, images whose exact model-input canvas
changed more also tended to have a larger seed-averaged target probability MAE.

This does not make RGB MAE a causal driver. Image brightness, contrast, texture and padding geometry can jointly
affect both pixel distance and router response, and the model is randomly initialized.

## Discrete dominant-expert switching

| Transform | Spearman rho | Image-bootstrap 95% percentile interval | Leave-one-image-out range |
| --- | ---: | ---: | ---: |
| brightness 0.9 | 0.5489 | 0.2384–0.7519 | 0.5070–0.5996 |
| contrast 0.9 | -0.0587 | -0.3894–0.2991 | -0.1305–0.0267 |
| Gaussian blur 0.75 | 0.3384 | -0.0250–0.6241 | 0.2724–0.3961 |

Brightness shows a moderate positive association. Contrast is near zero and its interval spans both directions.
Blur is positive in the observed and all leave-one-out estimates, but the bootstrap interval slightly crosses
zero. This mixed result is retained as evidence that raw input distance alone does not determine discrete expert
switching. The preceding margin analysis explains why: `argmax` also depends on how close the leading experts were
before perturbation.

## Why transforms are not pooled

Brightness, contrast and blur have different pixel-distance ranges and mechanisms. Pooling them would make the
between-transform separation dominate a correlation that is supposed to describe differences among images under
the same transform. The protocol therefore forbids pooled coefficients; no pooled result is computed or reported.

## Reproduction

```bat
run_tests.cmd
run_image_driver.cmd --run-id another-image-driver-run
```

The complete ledger is in
[`artifacts/p2/p2i-20260905-image-driver-v1`](../artifacts/p2/p2i-20260905-image-driver-v1/): verified parent
binding, 96 image records, all bootstrap and leave-one-out values, summary, figure, log and SHA-256 manifest.
