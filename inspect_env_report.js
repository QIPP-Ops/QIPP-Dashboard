const XLSX = require('xlsx');
const path = require('path');

const filePath = 'C:\\Users\\asus\\Acwa\\QIPP - QIPP Mail Ingest Temp\\Environment Report  03.02.2026.xlsx';

try {
    const workbook = XLSX.readFile(filePath);
    console.log("Sheet Names:", workbook.SheetNames);
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    const jsonData = XLSX.utils.sheet_to_json(sheet, {header: 1});
    
    // Print more rows
    jsonData.slice(0, 20).forEach((row, i) => {
        if (row && row.length > 0) console.log(`Row ${i}:`, row);
    });
} catch (e) {
    console.error(e);
}
