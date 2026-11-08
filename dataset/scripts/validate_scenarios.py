import json
import jsonschema

# Load schema
with open("schema.json") as f:
    schema = json.load(f)

# Validate scenario file
with open("scenarios/AUTO-LONG-001.json") as f:
    scenario = json.load(f)

# 1. Validate against JSON schema
jsonschema.validate(instance=scenario, schema=schema)

# 2. Check Traceability Invariant: Every Req has >= 1 Test Case
req_ids = {r["req_id"] for r in scenario["ground_truth"]["formal_requirements"]}
test_parent_ids = {t["parent_req_id"] for t in scenario["ground_truth"]["verification_test_cases"]}

assert req_ids == test_parent_ids, f"Traceability mismatch: {req_ids ^ test_parent_ids}"
print("Scenario validation passed!")