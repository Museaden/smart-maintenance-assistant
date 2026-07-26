# Electric Motor Maintenance Manual (Motors M-01 through M-24)

## 1. Scope and Purpose

This manual covers preventive and predictive maintenance for three-phase induction motors rated 5–250 HP across Production Halls A and B. It supports maintenance technicians, reliability engineers, and the Smart Maintenance Assistant decision-support system.

### 1.1 Applicable Equipment
- Line motors M-01 to M-12 (conveyor drives)
- Pump motors M-13 to M-18 (process pumps)
- Fan motors M-19 to M-24 (HVAC and exhaust)

### 1.2 Document Control
Revision 3.2 | Effective date: January 2026 | Owner: Reliability Engineering

## 2. Operating Parameters

### 2.1 Normal Operating Ranges
| Parameter | Normal | Warning | Critical |
|-----------|--------|---------|----------|
| Bearing temperature | 40–70°C | 70–85°C | >85°C |
| Winding temperature (RTD) | 50–90°C | 90–110°C | >110°C |
| Vibration (ISO 10816) | <2.8 mm/s | 2.8–7.1 mm/s | >7.1 mm/s |
| Current imbalance | <5% | 5–10% | >10% |
| Insulation resistance | >100 MΩ | 10–100 MΩ | <10 MΩ |

### 2.2 Nameplate Verification
At commissioning and after any rewind, verify nameplate data against the CMMS asset record: voltage, full-load amps, service factor, insulation class, and bearing part numbers.

## 3. Predictive Maintenance Sensors

Each critical motor (M-01 through M-18) is instrumented with:
1. Dual bearing temperature RTDs (drive end and non-drive end)
2. Winding temperature RTD (where fitted)
3. Vibration sensor at drive-end bearing housing
4. Current transducer on one phase (trend all three during quarterly inspection)

Data is logged to the historian at 1-minute intervals. The predictive model flags motors when vibration and temperature trends exceed baseline by more than 15% over 14 days.

## 4. Inspection Procedures

### 4.1 Weekly Visual Inspection (15 minutes per motor group)
- Listen for abnormal noise (grinding, squealing, humming changes)
- Check for oil leaks at bearing housings
- Verify cooling fan is intact and rotating
- Inspect coupling guard and foundation bolts
- Record any odor (overheated insulation, burnt grease)

### 4.2 Monthly Detailed Inspection
- Measure vibration at DE and NDE bearing points (horizontal, vertical, axial)
- Compare current draw to baseline at known load
- Inspect air gaps and cooling passages for dust buildup
- Verify lubrication fittings are accessible and capped

### 4.3 Quarterly Electrical Tests
- Insulation resistance (megger) phase-to-ground and phase-to-phase
- Polarization index for motors >50 HP
- Thermographic survey of terminations and junction boxes

## 5. Lubrication

### 5.1 Grease Type
Use lithium complex grease NLGI Grade 2, per specification LUB-G2-LC. Do not mix grease types.

### 5.2 Relubrication Interval
| Bearing type | Interval | Quantity |
|--------------|----------|----------|
| Shielded rolling element | 8,000 hours | Per manufacturer chart |
| Open rolling element | 4,000 hours | Per manufacturer chart |
| Sleeve (oil ring) | Continuous | Maintain sight glass mid-point |

### 5.3 Over-greasing Risk
Over-greasing is a leading cause of bearing failure. Purge old grease through relief plug; run motor 30 minutes before reinstalling plug.

## 6. Failure Modes and Diagnostics

### 6.1 Bearing Defects
High-frequency vibration peaks at bearing defect frequencies indicate inner race, outer race, ball, or cage defects. Schedule replacement within 7 days if vibration exceeds 7.1 mm/s and temperature is rising.

### 6.2 Stator Winding Issues
Increasing current at constant load, hot spots on thermal imaging, or decreasing insulation resistance suggest winding deterioration. Plan outage for surge testing.

### 6.3 Rotor Bar Defects
Sidebands around running speed in spectrum at ± slip frequency × pole pass. May cause torque pulsation and accelerated coupling wear.

### 6.4 Misalignment
2× running speed dominant in axial vibration. Correct alignment to within 0.05 mm offset and 0.05 mm/100 mm angularity.

## 7. Maintenance Decision Matrix

| Risk score | Indicators | Recommended action |
|------------|------------|-------------------|
| Low (0–30) | All parameters normal | Continue monitoring |
| Medium (31–60) | One warning parameter | Inspect within 72 hours |
| High (61–85) | Two warnings or one critical | Plan maintenance within 1 week |
| Urgent (86–100) | Critical vibration/temp or imminent failure | Shutdown if safe; emergency work order |

## 8. Spare Parts
- Bearing sets: catalog section MOT-BRG in CMMS
- Coupling inserts: verify bore size before ordering
- Space heaters: replace if insulation resistance <2 MΩ when cold

## 9. Safety
LOTO per site standard EHS-LOTO-001 before any contact with rotating or electrical components. Never bypass thermal overloads.

## 10. Records
Log all readings in CMMS work order. Attach vibration spectra for any out-of-spec finding. Smart Maintenance Assistant queries this manual for threshold guidance.


---


## Appendix: Motor Inspection Checklists — Extended Reference

### Monthly Route Checklist

- [ ] Record DE bearing vibration (H, V, A axes)
- [ ] Record NDE bearing vibration
- [ ] Measure all three phase currents at stable load
- [ ] IR scan junction box and cable terminations
- [ ] Verify cooling fan rotation and guard secure
- [ ] Check foundation grout for cracks
- [ ] Listen for rubbing or scraping at coupling
- [ ] Compare RTD readings to handheld IR gun
- [ ] Log ambient temperature and humidity
- [ ] Update CMMS with pass/fail per threshold table

### Troubleshooting Guide

| Symptom | Probable cause | Corrective action |
|---------|----------------|-------------------|
| High vibration 1x | Unbalance | Balance rotor; check for buildup on fan |
| High vibration 2x | Misalignment | Laser align; inspect soft foot |
| Hot bearing one end | Lubrication failure | Regrease; check seal and contamination |
| High current all phases | Overload or voltage imbalance | Check supply; reduce load |
| Insulation resistance drop | Moisture or contamination | Dry out; clean windings |
| Bearing noise increasing | Defect developing | Schedule replacement; increase monitoring |

### Historical Baseline Notes

Establish baseline within 30 days of installation or major repair. Store spectra, photos, and megger readings in CMMS asset folder. Review baseline annually or after any process change affecting load. Motors M-07 and M-14 serve variable torque loads — use speed-corrected vibration limits.


---


## Appendix A: Vibration Measurement Points

Measure at bearing housing closest to load. Use magnetic base accelerometer, 10–1000 Hz range for overall, 500–10000 Hz for bearing defects.

## Appendix B: Motor Current Baseline Table

Establish baseline within first 30 days of operation or after major repair. Record at 25%, 50%, 75%, and 100% load where variable speed drives permit.

## Appendix C: Escalation Contacts

Reliability Engineer on-call: extension 4200. Electrical maintenance supervisor: extension 4105. After-hours: site operations center.


---


## Appendix: Motor Maintenance Manual Field Notes — Extended Reference

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
