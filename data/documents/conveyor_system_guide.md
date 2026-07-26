# Conveyor Belt System Maintenance Guide

## Systems Covered
- CV-100 through CV-108 (main product line)
- CV-200 through CV-204 (packaging feed)
- CV-300 (bulk material incline)

## Components
Drive pulley, tail pulley, idlers, belt, gearbox, motor, take-up, scrapers, and belt alignment sensors.

## Belt Tension
Correct tension: belt sag between idlers at 2% of span length. Over-tension reduces bearing and idler life; under-tension causes slip and heat.

## Alignment
Maximum belt mistrack: 25 mm from center at any point. Adjust take-up and idler frames incrementally. Never pry belt while running.

## Predictive Monitoring
- Drive motor current (slip indicator)
- Gearbox oil temperature
- Bearing vibration on drive and tail pulley
- Belt speed encoder vs. motor RPM (slip detection)

## Warning Signs
| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Current spike at start | Seized idler or material buildup | Inspect and clear |
| Belt wander to one side | Mistracking, worn idler, material on pulley | Align and clean |
| Burning smell | Slip, seized bearing | Stop conveyor — LOTO |
| Unusual noise at gearbox | Low oil, bearing wear | Sample oil; plan outage |

## Idler Replacement
Replace idlers when:
- Visual flat spots or seized rotation
- Shell wear >3 mm
- Noise on rotation hand test

## Scheduled Maintenance
- Daily: visual walk, listen, check scraper contact
- Weekly: lubricate take-up bearings
- Monthly: belt thickness measurement at three points
- Annually: gearbox oil change, laser alignment check

## Spare Parts
Belt spec CV-100: 1200 mm × EP400/3 × 5 mm. Order 6-week lead time. Keep one spare belt on site for CV-100 and CV-200 only.


---


## Appendix: Conveyor System Guide Field Notes — Extended Reference

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
