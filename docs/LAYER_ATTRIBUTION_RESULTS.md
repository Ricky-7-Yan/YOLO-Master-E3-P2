# Model.16 layer-attribution results

## Formal run

- Run: `p2d-20260905-layer16-attribution-v2`
- Tool source: `66f280230057dbb91d32c9fb2484f4402f2e4100`, clean implementation paths
- Parent: `p2a-20260905-cpu-appearance-v2`
- Parent manifest SHA-256: `7df8fbaf1d10d61d268559ff688cc81a67ab5c3e428b8deb45f1ea2904dd5d21`
- Parent verification: exact 72-file path set, byte lengths and SHA-256, zero mismatches
- Scope: MoA, four router layers, five appearance perturbations, three seeds and four images
- Output: 240 layer comparisons, 60 target-layer cases and 11,520 valid token-comparison exposures

The analysis itself did not run the detector again. It consumed the locked original-coordinate comparisons, raw
router arrays and padding masks retained by the parent formal run. Its own 14-file evidence manifest also passed
independent rehashing with zero mismatches.

## Layer ranking

| Perturbation | `model.16` mean probability MAE | Share of four-layer mean-MAE sum | Rank |
| --- | ---: | ---: | ---: |
| Brightness 0.9 | `5.34e-07` | `95.30%` | 1/4 |
| Brightness 1.1 | `4.36e-07` | `95.05%` | 1/4 |
| Contrast 0.9 | `2.27e-07` | `94.15%` | 1/4 |
| Contrast 1.1 | `1.98e-07` | `94.08%` | 1/4 |
| Gaussian blur 0.75 | `2.34e-08` | `92.90%` | 1/4 |

The target ranked first not only after pooling seeds, but in all 15 transformation×seed strata. Each seed-level
ranking averages the same four images, so an unfavorable initialization was not hidden by the aggregate.

The share denominator is the sum of the four module-level mean MAEs. It shows that the numerical response is
concentrated at this depth under the declared conditions; it is not a causal decomposition of detector output.

## Margin-conditioned switches

At the raw 16×16 target-layer grid, letterbox padding is excluded. Every valid token-comparison exposure is
assigned to exactly one empirical reference-margin decile.

| Reference-margin decile | Token-comparison exposures | Dominant switch rate |
| --- | ---: | ---: |
| 1, lowest margin | 1,115 | `22.60%` |
| 2 | 1,135 | `3.35%` |
| 3 | 1,200 | `0.67%` |
| 4 | 1,125 | `0%` |
| 5 | 1,175 | `0%` |
| 6 | 1,160 | `0%` |
| 7 | 1,135 | `0%` |
| 8 | 1,155 | `0%` |
| 9 | 1,160 | `0%` |
| 10, highest margin | 1,160 | `0%` |

The overall target-layer switch rate is `2.59%`. Brightness 0.9 is the strongest condition: its lowest decile
switches `39.01%`, then falls to `9.25%`, `2.08%` and zero from the fourth decile onward. Even the weakest blur
condition switches `4.04%` in the lowest decile and zero in every other decile.

The decile curve therefore sharpens the previous near-tie diagnosis: all observed target-layer switches lie in
the lowest 30% of the reference-margin distribution, and most lie in the lowest 10%. Because identity margins
repeat once for each candidate transformation, these are token-comparison exposures rather than independent
tokens or images.

## Worst-case localization

One case per perturbation is selected by maximum valid-token switch fraction, then MAE, then a deterministic
seed/sample tie-break. The largest case is brightness 0.9 at seed 1, sample 0: `13.54%` of 192 valid tokens switch,
while raw probability MAE remains only `8.02e-07`. Each case figure preserves the exact 128px inputs and shows
categorical expert maps, a binary switch mask and within-case reference-margin rank. Token fields use
nearest-neighbor enlargement and gray padding.

## Verdict

The formal run passes evidence-lineage, layer-ranking, seed-stratification, raw-array geometry, margin partition,
visual-selection and output-integrity checks. It supports prioritizing `model.16.m.0.router` when a compatible
trained checkpoint becomes available. It does not prove that this layer causes detector errors, that switches
change predictions, or that the cold-start pattern generalizes beyond the declared four-image CPU study.
