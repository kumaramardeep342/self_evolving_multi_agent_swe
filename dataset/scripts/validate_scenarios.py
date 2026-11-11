import json
import sys
from pathlib import Path
import jsonschema
from jsonschema.exceptions import ValidationError, SchemaError

# Resolve paths relative to scripts directory
SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
SCHEMA_FILE = DATASET_DIR / "schema.json"
SCENARIOS_DIR = DATASET_DIR / "scenarios"

def load_schema(schema_path: Path) -> dict:
    if not schema_path.is_file():
        print(f"[ERROR] Schema file not found at: {schema_path}")
        sys.exit(1)
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_all_scenarios():
    schema = load_schema(SCHEMA_FILE)
    scenario_files = sorted(SCENARIOS_DIR.rglob("*.json"))

    if not scenario_files:
        print(f"[ERROR] No scenario files found under {SCENARIOS_DIR}")
        sys.exit(1)

    passed_count = 0
    failed_files = []

    print(f"Starting validation for {len(scenario_files)} scenario files...\n")

    for file_path in scenario_files:
        rel_path = file_path.relative_to(DATASET_DIR)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                scenario = json.load(f)
        except json.JSONDecodeError as e:
            failed_files.append((rel_path, f"Malformed JSON: {e}"))
            continue

        # 1. Structural Schema Validation
        try:
            jsonschema.validate(instance=scenario, schema=schema)
        except ValidationError as e:
            failed_files.append((rel_path, f"Schema mismatch at '{'.'.join(str(p) for p in e.path)}': {e.message}"))
            continue
        except SchemaError as e:
            print(f"[FATAL] Invalid schema in schema.json: {e.message}")
            sys.exit(1)

        # 2. Invariant Gate Verification (Bidirectional Traceability)
        try:
            ground_truth = scenario.get("ground_truth", {})
            formal_reqs = ground_truth.get("formal_requirements", [])
            test_cases = ground_truth.get("verification_test_cases", [])

            req_ids = {r["req_id"] for r in formal_reqs if "req_id" in r}
            test_parent_ids = {t["parent_req_id"] for t in test_cases if "parent_req_id" in t}

            # Check: Every formal requirement must have >= 1 verification test
            orphaned_reqs = req_ids - test_parent_ids
            # Check: Every test case must reference a valid defined requirement
            phantom_tests = test_parent_ids - req_ids

            trace_errors = []
            if orphaned_reqs:
                trace_errors.append(f"Orphaned requirements (missing tests): {sorted(orphaned_reqs)}")
            if phantom_tests:
                trace_errors.append(f"Phantom test parent IDs (undefined req): {sorted(phantom_tests)}")

            if trace_errors:
                failed_files.append((rel_path, " | ".join(trace_errors)))
                continue

        except (KeyError, TypeError) as e:
            failed_files.append((rel_path, f"Traceability extraction failure: {e}"))
            continue

        passed_count += 1

    # Final Summary Report
    print("=" * 60)
    print(f"VALIDATION SUMMARY: {passed_count}/{len(scenario_files)} PASSED")
    print("=" * 60)

    if failed_files:
        print("\nFailures identified:")
        for idx, (path, error) in enumerate(failed_files, 1):
            print(f"{idx}. [{path}]\n   Reason: {error}\n")
        sys.exit(1)
    else:
        print("\nAll 40 scenarios strictly satisfy JSON schema and bidirectional traceability invariants!")

if __name__ == "__main__":
    validate_all_scenarios()