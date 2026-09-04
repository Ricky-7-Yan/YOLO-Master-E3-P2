# Five-family token-overlay feasibility audit

## Decision table

| Family | Source/runtime observation | Spatial semantics | P2 decision |
| --- | --- | --- | --- |
| MoT | `_MoTRouter` returns probabilities/logits `[B,3,H,W]` and Top-K indices `[B,K,H,W]` | token routing | supported |
| MoA | `_MoARouter` returns probabilities/logits `[B,3,H,W]` | token routing over attention groups | supported |
| MoE | 12 full-detector nested routers returned `[1,2]` Top-K tensors | one decision per image/sample | unsupported |
| Latent | three full-detector modules exposed `[1,4]`, `routing_axis=expert` | pooled expert decision | unsupported |
| MoLoRA | official linear, spatial and hybrid router probes all returned `[1,4]` from `[1,16,8,8]` | spatial features are pooled before the returned decision | unsupported |

## Why `SpatialRouter` in MoLoRA is still unsupported

The name describes how features are processed, not the granularity of the returned route. Its official forward path
computes `[B,E,H,W]` intermediate logits and then averages the two spatial dimensions, returning `[B,E]`. P2 uses
the returned routing contract, so it does not hook an internal convolution and present pre-pooling activations as
the actual expert assignment.

## Full-model evidence versus isolated evidence

- MoT, MoA, MoE and Latent are audited through complete YOLO detector forwards using their shipped YAMLs.
- MoLoRA is a post-construction PEFT injection system rather than a standalone detector YAML in this source
  snapshot. Its three official router classes are therefore tested directly and labelled
  `isolated_official_router_contract`; the report does not describe this as a full-model run.

## Random-initialization observation

MoT maps are spatially constant in all 16 captures. Across MoA's 16 captures, the largest within-expert spatial
range is only `4.0948391e-05`; probabilities stay between `0.33330452` and `0.33335134`. These are expected
near-uniform cold-start results, not evidence of expert specialization. The value of this run is the verified
capture/mapping mechanism and the explicit feasibility boundary.

The strengthened diagnostics quantify that boundary. Across 400 aggregated feature tokens per family, MoT has
normalized entropy `0.6056926`, Top-1 margin `0.04` and zero neighboring-token variation; its dominant expert owns
all 400 tokens. MoA has entropy `1.0`, margin `3.365e-06` and neighboring-token variation `2.555e-06`. Although its
argmax view splits tokens `221 / 59 / 120`, those regions are near-tie discretization, not semantic specialization.
