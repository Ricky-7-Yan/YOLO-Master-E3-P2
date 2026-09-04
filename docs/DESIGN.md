# Design: spatial truth before visual polish

## Data path

```text
coco8 image
  -> deterministic letterbox + recorded geometry
  -> unchanged YOLO-Master detector forward
  -> temporary hook on _MoTRouter / _MoARouter
  -> detached CPU weights, logits and optional Top-K indices
  -> semantic and repeatability gates
  -> exact unpad + original-size mapping
  -> fixed-scale probability / categorical dominant-expert overlays
  -> immutable JSON/NPZ/PNG evidence + local demo
```

The hook is attached to the router child rather than the block snapshot because the public block snapshot averages
over batch and spatial axes. Capturing at the child preserves the real `[B,E,H,W]` tensor while leaving the model
forward signature and return value unchanged. Every hook is removed in `finally`.

## Feasibility gate

An output is eligible for original-image overlay only if all conditions hold:

- it has exactly four axes interpreted as `[batch, expert, height, width]`;
- both spatial axes are larger than one;
- all values are finite and non-negative;
- probabilities sum to one across experts within `1e-5`;
- logits and probability grids align;
- for MoT, Top-K indices have the same token grid, are in range and select all nonzero routing mass.

This gate prevents `[B,E]` and `[B,E,1,1]` image decisions from being enlarged into fake token maps.

## Coordinate mapping

The input transform records original width/height, resized width/height, four integer paddings and the floating
scale. A feature map is bilinearly resized into the square network-input coordinate system, cropped with the exact
recorded padding, then resized to the original image dimensions. Odd padding is represented asymmetrically instead
of being recomputed from a rounded ratio.

Probability overlays use raw probability on a fixed `[0,1]` scale; no per-image min-max normalization is used.
This avoids exaggerating tiny random-init differences. The dominant view uses `argmax` at the feature-grid level,
then maps one-hot expert planes through the same geometry before recoloring.

## Reproducibility and tamper evidence

The formal run refuses uncommitted changes under implementation paths. It records source commit
`d8a1b5ffdb5bfea9607e5f363c760574c79bb1ed`, validates nine upstream SHA-256 fingerprints and writes raw arrays
before derived views. The manifest hashes every evidence file by raw bytes; `.gitattributes` disables text
normalization under `artifacts/**` so a Windows clone does not silently invalidate those hashes.

## Demo boundary

The demo is a static consumer of `demo-index.json`; it cannot modify model state. The standard-library server binds
to `127.0.0.1` by default. Only supported families appear in overlay selectors, while the five-family decision cards
remain visible so unsupported cases are part of the result rather than silently omitted.

