package com.inventory.service;

import com.inventory.model.Product;
import com.inventory.model.UnitOfMeasure;
import com.inventory.repository.ProductRepository;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.ss.usermodel.WorkbookFactory;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.File;
import java.io.FileInputStream;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Service
public class ExcelImportService {

    private final ProductRepository productRepository;

    public ExcelImportService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Transactional
    public int importProductsFromExcel(File file) throws Exception {
        List<Product> productsToSave = new ArrayList<>();
        
        try (FileInputStream fis = new FileInputStream(file);
             Workbook workbook = WorkbookFactory.create(fis)) {
            
            Sheet sheet = workbook.getSheetAt(0);
            
            // Check if it's the Tally "Godown Summary" format
            boolean isTallyFormat = false;
            for (int i = 0; i < 10; i++) {
                Row r = sheet.getRow(i);
                if (r != null && r.getCell(0) != null) {
                    String val = r.getCell(0).getStringCellValue();
                    if (val != null && val.contains("Godown Summary")) {
                        isTallyFormat = true;
                        break;
                    }
                }
            }

            for (int i = 0; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row == null) continue;

                Cell firstCell = row.getCell(0);
                if (firstCell == null || firstCell.getCellType() != CellType.STRING) continue;

                String cellValue = firstCell.getStringCellValue().trim();
                
                if (isTallyFormat) {
                    // Tally logic: "SKU (Name)" or just Name
                    if (cellValue.contains("(") && cellValue.contains(")")) {
                        String sku = cellValue.substring(0, cellValue.indexOf("(")).trim();
                        String name = cellValue.substring(cellValue.indexOf("(") + 1, cellValue.indexOf(")")).trim();
                        
                        if (sku.isEmpty() || sku.equalsIgnoreCase("Particulars")) continue;

                        int stock = 0;
                        // Find the last numeric column for Closing Balance
                        for (int col = row.getLastCellNum() - 1; col >= 1; col--) {
                            Cell c = row.getCell(col);
                            if (c != null && c.getCellType() == CellType.NUMERIC) {
                                stock = (int) c.getNumericCellValue();
                                break;
                            }
                        }

                        // Check if exists
                        Product p = productRepository.findAll().stream()
                                .filter(prod -> prod.getSku().equalsIgnoreCase(sku))
                                .findFirst().orElse(new Product());

                        p.setSku(sku);
                        p.setName(name);
                        p.setCurrentStock(p.getCurrentStock() == null ? stock : p.getCurrentStock() + stock);
                        if (p.getUnitOfMeasure() == null) p.setUnitOfMeasure(UnitOfMeasure.PIECE);
                        if (p.getCostPrice() == null) p.setCostPrice(BigDecimal.ZERO);
                        if (p.getSellingPrice() == null) p.setSellingPrice(BigDecimal.ZERO);

                        productsToSave.add(p);
                    }
                } else {
                    // Standard Logic: SKU | Name | Cost | Price | Stock
                    if (i == 0 || cellValue.equalsIgnoreCase("SKU")) continue; // Skip header

                    String sku = cellValue;
                    String name = getCellString(row.getCell(1));
                    BigDecimal cost = getCellBigDecimal(row.getCell(2));
                    BigDecimal price = getCellBigDecimal(row.getCell(3));
                    int stock = (int) getCellDouble(row.getCell(4));

                    Product p = productRepository.findAll().stream()
                            .filter(prod -> prod.getSku().equalsIgnoreCase(sku))
                            .findFirst().orElse(new Product());

                    p.setSku(sku);
                    p.setName(name);
                    p.setCostPrice(cost);
                    p.setSellingPrice(price);
                    p.setCurrentStock(stock);
                    if (p.getUnitOfMeasure() == null) p.setUnitOfMeasure(UnitOfMeasure.PIECE);

                    productsToSave.add(p);
                }
            }
            
            productRepository.saveAll(productsToSave);
            return productsToSave.size();
        }
    }

    private String getCellString(Cell cell) {
        if (cell == null) return "";
        if (cell.getCellType() == CellType.STRING) return cell.getStringCellValue();
        if (cell.getCellType() == CellType.NUMERIC) return String.valueOf((int)cell.getNumericCellValue());
        return "";
    }

    private BigDecimal getCellBigDecimal(Cell cell) {
        if (cell == null || cell.getCellType() != CellType.NUMERIC) return BigDecimal.ZERO;
        return BigDecimal.valueOf(cell.getNumericCellValue());
    }

    private double getCellDouble(Cell cell) {
        if (cell == null || cell.getCellType() != CellType.NUMERIC) return 0.0;
        return cell.getNumericCellValue();
    }
}
