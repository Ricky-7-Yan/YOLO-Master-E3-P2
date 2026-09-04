# CPU resolution and horizontal-flip protocol

## Questions

This protocol asks two bounded questions about the real MoT and MoA router probability grids:

1. With one fixed random model state, how much do original-coordinate probability maps change when the letterboxed input grows from 64 to 128 or 256 pixels?
2. After a horizontal flip is mapped back to the original coordinate system, how close is it to the identity-input probability map?

It also counts ground-truth foreground, valid background and letterbox-padding tokens at each resolution. That count tests whether higher resolution reduces `INSUFFICIENT_TOKENS` cases in the existing region-analysis protocol.

## Controlled variables

- Device: CPU only.
- Model families: the official MoT and MoA configs whose routers expose true `[B,E,H,W]` probabilities.
- Seeds: 0, 1 and 2. A model is initialized once per family and seed; all transformations for that pair reuse the same state.
- Data: four fixed COCO8 validation images and their archived YOLO labels.
- Resolutions: 64, 128 and 256; 64 is the cross-resolution reference.
- Transformations: identity and horizontal flip only.
- Source: locked official runtime ref plus per-file SHA-256 checks.

## Coordinate alignment

Each expert grid is bilinearly upsampled into letterbox input space, cropped with the recorded integer padding and resized to the original image dimensions. Experts are re-normalized per pixel after interpolation. A flipped observation is then horizontally unflipped. Metrics therefore compare equal expert channels at equal original-image pixels.

## Metrics

- Probability MAE, RMSE and maximum absolute error.
- Mean and maximum total-variation distance across the expert distribution at each pixel.
- Mean and maximum Jensen-Shannon divergence in natural-log units.
- Dominant-expert agreement fraction.
- Reference and candidate mean top-1 probability margins, retained so near-tie `argmax` changes are not mistaken for large probability shifts.
- Per-expert Pearson correlation. If either map is constant, correlation is recorded as `null` with `UNDEFINED_CONSTANT_INPUT`; it is never replaced by a convenient numeric value.

Jensen-Shannon divergence is mathematically non-negative. Values below zero caused only by floating-point roundoff are clipped to zero before aggregation.

Each seed × sample × router-module comparison has equal weight in aggregate summaries. Raw per-comparison records remain available so pooled values can be audited.

## Invariants and failure policy

The run stops if source fingerprints drift, tracked implementation files are uncommitted, router module order changes, hooks alter model output, repeat inference differs, hooks leak, probabilities are invalid, or coordinate restoration fails. The manifest hashes every artifact.

`PASS` means the capture, geometry, alignment, determinism and evidence-integrity checks completed. It does **not** mean a randomly initialized detector is accurate, trained, flip-invariant or production-robust. Learned robustness requires an approved checkpoint and downstream accuracy evaluation.

## Reproduction

From `cmd.exe` in the repository root:

```bat
run_tests.cmd
run_robustness.cmd
```

The formal run is written under `artifacts/p2/<run-id>/`; `ROBUSTNESS_LATEST.txt` contains the latest formal run id.
