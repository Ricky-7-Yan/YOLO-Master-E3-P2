# Ground-truth region routing protocol

## Question

Do spatial routers assign measurably different expert distributions to annotated-object tokens and valid
background tokens? This protocol makes that comparison reproducible without claiming that a randomly
initialized model has learned specialization.

## Inputs and provenance

- The image subset is fixed by `dataset`, `dataset_split`, and `sample_indices` in `configs/p2.yaml`.
- Every selected image and YOLO detection label file is SHA-256 hashed and archived inside the run.
- Normalized YOLO boxes are parsed strictly as `class cx cy width height`; malformed or out-of-range rows fail
  the run instead of being clipped silently.
- The model source and nine routing/config files remain fingerprint-locked to the declared upstream snapshot.

## Token assignment

For a router grid `[E,H,W]`, each spatial cell is represented by its center in the square model input. The exact
recorded integer letterbox transform maps each ground-truth box from original-image coordinates into that input.
The horizontal and vertical factors use the realized resized dimensions, not the pre-rounding nominal scale.

- `foreground`: the center lies inside at least one ground-truth box and inside the resized image area.
- `background`: the center lies inside the resized image area but outside every ground-truth box.
- `padding`: the center lies in letterbox padding; it is excluded from both comparison groups.

This center rule is deterministic and avoids manufacturing pixel-level precision from coarse feature cells. It
also prevents aspect-ratio padding from being counted as image background. Boolean foreground, background and
padding masks are stored alongside every raw routing tensor.

## Reported measurements

For each sample and router module, the run records foreground/background token counts, mean expert probability,
dominant-expert counts and fractions, normalized entropy, and Top-1 margin. The contrast contains:

- per-expert foreground-minus-background mean probability;
- total-variation distance, `0.5 * sum(abs(p_fg - p_bg))`;
- Jensen-Shannon divergence in natural-log units;
- foreground-minus-background normalized entropy and Top-1 margin.

Family and module region summaries are token weighted. Their `pooled_contrast` compares the pooled foreground and
background distributions. A separate `paired_capture_contrast` gives each capture containing both groups equal
weight and reports mean/min/max, so pooled token imbalance is visible rather than hidden. Captures sharing an
image are not treated as statistically independent replicates. A capture with no foreground or no valid
background token is labelled `INSUFFICIENT_TOKENS`; missing measurements remain `null` instead of being replaced
with zero.

The paired-capture result is the primary descriptive comparison. The pooled contrast is diagnostic only: when
router layers have different baseline distributions and different foreground/background token availability,
pooling can create an apparent region difference even though every within-capture difference is zero.

## Interpretation and acceptance

The current run is an instrumentation baseline because the repository has no compatible trained MoT/MoA
checkpoint. Acceptance therefore concerns data lineage and analysis correctness: strict labels, exact partition
of every grid, stored masks, finite routing probabilities, explicit empty-group handling, reproducible aggregation,
and an inspectable original/ground-truth toggle in the demo.

After a compatible checkpoint is available, the identical pipeline can compare trained and initialization
baselines. Only then, with a larger validation set and uncertainty estimates, should region-specific expert
behavior be interpreted as learned specialization.
