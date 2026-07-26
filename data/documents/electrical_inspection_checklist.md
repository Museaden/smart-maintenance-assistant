# Electrical Panel and Distribution Inspection Checklist

## Scope
Main switchgear MS-1, distribution panels DP-A through DP-F, MCC buckets for lines 1–6.

## Monthly Thermographic Survey
- Scan all breakers >100 A under >40% load
- Delta-T alarm: 15°C above adjacent phases or ambient reference
- Document hot spots with photo and load at time of scan

## Quarterly Physical Inspection
1. Torque check line-side terminations (per torque table TQ-EL-01)
2. Inspect for discoloration, moisture, pest intrusion
3. Test arc flash labels present and legible
4. Verify ventilation fans on MCC operate

## Insulation Testing (Annual)
- Bus insulation resistance phase-to-ground
- Trip test ground fault relays per schedule
- Calibrate protective relays per manufacturer interval

## Predictive Indicators
| Indicator | Threshold | Action |
|-----------|-----------|--------|
| Breaker trip count | >3 nuisance trips/month | Investigate inrush or fault |
| Harmonic THD | >8% on feeder | Power quality study |
| Panel temp | >45°C internal | Improve ventilation |
| Partial discharge | Any increase | Specialist assessment |

## Safety
Only qualified electricians (NFPA 70E trained) open energized panels. Full PPE per arc flash label. Never defeat interlocks.

## Documentation
Use form EL-INSP-04 in CMMS. Link thermography images to asset record.


---


## Appendix: Electrical Inspection Checklist Field Notes — Extended Reference

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
