import os

base_dir = "/Users/chinmoy/IdeaProjects/InventoryIQ"
files = {}

files["src/main/resources/fxml/product_view.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<HBox spacing="20" prefHeight="768.0" prefWidth="1024.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.ProductController" styleClass="background-pane">
    <padding>
        <Insets top="30" right="30" bottom="30" left="30"/>
    </padding>

    <!-- Left Form -->
    <VBox spacing="20" styleClass="card" prefWidth="350">
        <HBox alignment="CENTER_LEFT">
             <Label text="New Product" styleClass="page-title" HBox.hgrow="ALWAYS" maxWidth="Infinity"/>
             <Button fx:id="uploadExcelBtn" text="📁 Import Excel" styleClass="accent"/>
        </HBox>
        <Separator/>
        <GridPane hgap="10" vgap="20">
            <Label text="SKU" GridPane.columnIndex="0" GridPane.rowIndex="0" styleClass="text-muted"/>
            <TextField fx:id="skuField" GridPane.columnIndex="0" GridPane.rowIndex="1" GridPane.columnSpan="2" promptText="e.g. PRD-001"/>
            
            <Label text="Product Name" GridPane.columnIndex="0" GridPane.rowIndex="2" styleClass="text-muted"/>
            <TextField fx:id="nameField" GridPane.columnIndex="0" GridPane.rowIndex="3" GridPane.columnSpan="2" promptText="Enter product name"/>
            
            <Label text="Unit" GridPane.columnIndex="0" GridPane.rowIndex="4" styleClass="text-muted"/>
            <ComboBox fx:id="uomComboBox" GridPane.columnIndex="0" GridPane.rowIndex="5" GridPane.columnSpan="2" maxWidth="Infinity"/>
            
            <Label text="Cost ($)" GridPane.columnIndex="0" GridPane.rowIndex="6" styleClass="text-muted"/>
            <TextField fx:id="costPriceField" GridPane.columnIndex="0" GridPane.rowIndex="7" promptText="0.00"/>
            
            <Label text="Price ($)" GridPane.columnIndex="1" GridPane.rowIndex="6" styleClass="text-muted"/>
            <TextField fx:id="sellingPriceField" GridPane.columnIndex="1" GridPane.rowIndex="7" promptText="0.00"/>
            
            <Label text="Initial Stock" GridPane.columnIndex="0" GridPane.rowIndex="8" styleClass="text-muted"/>
            <TextField fx:id="stockField" GridPane.columnIndex="0" GridPane.rowIndex="9" GridPane.columnSpan="2" promptText="0"/>
        </GridPane>
        
        <Button fx:id="saveButton" text="Save Product" styleClass="accent" maxWidth="Infinity" prefHeight="40" style="-fx-font-weight: bold; -fx-font-size: 14px;"/>
        
        <Region VBox.vgrow="ALWAYS"/>
        
        <Label text="Manual Stock Adjustment" styleClass="section-title"/>
        <Separator/>
        <GridPane hgap="10" vgap="10">
            <TextField fx:id="adjustProductIdField" promptText="Selected Product ID" editable="false" GridPane.columnIndex="0" GridPane.rowIndex="0" GridPane.columnSpan="2" style="-fx-background-color: #f3f6f9;"/>
            <Label text="Select Quantity:" GridPane.columnIndex="0" GridPane.rowIndex="1" styleClass="text-muted"/>
            <Spinner fx:id="adjustQtySpinner" editable="true" GridPane.columnIndex="1" GridPane.rowIndex="1" maxWidth="Infinity"/>
        </GridPane>
        <HBox spacing="10">
             <Button fx:id="addStockBtn" text="✚ Add Stock" styleClass="success" HBox.hgrow="ALWAYS" maxWidth="Infinity"/>
             <Button fx:id="removeStockBtn" text="➖ Remove Stock" styleClass="warning" HBox.hgrow="ALWAYS" maxWidth="Infinity"/>
        </HBox>
    </VBox>
    
    <!-- Right Table -->
    <VBox spacing="15" styleClass="card" HBox.hgrow="ALWAYS">
        <HBox alignment="CENTER_LEFT" spacing="15">
             <Label text="Inventory Overview" styleClass="page-title"/>
             <Region HBox.hgrow="ALWAYS"/>
             <TextField fx:id="searchField" promptText="🔍 Search Products..." prefWidth="250" style="-fx-background-radius: 20;"/>
             <Button fx:id="deleteProductBtn" text="Delete Selected" styleClass="danger"/>
        </HBox>
        <Separator/>
        <TableView fx:id="productTable" VBox.vgrow="ALWAYS">
            <columns>
                <TableColumn fx:id="colId" text="ID" prefWidth="50"/>
                <TableColumn fx:id="colSku" text="SKU" prefWidth="120"/>
                <TableColumn fx:id="colName" text="Name" prefWidth="250"/>
                <TableColumn fx:id="colUom" text="Unit" prefWidth="80"/>
                <TableColumn fx:id="colStock" text="Stock" prefWidth="100"/>
            </columns>
        </TableView>
    </VBox>
</HBox>
"""

files["src/main/java/com/inventory/ui/controller/ProductController.java"] = """package com.inventory.ui.controller;

import com.inventory.model.Product;
import com.inventory.model.UnitOfMeasure;
import com.inventory.repository.ProductRepository;
import com.inventory.service.InventoryService;
import com.inventory.service.ExcelImportService;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.collections.transformation.SortedList;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import org.springframework.stereotype.Component;
import javafx.application.Platform;

import java.io.File;
import java.math.BigDecimal;

@Component
public class ProductController {

    @FXML private TextField skuField;
    @FXML private TextField nameField;
    @FXML private ComboBox<UnitOfMeasure> uomComboBox;
    @FXML private TextField costPriceField;
    @FXML private TextField sellingPriceField;
    @FXML private TextField stockField;
    @FXML private Button saveButton;
    @FXML private Button uploadExcelBtn;
    
    @FXML private TableView<Product> productTable;
    @FXML private TableColumn<Product, Long> colId;
    @FXML private TableColumn<Product, String> colSku;
    @FXML private TableColumn<Product, String> colName;
    @FXML private TableColumn<Product, UnitOfMeasure> colUom;
    @FXML private TableColumn<Product, Integer> colStock;
    @FXML private Button deleteProductBtn;
    @FXML private TextField searchField;

    @FXML private TextField adjustProductIdField;
    @FXML private Spinner<Integer> adjustQtySpinner;
    @FXML private Button addStockBtn;
    @FXML private Button removeStockBtn;

    private final ProductRepository productRepository;
    private final InventoryService inventoryService;
    private final ExcelImportService excelImportService;
    private ObservableList<Product> masterData = FXCollections.observableArrayList();

    public ProductController(ProductRepository productRepository, InventoryService inventoryService, ExcelImportService excelImportService) {
        this.productRepository = productRepository;
        this.inventoryService = inventoryService;
        this.excelImportService = excelImportService;
    }

    @FXML
    public void initialize() {
        uomComboBox.setItems(FXCollections.observableArrayList(UnitOfMeasure.values()));
        uomComboBox.getSelectionModel().selectFirst();

        adjustQtySpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, 10000, 1));

        colId.setCellValueFactory(new PropertyValueFactory<>("id"));
        colSku.setCellValueFactory(new PropertyValueFactory<>("sku"));
        colName.setCellValueFactory(new PropertyValueFactory<>("name"));
        colUom.setCellValueFactory(new PropertyValueFactory<>("unitOfMeasure"));
        colStock.setCellValueFactory(new PropertyValueFactory<>("currentStock"));

        loadProducts();

        saveButton.setOnAction(e -> saveProduct());
        deleteProductBtn.setOnAction(e -> deleteSelectedProduct());
        uploadExcelBtn.setOnAction(e -> uploadExcel());

        productTable.getSelectionModel().selectedItemProperty().addListener((obs, oldSel, newSel) -> {
            if (newSel != null) {
                adjustProductIdField.setText(String.valueOf(newSel.getId()));
            }
        });

        addStockBtn.setOnAction(e -> adjustStock(true));
        removeStockBtn.setOnAction(e -> adjustStock(false));
        
        FilteredList<Product> filteredData = new FilteredList<>(masterData, p -> true);
        searchField.textProperty().addListener((observable, oldValue, newValue) -> {
            filteredData.setPredicate(product -> {
                if (newValue == null || newValue.isEmpty()) return true;
                String lowerCaseFilter = newValue.toLowerCase();
                if (product.getName().toLowerCase().contains(lowerCaseFilter)) return true;
                if (product.getSku().toLowerCase().contains(lowerCaseFilter)) return true;
                return false;
            });
        });
        SortedList<Product> sortedData = new SortedList<>(filteredData);
        sortedData.comparatorProperty().bind(productTable.comparatorProperty());
        productTable.setItems(sortedData);
    }

    private void loadProducts() {
        masterData.setAll(productRepository.findAll());
    }

    private void uploadExcel() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Excel File");
        fileChooser.getExtensionFilters().addAll(
            new FileChooser.ExtensionFilter("Excel Files", "*.xls", "*.xlsx")
        );
        File selectedFile = fileChooser.showOpenDialog(null);
        if (selectedFile != null) {
            try {
                int imported = excelImportService.importProductsFromExcel(selectedFile);
                showInfo("Successfully imported/updated " + imported + " products from Excel!");
                loadProducts();
            } catch (Exception ex) {
                showError("Failed to parse Excel file: " + ex.getMessage());
            }
        }
    }

    private void saveProduct() {
        try {
            Product product = new Product();
            product.setSku(skuField.getText());
            product.setName(nameField.getText());
            product.setUnitOfMeasure(uomComboBox.getValue());
            product.setCostPrice(new BigDecimal(costPriceField.getText()));
            product.setSellingPrice(new BigDecimal(sellingPriceField.getText()));
            product.setCurrentStock(Integer.parseInt(stockField.getText()));

            productRepository.save(product);
            showInfo("Product saved successfully!");
            
            loadProducts();
            
            skuField.clear(); nameField.clear(); costPriceField.clear();
            sellingPriceField.clear(); stockField.clear();
        } catch (Exception ex) {
            showError("Error saving product: " + ex.getMessage());
        }
    }

    private void deleteSelectedProduct() {
        Product selected = productTable.getSelectionModel().getSelectedItem();
        if (selected == null) {
            showError("Please select a product from the table to delete.");
            return;
        }

        Alert confirm = new Alert(Alert.AlertType.CONFIRMATION, "Are you sure you want to delete this product?", ButtonType.YES, ButtonType.NO);
        confirm.showAndWait().ifPresent(res -> {
            if (res == ButtonType.YES) {
                try {
                    inventoryService.deleteProduct(selected.getId());
                    loadProducts();
                } catch (Exception ex) {
                    showError("Could not delete product: " + ex.getMessage());
                }
            }
        });
    }

    private void adjustStock(boolean isAdding) {
        try {
            Long productId = Long.parseLong(adjustProductIdField.getText());
            int qty = adjustQtySpinner.getValue();
            
            if (qty <= 0) {
                showError("Quantity must be greater than zero.");
                return;
            }

            int delta = isAdding ? qty : -qty;
            String note = isAdding ? "Manual Add" : "Manual Remove";
            
            inventoryService.adjustProductStock(productId, delta, note);
            showInfo("Stock adjusted successfully!");
            loadProducts();
            adjustQtySpinner.getValueFactory().setValue(1);
            
        } catch (NumberFormatException ex) {
            showError("Please enter valid Product ID and Quantity.");
        } catch (Exception ex) {
            showError(ex.getMessage());
        }
    }

    private void showError(String msg) {
        Platform.runLater(() -> new Alert(Alert.AlertType.ERROR, msg).showAndWait());
    }

    private void showInfo(String msg) {
        Platform.runLater(() -> new Alert(Alert.AlertType.INFORMATION, msg).showAndWait());
    }
}
"""

for filepath, content in files.items():
    with open(os.path.join(base_dir, filepath), "w") as f:
        f.write(content)
