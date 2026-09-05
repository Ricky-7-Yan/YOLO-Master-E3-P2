# Coco128 image-level scaling result

## Verdict

Run `p2s-20260905-coco128-32-v1` passed its predeclared CPU contract. It expands the primary analysis unit from
four images/repeated tokens to 32 deterministically selected coco128 images. The result supports a bounded
engineering conclusion: under the tested random initializations and mild negative-direction appearance
perturbations, `model.16.m.0.router` is consistently the largest-response MoA router among the four audited
layers.

It does not establish learned expert specialization, causal importance to detector output, detector accuracy or
population generalization.

## Locked coverage and integrity

| Check | Formal result |
| --- | ---: |
| Declared coco128 split | 128 images |
| Deterministically selected | 32 images |
| Seeds / candidate transforms / routers | 3 / 3 / 4 |
| Spatial captures / raw arrays | 1,536 / 1,568 |
| Aligned layer comparisons / target cases | 1,152 / 288 |
| Hook output / repeat weight / repeat logit max delta | 0 / 0 / 0 |
| Tests and lint | 47 passed / Ruff passed |
| Manifest | 80 files, exact set, 0 hash or size mismatch |
| Evidence directory size including manifest | 8,769,286 bytes |

The formal runner recorded local source commit `fc58cc8d945649380c3f647e90f7fea85966bea6` before the run. Its
source tree is `373b6cda6f92635228f76faf2a4924dfc865fda6`; the publication-equivalent GitHub commit is
`f40552a94adbff8e238f156d405f3d0404e56646` with that exact tree. Upstream fingerprints, clean source state,
module order, repeat inference, hook cleanup, restored probability sums and the 64 MiB evidence budget were all
fail-closed checks. The manifest SHA-256 is
`42d85cb411ef3776bc03b857025dcb77304b5530c4b4b2b4218d0d773d8d45c1`.

The hash rule selected two coco128 images whose label files are absent. They remain in the analysis as
`MISSING_DATASET_LABEL`; no post-selection replacement occurred. Labels do not enter the layer ranking or switch
calculations, and padding is derived from recorded image geometry.

## Input-effect audit

Every candidate changed all 32 identity canvases.

| Transform | Mean RGB MAE, 0–255 | Mean changed-channel fraction |
| --- | ---: | ---: |
| brightness 0.9 | 8.0698 | 72.71% |
| contrast 0.9 | 3.6119 | 68.69% |
| Gaussian blur 0.75 | 0.3026 | 23.95% |

## Image-level layer attribution

`model.16.m.0.router` ranked first in all `288/288` image×seed×transform cases, all `96/96`
image×transform aggregates, all `32/32` image aggregates and all `96/96` leave-one-image-out checks.

| Transform | Observed target share | Image-bootstrap 95% percentile interval | Rank-one bootstrap draws |
| --- | ---: | ---: | ---: |
| brightness 0.9 | 95.1290% | 95.0257%–95.2268% | 10,000/10,000 |
| contrast 0.9 | 93.8541% | 93.6705%–94.0191% | 10,000/10,000 |
| Gaussian blur 0.75 | 91.8630% | 91.3256%–92.4304% | 10,000/10,000 |

Share means the target layer's image-mean probability MAE divided by the sum across the four routers. It is a
relative descriptive statistic, not a causal decomposition. Leave-one-image-out stability shows that no single
selected image is necessary for the rank, but it does not remove the fixed-subset or random-initialization limits.

## Target-layer switch localization

Image-level mean switch rates and their image-resampling intervals were:

| Transform | Mean switch rate | Image-bootstrap 95% percentile interval |
| --- | ---: | ---: |
| brightness 0.9 | 3.7891% | 3.2273%–4.3934% |
| contrast 0.9 | 2.2079% | 1.9376%–2.4953% |
| Gaussian blur 0.75 | 0.3978% | 0.3002%–0.5012% |

Across 53,424 valid target-layer token-comparison exposures, 1,125 changed dominant expert. The lowest reference-
margin decile contained 953 switches and had a 17.90% switch rate; deciles 2 and 3 had 2.74% and 0.37%. In total,
84.71% of switches occurred in the first decile, 99.38% in the first three, and none occurred above the fifth
decile. These token counts localize the effect; they are not treated as independent inferential units.

## Reproduction

Run from Windows CMD after placing the repository beside the pinned source and project-local environment:

```bat
run_tests.cmd
run_image_scale.cmd --run-id another-image-scale-run
```

The full machine-readable chain is in
[`artifacts/p2/p2s-20260905-coco128-32-v1`](../artifacts/p2/p2s-20260905-coco128-32-v1/): resolved config,
command, environment, selected input hashes, transformation audit, raw NPZ arrays, per-case comparisons,
image-level rankings, switch summaries, margin deciles, full log and SHA-256 manifest.
