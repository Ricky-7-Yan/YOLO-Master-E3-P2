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
