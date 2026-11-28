# self_evolving_multi_agent_swe
Self-Evolving Multi-Agent Software Enginnering using LLMs , Long-Term Memory and Continual Learning..

## dataset
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
│    └── compile_dataset.py             # Combines individual files into dataset.json
│    └── count_per_scenario.py          # Decomposition, Requirements and Tescase Count for each scenario's
│    └── dataset_summary.py             # Summary of all the scenario's
│    └── test_category_count_debug.py   # For scenario's debugging
│    ├── validate_scenarios.py          # Asserts schema, signal types, and G_trace
└── results/                            # Scripts run results
└── archive/                            # Not in use
```

## run the scripts
```plaintext
cd ~/projects/self_evolving_multi_agent_swe
python dataset/scripts/count_per_scenario.py
python dataset/scripts/dataset_summary.py
python dataset/scripts/test_category_count_debug.py

cd ~/projects/self_evolving_multi_agent_swe/dataset/scripts
python compile_dataset.py
python validate_scenarios.py
```


## taxonomy and inclusion/exclusion mapping of the 30 screened automotive reference documents

The table below outlines the complete taxonomy of the 30 screened regulatory artifacts, detailing their V-model allocation, feature classification, inclusion status within the benchmark synthesis pipeline, and source links.

| # | Document Title / Standard Name | Functional Group | Sub-System Domain | V-Cycle Stage Mapping | Benchmark Role | PDF URL |
| :-: | :--- | :--- | :--- | :--- | :--- | :-: |
| 1 | EU Regulation No 130 (LDWS) | Operational Protocols | Lateral Control | SYS.5 / Vehicle Validation | Reqs & Tests | [Link](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:42014X0618(01)) |
| 2 | UN Regulation R152e (AEBS) | Operational Protocols | Longitudinal Control | SYS.5 / Vehicle Validation | Excluded | [PDF](https://unece.org/fileadmin/DAM/trans/main/wp29/wp29regs/2020/R152e.pdf) |
| 3 | UN Regulation R152e Amendment 1 | Operational Protocols | Longitudinal Control | SYS.5 / Vehicle Validation | Reqs & Tests | [PDF](https://unece.org/sites/default/files/2024-04/R152am1e%20%282%29.pdf) |
| 4 | ADAS Regulations (EU GSR) | Operational Protocols | Multi-Domain ADAS | SYS.1 / SYS.5 / Validation | Reqs & Tests | [PDF](https://unece.org/DAM/trans/doc/2018/wp29grsp/GRSP-63-31e.pdf) |
| 5 | AEB-NPRM Light Vehicles | Operational Protocols | Longitudinal Control | SYS.1 / Vehicle Validation | Excluded | [PDF](https://www.nhtsa.gov/sites/nhtsa.gov/files/2023-05/AEB-NPRM-Web-Version-05-31-2023.pdf) |
| 6 | AUTOSAR AP TR Methodology | Architecture & Constraints | Software Middleware | SYS.3 / SWE.2 | Excluded | [PDF](https://www.autosar.org/fileadmin/standards/R24-11/AP/AUTOSAR_AP_TR_Methodology.pdf) |
| 7 | AUTOSAR AP Adaptive Interfaces | Architecture & Constraints | Software Middleware | SYS.3 / SWE.2 | Excluded | [PDF](https://www.autosar.org/fileadmin/standards/R24-11/AP/AUTOSAR_AP_EXP_InterfacesGuidelines.pdf) |
| 8 | C-NCAP 2024 Management Regulation | Operational Protocols | Vehicle Active Safety | Vehicle Level Validation | Excluded | [Link](https://www.c-ncap.org.cn/cncap-guicheng-detail?id=8) |
| 9 | C-NCAP 2024 App O (AEB VRU) | Operational Protocols | Collision Mitigation | SYS.5 / Vehicle Validation | Test Cases | [Link](https://www.c-ncap.org.cn/cncap-guicheng-detail?id=8) |
| 10 | C-NCAP 2024 App K (Headform/Legform) | Operational Protocols | Passive Body Bumper | Vehicle Validation (Passive) | Excluded | [Link](https://www.c-ncap.org.cn/cncap-guicheng-detail?id=8) |
| 11 | C-NCAP 2024 App L (Active Safety) | Operational Protocols | Longitudinal Active | SYS.5 / Vehicle Validation | Excluded | [Link](https://www.c-ncap.org.cn/cncap-guicheng-detail?id=8) |
| 12 | Euro NCAP AEB C2C Protocol v4.2 | Operational Protocols | Longitudinal Control | SYS.5 / Vehicle Validation | Excluded | [PDF](https://cdn.euroncap.com/cars/assets/euro_ncap_aeb_c2c_test_protocol_v42_af2bd7186c.pdf) |
| 13 | Euro NCAP AEB C2C Protocol v4.3 | Operational Protocols | Longitudinal Control | SYS.5 / Vehicle Validation | Test Cases | [PDF](https://cdn.euroncap.com/cars/assets/euro_ncap_aeb_c2c_test_protocol_v43_1e6ed06def.pdf) |
| 14 | Euro NCAP Assessment Protocol SA v10.3 | Operational Protocols | Active Safety Assessment | Vehicle Level Validation | Excluded | [PDF](https://cdn.euroncap.com/cars/assets/euro_ncap_assessment_protocol_sa_collision_avoidance_v103_28cefe0cb5.pdf) |
| 15 | Euro NCAP Assessment Protocol SA v10.4 | Operational Protocols | Active Safety Assessment | Vehicle Level Validation | Excluded | [PDF](https://cdn.euroncap.com/cars/assets/euro_ncap_assessment_protocol_sa_collision_avoidance_v104_87a5f7e758.pdf) |
| 16 | Euro NCAP Assisted Driving v1.1 | Operational Protocols | Longitudinal Active | SYS.2 / SYS.5 / Validation | Full Top-V | [PDF](https://cdn.euroncap.com/cars/assets/euro_ncap_protocol_assisted_driving_v11_a6bfe1b5f2.pdf) |
| 17 | Euro NCAP Frontal Collisions v1.1 | Operational Protocols | Longitudinal Control | SYS.5 / Vehicle Validation | Test Case | [PDF](https://cdn.euroncap.com/cars/assets/euro_ncap_protocol_crash_avoidance_frontal_collisions_v11_bc661b4bdc.pdf) |
| 18 | Euro NCAP CV Lane Departure v1.0 | Operational Protocols | Lateral Control (CV) | SYS.2 / SYS.5 / Validation | Excluded | [PDF](https://cdn.euroncap.com/commercial-vehicles/assets/euro_ncap_cv_protocol_crash_avoidance_lane_departure_collisions_v10_54a6512af6.pdf) |
| 19 | Euro NCAP Lane Departure v1.2 | Operational Protocols | Lateral Control | SYS.2 / SYS.5 / Validation | Full Top-V | [PDF](https://cdn.euroncap.com/cars/assets/Euro_NCAP_Protocol_Crash_Avoidance_Lane_Departure_Collisions_v1_2_4c2613beca.pdf) |
| 20 | NHTSA AEB Final Rule | Operational Protocols | Longitudinal Control | SYS.1 / SYS.5 / Validation | Full Top-V | [PDF](https://www.nhtsa.gov/sites/nhtsa.gov/files/2024-04/final-rule-automatic-emergency-braking-systems-light-vehicles_web-version.pdf) |
| 21 | ISO 19638:2018 (Road Boundary) | Operational Protocols | Lateral Control | SYS.2 / SYS.5 | Excluded | [PDF](https://cdn.standards.iteh.ai/samples/65599/fffa9c29024747ee822c116fb3da8e78/ISO-19638-2018.pdf) |
| 22 | ISO 26262-2:2018 (Safety Management) | Functional Safety | Safety Management | Supporting Process | Excluded | [PDF](https://cdn.standards.iteh.ai/samples/68384/a48c82d694274496bcb249700a63ac2f/ISO-26262-2-2018.pdf) |
| 23 | ISO 26262 2nd Edition Overview Paper | Functional Safety | System Safety Lifecycle | Concept to SYS.5 | Reqs (FSR/TSR) | [PDF](https://www.researchgate.net/profile/Rami-Debouk/publication/331650722_Overview_of_the_2nd_Edition_of_ISO_26262_Functional_Safety-Road_Vehicles/links/5c8660fc299bf16918f61f43/Overview-of-the-2nd-Edition-of-ISO-26262-Functional-Safety-Road-Vehicles.pdf) |
| 24 | ISO 17387:2008 (LCDAS) | Operational Protocols | Lateral Control | SYS.2 / SYS.5 | Excluded | [PDF](https://cdn.standards.iteh.ai/samples/43654/701fd49bde7b4d3db165444b7c6f0c53/ISO-17387-2008.pdf) |
| 25 | ISO 17387:2026 (LCDAS) | Operational Protocols | Lateral Control | SYS.2 / SYS.5 | Reqs & Tests | [PDF](https://cdn.standards.iteh.ai/samples/iso/iso-17387-2026/a5178d14e8c1444a979194365813a103/iso-17387-2026.pdf) |
| 26 | ISO 21448:2022 (SOTIF) | Functional Safety | Functional Deficiencies | SYS.2 / SYS.4 / SYS.5 | Test Cases | [PDF](https://cdn.standards.iteh.ai/samples/77490/d9843a45e11947e0aa79aaf2f00b65a8/ISO-21448-2022.pdf) |
| 27 | ROHM ISO 26262 Safety Whitepaper | Functional Safety | Semiconductor / ASIL | SYS.2 / SWE.1 to SYS.4 | Reqs (ASIL/FTTI) | [PDF](https://fscdn.rohm.com/en/products/databook/white_paper/iso26262_wp-e.pdf) |
| 28 | MISRA Software Guidelines | Architecture & Constraints | Source Code Quality | SWE.3 / SWE.4 | Excluded | [Site](https://misra.org.uk/product-category/pdf-copies/) |
| 29 | AUTOSAR C++14 Guidelines | Architecture & Constraints | Source Code Quality | SWE.3 / SWE.4 | Excluded | [PDF](https://www.autosar.org/fileadmin/standards/R17-10_R1.2.0/AP/AUTOSAR_RS_CPP14Guidelines.pdf) |
| 30 | NHTSA ADAS Roadmap | Operational Protocols | Policy & Active Safety | SYS.1 (Stakeholder) | Excluded | [PDF](https://www.nhtsa.gov/sites/nhtsa.gov/files/2024-11/NCAP-Final-Decision-Notice-Advanced-Driver-Assistance-Systems-Roadmap-11182024-web.pdf) |
