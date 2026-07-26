"""One-time generator for the maintenance document corpus (30–120 pages)."""

from pathlib import Path

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "documents"


def write(name: str, content: str) -> None:
    path = DOCS_DIR / name
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"  wrote {name} ({len(content):,} chars)")


def page_break() -> str:
    return "\n\n---\n\n"


def sanitize_for_pdf(text: str) -> str:
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2022": "-",
        "\u00b0": " deg",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def expand_appendix(title: str, sections: list[tuple[str, str]]) -> str:
    """Add detailed appendix sections to reach target document length."""
    parts = [page_break(), f"## Appendix: {title} — Extended Reference\n"]
    for heading, body in sections:
        parts.append(f"### {heading}\n\n{body.strip()}\n")
    return "\n".join(parts)


def checklist_block(items: list[str]) -> str:
    return "\n".join(f"- [ ] {item}" for item in items)


def troubleshooting_table(rows: list[tuple[str, str, str]]) -> str:
    lines = ["| Symptom | Probable cause | Corrective action |", "|---------|----------------|-------------------|"]
    for sym, cause, action in rows:
        lines.append(f"| {sym} | {cause} | {action} |")
    return "\n".join(lines)


MOTOR_APPENDIX = expand_appendix(
    "Motor Inspection Checklists",
    [
        ("Monthly Route Checklist", checklist_block([
            "Record DE bearing vibration (H, V, A axes)",
            "Record NDE bearing vibration",
            "Measure all three phase currents at stable load",
            "IR scan junction box and cable terminations",
            "Verify cooling fan rotation and guard secure",
            "Check foundation grout for cracks",
            "Listen for rubbing or scraping at coupling",
            "Compare RTD readings to handheld IR gun",
            "Log ambient temperature and humidity",
            "Update CMMS with pass/fail per threshold table",
        ])),
        ("Troubleshooting Guide", troubleshooting_table([
            ("High vibration 1x", "Unbalance", "Balance rotor; check for buildup on fan"),
            ("High vibration 2x", "Misalignment", "Laser align; inspect soft foot"),
            ("Hot bearing one end", "Lubrication failure", "Regrease; check seal and contamination"),
            ("High current all phases", "Overload or voltage imbalance", "Check supply; reduce load"),
            ("Insulation resistance drop", "Moisture or contamination", "Dry out; clean windings"),
            ("Bearing noise increasing", "Defect developing", "Schedule replacement; increase monitoring"),
        ])),
        ("Historical Baseline Notes", (
            "Establish baseline within 30 days of installation or major repair. "
            "Store spectra, photos, and megger readings in CMMS asset folder. "
            "Review baseline annually or after any process change affecting load. "
            "Motors M-07 and M-14 serve variable torque loads — use speed-corrected vibration limits."
        )),
    ],
)


def motor_manual() -> str:
    return """
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
""" + MOTOR_APPENDIX + page_break() + """
## Appendix A: Vibration Measurement Points

Measure at bearing housing closest to load. Use magnetic base accelerometer, 10–1000 Hz range for overall, 500–10000 Hz for bearing defects.

## Appendix B: Motor Current Baseline Table

Establish baseline within first 30 days of operation or after major repair. Record at 25%, 50%, 75%, and 100% load where variable speed drives permit.

## Appendix C: Escalation Contacts

Reliability Engineer on-call: extension 4200. Electrical maintenance supervisor: extension 4105. After-hours: site operations center.
"""


def compressor_sop() -> str:
    return """
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
"""


def conveyor_guide() -> str:
    return """
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
"""


def lubrication_standards() -> str:
    return """
# Plant Lubrication Standards and Procedures

## 1. Purpose
Standardize lubricant selection, application, storage, and contamination control across all rotating equipment.

## 2. Lubricant Storage
- Store indoors, 10–30°C, lids sealed
- FIFO inventory; max shelf life 24 months sealed
- Color-code transfer containers: hydraulic (blue), grease (yellow), gear oil (green)
- Filter all bulk transfers to ISO 4406 18/16/13 or better

## 3. Approved Lubricants by Application
| Application | Product code | Viscosity | Notes |
|-------------|--------------|-----------|-------|
| General bearing grease | LUB-G2-LC | NLGI 2 | Motors, fans |
| High-temp bearing | LUB-G2-HT | NLGI 2 | Oven fans |
| Hydraulic systems | LUB-HYD-46 | ISO VG 46 | Presses, lifts |
| Gearboxes | LUB-GEAR-220 | ISO VG 220 | Conveyors |
| Compressor oil | LUB-AC-SR | Synthetic | Screw compressors only |

## 4. Contamination Control
Particle contamination causes 60–80% of hydraulic and bearing failures. Use breathers with 3 µm filtration on all bulk tanks. Sample oil annually minimum.

## 5. Grease Application Methods
- Manual gun: slow strokes, purge until clean grease appears
- Automatic single-point: verify dispense rate monthly
- Never use grease fittings without knowing required quantity

## 6. Oil Change Criteria
Change oil when:
- Scheduled interval reached
- Water >500 ppm (hydraulic)
- Viscosity change >10%
- Acid number doubles from new oil baseline

## 7. Predictive Integration
Oil sample due dates are in CMMS. Smart Maintenance Assistant can answer lubrication type questions by equipment ID when cross-referenced with asset records.

## 8. Disposal
Used oil to waste oil tank WO-01. Contaminated rags in fire-rated bins. SDS sheets at lubricant store kiosk.
"""


def vibration_handbook() -> str:
    return """
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
"""


def electrical_inspection() -> str:
    return """
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
"""


def cmms_procedures() -> str:
    return """
# CMMS Data Logging and Work Order Procedures

## Purpose
Ensure maintenance decisions, sensor data, and completed work are recorded consistently for regulatory compliance and predictive model training.

## Work Order Types
- PM: preventive maintenance (scheduled)
- PdM: predictive (condition-triggered)
- CM: corrective (breakdown)
- EM: emergency

## Required Fields
Every closed work order must include:
1. Asset ID (matches historian tag)
2. Failure code (if applicable) from taxonomy FC-100
3. Cause code and remedy code
4. Parts consumed with lot numbers
5. Labor hours by craft
6. Machine condition at start and end (running/stopped)
7. Attachments: photos, spectra, oil reports

## Sensor Data Linking
When closing PdM work orders, reference the alert ID from the condition monitoring system. This closes the loop for model accuracy review.

## Downtime Recording
Record downtime in minutes. Classify as: planned, unplanned operational, unplanned maintenance.

## Smart Maintenance Assistant Integration
The RAG chatbot retrieves SOP thresholds from this document corpus. Technicians should verify chatbot recommendations against current CMMS asset status before execution.

## Audit Trail
No deletion of closed work orders. Corrections via supplemental note with supervisor approval.

## KPIs
- PM compliance: target >95%
- PdM findings acted within SLA: 90%
- Repeat failure rate: <5% per asset class quarterly
"""


def emergency_procedures() -> str:
    return """
# Emergency Response and Equipment Shutdown Procedures

## Emergency Classification
- Level 1: imminent injury or major environmental release — evacuate and call 911
- Level 2: equipment failure with production/safety risk — controlled shutdown
- Level 3: degraded operation — continue with monitoring

## Authorized Shutdown Authority
Operators: Level 2 for their line only. Maintenance supervisor: all plant equipment. Plant manager: full site.

## Critical Equipment Shutdown Sequence (Process Line 1)
1. Stop feed at upstream interlock
2. Run out product on conveyor CV-100 (max 5 min)
3. Stop main drive M-01 via HMI emergency stop
4. Close isolation valves V-101, V-102
5. Depressurize vessel P-101 per SOP PRESS-REL-01
6. LOTO at MCC bucket L1-DRV-01

## Post-Emergency
Do not restart until maintenance releases equipment. Complete incident report IR-01 within 24 hours. Preserve historian data for 30 days.

## Fire Involving Electrical Equipment
Use CO2 or dry chemical only. De-energize if safe. Do not use water on energized panels.

## Spill Response
Chemical spills: refer to SDS and spill kit SK-CHEM at column locations. Hydraulic oil: diatomaceous earth, notify EHS.

## Communication
Site PA code: "Code Orange" = equipment emergency. Radio channel 2 for maintenance response team.
"""


def sensor_calibration() -> str:
    return """
# Sensor Calibration and Validation Guide

## Instrumentation Scope
Temperature RTDs and thermocouples, pressure transmitters, vibration accelerometers, current loops, and flow meters on critical assets.

## Calibration Intervals
| Sensor type | Interval | Method |
|-------------|----------|--------|
| RTD (critical) | 12 months | Ice bath / dry block |
| Pressure 4–20 mA | 12 months | Dead-weight or calibrator |
| Vibration | 24 months | Reference shaker or factory return |
| Current CT | 24 months | Clamp meter comparison |
| Proximity probes | 24 months | Micrometer gap check |

## As-Found / As-Left
Record both readings. If as-found error >2× accuracy spec, investigate process impact for period since last calibration.

## Out-of-Tolerance Response
1. Tag sensor "OUT OF CAL — DO NOT USE FOR SAFETY INTERLOCK"
2. Open calibration work order within 24 hours
3. Review historian data; flag affected predictive alerts for manual review

## NIST Traceability
All reference standards must have current NIST-traceable certificates on file in Metrology shop.

## Spare Sensor Policy
Critical loops maintain one spare calibrated sensor on shelf. Shelf life: recalibrate if >12 months on shelf.

## Documentation
Form CAL-10 in CMMS. Attach certificate PDF. Update asset calibration due date automatically.
"""


def pdm_program() -> str:
    return """
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
"""


def chiller_boiler() -> str:
    return """
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
"""


def gearbox_manual() -> str:
    return """
# Industrial Gearbox Maintenance Manual

## Assets
Gearboxes GB-01 through GB-45 on conveyors, mixers, and agitators.

## Types
- Helical reducers (majority)
- Worm gears (low-speed agitators)
- Planetary (high torque compact drives)

## Oil Level and Condition
Check level weekly via sight glass or dipstick. Oil color should be clear amber; dark oil or metallic glitter indicates wear.

## Oil Change Interval
First change at 500 hours, then every 2,500 hours or per oil analysis. Synthesize worm gear oil separately — do not use EP gear oil on bronze worms unless specified.

## Vibration Limits
ISO 10816 Group 2: alarm at 7.1 mm/s, trip planning at 11 mm/s on bearing caps.

## Common Failures
1. Micropitting on gear teeth — lubricant film breakdown
2. Spalling — overload or misalignment
3. Seal leak — shaft wear or improper install
4. Bearing failure — contamination or brinelling from VFD-induced currents (use grounding ring)

## Alignment
Input and output shaft alignment to driver and driven equipment per coupling manufacturer. Laser align after any gearbox replacement.

## Breathers
Use desiccant breathers DB-01 on all gearboxes in washdown areas. Replace desiccant when color changes to pink.

## Repair vs. Replace
If gear contact pattern shows >30% wear or backlash exceeds manufacturer limit, replace unit. Field rebuild only by approved vendor for A-rank assets.
"""


def safety_loto_txt() -> str:
    return """
LOCKOUT/TAGOUT PROCEDURES — SITE STANDARD EHS-LOTO-001
========================================================

1. PURPOSE
Protect personnel from unexpected energization during maintenance.

2. SCOPE
All equipment with electrical, pneumatic, hydraulic, thermal, chemical, or gravitational energy.

3. PROCEDURE (SEVEN STEPS)
   a. Notify affected personnel
   b. Shut down equipment using normal stopping procedure
   c. Isolate all energy sources
   d. Apply locks and tags (one person, one lock per energy source)
   e. Release stored energy (bleed, block, dissipate)
   f. Verify zero energy (try start, check voltage, check pressure)
   g. Perform work

4. GROUP LOTO
Complex jobs use group lockbox. Lead craft holds key. Each worker applies personal lock to box.

5. SHIFT CHANGE
Outgoing worker removes only their lock after briefing incoming worker who applies their lock.

6. PROHIBITED
Never use someone else's lock. Never defeat interlocks without written MOC. Never test machine with guards removed.

7. PREDICTIVE MAINTENANCE NOTE
Sensor installation on running equipment requires alternative safeguards per risk assessment RA-LOTO-09.

8. TRAINING
Annual refresher required. Contractors must sign LOTO acknowledgment before site access.

9. AUDIT
EHS audits 10% of LOTO jobs monthly. Deficiencies corrected within 48 hours.

10. EMERGENCY REMOVAL OF LOCK
Only plant manager may authorize. Investigate incident. Document on form LOTO-EMR-01.
"""


def spare_parts_txt() -> str:
    return """
SPARE PARTS INVENTORY POLICY — MAINTENANCE DEPARTMENT
======================================================

CRITICALITY CLASSES
  A — Stock on site, 0 day lead time target
  B — Stock on site or consignment, 3 day lead
  C — Order on demand, 14+ day lead

MINIMUM STOCK LEVELS (EXAMPLES)
  Pump-3 bearing set BRG-P3-220     : 2 units (Class A)
  HVAC Unit-7 filter FILT-U7-MERV13 : 4 sets (Class A)
  Motor M-01 coupling insert        : 1 unit (Class B)
  Gearbox GB-12 seal kit            : 1 kit (Class B)
  Compressor AC-1 separator element : 1 unit (Class A)

REORDER TRIGGERS
  When quantity on hand = reorder point, CMMS auto-generates PR.
  Review reorder points quarterly based on consumption and lead time.

STORAGE
  Bearings in climate-controlled crib, vibration-free shelf.
  Belts coiled, no sharp bends. Seals in original packaging, <24 months.

KITTING
  Major outages use pre-kitted BOM in CMMS. Kit location tagged on asset page.

OBSOLESCENCE
  Review slow-moving stock (>2 years no issue) annually. Redistribute or scrap per finance.

SMART MAINTENANCE ASSISTANT
  Chatbot may cite part numbers from SOPs. Always verify stock in CMMS before promising downtime.
"""


def scheduling_policy_txt() -> str:
    return """
MAINTENANCE SCHEDULING POLICY
=============================

OBJECTIVE
Balance production demand with equipment reliability through integrated planning.

PLANNING HORIZON
  Weekly — operations coordination meeting (Monday 09:00)
  Monthly — PM schedule freeze for next calendar month
  Quarterly — major outage window negotiation with production

WORK PRIORITIZATION
  1. Safety and regulatory compliance
  2. Emergency breakdowns
  3. Predictive alerts (Critical > High > Medium)
  4. Scheduled PM
  5. Discretionary improvements

WINDOW ALLOCATION
  Production Line 1: Saturday 06:00–18:00 default maintenance window
  Line 2: Sunday same hours
  Utilities (boiler/chiller): Tuesday night 22:00–06:00

RESOURCE PLANNING
  Planner assigns craft by skill matrix. Minimum 2 electricians for MCC work.
  Overtime requires maintenance manager approval.

DEFERRAL RULES
  PM may defer once max 14 days with production VP approval.
  PdM Critical alerts cannot defer without reliability engineer sign-off.
  Deferred work auto-escalates to red flag in weekly meeting.

METRICS
  Schedule compliance, wrench time, backlog weeks, PM/PdM ratio target 60/40.

DOCUMENTATION
  Schedule changes logged in CMMS with reason code.
"""


def transformer_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Transformer Maintenance Guide</title>
</head>
<body>
<h1>Transformer Maintenance Guide (T-01 through T-06)</h1>

<h2>1. Overview</h2>
<p>This guide covers oil-filled and dry-type distribution transformers serving Production and Utilities. Predictive maintenance focuses on oil quality, thermal performance, and electrical testing.</p>

<h2>2. Oil-Filled Transformers (T-01, T-02, T-03)</h2>
<h3>2.1 Dissolved Gas Analysis (DGA)</h3>
<p>Sample annually; quarterly for transformers &gt;5 MVA or &gt;20 years age. Key gases:</p>
<ul>
  <li><strong>Hydrogen (H2):</strong> partial discharge or corona — investigate if &gt;100 ppm</li>
  <li><strong>Acetylene (C2H2):</strong> arcing — immediate investigation if &gt;5 ppm</li>
  <li><strong>Ethylene (C2H4):</strong> oil overheating — trend with temperature</li>
</ul>

<h3>2.2 Oil Physical Tests</h3>
<table border="1" cellpadding="6">
  <tr><th>Test</th><th>Limit</th><th>Action</th></tr>
  <tr><td>Dielectric strength</td><td>&gt;30 kV</td><td>Filter or replace oil</td></tr>
  <tr><td>Moisture</td><td>&lt;20 ppm</td><td>Dry-out procedure</td></tr>
  <tr><td>Acidity</td><td>&lt;0.15 mg KOH/g</td><td>Oil reclamation</td></tr>
</table>

<h3>2.3 Visual Inspection (Quarterly)</h3>
<ul>
  <li>Check silica gel breather — replace when 60% discolored</li>
  <li>Inspect bushings for cracks or tracking</li>
  <li>Listen for unusual hum (loose laminations)</li>
  <li>Verify cooling fans and pumps operate</li>
</ul>

<h2>3. Dry-Type Transformers (T-04, T-05, T-06)</h2>
<p>Thermography monthly under load. Hot spot &gt;10°C above similar phase requires internal inspection at outage.</p>
<p>Vacuum clean coils annually. Maintain room ventilation; ambient max 40°C.</p>

<h2>4. Electrical Tests (Annual)</h2>
<ul>
  <li>Insulation power factor (tip-up test)</li>
  <li>Turns ratio and excitation current</li>
  <li>DC winding resistance balance</li>
</ul>

<h2>5. Predictive Alerts</h2>
<p>Integrate top oil temperature trend with load. Sudden increase at constant load suggests cooling failure or internal fault development.</p>

<h2>6. Safety</h2>
<p>Assume all bushings energized. Minimum approach distance per voltage class. Only qualified high-voltage technicians perform switching.</p>

<h2>7. Spares</h2>
<p>Fuses, silica gel, gasket sets on shelf TR-SPARE-KIT. Full transformer replacement lead time 16–24 weeks — maintain contingency plan.</p>
</body>
</html>
"""


def hydraulic_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Hydraulic Systems Maintenance Guide</title>
</head>
<body>
<h1>Hydraulic Systems Maintenance Guide</h1>

<h2>Systems</h2>
<ul>
  <li>HYD-01 — Press line 1000 ton</li>
  <li>HYD-02 — Scrap baler</li>
  <li>HYD-03 — Mobile lift table bank</li>
</ul>

<h2>Fluid Specification</h2>
<p>ISO VG 46 anti-wear hydraulic oil, cleanliness target ISO 4406 code 18/16/13. Never mix viscosities or brands without flushing.</p>

<h2>Operating Parameters</h2>
<table border="1" cellpadding="6">
  <tr><th>Parameter</th><th>Normal</th><th>Alarm</th></tr>
  <tr><td>Reservoir temperature</td><td>40–55°C</td><td>&gt;65°C</td></tr>
  <tr><td>Pressure at relief setting</td><td>Design ±5%</td><td>Drift &gt;10%</td></tr>
  <tr><td>Pump case drain flow</td><td>Baseline</td><td>2× baseline</td></tr>
  <tr><td>Filter differential</td><td>&lt;2 bar</td><td>&gt;3 bar — change element</td></tr>
</table>

<h2>Daily Checks</h2>
<ol>
  <li>Reservoir level at temperature line</li>
  <li>Listen for cavitation at pump inlet</li>
  <li>Scan for external leaks</li>
  <li>Check accumulator pre-charge monthly (nitrogen)</li>
</ol>

<h2>Oil Analysis</h2>
<p>Quarterly samples. Elevated silicon indicates dirt ingress; iron indicates pump or valve wear. Water &gt;500 ppm risks cavitation and corrosion.</p>

<h2>Common Failures</h2>
<ul>
  <li><strong>Pump wear:</strong> increasing noise, flow loss, case drain flow up</li>
  <li><strong>Valve sticking:</strong> slow cycles, heat at relief valve</li>
  <li><strong>Cylinder seal bypass:</strong> drift under load, oil on rod</li>
  <li><strong>Contamination:</strong> valve spool scoring, filter clogging</li>
</ul>

<h2>Preventive Tasks</h2>
<p>Change return filters at 3 bar differential or 2,000 hours. Replace suction strainer at major overhaul only. Hose replacement every 5 years or per manufacturer.</p>

<h2>Safety</h2>
<p>Depressurize before disconnecting lines. Fluid injection injuries are medical emergencies. Use cardboard for leak search, not hands.</p>
</body>
</html>
"""


PDF_SOURCES = {
    "cooling_tower_operations.pdf": """
COOLING TOWER OPERATIONS AND MAINTENANCE MANUAL
CT-1 and CT-2 — Induced Draft Counterflow

1. PURPOSE
Maintain heat rejection capacity for chillers and process cooling. Predictive focus: fan vibration, gearbox oil, basin water quality, and fill condition.

2. OPERATING PARAMETERS
  Approach temperature: design 5-7 F above wet bulb
  Basin water temperature: 29-35 C typical summer
  Fan motor current: within 10% of baseline
  Blowdown rate: maintain conductivity per water treatment sheet

3. DAILY OPERATOR ROUNDS
  - Inspect fan operation and unusual vibration
  - Check drift eliminator carryover (excess water loss)
  - Verify chemical feed pumps operating
  - Record basin level and makeup water meter

4. WEEKLY MAINTENANCE
  - Clean suction strainer
  - Inspect belt tension on fan drive (if belt-driven)
  - Check gearbox oil level and leaks
  - Sample basin water for Legionella protocol per health code

5. MONTHLY TASKS
  - Lubricate fan bearings per LUB-G2-LC chart
  - Inspect fill for scaling or biological growth
  - Thermography on fan motor and gearbox

6. PREDICTIVE TRIGGERS
  Schedule fill section replacement when:
  - Approach temp degrades 15% at same load and wet bulb
  - Visible fill collapse or heavy scale
  - Fan vibration exceeds 7.1 mm/s for 3 consecutive readings

7. WATER TREATMENT
  Maintain biocide, scale inhibitor, and corrosion inhibitor per vendor. Over-blowdown wastes water; under-blowdown scales fill.

8. SEASONAL
  Spring startup: disinfect basin, inspect louvers, test vibration switches.
  Fall shutdown (if applicable): drain basin, protect motors from freeze.

9. SAFETY
  Lockout fans before entering cell. Fall protection required on elevated walks. Legionella risk — no pressure washing without mist control PPE.

10. SPARES
  Fan belts, gearbox oil GL-220, fill sections (lead time 8 weeks), level switch floats.
""",
    "press_machine_maintenance.pdf": """
HYDRAULIC PRESS MAINTENANCE MANUAL — PRESS-1000
1000 Ton Four-Post Hydraulic Press

SECTION 1 — MACHINE OVERVIEW
The press consists of main cylinder, four tie rods, moving platen, hydraulic power unit HPU-P1000, and PLC safety system. Cycle time 12 sec full stroke at rated tonnage.

SECTION 2 — SAFETY SYSTEMS
Light curtain LC-01, two-hand control, pressure switch proof-of-tonnage, and redundant relief valves. Test light curtain daily per shift start checklist. Never bypass safety PLC inputs.

SECTION 3 — HYDRAULIC PARAMETERS
  System pressure rated: 315 bar
  Tank temperature normal: 45-55 C
  Pre-fill valve response: <200 ms
  Decompression time: adjustable 0.5-2.0 sec to prevent shock

SECTION 4 — PREDICTIVE MONITORING
  - Pressure hold test weekly: drift >5% indicates seal bypass
  - Pump noise trending via ultrasonic meter monthly
  - Oil particle count quarterly
  - Cylinder rod coating inspection for scoring

SECTION 5 — PREVENTIVE MAINTENANCE SCHEDULE
  Daily: oil level, leak check, safety test
  250 hours: filter indicator check
  500 hours: return filter change
  2000 hours: oil sample and cooler clean
  8000 hours: pump overhaul inspection
  16000 hours: cylinder seal replacement (planned outage)

SECTION 6 — TROUBLESHOOTING
  Slow approach speed: check pump flow, temperature, suction strainer
  Hammer on decompression: adjust valve, check accumulators
  Overheating: cooler fouling, relief valve passing, wrong viscosity
  Tonnage loss: seal wear, pressure gauge error, PLC scaling

SECTION 7 — ALIGNMENT
  Check platen parallelism annually with four corner pressure film or electronic level. Misalignment damages tooling and tie rods.

SECTION 8 — DOCUMENTATION
  Log each overload trip with die number and material thickness. Pattern of trips indicates tooling or alignment issue, not random faults.

SECTION 9 — SPARE PARTS
  Seal kits SK-P1000-CYL, pump cartridge PC-P1000, filters FLT-HYD-10-200. Store seals in climate-controlled area.

SECTION 10 — SHUTDOWN FOR MAINTENANCE
  LOTO HPU-P1000 breakers, bleed accumulators, block cylinder with mechanical supports before working under ram.
""",
    "dust_collector_sop.pdf": """
DUST COLLECTOR STANDARD OPERATING PROCEDURE
DC-01 through DC-08 — Baghouse Units

1. SCOPE
Baghouse dust collectors on grinding, sanding, and bulk material handling exhausts.

2. NORMAL OPERATION
  Differential pressure across bags: 2-4 in w.c.
  Pulse jet cleaning cycle: every 30-90 sec as needed
  Hopper discharge rotary valve: must run when collector runs
  Fan damper: minimum 80% open unless energy optimization approved

3. ALARMS
  High DP (>6 in w.c.): bag blinded or heavy loading — inspect process source
  Low airflow: fan belt slip, damper closed, duct blockage
  High emissions (opacity): bag tear, seal leak, failed cage

4. PREDICTIVE MAINTENANCE
  Trend fan motor current — increase suggests duct restriction or bearing wear
  Vibration on fan bearings monthly
  Replace bags when DP baseline rises 40% after cleaning cycle optimization

5. BAG REPLACEMENT PROCEDURE
  LOTO fan and rotary valve. Confined space permit if entering hopper.
  Use correct bag length and cage count. Double-check grounding clips for static.

6. EXPLOSION PROTECTION
  NFPA 68 compliant relief panels on DC-01, DC-03. Never seal panels.
  Grounding straps intact on all ducts handling combustible dust.

7. HOUSEKEEPING
  No accumulation >1/8 inch combustible dust on horizontal surfaces within 30 ft per NFPA 652.

  8. RECORDS
  Log DP, cleaning cycles, and hopper dumps daily on form DC-LOG-01.

9. TROUBLESHOOTING REFERENCE
  High DP with clean bags: check inlet damper, duct leak, or process surge.
  Fan vibration step change: bearing, buildup on wheel, or resonance after speed change.
  Emissions spike after bag change: verify bag install direction and cage seating.

10. MAINTENANCE INTERVALS
  Bags: 18-24 months typical; 12 months abrasive service.
  Fan bearings: lubricate quarterly; replace at vibration alarm.
  Hopper screw: inspect wear annually.
""",
}


def annual_pm_library() -> str:
    procedures = []
    equipment = [
        ("Pump-3", "Replace mechanical seal if leak >5 drops/min", "Annual or 8000 hr"),
        ("Pump-3", "Laser align motor to pump", "Annual"),
        ("Pump-3", "Bearing vibration route and trending", "Monthly"),
        ("Pump-3", "Inspect coupling and guard", "Weekly"),
        ("HVAC Unit-7", "Replace MERV-13 filters", "90 days or 1.2 in w.c. DP"),
        ("HVAC Unit-7", "Clean condensate drain and trap", "Monthly"),
        ("HVAC Unit-7", "Verify economizer damper stroke", "Quarterly"),
        ("HVAC Unit-7", "Belt tension and sheave alignment", "Semi-annual"),
        ("M-01", "Megger windings phase to ground", "Annual"),
        ("M-07", "Vibration route all axes", "Monthly"),
        ("M-14", "Thermography junction box", "Quarterly"),
        ("GB-12", "Oil sample and particle count", "Quarterly"),
        ("GB-12", "Breather desiccant replacement", "Semi-annual"),
        ("AC-1", "Separator element replacement", "4000 hr"),
        ("AC-2", "Oil analysis sample", "Quarterly"),
        ("CH-1", "Refrigerant leak survey", "Quarterly"),
        ("CH-2", "Condenser coil chemical clean", "Annual"),
        ("BL-1", "Fire side inspection and brush", "Annual outage"),
        ("BL-2", "Safety valve bench test coordination", "Annual"),
        ("CV-100", "Belt thickness and splice inspection", "Monthly"),
        ("CV-200", "Idler roll spin test and replace seized", "Quarterly"),
        ("DC-03", "Bag leak detection lamp test", "Semi-annual"),
        ("T-02", "DGA oil sample", "Annual"),
        ("HYD-01", "Accumulator pre-charge verify", "Monthly"),
        ("PRESS-1000", "Safety light curtain function test", "Daily per shift"),
        ("CT-1", "Basin sediment removal and biocide check", "Monthly"),
        ("CT-2", "Gearbox oil sample", "Quarterly"),
        ("DC-01", "Hopper rotary valve seal inspect", "Monthly"),
        ("FILT-MAIN", "Plant intake filter change", "Quarterly"),
        ("LOTO-STATION", "Audit lock board completeness", "Monthly"),
    ]
    for i, (asset, task, interval) in enumerate(equipment, 1):
        procedures.append(f"""
### PM-{i:03d}: {asset} — {task}

**Interval:** {interval}

**Procedure summary:**
1. Review open alerts and last work order for this asset.
2. Apply LOTO if physical contact with moving or energized parts is required.
3. Perform task per equipment-specific SOP in this document library.
4. Record readings before and after in CMMS form PM-STD-01.
5. If any reading exceeds warning threshold, open predictive work order before closing PM.

**Acceptance criteria:** Task complete with all readings within SOP limits or escalation documented.

**Tools required:** Per task — standard maintenance tool cart, calibrated instruments per sensor_calibration_guide.md.

**Estimated duration:** 1–4 hours depending on asset class.
""")
    return "# Annual and Recurring PM Procedure Library\n\n" + "\n".join(procedures)


def asset_registry_reference() -> str:
    assets = []
    for i in range(1, 25):
        crit = "A" if i <= 12 else "B"
        assets.append(f"| M-{i:02d} | Motor | Line {((i-1)//6)+1} | {crit} | Monthly vibration |")
    for i in range(1, 10):
        assets.append(f"| CV-{100+i} | Conveyor | Transport | B | Weekly walkdown |")
    for i in range(1, 4):
        assets.append(f"| AC-{i} | Compressor | Utilities | A | Daily rounds + oil quarterly |")
    for i in range(1, 4):
        assets.append(f"| CH-{i} | Chiller | HVAC | A | Continuous BMS + quarterly PM |")
    table = "\n".join(assets)
    return f"""
# Plant Asset Registry — Maintenance Cross-Reference

## Purpose
Master list linking asset IDs to equipment class, criticality, and default PdM tasks. Used by CMMS, historian, and Smart Maintenance Assistant for context.

## Motor Assets
| Asset ID | Class | Location | Criticality | Default PdM |
|----------|-------|----------|-------------|-------------|
{table}

## Threshold Lookup
When the chatbot cites an asset, verify live sensor data in the historian before acting. Documentation thresholds are nominal; operating context may justify adjusted limits per reliability engineer approval.

## Revision History
Rev 1.0 — Initial load. Rev 1.1 — Added AC-3 standby. Rev 1.2 — Criticality update post FMEA 2025-Q4.

## Appendix: Location Maps
Hall A: M-01 to M-12, CV-100 to CV-105, AC-1, CH-1.
Hall B: M-13 to M-18, CV-200 to CV-204, AC-2.
Utilities mezzanine: AC-3, BL-1, BL-2, T-01 to T-03.
East wing roof: CH-2, CT-1, CT-2, HVAC Unit-7.
"""


def fault_code_reference() -> str:
    codes = []
    descriptions = [
        ("VIB-WARN", "Vibration exceeded warning threshold"),
        ("VIB-CRIT", "Vibration exceeded critical threshold"),
        ("TEMP-WARN", "Bearing or winding temperature warning"),
        ("TEMP-CRIT", "Temperature critical — shutdown recommended"),
        ("CURR-HIGH", "Motor current above baseline"),
        ("PRES-LOW", "Discharge or process pressure low"),
        ("PRES-HIGH", "Pressure relief risk"),
        ("FILT-DP", "Filter differential pressure high"),
        ("OIL-DEG", "Oil analysis degradation flag"),
        ("ALIGN", "Misalignment indicator from vibration"),
        ("LOTO-VIOL", "Safety interlock or LOTO violation detected"),
    ]
    for code, desc in descriptions:
        for i in range(1, 6):
            codes.append(f"| {code}-{i:02d} | {desc} — variant {i} | PdM | 24-72 hr per severity |")
    body = "\n".join(codes)
    return f"""
# Condition Monitoring Fault Code Reference

## Usage
Fault codes are assigned by the analytics layer when sensor trends exceed SOP limits. Maintenance planner maps codes to work order templates.

## Code Table (Excerpt)
| Code | Description | WO Type | SLA |
|------|-------------|---------|-----|
{body}

## Escalation Matrix
Critical codes auto-page on-call reliability engineer. Warning codes queue in daily PdM review. Duplicate codes within 7 days on same asset trigger root cause review.

## Clearing Codes
Codes clear when sensor returns to normal for 24 consecutive hours OR work order documents corrective action. Do not manually clear without supervisor approval.
"""


def regulatory_compliance_guide() -> str:
    return """
# Regulatory Compliance Guide for Maintenance Operations

## OSHA 1910 — General Industry
Lockout/tagout (1910.147): full compliance with site EHS-LOTO-001. Annual audit and training documented.

Machine guarding (1910.212): guards replaced before restart. No maintenance with guards removed unless LOTO prevents motion.

## NFPA 70E — Electrical Safety
Arc flash study updated 2024. PPE category on each panel label. Only qualified persons work inside restricted approach boundary.

## NFPA 70 — National Electrical Code
Panel work per NEC and local amendments. Thermography supports preventive compliance for connections.

## EPA — Spill Prevention and Reporting
Oil storage >1,320 gallons SPCC plan on file. Spill kits at 12 locations. Reportable quantity releases per EHS within 1 hour.

## FDA / cGMP (where applicable on packaging line)
PM and calibration records retained 7 years. Change control for equipment modifications affecting product contact.

## ISO 55000 — Asset Management Alignment
Documented maintenance strategy, risk-based inspection, and KPI review quarterly. This corpus supports ISO 55001 evidence for competence and information requirements.

## Pressure Vessels
State boiler and pressure vessel code: BL-1, BL-2 certificates current. Third-party inspection per jurisdiction.

## Environmental — Refrigerants
F-Gas log for CH-1, CH-2. Leak check quarterly. Recovery certification for technicians.

## Documentation Retention
| Record type | Retention |
|-------------|-----------|
| PM work orders | 7 years |
| PdM spectra | 5 years |
| Calibration certs | Life of instrument + 3 years |
| Incident reports | 10 years |
| Training records | Employment + 5 years |

## Audit Preparation
Maintenance manager maintains audit binder: LOTO samples, hot work permits, calibration due list, overdue PM report, management of change log.
""" + page_break() + """
## Appendix: Inspection Frequencies by Regulation

Boiler operator rounds: per state rule daily when in service.
Fire extinguisher on mobile equipment: monthly visual.
Eyewash stations near chemical maintenance areas: weekly activation test.
Crane hooks and rigging: annual certified inspection.
Elevated work platforms: annual structural and functional test.

## Appendix: Contractor Requirements
All contractors sign safety orientation, LOTO acknowledgment, and confined space policy before work. Hot work permit required for welding and grinding in designated areas.
"""


def wrap_with_standard_appendix(content: str, doc_name: str) -> str:
    appendix = expand_appendix(
        f"{doc_name} Field Notes",
        [
            ("Pre-Work Verification", checklist_block([
                "Confirm correct asset ID and equipment is stopped",
                "Verify LOTO applied per EHS-LOTO-001",
                "Review last 30 days historian trends",
                "Check open work orders for duplicate work",
                "Confirm spare parts on hand or PR issued",
                "Notify production of estimated downtime",
            ])),
            ("Post-Work Verification", checklist_block([
                "Remove all tools and materials from work area",
                "Restore guards and interlocks",
                "Remove LOTO per procedure — each worker own lock",
                "Test run at no load then under load",
                "Record as-found and as-left readings in CMMS",
                "Update predictive baseline if component replaced",
            ])),
            ("Related Documents", (
                "Cross-reference: lubrication_standards.md, vibration_analysis_handbook.md, "
                "safety_loto_procedures.txt, spare_parts_inventory_policy.txt, "
                "predictive_maintenance_program.md."
            )),
        ],
    )
    return content + appendix


def generate_pdf(filename: str, text: str) -> None:
    if FPDF is None:
        print(f"  skip {filename} (install fpdf2)")
        return
    text = sanitize_for_pdf(text)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    def write_wrapped(line: str, bold: bool = False) -> None:
        line = line.strip()
        if not line:
            pdf.ln(4)
            return
        pdf.set_x(pdf.l_margin)
        pdf.set_font("Helvetica", "B" if bold else "", size=12 if bold else 11)
        pdf.multi_cell(pdf.epw, 5, line)
        pdf.set_font("Helvetica", size=11)

    for line in text.strip().splitlines():
        stripped = line.strip()
        if stripped.isupper() and len(stripped) < 80 and not stripped.startswith("|"):
            write_wrapped(stripped, bold=True)
        else:
            write_wrapped(stripped)

    path = DOCS_DIR / filename
    pdf.output(str(path))
    pages = pdf.page_no()
    print(f"  wrote {filename} ({pages} pages)")


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating maintenance document corpus...\n")

    md_docs = [
        ("motor_maintenance_manual.md", motor_manual()),
        ("compressor_sop.md", compressor_sop()),
        ("conveyor_system_guide.md", conveyor_guide()),
        ("lubrication_standards.md", lubrication_standards()),
        ("vibration_analysis_handbook.md", vibration_handbook()),
        ("electrical_inspection_checklist.md", electrical_inspection()),
        ("predictive_maintenance_program.md", pdm_program()),
        ("chiller_boiler_operations.md", chiller_boiler()),
        ("annual_pm_procedure_library.md", annual_pm_library()),
        ("fault_code_reference.md", fault_code_reference()),
        ("regulatory_compliance_guide.md", regulatory_compliance_guide()),
    ]
    for fname, content in md_docs:
        name = fname.replace(".md", "").replace("_", " ").title()
        write(fname, wrap_with_standard_appendix(content, name))

    write("safety_loto_procedures.txt", safety_loto_txt())
    write("maintenance_scheduling_policy.txt", scheduling_policy_txt())

    write("transformer_maintenance.html", transformer_html())
    write("hydraulic_systems_guide.html", hydraulic_html())

    pdf_only = {k: v for k, v in PDF_SOURCES.items() if k != "dust_collector_sop.pdf"}
    for fname, content in pdf_only.items():
        generate_pdf(fname, content)

    # Remove files no longer in the 20-file corpus
    for obsolete in [
        "cmms_logging_procedures.md",
        "emergency_response_procedures.md",
        "sensor_calibration_guide.md",
        "gearbox_maintenance_manual.md",
        "asset_registry_reference.md",
        "spare_parts_inventory_policy.txt",
        "dust_collector_sop.pdf",
    ]:
        path = DOCS_DIR / obsolete
        if path.exists():
            path.unlink()
            print(f"  removed {obsolete}")

    files = [f for f in DOCS_DIR.glob("*") if f.is_file()]
    total_chars = sum(f.stat().st_size for f in files)
    est_pages = total_chars // 2500
    print(f"\nDone: {len(files)} files, ~{total_chars:,} chars, ~{est_pages} estimated pages")


if __name__ == "__main__":
    main()
