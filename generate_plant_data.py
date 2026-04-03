import csv
import json
from collections import defaultdict
from datetime import datetime
import os

CSV_FILE = os.path.join(os.path.dirname(__file__), 'powerbi_export.csv')
OUT_FILE = os.path.join(os.path.dirname(__file__), 'plant_data.json')

def safe_float(v):
    try:
        f = float(v)
        return f if f == f else None  # NaN check
    except (TypeError, ValueError):
        return None

def parse_date(dt_str):
    """Convert '2026-03-13T00:00:00' or '2026-03-13' -> 'DD.MM.YYYY'"""
    dt_str = dt_str.strip()
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
        try:
            dt = datetime.strptime(dt_str, fmt)
            return dt.strftime('%d.%m.%Y')
        except ValueError:
            continue
    return None

days = defaultdict(lambda: {
    'Generation': None,
    'NetGen': None,
    'Load': None,
    'PLF': None,
    'Efficiency': None,
    'HeatRate': None,
    'Fuel': None,
    'Emissions': {'NOx': None, 'SOx': None, 'CO': None, 'Particulate': None, 'StackTemp': None},
    'Water': {'ROProduction': None},
    'AirIntakeDP': None,
    'Units': []
})

with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date_raw = row.get('DailyOperation[ReportDate]', '').strip()
        date_str = parse_date(date_raw)
        if not date_str:
            continue

        gross_mwh  = safe_float(row.get('DailyOperation[GrossMWH]'))
        net_mwh    = safe_float(row.get('DailyOperation[NetMWH]'))
        load_mw    = safe_float(row.get('DailyOperation[TotalLoadMW]'))
        fuel_tons  = safe_float(row.get('DailyOperation[FuelGasTons]'))
        heat_rate  = safe_float(row.get('DailyOperation[HeatRate]'))
        net_eff    = safe_float(row.get('DailyOperation[NetEff_Pct]'))
        group      = row.get('DailyOperation[Group]', '').strip()
        unit_num   = row.get('DailyOperation[Unit]', '').strip()
        unit_type  = row.get('DailyOperation[UnitType]', '').strip()
        avg_load   = safe_float(row.get('DailyOperation[AvgLoad_MW]'))
        gen_day    = safe_float(row.get('DailyOperation[GenDay_MWH]'))
        mfeqh      = safe_float(row.get('DailyOperation[MFEQH_Hours]'))
        plf        = safe_float(row.get('DailyOperation[PLF_Pct]'))

        d = days[date_str]

        # Aggregate plant-level totals (sum across all rows for this date)
        # Use first non-null value for plant-level daily totals
        if gross_mwh is not None:
            d['Generation'] = (d['Generation'] or 0) + gross_mwh
        if net_mwh is not None:
            d['NetGen'] = (d['NetGen'] or 0) + net_mwh
        if load_mw is not None and d['Load'] is None:
            d['Load'] = load_mw
        if fuel_tons is not None:
            d['Fuel'] = (d['Fuel'] or 0) + fuel_tons
        if heat_rate is not None and d['HeatRate'] is None:
            d['HeatRate'] = heat_rate
        if net_eff is not None and d['Efficiency'] is None:
            d['Efficiency'] = round(net_eff * 100, 2) if net_eff < 1 else round(net_eff, 2)
        if plf is not None and d['PLF'] is None:
            d['PLF'] = round(plf * 100, 2) if plf < 1 else round(plf, 2)

        # Add unit-level entry
        if group and unit_num:
            d['Units'].append({
                'Group': group,
                'Unit': unit_num,
                'Type': unit_type,
                'Load': avg_load,
                'Generation': gen_day,
                'MFEQH': mfeqh
            })

# Deduplicate and aggregate Generation/NetGen/Fuel per day
# The CSV has multiple rows per day (one per unit), so we already summed above.
# But Load, HeatRate, Efficiency come from the first row per day (plant-level).
# We need to re-aggregate properly: sum unique unit rows only.

# Redo: group rows per date, handle duplicates
rows_by_date = defaultdict(list)
with open(CSV_FILE, newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date_raw = row.get('DailyOperation[ReportDate]', '').strip()
        date_str = parse_date(date_raw)
        if date_str:
            rows_by_date[date_str].append(row)

result = []
for date_str in sorted(rows_by_date.keys(),
                        key=lambda s: datetime.strptime(s, '%d.%m.%Y')):
    rows = rows_by_date[date_str]

    # Plant-level values come from the first row (they repeat per unit row)
    first = rows[0]
    gross_total = safe_float(first.get('DailyOperation[GrossMWH]'))
    net_total   = safe_float(first.get('DailyOperation[NetMWH]'))
    load_mw     = safe_float(first.get('DailyOperation[TotalLoadMW]'))
    fuel_tons   = safe_float(first.get('DailyOperation[FuelGasTons]'))
    heat_rate   = safe_float(first.get('DailyOperation[HeatRate]'))
    net_eff_raw = safe_float(first.get('DailyOperation[NetEff_Pct]'))
    plf_raw     = safe_float(first.get('DailyOperation[PLF_Pct]'))

    net_eff = None
    if net_eff_raw is not None:
        net_eff = round(net_eff_raw * 100, 2) if net_eff_raw < 1 else round(net_eff_raw, 2)

    plf = None
    if plf_raw is not None:
        plf = round(plf_raw * 100, 2) if plf_raw < 1 else round(plf_raw, 2)

    # Build units list (deduplicate by Group+Unit)
    seen_units = set()
    units = []
    for row in rows:
        group    = row.get('DailyOperation[Group]', '').strip()
        unit_num = row.get('DailyOperation[Unit]', '').strip()
        unit_key = (group, unit_num)
        if unit_key in seen_units:
            continue
        seen_units.add(unit_key)
        units.append({
            'Group': group,
            'Unit': unit_num,
            'Type': row.get('DailyOperation[UnitType]', '').strip(),
            'Load': safe_float(row.get('DailyOperation[AvgLoad_MW]')),
            'Generation': safe_float(row.get('DailyOperation[GenDay_MWH]')),
            'MFEQH': safe_float(row.get('DailyOperation[MFEQH_Hours]'))
        })

    entry = {
        'Date': date_str,
        'Generation': gross_total,
        'NetGen': net_total,
        'Load': load_mw,
        'PLF': plf,
        'Efficiency': net_eff,
        'HeatRate': heat_rate,
        'Fuel': fuel_tons,
        'Emissions': {'NOx': None, 'SOx': None, 'CO': None, 'Particulate': None, 'StackTemp': None},
        'Water': {'ROProduction': None},
        'AirIntakeDP': None,
        'Units': units
    }
    result.append(entry)

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)

print(f'Done: {len(result)} days written to {OUT_FILE}')
