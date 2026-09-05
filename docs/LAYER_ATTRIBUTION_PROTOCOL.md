# Model.16 layer-attribution protocol

## Question and scope

The formal CPU appearance run found `model.16.m.0.router` to have the largest mean MoA probability MAE for
every tested perturbation. This protocol tests whether that ranking survives seed stratification and whether
dominant-expert switches concentrate in low-margin target-layer tokens. It is a post-hoc mechanism analysis of
the already locked evidence, not a new model run and not a trained-robustness benchmark.

## Locked parent evidence

- Parent run: `p2a-20260905-cpu-appearance-v2`
- Parent manifest SHA-256: `7df8fbaf1d10d61d268559ff688cc81a67ab5c3e428b8deb45f1ea2904dd5d21`
- Family: MoA
- Target: `model.16.m.0.router`
- Perturbations: brightness 0.9/1.1, contrast 0.9/1.1 and Gaussian blur 0.75
- Parent coverage: three seeds, four images and four router layers at 128px

Before analysis, every parent file must match the manifest by exact path set, byte count and SHA-256. The run
also checks the parent summary identity and PASS status. A modified, missing or additional parent file aborts the
analysis.

## Predeclared measurements

### Layer ranking

For each perturbation and router layer, average original-coordinate probability MAE equally across the 12
seed-image comparisons. Rank the four layers by this mean. The target share is its mean divided by the sum of the
four layer means. This share is descriptive and must not be presented as a causal decomposition.

Repeat the ranking separately for each of the 15 perturbation-seed groups, averaging equally across the four
images. Report how often the target ranks first; do not hide an unfavorable seed.

### Margin-conditioned switches

At the raw target-layer grid, exclude letterbox-padding tokens using the archived mask. For every valid token,
compute the identity Top-1 minus Top-2 expert-probability margin and whether the perturbation changes the dominant
expert. Pool token-comparison exposures across the declared scope and partition them exactly once using ten
empirical-quantile bins. Report counts and switch fractions for all bins, including empty bins if tied edges make
one occur.

The identity margin appears once per candidate perturbation because the analysis unit is a token-comparison
exposure. This is deliberate and stated in the machine-readable output. Case-level summaries remain separate so
the pooled curve is not confused with an image-level uncertainty estimate.

### Visual cases

Select one worst case per perturbation by maximum valid-token switch fraction, then MAE, then lowest seed and
sample index. Each figure shows the exact identity/candidate 128px inputs, both categorical expert maps, the
binary switch mask and the within-case identity-margin rank. Token maps use nearest-neighbor enlargement; gray
means padding. These panels localize evidence and do not imply pixel-level detector explanations.

## Pass contract

A PASS requires all of the following:

1. exact parent manifest verification;
2. all five declared perturbations and four layers present;
3. the target present in every transform and seed stratum;
4. raw reference/candidate weights and padding masks with matching geometry;
5. mutually exclusive margin bins covering every valid token-comparison exposure once;
6. deterministic worst-case selection, machine-readable records, figures and a new SHA-256 manifest;
7. a committed, clean analysis implementation at run start.

PASS means the evidence lineage and calculations completed under this contract. It does not mean the target is
causally responsible for detector behavior, that the model is trained, or that the finding generalizes beyond
the four images and mild perturbations.
