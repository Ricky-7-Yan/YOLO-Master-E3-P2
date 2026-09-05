# P2 requirement and acceptance mapping

## Scope

The E3 P2 requirement is interpreted as three testable outcomes:

1. overlay token routing heatmaps on the original image;
2. provide a command-started demo that can show sample, layer and expert selection within two minutes;
3. extend coverage beyond the P0 MoE/MoT/Latent set without hiding unsupported semantics.

The implementation runs against YOLO-Master runtime ref
`07d330325b5a26b75aabfc75389f9bcbc0d40245`, tree
`e4a900338bd6679d5ad9f8673e466b250ba2c711`. Nine relevant source/config files are SHA-256 pinned before a run.

## Acceptance matrix

| Requirement | Hard check | Formal evidence | Result |
| --- | --- | --- | --- |
| Real token route source | Require finite normalized `[B,E,H,W]`, with `H>1,W>1` | `spatial-captures.json` | PASS |
| Original-image alignment | Exact recorded letterbox resize, integer unpad, original-size restore | `input.json`, geometry tests | PASS |
| MoT sparse consistency | Selected mass is one; unselected probability is zero; indices in range | per-capture validation | PASS |
| Non-invasive collection | Compare full model tensors with/without hook | MoT/MoA max abs delta `0` | PASS |
| Repeatability | Repeat weights/logits exactly; MoT indices exactly | `family-feasibility.json` | PASS |
| Batch/sample identity | Compare every batch=2/4 router record against its single-image source | 64 comparisons; max probability delta `0` | PASS |
| Uncertainty is not visual guesswork | Fixed-scale normalized entropy and Top-1 margin derived from raw probabilities | `spatial-diagnostics.json`, raw NPZ | PASS |
| More families | Runtime audit MoE, MoT, Latent, MoA, MoLoRA | `family-feasibility.json` | PASS |
| Honest unsupported path | Singleton or absent spatial axes must fail closed | code + negative tests | PASS |
| Two-minute demo | One command; paired original/overlay; select sample/layer/view; copy metadata; export PNG | `demo.html`, `demo-smoke.json` | PASS |
| Reproducible evidence | Config, command, input hashes, environment, source hashes, full log, manifest | formal run directory | PASS |
| Image-level scaling | Select 32/128 images without reading content, labels or model output | `input.json`, selection tests | PASS |
| Cross-image layer ranking | Complete image×seed×transform matrices plus per-image and leave-one-out ranks | `image-level-attribution.json` | PASS |
| Image-level uncertainty | Bootstrap image aggregates, never repeated tokens, with fixed seeds and 10,000 draws | attribution/switch JSON | PASS |
| Dataset edge cases | Retain and label hash-selected missing-label records; never replace after selection | archived input ledger | PASS |
| Non-confounded association | Analyze input/routing changes within each transform using image units | image-driver association ledger | PASS |
| Result-independent verdict | Correlation sign and magnitude are not PASS criteria; mixed results retained | protocol and result report | PASS |

## Non-goals

- No upstream pull request is created.
- No model forward implementation is modified to manufacture visualization state.
- No claim is made about trained specialization, detector accuracy, CUDA behavior or GPU performance.
- MoE/Latent/MoLoRA are not interpolated into image heatmaps when their runtime contract has no token grid.
