# Two-minute demo

## Start

```bat
run_demo.cmd
```

The command serves the latest evidence on `http://127.0.0.1:8766/demo.html` and opens it in the default browser.

## Suggested flow

1. Point to the five cards: MoT/MoA are supported; MoE/Latent/MoLoRA are explicitly unsupported for token overlay.
2. Keep MoT selected and switch between dominant and expert views. Explain that its cold-start maps are constant,
   which is an honest negative observation rather than a rendering failure.
3. Switch to MoA, sample 2, `model.16.m.0.router`, expert 2/global. Point to source shape `1×3×8×8` and the
   original-size overlay.
4. Change sample and layer to show that the UI is driven by 128 archived evidence entries, not a hard-coded image.
5. Click **Export current PNG**. Close by stating that the raw NPZ, geometry, config, log and SHA-256 manifest are
   preserved beside the demo.

## Reproduce before presenting

Run `run_tests.cmd`, confirm all tests pass, then open the run's `summary.json` and verify `status: PASS`. If a
trained compatible checkpoint becomes available, generate a separate run ID and keep the random-init result as the
pipeline baseline; never overwrite evidence directories.

