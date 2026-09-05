# Limitations and safe interpretation

- No compatible trained MoT/MoA checkpoint was used. Random-init patterns must not be described as learned
  specialization, semantic attention or accuracy improvement.
- The base visualization run uses input size 64 and four coco8 validation images. The stability extension adds
  128/256 inputs and three initialization seeds, but remains a small CPU mechanism study rather than a population
  estimate of routing behavior.
- Foreground membership uses the feature-cell center inside any ground-truth box. Coarse 2×2 or 4×4 grids can miss
  small objects or contain only foreground; those captures are marked `INSUFFICIENT_TOKENS`.
- Multiple layers from the same four images are not independent statistical samples. Paired-capture contrasts are
  descriptive; no confidence interval or population-level conclusion is claimed.
- Batch sizes 2 and 4 validate sample identity for the selected four images, but do not substitute for a varied
  training dataloader, multi-worker ordering or distributed-rank validation.
- MoE, Latent and MoLoRA do not expose reversible token-to-image assignments in the audited runtime contracts.
  Their `UNSUPPORTED` result is intentional and prevents deceptive visualization.
- MoLoRA was tested at its official router contract, not after injection into a complete detector; the evidence
  labels this distinction.
- Bilinear restoration makes a low-resolution routing field viewable but does not increase its information content.
  The UI always displays the source grid shape.
- CPU results do not establish CUDA correctness, GPU overhead, memory cost or full-training performance.
- Horizontal-flip and resolution comparisons cover only two perturbation families. They do not establish
  robustness to color, blur, crop, scale distribution shift or adversarial changes.
- The appearance extension adds mild brightness, contrast and blur, but uses one strength per direction and only
  four images. It is a controlled sensitivity probe, not a corruption benchmark.
- MoA's cold-start probabilities are nearly tied. Dominant-expert agreement is therefore interpreted together
  with probability error and Top-1 margin, never as a stand-alone robustness score.
- Foreground/background appearance differences change direction across perturbations and remain extremely small;
  no semantic region-sensitivity conclusion is supported.
- The layer-attribution extension reuses the same four-image appearance run. Its 11,520 token-comparison
  exposures are repeated measurements, not independent data points or a population sample.
- The target-layer share is normalized by the sum of four descriptive mean MAEs. It localizes the observed
  numerical response but does not establish a causal layer contribution to detection output.
- The image-level extension increases the image unit to 32 deterministic coco128 samples, but it is still a
  fixed subset of a small training split under random initialization. It is not a random population sample, a
  corruption benchmark or evidence of learned detector generalization.
- Image bootstrap intervals quantify heterogeneity under resampling of the 32 selected images. They must not be
  reported as model-accuracy confidence intervals or as guarantees for the full COCO distribution.
- Two hash-selected coco128 images have no label file. They were retained rather than silently replaced and are
  treated as empty-box records only because labels are not used by the padding-only image-level analysis.
- The scaled run covers brightness 0.9, contrast 0.9 and blur 0.75 at one resolution. It does not establish a
  monotone dose-response relationship or behavior under positive perturbation directions.
- RGB MAE is a pixel-distance proxy, not a perceptual severity scale shared by brightness, contrast and blur.
  The association analysis therefore keeps transforms separate and forbids a pooled correlation.
- A positive input-change/probability-MAE rank association does not establish that pixel distance causes routing
  change or that either quantity changes detector predictions. Image content can affect both quantities.
- Dominant-expert switch rate is a thresholded `argmax` outcome under near-tied random-init probabilities. Its
  mixed correlations must not be used to contradict or replace the continuous probability analysis.
- The strength ladder contains only three darker/lower-contrast levels and three Gaussian blur radii. It does not
  cover brightening, contrast amplification, other corruptions, intermediate hold-out levels or a standard
  perceptual severity calibration. Monotonicity describes only these predeclared values.
- All dose-response intervals resample the same fixed 32-image subset. They describe within-subset heterogeneity,
  not a population dose curve or model-accuracy uncertainty.
- In the output-coupling run, randomly initialized classification scores and decoded Top-300 tensors were exactly
  unchanged for all comparisons. Their correlations are undefined; this run cannot support a classification-
  output or prediction-list coupling claim.
- Box-tensor changes are finite but extremely small and one-to-one/one-to-many boxes are numerically identical in
  the audited eval return. Their strong rank associations are descriptive numerical coupling, not independent
  replication, causal mediation, detection correctness or accuracy impact.
- The demo was rendered in Microsoft Edge at 1440×1000 and 390×844. Other browsers and assistive
  technology were not exhaustively tested.
