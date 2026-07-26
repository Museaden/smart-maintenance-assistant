# Chiller and Boiler Operations Maintenance Manual

## Chillers CH-1, CH-2 (Centrifugal, 500 Ton Each)

### Normal Operating Parameters
- Chilled water supply: 6.7°C (setpoint)
- Chilled water return: 12.8°C typical
- Condenser approach: <3°C above wet bulb
- Oil sump pressure: per manufacturer (Alfa CH spec sheet)
- Vibration: <3.5 mm/s on compressor

### Predictive Maintenance
- Refrigerant leak detection ultrasonic survey quarterly
- Oil analysis annually
- Motor winding insulation annual megger
- Economizer damper exercise monthly

### Alarms
High condenser pressure: check cooling tower, fouling, non-condensables. Low chilled pressure: verify expansion valve, refrigerant charge.

## Boilers BL-1, BL-2 (Fire Tube, 200 HP Steam)

### Daily Checks
- Blowdown bottom and surface skimmer per schedule
- Feedwater chemistry log (hardness, conductivity)
- Flame pattern observation port
- Stack temperature trend

### Water Treatment
Maintain phosphate and sulfite per chemist sheet. Conductivity blowdown when >3500 µS. Scale increases fuel cost 3% per 1 mm deposit.

### Safety Devices
Test low water cutoff weekly (shift change). Safety valve bench test annually by certified vendor. Flame safeguard test monthly.

### Predictive Indicators
| Parameter | Limit | Action |
|-----------|-------|--------|
| Stack temp rise | >40°C above baseline | Tube fouling — schedule cleaning |
| Feedwater O2 | >10 ppb | Deaerator inspection |
| Blowdown rate | >5% make-up | Investigate leaks or treatment |

## Seasonal Changeover
Spring: chiller startup checklist CHK-CH-01. Fall: boiler startup CHK-BL-01. Allow 72-hour stabilization before performance test.


---


## Appendix: Chiller Boiler Operations Field Notes — Extended Reference

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
