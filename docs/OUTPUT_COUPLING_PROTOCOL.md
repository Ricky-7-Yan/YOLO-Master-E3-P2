# Router-to-detector-output association protocol

## Question

The dose-response run shows monotone target-router change as appearance strength increases. This protocol asks a
separate end-to-end question: across images under one high-strength transformation, is larger target-router
probability change associated with larger detector-head score change?

The analysis is observational and the model is randomly initialized. It does not establish that the router causes
the detector change, that detections are correct, or that accuracy changes.

## Locked design

- Same 32 deterministic coco128 images, seeds 0/1/2, CPU, 128px and MoA target `model.16.m.0.router`
- Conditions: brightness 0.8, contrast 0.8 and Gaussian blur 1.5, each compared with identity
- Primary detector endpoint: mean absolute change of `one2one.scores`, retaining its fixed grid/channel order
- Secondary detector evidence: `one2one.boxes`, `one2many.scores`, `one2many.boxes` and decoded Top-300 tensors
- Primary router predictor: raw-grid target probability MAE; secondary predictor: dominant-expert switch fraction
- Unit: image after equal averaging over three seeds
- Statistic: within-transform tie-aware Spearman, 10,000 image bootstrap draws and leave-one-image-out checks

Decoded Top-300 row order can change after score sorting, so decoded output is archived but never used as the
primary aligned endpoint. Transformations are analyzed separately and never pooled.

## Pass contract

PASS requires clean committed tooling, exact source fingerprints, complete 32×3×3 detector/router comparison
coverage, fixed detector tensor keys and shapes, finite values, unchanged hook invariants, image-level aggregation,
all predeclared associations regardless of sign, evidence below 64 MiB and an exact SHA-256 manifest.

Correlation magnitude and direction are not pass criteria. Weak or mixed results must remain visible.
If either vector is constant, the association is archived as undefined with its unique-value counts; no endpoint
substitution, epsilon injection or fabricated zero correlation is permitted. The predeclared primary remains primary
even if a secondary endpoint is the only one with measurable variation.
