# Two-minute demo

## Start

```bat
run_demo.cmd
```

The command serves the latest evidence on `http://127.0.0.1:8766/demo.html` and opens it in the default browser.

## Suggested flow

1. Point to the five cards: MoT/MoA are supported; MoE/Latent/MoLoRA are explicitly unsupported for token overlay.
2. Keep MoT selected and switch between dominant, probability, entropy and margin views. Explain that its
   cold-start maps are constant and its aggregate entropy is `0.605693`,
   which is an honest negative observation rather than a rendering failure.
3. Switch to MoA, sample 2, `model.16.m.0.router`, then choose normalized entropy. Point to the side-by-side
   381×500 original/overlay pair and source shape `1×3×8×8`.
4. Enable **Show archived ground-truth boxes**. Point to 12 foreground and 36 valid-background tokens for this
   capture; letterbox padding is excluded. Its foreground/background TV is only `6.35e-06`.
5. Explain the aggregate MoA entropy `1.0`, Top-1 margin `3.37e-06` and neighboring-token variation `2.55e-06`:
   the colorful argmax regions amplify tiny cold-start differences and are not learned semantics.
6. Change sample and layer to show that the UI is driven by 192 archived evidence entries, not a hard-coded image.
7. Click **Copy evidence metadata** and **Export current PNG**. Close by stating that raw tensors, boolean region
   masks, labels, geometry, batch-equivalence results, config, log and SHA-256 manifest are preserved beside the
   demo.

## Reproduce before presenting

Run `run_tests.cmd`, confirm all tests pass, then open the run's `summary.json` and verify `status: PASS`. If a
trained compatible checkpoint becomes available, generate a separate run ID and keep the random-init result as the
pipeline baseline; never overwrite evidence directories.
