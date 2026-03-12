const fs = require('fs');
const path = require('path');
const XLSX = require('xlsx');

const DEFAULT_INPUT = path.join(__dirname, 'powerbi_export.csv');
const inputPath = process.argv[2] || DEFAULT_INPUT;
const outputPath = path.join(__dirname, 'plant_data.json');

if (!fs.existsSync(inputPath)) {
    console.error(`❌ Input file not found: ${inputPath}`);
    process.exit(1);
}

function parseDate(value) {
    if (!value) return null;
    const s = String(value).trim();
    if (s.includes('T')) {
        const d = new Date(s);
        return isNaN(d.getTime()) ? null : d;
    }
    return null;
}

function formatDate(d) {
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = String(d.getFullYear());
    return `${day}.${month}.${year}`;
}

function sv(val) {
    if (val == null || val === '') return null;
    const n = Number(val);
    return (!isNaN(n) && isFinite(n)) ? n : null;
}

try {
    const workbook = XLSX.readFile(inputPath, { raw: false });
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    const rawRows = XLSX.utils.sheet_to_json(sheet);

    console.log(`✅ Read ${rawRows.length} rows from CSV`);

    const byDate = new Map();

    rawRows.forEach(row => {
        /** @type {Record<string, any>} */
        const rowData = row;
        const cleanRow = {};

        for (const [k, v] of Object.entries(rowData)) {
            const cleanKey = k.replace('DailyOperation[', '').replace(']', '').trim();
            cleanRow[cleanKey] = v;
        }

        const dateObj = parseDate(cleanRow['ReportDate']) || parseDate(cleanRow['Date']);
        if (!dateObj) return;
        const dStr = formatDate(dateObj);

        if (!byDate.has(dStr)) {
            let eff = sv(cleanRow['NetEff_Pct']);
            if (eff !== null && eff < 1) eff = parseFloat((eff * 100).toFixed(2));

            let load = sv(cleanRow['TotalLoadMW']);
            if (load !== null && load > 10000) load = load / 24;

            byDate.set(dStr, {
                Date: dStr,
                Generation: sv(cleanRow['GrossMWH']),
                NetGen: sv(cleanRow['NetMWH']),
                Load: load,
                PLF: (load !== null) ? parseFloat((load / 3883.2 * 100).toFixed(2)) : null,
                Efficiency: eff,
                HeatRate: sv(cleanRow['HeatRate']),
                Fuel: sv(cleanRow['FuelGasTons']),
                Emissions: {
                    NOx: null,
                    SOx: null,
                    CO: null,
                    Particulate: null,
                    StackTemp: null
                },
                Water: { ROProduction: sv(cleanRow['ROProduction']) },
                AirIntakeDP: sv(cleanRow['AirIntakeDP']),
                Units: []
            });
        }

        const day = byDate.get(dStr);

        // Map Environment data (Pivoted or Row-based)
        const nox = sv(cleanRow['NOx']) || sv(cleanRow['Env.NOx']);
        const sox = sv(cleanRow['SOx']) || sv(cleanRow['Env.SOx']);
        const co = sv(cleanRow['CO']) || sv(cleanRow['Env.CO']);
        const particulate = sv(cleanRow['Particulate']) || sv(cleanRow['Dust']);
        const temp = sv(cleanRow['Stack Temp']) || sv(cleanRow['StackTemp']);

        if (nox !== null) day.Emissions.NOx = nox;
        if (sox !== null) day.Emissions.SOx = sox;
        if (co !== null) day.Emissions.CO = co;
        if (particulate !== null) day.Emissions.Particulate = particulate;
        if (temp !== null) day.Emissions.StackTemp = temp;
    });

    const output = Array.from(byDate.values()).sort((a, b) => {
        const p = s => {
            const parts = s.split('.');
            return new Date(`${parts[2]}-${parts[1]}-${parts[0]}`).getTime();
        };
        return p(a.Date) - p(b.Date);
    });

    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));

    const last = output[output.length - 1];
    console.log(`✅ Success! Data synced for ${output.length} days.`);
    console.log(`📊 Last Date: ${last.Date} | NOx: ${last.Emissions.NOx} | Temp: ${last.Emissions.StackTemp}`);

} catch (err) {
    console.error('❌ Error processing CSV:', err);
}