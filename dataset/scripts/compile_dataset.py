import json
from pathlib import Path

scenarios_dir = Path("dataset/scenarios")
scenario_files = sorted(scenarios_dir.glob("*.json"))

combined_dataset = []
for file_path in scenario_files:
    with open(file_path, "r", encoding="utf-8") as f:
        combined_dataset.append(json.load(f))

with open("dataset/dataset.json", "w", encoding="utf-8") as f:
    json.dump(combined_dataset, f, indent=2)

print(f"Successfully compiled {len(combined_dataset)} scenarios into dataset.json")