"""CPU-only resolution and horizontal-flip diagnostics for P2 spatial routers."""

from __future__ import annotations

import hashlib
import logging
import os
import random
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFont

from .capture import SpatialRouterCollector, max_output_delta
from .geometry import LetterboxMeta, letterbox
from .io_utils import environment, sha256_file, write_json, write_manifest
from .regions import label_path_for_image, parse_yolo_labels, token_region_masks
from .runner import (
    PROJECT_ROOT,
    RUN_ID_PATTERN,
    _detach_tree,
    _resolve_images,
    _slug,
    _verify_project_source_state,
    _verify_source,
)
from .stability import aggregate_stability_comparisons, probability_map_comparison, restore_probability_stack


def _load_config(path: Path, run_id_override: str | None) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise TypeError(f"config must contain a mapping: {path}")
    config = dict(loaded)
    run_id = str(run_id_override if run_id_override is not None else config.get("run_id", "")).strip()
    if not RUN_ID_PATTERN.fullmatch(run_id):
        raise ValueError("run_id must be path-safe and at most 128 characters")
    config["run_id"] = run_id
    resolutions = [int(value) for value in config.get("resolutions", [])]
    if len(resolutions) < 2 or len(set(resolutions)) != len(resolutions) or min(resolutions) < 32:
        raise ValueError("resolutions must contain at least two unique integers >= 32")
    config["resolutions"] = resolutions
    reference = int(config.get("reference_resolution", 0))
    if reference not in resolutions:
        raise ValueError("reference_resolution must be present in resolutions")
    config["reference_resolution"] = reference
    seeds = [int(value) for value in config.get("seeds", [])]
    if len(seeds) < 2 or len(set(seeds)) != len(seeds):
        raise ValueError("seeds must contain at least two unique integers")
    config["seeds"] = seeds
    indices = [int(value) for value in config.get("sample_indices", [])]
    if not indices or len(set(indices)) != len(indices):
        raise ValueError("sample_indices must be non-empty and unique")
    config["sample_indices"] = indices
    if config.get("device") != "cpu":
        raise ValueError("this evidence protocol is intentionally CPU-only")
    if config.get("transformations") != ["identity", "horizontal_flip"]:
        raise ValueError("transformations must be exactly identity and horizontal_flip")
    if set(config.get("spatial_profiles", {})) != {"mot", "moa"}:
        raise ValueError("spatial_profiles must be exactly MoT and MoA")
    return config


def _logger(path: Path) -> logging.Logger:
    logger = logging.getLogger("e3_p2_robustness")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    for handler in (logging.StreamHandler(sys.stdout), logging.FileHandler(path, encoding="utf-8", mode="w")):
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def _tensor(image: Image.Image, resolution: int, flipped: bool, torch_module: Any) -> tuple[Any, LetterboxMeta]:
    source = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flipped else image
    canvas, meta = letterbox(source, resolution)
    array = canvas.astype(np.float32).transpose(2, 0, 1) / 255.0
    return torch_module.from_numpy(array).unsqueeze(0).contiguous(), meta


def _capture_once(model: Any, family: str, router_class: str, tensor: Any, torch_module: Any) -> tuple[Any, list[Any], list[str]]:
    collector = SpatialRouterCollector(family=family, router_class=router_class)
    registered = collector.register(model)
    try:
        with torch_module.inference_mode():
            output = model(tensor)
    finally:
        collector.remove()
    if collector.handles or len(collector.records) != len(registered):
        raise RuntimeError(f"capture count or hook cleanup failed for family={family}")
    if [record.module_name for record in collector.records] != registered:
        raise RuntimeError(f"capture module order changed for family={family}")
    return _detach_tree(output), collector.records, registered


def _archive_inputs(paths: list[Path], sample_indices: list[int], run_dir: Path) -> list[dict[str, Any]]:
    destination = run_dir / "inputs"
    destination.mkdir(parents=True, exist_ok=True)
    records = []
    for sample_index, path in zip(sample_indices, paths):
        label = label_path_for_image(path)
        image_relative = Path("inputs") / f"sample-{sample_index}--{path.name}"
        label_relative = Path("inputs") / f"sample-{sample_index}--{label.name}"
        shutil.copyfile(path, run_dir / image_relative)
        shutil.copyfile(label, run_dir / label_relative)
        with Image.open(path) as image:
            width, height = image.size
        boxes = parse_yolo_labels(label)
        records.append(
            {
                "sample_index": sample_index,
                "name": path.name,
                "original_width": width,
                "original_height": height,
                "sha256": sha256_file(path),
                "label_sha256": sha256_file(label),
                "ground_truth_box_count": len(boxes),
                "image_artifact": image_relative.as_posix(),
                "label_artifact": label_relative.as_posix(),
            }
        )
    return records


def _coverage_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for item in records:
        grouped[(item["family"], int(item["resolution"]))].append(item)
    return {
        "method": {
            "seed": "first configured seed only; geometry and annotations are seed-independent",
            "assignment_rule": "valid token center inside any ground-truth box",
            "padding_policy": "excluded from foreground and background",
            "purpose": "measure whether higher input resolution reduces empty foreground/background comparisons",
        },
        "capture_count": len(records),
        "by_family_resolution": {
            f"{family}:{resolution}": {
                "capture_count": len(items),
                "supported_capture_count": sum(item["status"] == "SUPPORTED" for item in items),
                "insufficient_capture_count": sum(item["status"] == "INSUFFICIENT_TOKENS" for item in items),
                "foreground_token_count": sum(item["foreground_token_count"] for item in items),
                "background_token_count": sum(item["background_token_count"] for item in items),
                "padding_token_count": sum(item["padding_token_count"] for item in items),
            }
            for (family, resolution), items in sorted(grouped.items())
        },
        "records": records,
    }


def _save_overview(aggregate: dict[str, Any], coverage: dict[str, Any], path: Path) -> None:
    canvas = Image.new("RGB", (1800, 1120), "#061022")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    draw.rounded_rectangle((45, 40, 1755, 1080), radius=28, fill="#0b1932", outline="#1d5d80", width=3)
    draw.text((85, 75), "E3 P2 / CPU RESOLUTION + FLIP STABILITY", fill="#00e5ff", font=font)
    draw.text((85, 108), "Random initialization: pipeline diagnostic, not learned robustness", fill="#ffcc66", font=font)
    draw.text((85, 160), "ALIGNED PROBABILITY COMPARISONS", fill="#a66cff", font=font)
    y = 205
    header = "comparison / family / size       count    MAE(mean)     JS(mean,nats)    dominant agreement    Pearson defined/undefined"
    draw.text((85, y), header, fill="#9bb8d6", font=font)
    y += 32
    for key, item in aggregate["by_type_family_resolution"].items():
        pearson = item["expert_pearson"]
        line = (
            f"{key:<34} {item['comparison_count']:>5}    "
            f"{item['probability_mae']['mean']:.8f}    "
            f"{item['mean_jensen_shannon_divergence_nats']['mean']:.3e}        "
            f"{item['dominant_expert_agreement_fraction']['mean']:.6f}            "
            f"{pearson['defined_count']}/{pearson['undefined_count']}"
        )
        draw.text((85, y), line, fill="#eaf4ff", font=font)
        y += 30
    y += 34
    draw.text((85, y), "GROUND-TRUTH TOKEN COVERAGE BY RESOLUTION", fill="#a66cff", font=font)
    y += 44
    draw.text((85, y), "family / size                 captures    supported    insufficient    foreground    background    padding", fill="#9bb8d6", font=font)
    y += 32
    for key, item in coverage["by_family_resolution"].items():
        line = (
            f"{key:<29} {item['capture_count']:>8}    {item['supported_capture_count']:>9}    "
            f"{item['insufficient_capture_count']:>12}    {item['foreground_token_count']:>10}    "
            f"{item['background_token_count']:>10}    {item['padding_token_count']:>7}"
        )
        draw.text((85, y), line, fill="#eaf4ff", font=font)
        y += 30
    draw.text((85, 1015), "Every value is regenerated from archived inputs, locked source fingerprints and raw router arrays.", fill="#63e6a7", font=font)
    canvas.save(path)


def run(config_path: Path, *, run_id: str | None = None, update_latest: bool = True) -> Path:
    config = _load_config(config_path, run_id)
    project_source = _verify_project_source_state(bool(config.get("require_committed_source", False)))
    run_dir = PROJECT_ROOT / "artifacts" / "p2" / config["run_id"]
    if run_dir.exists() and any(run_dir.iterdir()):
        raise FileExistsError(f"refusing to overwrite non-empty evidence directory: {run_dir}")
    run_dir.mkdir(parents=True, exist_ok=True)
    logger = _logger(run_dir / "full.log")
    (run_dir / "config.resolved.yaml").write_text(
        yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    (run_dir / "command.txt").write_text("run_robustness.cmd\n", encoding="utf-8")
    started = time.perf_counter()

    source_root = (PROJECT_ROOT / config["runtime_root"]).resolve()
    checks = _verify_source(source_root, config["source_fingerprints"])
    sys.path.insert(0, str(source_root))
    os.chdir(PROJECT_ROOT)
    import torch
    from ultralytics import YOLO

    paths, dataset_meta = _resolve_images(config["dataset"], config["dataset_split"], config["sample_indices"])
    input_records = _archive_inputs(paths, config["sample_indices"], run_dir)
    input_record = {
        **dataset_meta,
        "selected_image_count": len(paths),
        "images": input_records,
        "image_and_annotation_set_sha256": hashlib.sha256(
            "\n".join(f"{item['sample_index']}:{item['sha256']}:{item['label_sha256']}" for item in input_records).encode("utf-8")
        ).hexdigest(),
    }
    write_json(run_dir / "input.json", input_record)
    write_json(run_dir / "source-fingerprint-checks.json", checks)

    arrays: dict[str, np.ndarray] = {}
    capture_metadata: list[dict[str, Any]] = []
    comparisons: list[dict[str, Any]] = []
    coverage_records: list[dict[str, Any]] = []
    invariants: dict[str, Any] = {}
    reference_resolution = config["reference_resolution"]
    first_seed = config["seeds"][0]
    logger.info(
        "scope=CPU resolution and horizontal-flip diagnostics resolutions=%s seeds=%s samples=%s",
        config["resolutions"],
        config["seeds"],
        config["sample_indices"],
    )

    for family, profile in config["spatial_profiles"].items():
        for seed in config["seeds"]:
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            wrapper = YOLO(source_root / profile["model_config"])
            model = wrapper.model.to("cpu").eval()
            representative, _ = _tensor(Image.open(paths[0]).convert("RGB"), reference_resolution, False, torch)
            with torch.inference_mode():
                baseline_output = _detach_tree(model(representative))
            hooked_output, first_records, module_order = _capture_once(
                model, family, profile["router_class"], representative, torch
            )
            hook_delta = max_output_delta(baseline_output, hooked_output)
            _, repeat_records, repeat_order = _capture_once(model, family, profile["router_class"], representative, torch)
            repeat_weight_delta = max(
                float(np.max(np.abs(first.weights - second.weights)))
                for first, second in zip(first_records, repeat_records)
            )
            repeat_logit_delta = max(
                float(np.max(np.abs(first.logits - second.logits)))
                for first, second in zip(first_records, repeat_records)
            )
            repeat_indices_equal = all(
                first.indices is None or np.array_equal(first.indices, second.indices)
                for first, second in zip(first_records, repeat_records)
            )
            if hook_delta != 0.0 or module_order != repeat_order or repeat_weight_delta != 0.0 or repeat_logit_delta != 0.0 or not repeat_indices_equal:
                raise RuntimeError(f"representative invariants failed for family={family}, seed={seed}")
            invariants[f"{family}:seed-{seed}"] = {
                "hook_output_max_abs_delta": hook_delta,
                "repeat_weight_max_abs_delta": repeat_weight_delta,
                "repeat_logit_max_abs_delta": repeat_logit_delta,
                "repeat_indices_equal": repeat_indices_equal if family == "mot" else None,
                "module_order": module_order,
                "hook_cleanup": True,
                "status": "PASS",
            }

            for sample_index, path in zip(config["sample_indices"], paths):
                with Image.open(path) as opened:
                    original = opened.convert("RGB")
                boxes = parse_yolo_labels(label_path_for_image(path))
                restored: dict[tuple[int, bool, str], np.ndarray] = {}
                observed_module_order = None
                for resolution in config["resolutions"]:
                    for flipped in (False, True):
                        tensor, meta = _tensor(original, resolution, flipped, torch)
                        _, records, registered = _capture_once(model, family, profile["router_class"], tensor, torch)
                        if observed_module_order is None:
                            observed_module_order = registered
                        if registered != module_order or registered != observed_module_order:
                            raise RuntimeError(f"module order changed across transformations for family={family}")
                        for record in records:
                            weights = record.weights[0]
                            aligned, restoration_validation = restore_probability_stack(weights, meta)
                            if flipped:
                                aligned = np.flip(aligned, axis=2).copy()
                            restored[(resolution, flipped, record.module_name)] = aligned
                            prefix = (
                                f"{family}__seed-{seed}__sample-{sample_index}__size-{resolution}__"
                                f"{'hflip' if flipped else 'identity'}__{_slug(record.module_name)}"
                            )
                            weight_key = f"{prefix}__weights"
                            logit_key = f"{prefix}__logits"
                            arrays[weight_key] = record.weights
                            arrays[logit_key] = record.logits
                            index_key = None
                            if record.indices is not None:
                                index_key = f"{prefix}__indices"
                                arrays[index_key] = record.indices
                            capture_metadata.append(
                                {
                                    "family": family,
                                    "seed": seed,
                                    "sample_index": sample_index,
                                    "sample_name": path.name,
                                    "resolution": resolution,
                                    "transformation": "horizontal_flip" if flipped else "identity",
                                    "module": record.module_name,
                                    "module_type": record.module_type,
                                    "source_shape": record.validation["shape"],
                                    "geometry": meta.to_dict(),
                                    "router_validation": record.validation,
                                    "restoration_validation": restoration_validation,
                                    "aligned_to_original_coordinates": True,
                                    "raw_keys": {"weights": weight_key, "logits": logit_key, "indices": index_key},
                                }
                            )
                            if seed == first_seed and not flipped:
                                masks = token_region_masks(boxes, meta, weights.shape[1], weights.shape[2])
                                foreground = int(masks["foreground"].sum())
                                background = int(masks["background"].sum())
                                coverage_records.append(
                                    {
                                        "family": family,
                                        "resolution": resolution,
                                        "sample_index": sample_index,
                                        "module": record.module_name,
                                        "grid_height": int(weights.shape[1]),
                                        "grid_width": int(weights.shape[2]),
                                        "foreground_token_count": foreground,
                                        "background_token_count": background,
                                        "padding_token_count": int(masks["padding"].sum()),
                                        "status": "SUPPORTED" if foreground and background else "INSUFFICIENT_TOKENS",
                                    }
                                )
                for module in module_order:
                    reference = restored[(reference_resolution, False, module)]
                    for resolution in config["resolutions"]:
                        identity = restored[(resolution, False, module)]
                        flipped = restored[(resolution, True, module)]
                        comparisons.append(
                            {
                                "comparison_type": "horizontal_flip",
                                "family": family,
                                "seed": seed,
                                "sample_index": sample_index,
                                "module": module,
                                "reference_resolution": resolution,
                                "candidate_resolution": resolution,
                                "alignment": "restore both maps to original pixels; horizontally unflip candidate",
                                "metrics": probability_map_comparison(identity, flipped),
                            }
                        )
                        if resolution != reference_resolution:
                            comparisons.append(
                                {
                                    "comparison_type": "resolution_vs_reference",
                                    "family": family,
                                    "seed": seed,
                                    "sample_index": sample_index,
                                    "module": module,
                                    "reference_resolution": reference_resolution,
                                    "candidate_resolution": resolution,
                                    "alignment": "restore both identity maps to original-image pixels",
                                    "metrics": probability_map_comparison(reference, identity),
                                }
                            )
                logger.info("family=%s seed=%d sample=%d captures=%d", family, seed, sample_index, len(module_order) * 6)
            del model, wrapper

    np.savez_compressed(run_dir / "stability-routing-raw.npz", **arrays)
    write_json(run_dir / "spatial-captures.json", capture_metadata)
    write_json(run_dir / "stability-comparisons.json", comparisons)
    aggregate = aggregate_stability_comparisons(comparisons)
    write_json(run_dir / "stability-aggregate.json", aggregate)
    coverage = _coverage_summary(coverage_records)
    write_json(run_dir / "region-resolution-coverage.json", coverage)
    write_json(run_dir / "invariants.json", invariants)
    write_json(run_dir / "environment.json", environment(torch, source_root, PROJECT_ROOT))
    _save_overview(aggregate, coverage, run_dir / "robustness-overview.png")

    summary = {
        "status": "PASS",
        "scope": "CPU-only resolution and horizontal-flip diagnostics for true MoT/MoA spatial router probabilities",
        "run_id": config["run_id"],
        "official_locked_base_ref": config["official_locked_base_ref"],
        "official_runtime_ref": config["official_runtime_ref"],
        "tool_source": project_source,
        "source_fingerprint_validation": "PASS",
        "source_fingerprint_count": len(checks),
        "device": "cpu",
        "seeds": config["seeds"],
        "resolutions": config["resolutions"],
        "reference_resolution": reference_resolution,
        "sample_count": len(paths),
        "spatial_capture_count": len(capture_metadata),
        "raw_array_count": len(arrays),
        "aligned_comparison_count": len(comparisons),
        "representative_invariants": invariants,
        "region_resolution_coverage": coverage["by_family_resolution"],
        "interpretation_boundary": "random initialization; pipeline and sensitivity evidence only, not learned robustness",
        "status_semantics": "PASS means capture, geometry, alignment, determinism and evidence integrity checks completed",
        "duration_seconds_observation_only": time.perf_counter() - started,
    }
    write_json(run_dir / "summary.json", summary)
    for handler in logger.handlers:
        handler.flush()
    write_manifest(run_dir)
    if update_latest:
        latest = PROJECT_ROOT / "artifacts" / "p2" / "ROBUSTNESS_LATEST.txt"
        latest.parent.mkdir(parents=True, exist_ok=True)
        latest.write_text(config["run_id"] + "\n", encoding="utf-8")
    logger.info("status=PASS captures=%d comparisons=%d arrays=%d", len(capture_metadata), len(comparisons), len(arrays))
    for handler in logger.handlers:
        handler.flush()
    write_manifest(run_dir)
    return run_dir
