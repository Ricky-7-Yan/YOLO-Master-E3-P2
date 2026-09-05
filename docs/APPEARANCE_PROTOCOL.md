# CPU appearance-perturbation protocol

## Question

With one fixed random model state and one fixed 128px geometry, how much do true MoT/MoA spatial-router
probabilities change under mild brightness, contrast and blur perturbations? Are discrete dominant-expert changes
concentrated where the reference router margin is small, and do foreground/background tokens show different
sensitivity in this mechanism test?

## Controlled design

- Device: CPU only.
- Data: the same four archived `coco8` validation images and 17 YOLO boxes used by the region experiment.
- Model states: seeds 0, 1 and 2; each family/seed model is initialized once and reused for every appearance input.
- Geometry: 128px aspect-preserving letterbox for every condition. The previous resolution experiment selected
  128 because all 16 layer/image captures per family contained both foreground and valid background tokens.
- Reference: identity input.
- Perturbations: brightness factors 0.9/1.1, contrast factors 0.9/1.1, Gaussian blur radius 0.75.
- Source: locked official runtime plus four per-file SHA-256 checks.

Every transformed original and the exact 128×128 uint8 letterbox canvas consumed by the model are archived. The
PNG file hash and raw RGB-byte hash are recorded before inference.
Each candidate canvas is also compared against its identity canvas on the `[0,255]` RGB scale. The run fails if
any configured perturbation becomes a no-op for any of the four selected samples; mean/min/max input MAE and
changed-channel fraction remain in the evidence bundle.

## Measurements

All expert maps are restored to original-image pixels and re-normalized before comparison. The experiment records
probability MAE/RMSE/max error, total variation, float64 Jensen-Shannon divergence, dominant-expert agreement,
Top-1 margins and per-expert Pearson correlation. Constant-map correlations remain explicitly undefined.

For each comparison, agreement is also recomputed on pixels whose reference margin is at or above its 0th, 25th,
50th, 75th and 90th percentile. These are diagnostic strata, not post-hoc pass thresholds. Aggregate reports keep
equal-weight summaries by transformation/family/resolution, router module and seed.

The raw 128px router grids are additionally sliced by ground-truth foreground and valid-background masks;
letterbox padding is excluded. Region comparisons are equal-weight descriptive summaries and do not treat layers
from the same image as independent population samples.

## Failure policy and interpretation

The run stops on source drift, uncommitted implementation files, transform-contract drift, router-module order
changes, hook output changes, repeat mismatch, invalid probabilities, failed restoration or hook leaks. A SHA-256
manifest covers every evidence file.

`PASS` means the controlled input audit, capture, comparison and evidence-integrity pipeline completed. The models
remain randomly initialized; results do not establish learned appearance robustness, detection accuracy or
behavior on a larger dataset.

## Reproduction

```bat
run_tests.cmd
run_appearance.cmd
```
