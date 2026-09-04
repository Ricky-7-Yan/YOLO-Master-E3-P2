# Compatible trained-checkpoint audit

## Result

No trained checkpoint explicitly matching the pinned `yolo26-master-mot-n.yaml` or
`yolo26-master-moa-n.yaml` configuration was found in the local project or the official release assets checked on
2026-09-04. The formal P2 evidence therefore remains a random-initialization instrumentation baseline.

## Reproducible checks

Local checkpoint inventory:

```powershell
rg --files YOLO-Master-E3-P2 YOLO-Master-main-07d3303 YOLO-Master-baseline `
  -g '*.pt' -g '*.pth' -g '*.ckpt' -g '*.onnx'
```

The command returned no files. Official release asset inventory:

```powershell
gh api repos/Tencent/YOLO-Master/releases --paginate `
  --jq '.[] | {tag_name, published_at, assets: [.assets[].name]}'
```

The current release page is [Tencent/YOLO-Master releases](https://github.com/Tencent/YOLO-Master/releases).
Available model assets are ES-MoE or older YOLO-Master variants; the source-only v26.08 release contains Python
packages. Asset names alone do not establish compatibility with the current MoT/MoA YAMLs, so none is loaded by
guessing or partial parameter matching.

## Safety decision

Using an architecture-mismatched checkpoint would mix missing/random parameters with loaded parameters and make
the heatmap difficult to interpret. The project instead records the limitation, preserves a controlled seed-zero
baseline, and keeps the capture/geometry/region pipeline ready for an explicitly compatible future checkpoint.
