import json
from pathlib import Path

# Anchor paths relative to this script's directory (.../dataset/scripts)
SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
SCENARIOS_DIR = DATASET_DIR / "scenarios"
OUTPUT_FILE = DATASET_DIR / "dataset.json"

# Recursively collect all JSON scenario files across all domain folders
scenario_files = sorted(SCENARIOS_DIR.rglob("*.json"))

combined_dataset = []
for file_path in scenario_files:
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            combined_dataset.append(data)
        except json.JSONDecodeError as e:
            print(f"Skipping malformed file {file_path.name}: {e}")

# Write to dataset/dataset.json
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(combined_dataset, f, indent=2)

print(f"Successfully compiled {len(combined_dataset)} scenarios into {OUTPUT_FILE.name}")