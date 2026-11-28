import json
from pathlib import Path
from collections import Counter


INPUT_PATH = Path("dataset/dataset.json")
OUTPUT_DIR = Path("dataset/result")

CANONICAL_MODES = [
    "Collision_Warning_State",
    "Autonomous_Emergency_Braking",
    "Driver_Override_Suppression",
]

CANONICAL_TEST_CATS = [
    "Nominal_Operational",
    "Boundary_Equivalence",
    "Negative_Fault_Injection",
    "Timing_Latency_Tolerance",
]

CANONICAL_ASILS = [
    "QM",
    "ASIL_A",
    "ASIL_B",
    "ASIL_C",
    "ASIL_D",
]

SIGNAL_BUCKETS = [
    "3 to 4 Signals",
    "5 to 6 Signals",
    "7 to 8 Signals",
    "9+ Signals",
    "Other (<3)",
]

FTTI_BUCKETS = [
    "Ultra-Critical (<= 20 ms)",
    "High (20-50 ms)",
    "Moderate (50-100 ms)",
    "Supervisory (> 100 ms)",
    "Missing / Unparsed",
]


def norm_label(val: str) -> str:
    if not isinstance(val, str):
        return ""
    return "_".join(val.strip().replace("-", "_").replace(" ", "_").split()).upper()


def map_canonical(raw_val: str, canonical_list: list[str], extra_counter: Counter) -> str:
    if not raw_val:
        return "Missing"
    canon_map = {norm_label(c): c for c in canonical_list}
    key = norm_label(raw_val)
    if key in canon_map:
        return canon_map[key]
    extra_counter[raw_val] += 1
    return f"Other ({raw_val})"


def classify_signal_bucket(count: int) -> str:
    if count < 3:
        return "Other (<3)"
    if 3 <= count <= 4:
        return "3 to 4 Signals"
    if 5 <= count <= 6:
        return "5 to 6 Signals"
    if 7 <= count <= 8:
        return "7 to 8 Signals"
    return "9+ Signals"


def classify_ftti_ms(ftti_val) -> str:
    if ftti_val is None:
        return "Missing / Unparsed"
    try:
        val = float(ftti_val)
    except (TypeError, ValueError):
        return "Missing / Unparsed"
    if 0 < val < 1.0:
        val *= 1000.0
    if val <= 20.0:
        return "Ultra-Critical (<= 20 ms)"
    if val <= 50.0:
        return "High (20-50 ms)"
    if val <= 100.0:
        return "Moderate (50-100 ms)"
    return "Supervisory (> 100 ms)"


def format_table(title: str, headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            widths[i] = max(widths[i], len(str(cell)))
    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"
    fmt = "| " + " | ".join(f"{str(h):<{widths[i]}}" for i, h in enumerate(headers)) + " |"
    lines = [f"\n=== {title} ===", sep, fmt, sep]
    for r in rows:
        lines.append("| " + " | ".join(f"{str(c):<{widths[i]}}" for i, c in enumerate(r)) + " |")
    lines.append(sep)
    return "\n".join(lines)


def load_scenarios(dataset_path: Path) -> list[dict]:
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
    raw = json.loads(dataset_path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        for key in ("scenarios", "data", "items", "benchmark_scenarios"):
            if isinstance(raw.get(key), list):
                return raw[key]
        # Fallback: dictionary keyed by scenario_id
        if all(isinstance(v, dict) for v in raw.values()):
            return list(raw.values())
    raise ValueError(f"Unsupported JSON structure in {dataset_path}")


def summarize_dataset(input_path: Path = INPUT_PATH, output_dir: Path = OUTPUT_DIR):
    scenarios = load_scenarios(input_path)
    n_scenarios = len(scenarios)

    total_tests = 0
    total_reqs = 0
    total_decomp = 0

    mode_counts = Counter()
    test_cat_counts = Counter()
    asil_counts = Counter()
    signal_bucket_counts = Counter()
    ftti_bucket_counts = Counter()
    unmapped_tracker = Counter()

    for data in scenarios:
        meta = data.get("metadata", {}) or {}
        inp_ctx = data.get("input_context", {}) or {}
        gt = data.get("ground_truth", {}) or {}

        decomp = gt.get("decomposition_targets", []) or []
        reqs = gt.get("formal_requirements", []) or []
        tests = gt.get("verification_test_cases", []) or []

        total_decomp += len(decomp)
        total_reqs += len(reqs)
        total_tests += len(tests)

        asil_label = map_canonical(meta.get("target_asil"), CANONICAL_ASILS, unmapped_tracker)
        asil_counts[asil_label] += 1

        iface = inp_ctx.get("interface_signals", {}) or {}
        in_sigs = iface.get("input_signals", []) or []
        out_sigs = iface.get("output_signals", []) or []
        sig_total = len(in_sigs) + len(out_sigs)
        signal_bucket_counts[classify_signal_bucket(sig_total)] += 1

        for item in decomp:
            mode_label = map_canonical(item.get("operational_mode"), CANONICAL_MODES, unmapped_tracker)
            mode_counts[mode_label] += 1

        for req in reqs:
            ftti_val = req.get("timing_ftti_ms", req.get("ftti_ms", req.get("ftti")))
            ftti_bucket_counts[classify_ftti_ms(ftti_val)] += 1

        for tc in tests:
            cat_label = map_canonical(tc.get("test_category"), CANONICAL_TEST_CATS, unmapped_tracker)
            test_cat_counts[cat_label] += 1

    output_blocks = []

    # Table 1: verification_test_cases
    output_blocks.append(
        format_table(
            f"verification_test_cases (All {n_scenarios} Scenarios Combined)",
            ["Metric", "Combined Count"],
            [
                ["Total Scenarios", str(n_scenarios)],
                ["verification_test_cases", str(total_tests)],
            ],
        )
    )

    # Table 2: formal_requirements + decomposition_targets
    output_blocks.append(
        format_table(
            f"formal_requirements + decomposition_targets (All {n_scenarios} Scenarios Combined)",
            ["Artifact Group", "Combined Count"],
            [
                ["formal_requirements", str(total_reqs)],
                ["decomposition_targets", str(total_decomp)],
                ["formal_requirements + decomposition_targets", str(total_reqs + total_decomp)],
            ],
        )
    )

    # Table 3: operational_mode
    mode_keys = CANONICAL_MODES + [k for k in mode_counts if k not in CANONICAL_MODES]
    total_modes = sum(mode_counts.values())
    output_blocks.append(
        format_table(
            f"operational_mode (All {n_scenarios} Scenarios Combined)",
            ["Operational Mode", "Count", "Share (%)"],
            [
                [k, str(mode_counts[k]), f"{100.0 * mode_counts[k] / total_modes:.1f}%" if total_modes else "0.0%"]
                for k in mode_keys
            ]
            + [["Total", str(total_modes), "100.0%" if total_modes else "0.0%"]],
        )
    )

    # Table 4: test_category
    cat_keys = CANONICAL_TEST_CATS + [k for k in test_cat_counts if k not in CANONICAL_TEST_CATS]
    total_cats = sum(test_cat_counts.values())
    output_blocks.append(
        format_table(
            f"test_category (All {n_scenarios} Scenarios Combined)",
            ["Test Category", "Count", "Share (%)"],
            [
                [k, str(test_cat_counts[k]), f"{100.0 * test_cat_counts[k] / total_cats:.1f}%" if total_cats else "0.0%"]
                for k in cat_keys
            ]
            + [["Total", str(total_cats), "100.0%" if total_cats else "0.0%"]],
        )
    )

    # Table 5: target_asil
    asil_keys = CANONICAL_ASILS + [k for k in asil_counts if k not in CANONICAL_ASILS]
    output_blocks.append(
        format_table(
            f"target_asil (All {n_scenarios} Scenarios Combined)",
            ["Target ASIL", "Scenario Count", "Share (%)"],
            [
                [k, str(asil_counts[k]), f"{100.0 * asil_counts[k] / n_scenarios:.1f}%" if n_scenarios else "0.0%"]
                for k in asil_keys
            ]
            + [["Total", str(n_scenarios), "100.0%" if n_scenarios else "0.0%"]],
        )
    )

    # Table 6: Signal Count per Scenario
    sig_keys = SIGNAL_BUCKETS + [k for k in signal_bucket_counts if k not in SIGNAL_BUCKETS]
    output_blocks.append(
        format_table(
            f"Signal Count per Scenario (All {n_scenarios} Scenarios Combined)",
            ["Signal Count Bucket", "Scenario Count", "Share (%)"],
            [
                [
                    k,
                    str(signal_bucket_counts[k]),
                    f"{100.0 * signal_bucket_counts[k] / n_scenarios:.1f}%" if n_scenarios else "0.0%",
                ]
                for k in sig_keys
            ]
            + [["Total", str(n_scenarios), "100.0%" if n_scenarios else "0.0%"]],
        )
    )

    # Table 7: Fault-Tolerant Time Interval (FTTI) Spectrum
    total_ftti = sum(ftti_bucket_counts.values())
    output_blocks.append(
        format_table(
            f"Fault-Tolerant Time Interval (FTTI) Spectrum (All {n_scenarios} Scenarios Combined)",
            ["FTTI Spectrum Band", "Requirement Count", "Share (%)"],
            [
                [
                    k,
                    str(ftti_bucket_counts[k]),
                    f"{100.0 * ftti_bucket_counts[k] / total_ftti:.1f}%" if total_ftti else "0.0%",
                ]
                for k in FTTI_BUCKETS
            ]
            + [["Total", str(total_ftti), "100.0%" if total_ftti else "0.0%"]],
        )
    )

    if unmapped_tracker:
        output_blocks.append(f"\n[Warning] Non-canonical label values encountered: {dict(unmapped_tracker)}")

    report_text = "\n".join(output_blocks).lstrip()
    print(report_text)

    # Save outputs to dataset/result
    output_dir.mkdir(parents=True, exist_ok=True)
    txt_out = output_dir / "summary_tables.txt"
    json_out = output_dir / "summary_counts.json"

    txt_out.write_text(report_text + "\n", encoding="utf-8")
    json_out.write_text(
        json.dumps(
            {
                "total_scenarios": n_scenarios,
                "verification_test_cases": total_tests,
                "formal_requirements": total_reqs,
                "decomposition_targets": total_decomp,
                "formal_requirements_plus_decomposition_targets": total_reqs + total_decomp,
                "operational_mode": {k: mode_counts[k] for k in mode_keys},
                "test_category": {k: test_cat_counts[k] for k in cat_keys},
                "target_asil": {k: asil_counts[k] for k in asil_keys},
                "signal_count_per_scenario": {k: signal_bucket_counts[k] for k in sig_keys},
                "ftti_spectrum": {k: ftti_bucket_counts[k] for k in FTTI_BUCKETS},
                "non_canonical_values": dict(unmapped_tracker),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nSaved text tables to: {txt_out}")
    print(f"Saved JSON summary to: {json_out}")


if __name__ == "__main__":
    summarize_dataset()