# self_evolving_multi_agent_swe
Self-Evolving Multi-Agent Software Enginnering using LLMs , Long-Term Memory and Continual Learning..

## Dataset
```plaintext
dataset/
├── schema.json                  # Top-level JSON schema definition
├── dataset-info.xlsx            # High-level tracking matrix and regulatory mapping
├── dataset.json                 # Auto-compiled master array of all 40 scenarios
├── scenarios/                   # The canonical source-of-truth scenario library
│   ├── AUTO-LONG-001.json
│   ├── AUTO-LONG-002.json
│   ├── ...
│   ├── AUTO-LAT-001.json
│   ├── ...
│   ├── AUTO-CRUISE-001.json
│   └── AUTO-SOTIF-001.json
└── scripts/
│    ├── validate_scenarios.py    # Asserts schema, signal types, and G_trace
│    └── compile_dataset.py       # Combines individual files into dataset.json
└── results/                      # Scripts run results
└── archive/                      # Not in use

```