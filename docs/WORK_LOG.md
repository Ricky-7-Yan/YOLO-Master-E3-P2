# Work log

## Feasibility boundary

- Audited five routing families at source and runtime level.
- Identified MoT and MoA as genuine spatial producers.
- Added explicit unsupported results for MoE, Latent and MoLoRA rather than synthesizing heatmaps.

## Implementation

- Added non-invasive child-router capture with guaranteed cleanup.
- Added probability, spatial-axis, shape and MoT Top-K consistency gates.
- Added exact letterbox metadata and reversible original-image mapping.
- Added fixed-scale probability overlays, categorical dominant-expert views and raw NPZ archival.
- Added fixed-scale normalized-entropy and Top-1-margin diagnostics with aggregate statistics.
- Added a static local demo with paired original/overlay images, sample/family/layer/view selection, metadata copy
  and PNG export.
- Added committed-source and pinned-upstream fingerprint checks.

## Verification

- Added positive and negative contract tests for geometry, capture, plotting, run IDs and demo resolution.
- Compared full model outputs before and after hooks.
- Repeated every MoT/MoA spatial capture and compared raw values exactly.
- Compared every routed record from batch sizes 2 and 4 against its single-image source and preserved the deltas.
- Checked all demo paths, uniqueness, archived originals and original-size output dimensions before PASS.
- Exercised the rendered demo at desktop and mobile widths and removed a favicon 404 found in the first browser pass.
- Recalculated the evidence manifest after browser validation; all file hashes match.

## Ground-truth region analysis

- Audited local and official release assets and found no explicitly compatible trained MoT/MoA checkpoint; kept
  the current result as an initialization baseline instead of partially loading mismatched weights.
- Added strict YOLO label parsing, label hashes and archived label evidence for all selected images.
- Added exact integer-letterbox token assignment with foreground, valid-background and padding masks; padding is
  excluded from the semantic comparison.
- Added per-capture expert probability, dominant load, entropy, margin, total-variation and Jensen-Shannon metrics.
- Preserved empty-group cases as `INSUFFICIENT_TOKENS` and added tests proving missing metrics stay null.
- Separated token-pooled and equal-weight within-capture contrasts after the pooled MoT result exposed a
  composition effect; paired-capture evidence is the primary conclusion basis.
- Added archived ground-truth previews and an interactive annotation toggle to the demo.
- Re-ran the full five-family experiment, unit/lint suite, desktop interaction flow, mobile layout flow and
  independent SHA-256 verification.

## CPU resolution and flip diagnostics

- Added a committed, CPU-only protocol covering 64/128/256 inputs, identity/horizontal-flip transformations,
  three initialization seeds, four fixed images and all four MoT/MoA router layers.
- Restored every expert distribution to original-image pixels, re-normalized after interpolation and horizontally
  unflipped transformed observations before comparison.
- Added probability MAE/RMSE/max error, total variation, float64 Jensen-Shannon divergence, dominant-expert
  agreement, Top-1 margin context and explicit undefined handling for constant-map Pearson correlation.
- Added source-state, module-order, hook-output, repeat-inference, Top-K, normalization and hook-cleanup invariants.
- Added per-resolution ground-truth token coverage to quantify when coarse grids cannot support foreground versus
  background comparison.
- Generated 576 spatial captures, 1,440 raw arrays, 480 aligned comparisons and a compact visual overview.
- Increased the unit suite to 33 passing tests and independently rehashed all 22 formal evidence files.
- Corrected historical browser evidence wording: those passes used Playwright with installed Edge; they did not
  establish that the Codex Browser plugin was unavailable.

## CPU appearance sensitivity

- Added a committed 128px protocol for brightness ±10%, contrast ±10% and Gaussian blur 0.75 across three seeds,
  four images and all MoT/MoA router layers.
- Archived and hashed every transformed original and exact model-input canvas, including raw RGB-byte hashes.
- Added a fail-closed input-effect audit proving every perturbation changes every configured sample.
- Added margin-percentile agreement curves plus equal-weight summaries by transform, router module and seed.
- Added foreground/background sensitivity on the raw token grids while excluding letterbox padding.
- Generated 576 spatial captures, 1,536 raw arrays, 480 original-coordinate comparisons and 960 region comparisons.
- Expanded the unit suite to 38 passing tests and independently rehashed all 72 formal evidence files.
- Identified `model.16.m.0.router` as the highest-MAE MoA layer for every tested perturbation; kept this as a
  cold-start diagnostic rather than a learned-vulnerability claim.
