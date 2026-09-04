# Strengthened P2 validation protocol

This protocol strengthens the original P2 acceptance contract without changing its interpretation boundary.
The run still validates an engineering and diagnostic pipeline on randomly initialized models; it does not claim
learned expert specialization or detection accuracy.

## 1. Sample identity under batching

The original-image overlay is only trustworthy if batch position `b` remains paired with the same input image.
For each supported family, the formal run therefore captures every image individually and again at batch sizes 2
and 4 using the same frozen model state.

For every sample and router module:

- probability and logit shapes must match;
- maximum single-versus-batch absolute difference must be at most `1e-5`;
- MoT Top-K indices must be exactly identical;
- all temporary hooks must be removed.

Any mismatch fails the run instead of silently producing a possibly misregistered overlay.

## 2. Absolute-scale uncertainty views

Each real `[E,H,W]` probability grid produces two additional token diagnostics:

- normalized routing entropy: `-sum(p * log(p)) / log(E)`;
- Top-1 routing margin: largest expert probability minus the second largest.

Both quantities have a fixed `[0,1]` meaning. The renderer never applies per-image min-max normalization. Entropy
near 1 and margin near 0 indicate an uncertain or near-uniform router; low entropy and high margin indicate a more
decisive route. These views are descriptive and cannot by themselves establish semantic specialization.

## 3. Traceable input-to-overlay pair

The evidence package stores a byte-identical copy of each selected coco8 input. Every demo entry references both
its original input and rendered overlay. Before the run may report PASS, the generator checks that:

- every referenced original and overlay exists;
- overlay paths are unique;
- every overlay has exactly the original image width and height;
- raw arrays, per-capture diagnostics and demo metadata remain available separately from PNGs.

## 4. Formal expected coverage

With four coco8 validation images, four routed modules in MoT and four in MoA, the expected formal coverage is:

| Evidence | Expected minimum |
| --- | ---: |
| True spatial captures | 32 |
| Single-versus-batch sample comparisons | 64 per family across batch sizes 2 and 4 |
| Raw arrays | 144 |
| Demo views | 192 |
| Archived original inputs | 4 |

The exact counts, source fingerprints, environment and validation deltas are machine-readable in `summary.json`,
`family-feasibility.json`, `spatial-captures.json`, `spatial-diagnostics.json` and the SHA-256 manifest.

## 5. Browser acceptance

The two-minute demo must pass a rendered-browser flow:

`load -> five-family matrix -> choose family/sample/layer -> choose probability/entropy/margin -> original and overlay update together -> export points to the rendered asset`.

Desktop and mobile checks cover page identity, meaningful content, missing assets, console errors or warnings,
horizontal overflow and at least one complete interaction path.
