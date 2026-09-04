# Formal P2 experiment report

## Configuration

- Run: `p2-20260904-cpu-five-family-v3`
- Tool source: `d8a1b5ffdb5bfea9607e5f363c760574c79bb1ed`, clean implementation paths
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

Combined output contains 32 capture records, 80 raw NPZ arrays and 128 selectable images. The evidence manifest
contains 142 files and independently rehashes with zero mismatches. End-to-end generation took 43.30 seconds on
this machine; that duration is an operational observation, not a performance benchmark.

## Browser demo validation

The tested flow was: load `demo.html` -> select MoA -> select coco8 sample 2 -> select
`model.16.m.0.router` -> select expert 2/global -> render the correct original-size asset and expose the same path
for export. It passed in installed Microsoft Edge through Playwright at 1440×1000 and 390×844. Page title and
meaningful content were correct, five feasibility cards rendered, the selected PNG had natural size 381×500,
mobile horizontal overflow was absent, and the console contained no errors or warnings.

## Verdict

P2 passes the implemented acceptance contract: two families provide truthful original-image token overlays, the
additional MoA family extends P0's model coverage, all five mixture families receive an explicit runtime decision,
and the demo is command-started, interactive and exportable. The result is an engineering/diagnostic validation,
not a learned-routing quality result.

