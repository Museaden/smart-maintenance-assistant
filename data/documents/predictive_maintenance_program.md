# Predictive Maintenance Program Overview

## Mission
Maximize equipment availability while minimizing life-cycle cost through condition-based maintenance.

## PdM Technologies Deployed
1. Vibration analysis (monthly routes, continuous on critical)
2. Thermography (quarterly electrical, annual mechanical)
3. Oil analysis (quarterly on gearboxes, compressors, hydraulics)
4. Motor current signature analysis (annual on selected motors)
5. Ultrasonic leak detection (semi-annual on compressed air)
6. Process historian trending (continuous)

## Criticality Ranking
Assets ranked ABC per consequence × failure frequency matrix CRIT-MAT-01. A-rank: weekly PdM review. B-rank: monthly. C-rank: quarterly.

## Alert Management
Alerts route to maintenance planner. Response SLA:
- Critical: 4 hours
- High: 24 hours
- Medium: 72 hours
- Low: next scheduled window

## Integration with Smart Maintenance Assistant
The RAG chatbot provides procedural guidance from SOPs and manuals. It does not replace CMMS work orders or live sensor dashboards. Always confirm live readings before shutdown decisions.

## Continuous Improvement
Quarterly PdM review meeting: false positive rate, missed failures, cost avoidance metrics. Update thresholds in documentation when formally approved.

## Training Requirements
All maintenance techs: PdM awareness 4 hr annual. Route collectors: 16 hr vibration Level 1. Reliability engineers: advanced diagnostics.

## Budget
PdM cost center 4400. Includes oil lab, outside analysis, sensor batteries, and thermography contractor.


---


## Appendix: Predictive Maintenance Program Field Notes — Extended Reference

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
