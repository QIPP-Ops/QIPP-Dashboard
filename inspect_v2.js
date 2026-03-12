const XLSX = require('xlsx');
const workbook = XLSX.readFile('C:\\Users\\asus\\Acwa\\QIPP - QIPP Mail Ingest Temp\\GTs Air Intake Filter DP 01.02.2026.xlsx');
const sheet = workbook.Sheets[workbook.SheetNames[0]];
const rows = XLSX.utils.sheet_to_json(sheet, { header: 1 });
console.log('Row count:', rows.length);
rows.slice(10, 20).forEach((r, i) => console.log(`Row ${i + 10}:`, JSON.stringify(r)));
