# Rotary Screw Air Compressor SOP (Compressors AC-1, AC-2, AC-3)

## Overview
Plant air compressors AC-1 (primary), AC-2 (secondary), and AC-3 (standby) supply 7-bar instrument and process air. This SOP defines monitoring thresholds, oil analysis, and predictive replacement triggers.

## Operating Limits
- Discharge pressure: 6.8–7.2 bar (normal)
- Oil sump temperature: 65–82°C (warning above 90°C)
- Aftercooler outlet: <40°C above ambient
- Motor amps: within 5% of baseline
- Specific power: <6.5 kW per 100 cfm (trend monthly)

## Daily Operator Checks
1. Check for oil leaks at separator tank, coolers, and hoses
2. Drain condensate traps — record volume (high volume indicates dryer issue)
3. Verify load/unload cycle is normal (AC-1 should not short-cycle <30 sec)
4. Read package discharge pressure and sump temperature from HMI

## Weekly Maintenance
- Clean cooler fins (compressed air, low pressure only)
- Inspect air intake filter — replace at 2.5 in. w.c. differential
- Check safety valve tag date

## Oil Analysis Program
Sample every 1,000 hours or quarterly. Send to lab with kit OIL-SAMPLE-AC.

| Parameter | Limit | Action |
|-----------|-------|--------|
| Viscosity change | >15% from new oil | Investigate overheating |
| Water content | >500 ppm | Check dryer and drains |
| Iron (Fe) | >50 ppm | Internal wear — borescope |
| Silicon | >20 ppm | Air filter breach |

## Predictive Triggers
Schedule major service when ANY of:
- Vibration at screw element bearings increases 25% over 90 days
- Oil iron trending up 3 consecutive samples
- Specific power degrades >8% from baseline
- Unplanned unload events >5 per shift

## Major Overhaul (Every 32,000 hours)
Replace screw element bearings, seals, oil, air filter, oil filter, and separator element. Verify pressure relief valve.

## Safety
Depressurize completely before opening oil circuit. Hot oil causes severe burns. Wear hearing protection (>85 dBA in compressor room).


---


## Appendix: Compressor Sop Field Notes — Extended Reference

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
