import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
INPUT_PATH = DATASET_DIR / "dataset.json"
OUTPUT_DIR = DATASET_DIR / "result"


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
        if all(isinstance(v, dict) for v in raw.values()):
            return list(raw.values())
    raise ValueError(f"Unsupported JSON structure in {dataset_path}")


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


def count_per_scenario(input_path: Path = INPUT_PATH, output_dir: Path = OUTPUT_DIR):
    scenarios = load_scenarios(input_path)

    total_decomp = 0
    total_reqs = 0
    total_tests = 0
    total_decomp_plus_reqs = 0
    total_all_three = 0

    rows = []
    json_records = []

    for idx, sc in enumerate(scenarios, start=1):
        sid = sc.get("scenario_id", f"SCENARIO_{idx:03d}")
        gt = sc.get("ground_truth", {}) or {}

        decomp = gt.get("decomposition_targets", []) or []
        reqs = gt.get("formal_requirements", []) or []
        tests = gt.get("verification_test_cases", []) or []

        n_decomp = len(decomp)
        n_reqs = len(reqs)
        n_tests = len(tests)
        n_decomp_plus_n_reqs = n_decomp + n_reqs
        n_all_three = n_decomp + n_reqs + n_tests

        total_decomp += n_decomp
        total_reqs += n_reqs
        total_tests += n_tests
        total_decomp_plus_reqs += n_decomp_plus_n_reqs
        total_all_three += n_all_three

        rows.append([
            str(idx),
            str(sid),
            str(n_decomp),
            str(n_reqs),
            str(n_tests),
            str(n_decomp_plus_n_reqs),
            str(n_all_three),
        ])
        json_records.append({
            "index": idx,
            "scenario_id": sid,
            "decomposition_targets": n_decomp,
            "formal_requirements": n_reqs,
            "verification_test_cases": n_tests,
            "decomposition_targets_plus_formal_requirements": n_decomp_plus_n_reqs,
            "decomp_plus_reqs_plus_tests": n_all_three,
        })

    rows.append([
        "",
        "TOTAL",
        str(total_decomp),
        str(total_reqs),
        str(total_tests),
        str(total_decomp_plus_reqs),
        str(total_all_three),
    ])

    table_str = format_table(
        f"Per-Scenario Counts ({len(scenarios)} Scenarios)",
        [
            "#",
            "Scenario ID",
            "decomposition_targets",
            "formal_requirements",
            "verification_test_cases",
            "decomp + reqs",
            "decomp + reqs + tests",
        ],
        rows,
    ).lstrip()

    print(table_str)

    output_dir.mkdir(parents=True, exist_ok=True)
    txt_out = output_dir / "per_scenario_counts.txt"
    json_out = output_dir / "per_scenario_counts.json"

    txt_out.write_text(table_str + "\n", encoding="utf-8")
    json_out.write_text(
        json.dumps(
            {
                "total_scenarios": len(scenarios),
                "totals": {
                    "decomposition_targets": total_decomp,
                    "formal_requirements": total_reqs,
                    "verification_test_cases": total_tests,
                    "decomposition_targets_plus_formal_requirements": total_decomp_plus_reqs,
                    "decomp_plus_reqs_plus_tests": total_all_three,
                },
                "scenarios": json_records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nSaved text table to: {txt_out}")
    print(f"Saved JSON counts to: {json_out}")


if __name__ == "__main__":
    count_per_scenario()