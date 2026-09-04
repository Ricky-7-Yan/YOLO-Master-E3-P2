# Limitations and safe interpretation

- No compatible trained MoT/MoA checkpoint was used. Random-init patterns must not be described as learned
  specialization, semantic attention or accuracy improvement.
- Input size 64 and four coco8 validation images are sufficient for a deterministic CPU mechanism test, not for a
  statistical study of routing behavior.
- MoE, Latent and MoLoRA do not expose reversible token-to-image assignments in the audited runtime contracts.
  Their `UNSUPPORTED` result is intentional and prevents deceptive visualization.
- MoLoRA was tested at its official router contract, not after injection into a complete detector; the evidence
  labels this distinction.
- Bilinear restoration makes a low-resolution routing field viewable but does not increase its information content.
  The UI always displays the source grid shape.
- CPU results do not establish CUDA correctness, GPU overhead, memory cost or full-training performance.
- The demo was rendered in Microsoft Edge at desktop and 390-pixel mobile widths. Other browsers and assistive
  technology were not exhaustively tested.

