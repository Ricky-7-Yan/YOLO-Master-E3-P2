# Gaussian-blur held-middle residual protocol

## Question

The held-middle analysis found a larger span-normalized probability interpolation error for Gaussian blur than
for brightness or contrast. Before calculating input-feature associations, this protocol fixes a narrow follow-up:
within the same 32 selected images, are blur residual ranks associated with three model-output-independent image
properties?

This is a retrospective diagnostic of an existing random-initialization evidence bundle. It is not a prospective
validation, mechanism intervention, trained-checkpoint result or accuracy analysis.

## Locked parents and analysis unit

- Held-middle parent: exact manifest of `p2h-20260907-dose-holdout-v1`
- Image source: exact manifest of `p2q-20260906-dose-response-v1`
- Selected image-and-label set digest:
  `80020696759bd2b6a6e68bb645c9c748e90c4b6425489563a746f72fbd161c4f`
- Family: Gaussian blur only
- Endpoint: span-normalized absolute held-middle `probability_mae` residual
- Unit: one selected image; 32 observations, with no token or seed pseudo-replication

## Three predeclared input-only features

The order and definitions below are fixed before association values are calculated.

1. `letterbox_content_fraction`: scaled source-image area divided by the 128×128 square canvas area. It captures
   padding/aspect-ratio exposure without labels or model output.
2. `luminance_mean_0_255`: source RGB converted with `0.299R + 0.587G + 0.114B`, then averaged over all pixels.
3. `edge_total_variation_0_1`: the average of horizontal and vertical absolute luminance differences, divided by
   255. This continuous texture proxy avoids choosing an edge threshold after seeing residuals.

Ground-truth box count and label availability may be copied into records for provenance, but they are explicitly
descriptive and are not inferential predictors in this protocol.

## Inference and multiplicity

- Primary coefficient: two-sided, tie-aware Spearman rank correlation for each feature versus residual.
- Uncertainty: 10,000 complete-image bootstrap resamples; an interval is emitted only when at least 95% of draws
  are defined.
- Randomization test: 20,000 fixed-seed permutations of residual assignments, using the finite-sample
  `(exceedances + 1) / (defined draws + 1)` two-sided p-value.
- Multiplicity: Holm adjustment across exactly the three predeclared tests at family-wise alpha 0.05.
- Influence check: all 32 leave-one-image-out coefficients, including undefined states and sign stability.
- Predictor collinearity: the three pairwise Spearman coefficients are descriptive, not additional tests.
- The six highest-residual images are displayed descriptively; their rank does not create new hypothesis tests.

No feature may be added, removed or renamed after results are observed under this run ID. A changed protocol must
use a new run ID.

## PASS gates

PASS requires both parent manifests and the selected-set digest to match, source images to match their recorded
SHA-256 values, the exact 32-image matrix, finite features/residuals, complete predeclared statistics, evidence
within the byte budget and a complete SHA-256 manifest. Association direction, p-values and Holm rejections are
observations and never PASS criteria.

## Interpretation boundary

A positive or negative association would prioritize a follow-up transformation or stratification; it would not
prove that the feature causes route interpolation error. A null result would also be useful: these three simple
input properties would then fail to explain the blur gap on this subset, and more features must not be mined under
the same confirmatory label.
