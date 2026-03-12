const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

const folderPath = 'C:\\Users\\asus\\Acwa\\QIPP - QIPP Mail Ingest Temp';

function inspect(pattern) {
    const files = fs.readdirSync(folderPath);
    const target = files.find(f => f.toUpperCase().includes(pattern.toUpperCase()) && f.endsWith('.xlsx'));
    if (target) {
        console.log(`\n--- Inspecting ${target} ---`);
        const workbook = XLSX.readFile(path.join(folderPath, target));
        console.log("Sheet Names:", workbook.SheetNames);
        const sheet = workbook.Sheets[workbook.SheetNames[0]];
        const data = XLSX.utils.sheet_to_json(sheet, {header: 1});
        data.slice(0, 15).forEach((row, i) => console.log(`Row ${i}:`, row));
    } else {
        console.log(`\nNo file found for pattern: ${pattern}`);
    }
}

inspect('Air Intake');
inspect('TIMERS-COUNTERS');
