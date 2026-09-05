# CPU appearance-sensitivity results

## Formal run

- Run: `p2a-20260905-cpu-appearance-v2`
- Tool source: `bfebd950e7a3f5f1dc06419c3bf0f46856c1ea98`, clean implementation paths
- Upstream runtime: `07d330325b5a26b75aabfc75389f9bcbc0d40245`; four source fingerprints matched
- Device/input: CPU, 128px letterbox
- Data/states: four `coco8` validation images, 17 boxes, seeds 0/1/2
- Conditions: identity, brightness 0.9/1.1, contrast 0.9/1.1 and Gaussian blur radius 0.75
- Output: 576 captures, 1,536 raw arrays, 480 original-coordinate comparisons and 960 token-region comparisons

All six family/seed invariant groups passed exact hooked-versus-unhooked output comparison, exact repeated
weights/logits, module-order checks and hook cleanup. MoT indices repeated exactly. Restoration expert-sum error
was at most `2.3841858e-07` before and `1.1920929e-07` after explicit normalization. The run took 95.00 seconds
on this machine; this is an operational observation, not a benchmark.

## Input-effect audit

| Perturbation | Changed samples | Mean model-input RGB MAE / 255 | Mean changed-channel fraction |
| --- | ---: | ---: | ---: |
| Brightness 0.9 | 4/4 | `10.620` | `75.78%` |
| Brightness 1.1 | 4/4 | `8.524` | `74.87%` |
| Contrast 0.9 | 4/4 | `4.027` | `72.05%` |
| Contrast 1.1 | 4/4 | `3.493` | `70.97%` |
| Gaussian blur 0.75 | 4/4 | `0.474` | `34.57%` |

The transformed original, exact 128×128 PNG canvas, PNG SHA-256 and raw uint8 RGB-byte SHA-256 are retained for
each sample/condition. The formal run would fail if any configured candidate were identical to identity.

## MoA result

| Perturbation | Probability MAE | Mean JS (nats) | Overall dominant agreement | Agreement at reference P90+ margin |
| --- | ---: | ---: | ---: | ---: |
| Brightness 0.9 | `1.40e-07` | `1.36e-13` | `95.54%` | `98.96%` |
| Brightness 1.1 | `1.15e-07` | `9.30e-14` | `96.24%` | `98.97%` |
| Contrast 0.9 | `6.03e-08` | `3.14e-14` | `97.76%` | `99.99%` |
| Contrast 1.1 | `5.26e-08` | `2.27e-14` | `97.86%` | `100%` |
| Gaussian blur 0.75 | `6.29e-09` | `3.47e-16` | `99.57%` | `100%` |

Pixels that changed dominant expert had mean reference margins between `2.55e-08` and `8.07e-08`; unchanged
pixels were between `7.54e-07` and `7.76e-07`. The changed/unchanged margin ratio is therefore only about
`3.4%–10.4%`. Together with the P90+ agreement, this directly supports the diagnosis that cold-start expert
switches concentrate around near-ties.

`model.16.m.0.router` had the largest MoA probability MAE under every perturbation. For brightness 0.9 its mean
MAE was `5.34e-07`, while the remaining layers were roughly one to two orders of magnitude lower. Seed 1 was also
the least agreement-stable brightness state (`91.88%` at factor 0.9), demonstrating why a single seed would be
insufficient for even this mechanism-level description.

## Region and MoT boundaries

Foreground and valid-background MoA probability MAE remained in the same tiny order for every perturbation. The
direction was not consistent: for brightness 0.9 and contrast 0.9/1.1 background MAE was slightly larger, while
brightness 1.1 and blur had slightly larger foreground MAE. These four-image descriptive differences do not
support a foreground-specific sensitivity claim.

MoT again produced exact zero MAE/JS and 100% agreement for every perturbation, but its cold-start maps were
spatially constant and all 144 Pearson values per transform group were undefined. This is repeatable constant-map
behavior, not evidence of trained appearance robustness.

## Verdict

The run passes the input-audit, routing-capture, original-coordinate comparison, region-analysis and integrity
contract. It strengthens the near-tie explanation and identifies a layer worth prioritizing after a compatible
trained checkpoint becomes available. It does not establish detection accuracy or learned robustness.
