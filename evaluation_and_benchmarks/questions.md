# Benchmark Questions (20)

Gold answers are grounded in `data/documents/`. Use this list for demos, manual grading, or portfolio evidence.

| ID | Category | Question | Gold answer (summary) | Primary source |
|----|----------|----------|----------------------|----------------|
| **Q01** | pump | What vibration level is critical for Pump-3? | Above **7.0 mm/s RMS**; reduce load; plan bearing replacement within **24 hours** | `pump_maintenance_sop.md` |
| **Q02** | pump | What is the warning vibration range for Pump-3, and when should inspection be scheduled? | **4.5–7.0 mm/s RMS**; inspect within **72 hours** | `pump_maintenance_sop.md` |
| **Q03** | pump | What bearing housing temperature is critical for Pump-3? | Above **80°C**; stop if process allows | `pump_maintenance_sop.md` |
| **Q04** | pump | What indicates high bearing failure risk for Pump-3 within 7 days? | Vib **>6.5** for 3+ readings **and** temp **>75°C** **and** **>800** hours since service | `pump_maintenance_sop.md` |
| **Q05** | hvac | When should I replace HVAC Unit-7 filters? | DP **>1.2 in. w.c.** or typically **90 days** | `hvac_unit7_manual.md` |
| **Q06** | hvac | What should I do if HVAC Unit-7 motor current exceeds 20A? | Warning above **20 A** — inspect filters/belts/coil; critical above **24 A** | `hvac_unit7_manual.md` |
| **Q07** | hvac | What supply-to-return air temperature difference indicates a cooling problem on HVAC Unit-7? | Delta-T **below 8°C for >48 hours** → check refrigerant/coil | `hvac_unit7_manual.md` |
| **Q08** | motor | What are the critical vibration and bearing temperature limits for plant electric motors? | Vib **>7.1 mm/s**; bearing temp **>85°C** | `motor_maintenance_manual.md` |
| **Q09** | motor | What grease type should be used for electric motor bearings, and what is the risk of over-greasing? | Lithium complex **NLGI 2**; over-greasing causes bearing failure | `motor_maintenance_manual.md` |
| **Q10** | bearing | What indicates high bearing failure risk and when should a bearing be replaced rather than monitored? | Rising vib **>10%/week**, critical temp, or **spalling**/noise/play → replace | `bearing_failure_guide.md` |
| **Q11** | compressor | What is the normal discharge pressure range for plant air compressors AC-1 through AC-3? | **6.8–7.2 bar** | `compressor_sop.md` |
| **Q12** | compressor | At what oil iron (Fe) level should compressor internal wear be investigated? | Fe **>50 ppm** → borescope | `compressor_sop.md` |
| **Q13** | conveyor | What is the maximum allowed belt mistrack on the conveyor systems? | **25 mm** from center | `conveyor_system_guide.md` |
| **Q14** | conveyor | When should conveyor idlers be replaced? | Seized/flat spots, shell wear **>3 mm**, or noisy hand test | `conveyor_system_guide.md` |
| **Q15** | safety | What are the seven steps of the site lockout/tagout procedure EHS-LOTO-001? | Notify → shut down → isolate → lock/tag → release stored energy → verify zero energy → work | `safety_loto_procedures.txt` |
| **Q16** | safety | Who may authorize emergency removal of a LOTO lock, and what form is used? | **Plant manager** only; form **LOTO-EMR-01** | `safety_loto_procedures.txt` |
| **Q17** | pdm | What are the PdM alert response SLAs for critical and high severity alerts? | Critical **4 h**; High **24 h** (Medium 72 h) | `predictive_maintenance_program.md` |
| **Q18** | vibration | According to the vibration handbook severity chart, what mm/s RMS range is unsatisfactory and requires planned repair? | **7.1–18 mm/s** unsatisfactory; **>18** unacceptable | `vibration_analysis_handbook.md` |
| **Q19** | fault_codes | What does fault code VIB-CRIT-01 mean in the condition monitoring system? | Vibration exceeded **critical** threshold (variant 1) | `fault_code_reference.md` |
| **Q20** | compliance | Which site LOTO standard must maintenance follow for OSHA 1910.147 compliance? | Site standard **EHS-LOTO-001** | `regulatory_compliance_guide.md` |

## How to ask in the chat UI

Copy any **Question** cell into Streamlit and compare the assistant answer + Sources expander to the gold answer and primary source.
