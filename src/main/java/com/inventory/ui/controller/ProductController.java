package com.inventory.ui.controller;

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
        productTable.sceneProperty().addListener((observable, oldScene, newScene) -> {
            if (newScene != null) { loadProducts(); }
        });
        productTable.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY_FLEX_LAST_COLUMN);
        productTable.setPlaceholder(new javafx.scene.control.Label("No products found. Add a product or change your search."));
        deleteProductBtn.disableProperty().bind(productTable.getSelectionModel().selectedItemProperty().isNull());
        addStockBtn.disableProperty().bind(productTable.getSelectionModel().selectedItemProperty().isNull());
        removeStockBtn.disableProperty().bind(productTable.getSelectionModel().selectedItemProperty().isNull());

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
            adjustProductIdField.setText(newSel == null ? "" : String.valueOf(newSel.getId()));
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
            adjustQtySpinner.commitValue();
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
