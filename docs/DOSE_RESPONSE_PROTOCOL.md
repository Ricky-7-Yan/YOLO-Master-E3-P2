# Appearance-strength dose-response protocol

## Question

The 32-image audit establishes that three mild appearance transformations change MoA routing, and the
image-driver analysis shows that raw input change is associated with continuous probability response. This
protocol asks whether increasing a transformation's predeclared strength produces a monotone increase in target-
router response within the same image.

This remains a CPU random-initialization mechanism study. It does not measure detector accuracy, causal mediation
or trained robustness.

## Locked ladder

The same 32 filename-hash-selected coco128 images, seeds 0/1/2, 128px geometry, four MoA routers and target
`model.16.m.0.router` are reused.

| Family | Low | Medium | High |
| --- | ---: | ---: | ---: |
| brightness factor | 0.95 | 0.90 | 0.80 |
| contrast factor | 0.95 | 0.90 | 0.80 |
| Gaussian blur radius | 0.25 | 0.75 | 1.50 |

Identity is the common reference. The order reflects increasing distance from identity, not a claim that the
three families share a perceptual severity scale. Families are never pooled.

## Measurements

For each family and level, aggregate target raw-grid probability MAE and dominant-expert switch fraction equally
across seeds within each image. Report:

1. equal-image means and 10,000-draw image-bootstrap percentile intervals at each level;
2. the high-minus-low image-paired difference and its image-bootstrap interval;
3. the fraction of 32 images whose seed-averaged response is non-decreasing across all three levels;
4. the same non-decreasing check across all 96 image×seed units;
5. raw RGB input-effect means and per-image monotonicity as a severity-order validity check.

Probability MAE is primary; expert switch is secondary because `argmax` also depends on the reference margin.
Monotonicity is descriptive and uses no tolerance beyond floating-point equality.

## Pass contract

PASS requires clean committed tooling, exact source fingerprints, the same deterministic 32/128 image selection,
complete 32×3×9×4 candidate comparison coverage, real input changes, monotonically ordered RGB effects for every
image in each ladder, complete seed matrices, image-level resampling, hook/repeat/restoration invariants, evidence
under 64 MiB and an exact SHA-256 manifest.

Routing monotonicity is deliberately not a pass criterion. A plateau, reversal or mixed switch response remains a
valid formal result and must not trigger replacement of levels, images or endpoints.
