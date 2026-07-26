# Vibration Analysis Handbook for Maintenance Technicians

## Introduction
Vibration analysis is a core predictive maintenance technology. This handbook explains measurement, basic fault diagnosis, and when to escalate to the reliability team.

## Measurement Standards
Follow ISO 10816 for general machinery and ISO 7919 for shaft vibration where applicable.

### Sensor Mounting
- Stud mount preferred for repeatability
- Magnetic mount acceptable for route data
- Hand-held probe: trend only, not for acceptance testing

### Route Frequencies
Overall velocity (mm/s RMS): 10–1000 Hz
Acceleration for bearings: 500–10000 Hz envelope demodulation

## Common Fault Frequencies
| Fault | Frequency characteristic |
|-------|-------------------------|
| Unbalance | 1× running speed, radial dominant |
| Misalignment | 2× running speed, axial increase |
| Looseness | harmonics of 1×, unstable phase |
| Bearing outer race | BPFO non-synchronous |
| Bearing inner race | BPFI non-synchronous |
| Gear mesh | GMF = teeth × RPM |

## Severity Chart (General Guide)
| mm/s RMS | Severity |
|----------|----------|
| 0–2.8 | Good |
| 2.8–7.1 | Satisfactory — increase monitoring |
| 7.1–18 | Unsatisfactory — plan repair |
| >18 | Unacceptable — consider shutdown |

## Trending Rules
A 20% increase over 30 days warrants investigation. A doubling within 90 days warrants planned replacement before next production peak.

## Reporting
Attach spectrum and waveform to CMMS. Note RPM, load, and operating conditions. Compare to last 6 readings.

## Training
Level 1 analysts: overall readings and alarm response. Level 2: spectra interpretation. Level 3: modal and advanced diagnostics — Reliability team only.


---


## Appendix: Vibration Analysis Handbook Field Notes — Extended Reference

### Pre-Work Verification

- [ ] Confirm correct asset ID and equipment is stopped
- [ ] Verify LOTO applied per EHS-LOTO-001
- [ ] Review last 30 days historian trends
- [ ] Check open work orders for duplicate work
- [ ] Confirm spare parts on hand or PR issued
- [ ] Notify production of estimated downtime

### Post-Work Verification

- [ ] Remove all tools and materials from work area
- [ ] Restore guards and interlocks
- [ ] Remove LOTO per procedure — each worker own lock
- [ ] Test run at no load then under load
- [ ] Record as-found and as-left readings in CMMS
- [ ] Update predictive baseline if component replaced

### Related Documents

Cross-reference: lubrication_standards.md, vibration_analysis_handbook.md, safety_loto_procedures.txt, spare_parts_inventory_policy.txt, predictive_maintenance_program.md.
