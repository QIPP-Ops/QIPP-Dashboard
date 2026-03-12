const XLSX = require('xlsx');
const path = require('path');
const fs = require('fs');

const baseDir = "C:\\Users\\asus\\Acwa\\QIPP - QIPP Mail Ingest Temp";
const file = path.join(baseDir, "Daily Operation Report 02.02.2026.xlsx");

if (fs.existsSync(file)) {
    const workbook = XLSX.readFile(file);
    console.log("Sheets:", workbook.SheetNames);
    const sheet = workbook.Sheets[workbook.SheetNames.find(n => n.includes("Daily Operation & Gen Report")) || workbook.SheetNames[0]];
    const data = XLSX.utils.sheet_to_json(sheet, { header: 1 });
    for (let i = 35; i < 45; i++) {
        console.log(`Row ${i+1}:`, data[i]);
    }
} else {
    console.log("File not found");
}
