# CPU resolution and horizontal-flip results

## Formal run

- Run: `p2r-20260905-cpu-resolution-flip-v4`
- Tool source: `bdc47a698b28dff87d1e5086755e3374485baeee`, clean implementation paths
- Upstream runtime: `07d330325b5a26b75aabfc75389f9bcbc0d40245`; four source fingerprints matched
- Device: CPU
- Data: all four `coco8` validation images and their 17 boxes
- Design: seeds 0/1/2, input sizes 64/128/256, identity plus horizontal flip, four router layers per family
- Output: 576 captures, 1,440 raw arrays and 480 aligned comparisons

Every family/seed representative passed exact hooked-versus-unhooked output comparison, exact repeat weights and
logits, stable router-module order and hook cleanup. MoT Top-K indices also repeated exactly. The largest restored
expert-sum error was `2.3841858e-07` before explicit normalization and `1.1920929e-07` after it. The 22-file
manifest independently rehashed with zero mismatches. The run took 86.02 seconds on this machine; this is an
operational observation, not a benchmark.

## Aligned MoA comparisons

| Comparison | Mean probability MAE | Mean JS (nats) | Mean dominant agreement | Reference mean Top-1 margin |
| --- | ---: | ---: | ---: | ---: |
| Horizontal flip, 64 | `6.86e-07` | `6.02e-12` | `65.96%` | `7.31e-07` |
| Horizontal flip, 128 | `5.27e-07` | `3.81e-12` | `75.55%` | `7.52e-07` |
| Horizontal flip, 256 | `4.36e-07` | `2.95e-12` | `80.56%` | `7.85e-07` |
| 128 versus 64 | `3.79e-07` | `1.34e-12` | `76.86%` | `7.31e-07` |
| 256 versus 64 | `5.23e-07` | `2.68e-12` | `70.29%` | `7.31e-07` |

The probabilities change only at roughly the same scale as the cold-start Top-1 margin. Consequently, a very
small continuous change can alter the discrete expert with the largest probability. The lowest individual
agreement was `18.90%` at seed 0, sample 0, `model.16.m.0.router`, horizontal flip at 64 pixels; its probability
MAE was still only `4.68e-06`. This is evidence of near-tie `argmax` sensitivity, not a large probability-distribution
shift. Pearson is retained as a secondary shape diagnostic because 23–28 of 144 expert-map pairs per group were
constant and therefore undefined.

## MoT boundary

All MoT resolution and flip comparisons had zero MAE/JS and 100% dominant agreement. However, the observed
cold-start maps were spatially constant. Each aggregate group therefore contains 0 defined and 144 undefined
Pearson correlations. The correct conclusion is that this initialization path produced identical constant maps;
it is not evidence that a trained MoT is robust.

## Ground-truth token coverage

| Input | Captures per family | Supported | Insufficient | Foreground tokens | Valid background | Padding |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 64 | 16 | 11 | 5 | 103 | 201 | 96 |
| 128 | 16 | 16 | 0 | 409 | 799 | 392 |
| 256 | 16 | 16 | 0 | 1,621 | 3,179 | 1,600 |

The counts are identical for MoT and MoA because both expose the same four grid scales under these configs. Moving
from 64 to 128 removes every empty foreground/background case for the selected images. This supports using at
least 128 pixels for the next CPU region experiment. It does not prove that 128 is sufficient for a larger or
more difficult dataset.

## Verdict

The extension passes its engineering contract and closes two local evidence gaps: transformation-aligned
probability comparison and resolution-dependent region coverage. The next learned-behavior claim remains blocked
on a compatible trained checkpoint; until then, all findings are explicitly labelled cold-start diagnostics.
