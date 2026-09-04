# Formal P2 experiment report

## Configuration

- Run: `p2-20260904-cpu-region-analysis-v7`
- Tool source: `3b4ab528428d836d6bf45682d0f5048aeb6374b7`, clean implementation paths
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

Combined output contains 32 capture records, 240 raw NPZ arrays, four archived images, four label files, four
ground-truth previews and 192 selectable views. The 64 single-versus-batch router-record comparisons cover batch
sizes 2 and 4 across both families. Every demo asset exists, has a unique path and matches its original image
dimensions. The final manifest contains 220 files and independently rehashes with zero mismatches. End-to-end
generation took 25.32 seconds on this machine; that duration is an operational observation, not a performance
benchmark.

MoT assigns every one of the aggregated 400 feature tokens to expert 0 in the dominant view, with zero neighboring
probability variation. MoA's dominant fractions are `55.25% / 14.75% / 30.00%`, but its entropy is 1.0 and routing
margin is only `3.37e-06`. The discrete regions therefore reflect argmax amplification of near-ties, not learned
semantic expert roles.

## Ground-truth region result

Each family contributes 400 grid tokens: 103 foreground, 201 valid background and 96 padding tokens. Padding is
excluded. Eleven of sixteen captures per family contain both foreground and background tokens; five are marked
`INSUFFICIENT_TOKENS`, primarily because a coarse grid can miss small boxes or a large box can cover every valid
cell center.

| Equal-weight paired-capture metric | MoT | MoA |
| --- | ---: | ---: |
| Supported captures | 11 | 11 |
| Mean foreground/background TV | 0 | `1.1595813e-06` |
| Maximum foreground/background TV | 0 | `6.3478947e-06` |
| Mean Jensen-Shannon divergence (nats) | 0 | `3.2067748e-12` |
| Mean entropy difference | `1.6255812e-08` | 0 |
| Mean Top-1 margin difference | 0 | `-3.5235719e-07` |

The paired result is the primary comparison and shows no meaningful cold-start region separation. The pooled MoT
TV is `0.0030913`, despite every supported within-capture TV being zero, because different router layers contribute
different region token counts and baseline distributions. It is retained as evidence that pooled-only analysis
can manufacture an apparent foreground/background effect.

## Browser demo validation

The tested desktop flow was: load `demo.html` -> select MoA -> sample 2 -> `model.16.m.0.router` -> normalized
entropy -> enable archived ground-truth boxes -> display the 381×500 original and overlay together -> verify six
statistic cards -> copy evidence metadata -> confirm the export path. The mobile flow selected MoT Top-1 margin at
390×844 and enabled ground-truth boxes. Both passed in installed
Microsoft Edge through Playwright: page identity and content were correct, five feasibility cards rendered, paired
assets loaded at equal natural dimensions, the annotation toggle changed the source image, mobile horizontal
overflow was absent, and no console warning, error or HTTP 4xx/5xx response occurred.

## Verdict

P2 passes the implemented acceptance contract: two families provide truthful original-image token overlays, the
additional MoA family extends P0's model coverage, all five mixture families receive an explicit runtime decision,
and the demo is command-started, interactive and exportable. The result is an engineering/diagnostic validation,
not a learned-routing quality result.
