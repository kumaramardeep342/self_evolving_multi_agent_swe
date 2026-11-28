import json
from collections import Counter

raw = json.load(open("dataset/dataset.json", encoding="utf-8"))
scenarios = raw if isinstance(raw, list) else raw.get("scenarios", [])

cats = Counter()
for sc in scenarios:
    for tc in sc.get("ground_truth", {}).get("verification_test_cases", []):
        cats[tc.get("test_category")] += 1

for k, v in cats.items():
    print(f"{k!r}: {v}")