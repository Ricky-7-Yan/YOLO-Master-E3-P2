# Coco128 image-level scaling protocol

## Purpose

The four-image appearance run and its layer drill-down identify `model.16.m.0.router` as the largest-response
MoA layer, but repeated pixels and tokens are not independent evidence that the ranking persists across images.
This CPU protocol expands the image unit and asks whether the target ranking survives image stratification,
leave-one-image-out analysis and image-level bootstrap resampling.

This remains a random-initialization mechanism study. It does not measure detector accuracy or learned routing
robustness.

## Locked design

- Dataset: standard `coco128.yaml`, exactly 128 images in the declared split
- Selection: 32 unique images, sorted by
  `SHA-256("e3-p2-coco128-image-v1" + NUL + unique_filename)` and taking the first 32
- Device/resolution: CPU, 128px
- Seeds: 0, 1 and 2
- Family/layers: MoA, all four returned spatial routers
- Target layer: `model.16.m.0.router`
- Conditions: identity, brightness 0.9, contrast 0.9 and Gaussian blur 0.75
- Bootstrap: 10,000 deterministic image-resampling draws per transform
- Evidence budget: at most 64 MiB before the manifest

The hash selection is path-independent, does not inspect image content, labels or model results, and is recorded
with original sorted-dataset indices. Every selected original and each present label are archived with SHA-256. All 128×128
model-input canvases are hashed as raw RGB bytes; candidates must change every selected identity canvas.

If a hash-selected image has no dataset label file, it remains selected and is recorded as
`MISSING_DATASET_LABEL`; no replacement image is chosen. Labels are not used for this study's image ranking or
switch metrics, and the padding mask depends only on recorded letterbox geometry.

Three perturbations represent the strongest, middle and weakest appearance families from the preceding run while
keeping CPU and evidence budgets bounded. This protocol does not compare positive and negative strength
directions.

## Measurements

1. Capture all four MoA router probability grids for each seed, image and condition.
2. Restore each expert distribution to original-image coordinates and re-normalize expert sums.
3. Compute probability MAE and the existing continuous/discrete stability metrics for each candidate condition.
4. Rank layers for every image×seed×transform case and after averaging seeds within each image×transform.
5. Average seeds and transforms within each image, keeping 32 image units for the overall target ranking.
6. For every transform, omit each image once and recompute layer ranking over the remaining 31 images.
7. Resample the 32 image-level layer vectors 10,000 times and report a percentile interval for the target share.
8. At the raw target grid, exclude padding and summarize switch rate per image across seeds; bootstrap images, not
   tokens. Retain token margin deciles only as descriptive localization.

The target share is its image-mean MAE divided by the sum of the four layer image-mean MAEs. It is a relative
diagnostic, not a causal contribution or accuracy effect.

## Pass contract

PASS requires exact upstream source fingerprints, clean committed tooling, a 128-image dataset count, complete
32×3×3×4 comparison coverage, real input effects for every image, invariant router order, exact repeated capture,
zero hook impact on detector output, valid probability restoration, complete image-level matrices, successful
leave-one-out/bootstrap calculations and evidence below the 64 MiB limit. Every retained file must be covered by
a new SHA-256 manifest.
