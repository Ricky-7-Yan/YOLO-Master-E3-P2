# Formal P2 experiment report

## Configuration

- Run: `p2-20260904-cpu-batch-diagnostics-v4`
- Tool source: `c2fb9cac3109fa44d64fd7289ef5e21d0159d7ed`, clean implementation paths
- Upstream runtime: `07d330325b5a26b75aabfc75389f9bcbc0d40245`
- Device: CPU; PyTorch reports CUDA unavailable
- Data: all four `coco8` validation images, fixed seed `0`, input size `64`
- Preprocess: aspect-preserving letterbox, RGB `/255.0`

## Quantitative result

| Check | MoT | MoA |
| --- | ---: | ---: |
| Routed modules | 4 | 4 |
| Images | 4 | 4 |
| Spatial captures | 16 | 16 |
| Observed grids | 2×2, 4×4, 8×8 | 2×2, 4×4, 8×8 |
| Max expert-sum error | 0 | `1.1920929e-07` |
| Hooked-vs-unhooked output max delta | 0 | 0 |
| Repeat weights/logits max delta | 0 | 0 |
| Repeat Top-K indices | identical | not applicable |
| Batch=2/4 probability max delta | 0 | 0 |
| Batch=2/4 logit max delta | 0 | `1.2369128e-10` |
| Batch=2/4 Top-K indices | identical | not applicable |
| Aggregate normalized entropy | `0.6056926` | `1.0` |
| Aggregate Top-1 margin | `0.04` | `3.3653527e-06` |
| Neighbor probability L1 mean | 0 | `2.5548041e-06` |

Combined output contains 32 capture records, 144 raw NPZ arrays, four archived original inputs and 192 selectable
views. The 64 single-versus-batch router-record comparisons cover batch sizes 2 and 4 across both families. Every
demo asset exists, has a unique path and matches its original image dimensions. The manifest contains 211 files
and independently rehashes with zero mismatches. End-to-end generation took 32.45 seconds on this machine; that
duration is an operational observation, not a performance benchmark.

MoT assigns every one of the aggregated 400 feature tokens to expert 0 in the dominant view, with zero neighboring
probability variation. MoA's dominant fractions are `55.25% / 14.75% / 30.00%`, but its entropy is 1.0 and routing
margin is only `3.37e-06`. The discrete regions therefore reflect argmax amplification of near-ties, not learned
semantic expert roles.

## Browser demo validation

The tested desktop flow was: load `demo.html` -> select MoA -> sample 2 -> `model.16.m.0.router` -> normalized
entropy -> display the 381×500 original and overlay together -> verify three statistic cards -> copy evidence
metadata -> confirm the export path. The mobile flow selected MoT Top-1 margin at 390×844. Both passed in installed
Microsoft Edge through Playwright: page identity and content were correct, five feasibility cards rendered, paired
assets loaded at equal natural dimensions, mobile horizontal overflow was absent, and no console warning, error or
HTTP 4xx/5xx response occurred.

## Verdict

P2 passes the implemented acceptance contract: two families provide truthful original-image token overlays, the
additional MoA family extends P0's model coverage, all five mixture families receive an explicit runtime decision,
and the demo is command-started, interactive and exportable. The result is an engineering/diagnostic validation,
not a learned-routing quality result.
