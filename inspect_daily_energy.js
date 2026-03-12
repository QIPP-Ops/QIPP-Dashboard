const XLSX = require('xlsx');
const path = require('path');

const filePath = 'C:\\Users\\asus\\Acwa\\QIPP - QIPP Mail Ingest Temp\\DAILY ACTUAL ENERGY PRODUCED REPORT QIPP 01-February-2026.xlsx';

try {
    const workbook = XLSX.readFile(filePath);
    console.log("Sheet Names:", workbook.SheetNames);
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    const jsonData = XLSX.utils.sheet_to_json(worksheet, {header: 1});
    
    console.log("First 20 rows:");
    jsonData.slice(0, 20).forEach((row, i) => {
        console.log(`Row ${i}:`, row);
    });
} catch (e) {
    console.error(e);
}
