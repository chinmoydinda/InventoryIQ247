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
        <Label text="New Product" styleClass="page-title"/>
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
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.collections.transformation.SortedList;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import org.springframework.stereotype.Component;
import javafx.application.Platform;

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
    private ObservableList<Product> masterData = FXCollections.observableArrayList();

    public ProductController(ProductRepository productRepository, InventoryService inventoryService) {
        this.productRepository = productRepository;
        this.inventoryService = inventoryService;
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

files["src/main/resources/fxml/bundle_view.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<HBox spacing="20" prefHeight="768.0" prefWidth="1024.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.BundleController" styleClass="background-pane">
    <padding>
        <Insets top="30" right="30" bottom="30" left="30"/>
    </padding>

    <!-- Left Pane: Bundle Creation -->
    <VBox spacing="20" styleClass="card" prefWidth="350">
        <Label text="Create Bundle" styleClass="page-title"/>
        <Separator/>
        <GridPane hgap="10" vgap="20">
            <Label text="Bundle SKU" GridPane.columnIndex="0" GridPane.rowIndex="0" styleClass="text-muted"/>
            <TextField fx:id="newBundleSkuField" GridPane.columnIndex="0" GridPane.rowIndex="1" GridPane.columnSpan="2"/>
            
            <Label text="Bundle Name" GridPane.columnIndex="0" GridPane.rowIndex="2" styleClass="text-muted"/>
            <TextField fx:id="newBundleNameField" GridPane.columnIndex="0" GridPane.rowIndex="3" GridPane.columnSpan="2"/>
            
            <Label text="Bundle Price ($)" GridPane.columnIndex="0" GridPane.rowIndex="4" styleClass="text-muted"/>
            <TextField fx:id="newBundlePriceField" GridPane.columnIndex="0" GridPane.rowIndex="5" GridPane.columnSpan="2"/>
        </GridPane>
        
        <Label text="Recipe Items" styleClass="section-title"/>
        <HBox spacing="10">
            <ComboBox fx:id="productComboBox" promptText="Select Product" HBox.hgrow="ALWAYS" maxWidth="Infinity"/>
            <TextField fx:id="requiredQtyField" promptText="Qty" prefWidth="70"/>
            <Button fx:id="addComponentBtn" text="+" styleClass="accent" prefWidth="40"/>
        </HBox>
        <ListView fx:id="recipeListView" prefHeight="130"/>
        
        <Region VBox.vgrow="ALWAYS"/>
        <Button fx:id="saveBundleBtn" text="Save Full Bundle" styleClass="success" maxWidth="Infinity" prefHeight="45" style="-fx-font-weight: bold; -fx-font-size: 14px;"/>
    </VBox>
    
    <!-- Middle & Right Pane: Tables and Dispatch -->
    <VBox spacing="20" HBox.hgrow="ALWAYS">
        
        <!-- Top Card: Bundle List -->
        <VBox spacing="15" styleClass="card" VBox.vgrow="ALWAYS">
            <HBox alignment="CENTER_LEFT" spacing="15">
                <Label text="Bundle Catalog" styleClass="page-title"/>
                <Region HBox.hgrow="ALWAYS"/>
                <TextField fx:id="searchField" promptText="🔍 Search Bundles..." prefWidth="250" style="-fx-background-radius: 20;"/>
                <Button fx:id="deleteBundleBtn" text="Delete Selected" styleClass="danger"/>
            </HBox>
            <TableView fx:id="bundleTable" VBox.vgrow="ALWAYS">
                <columns>
                    <TableColumn fx:id="colBundleId" text="ID" prefWidth="50"/>
                    <TableColumn fx:id="colBundleSku" text="SKU" prefWidth="120"/>
                    <TableColumn fx:id="colBundleName" text="Name" prefWidth="250"/>
                    <TableColumn fx:id="colBundlePrice" text="Price" prefWidth="100"/>
                </columns>
            </TableView>
        </VBox>
        
        <!-- Bottom Area: Components & Dispatch side-by-side -->
        <HBox spacing="20" prefHeight="260">
            <VBox spacing="10" styleClass="card" HBox.hgrow="ALWAYS" prefWidth="300">
                <Label text="Components List" styleClass="section-title"/>
                <TableView fx:id="componentsTable" VBox.vgrow="ALWAYS">
                    <columns>
                        <TableColumn fx:id="colCompSku" text="SKU" prefWidth="90"/>
                        <TableColumn fx:id="colCompName" text="Product" prefWidth="140"/>
                        <TableColumn fx:id="colCompQty" text="Qty" prefWidth="60"/>
                    </columns>
                </TableView>
            </VBox>
            
            <VBox spacing="15" styleClass="card" prefWidth="350">
                <Label text="Adjust Bundle Inventory" styleClass="section-title"/>
                <Separator/>
                <GridPane hgap="10" vgap="10">
                     <TextField fx:id="bundleIdField" promptText="Selected Bundle ID" editable="false" GridPane.columnIndex="0" GridPane.rowIndex="0" GridPane.columnSpan="2" style="-fx-background-color: #f3f6f9; -fx-text-fill: #7e8299;"/>
                     <Label text="Select Quantity:" GridPane.columnIndex="0" GridPane.rowIndex="1" styleClass="text-muted"/>
                     <Spinner fx:id="dispatchQtySpinner" editable="true" GridPane.columnIndex="1" GridPane.rowIndex="1" maxWidth="Infinity"/>
                </GridPane>
                
                <Label fx:id="availabilityLabel" text="Select a bundle from the catalog" style="-fx-text-fill: #3f4254; -fx-font-weight: bold;"/>
                
                <Region VBox.vgrow="ALWAYS"/>
                <HBox spacing="10">
                    <Button fx:id="dispatchBtn" text="➖ Dispatch" styleClass="danger" HBox.hgrow="ALWAYS" maxWidth="Infinity" prefHeight="35"/>
                    <Button fx:id="restockBtn" text="✚ Restock" styleClass="success" HBox.hgrow="ALWAYS" maxWidth="Infinity" prefHeight="35"/>
                </HBox>
            </VBox>
        </HBox>
    </VBox>
</HBox>
"""

files["src/main/java/com/inventory/ui/controller/BundleController.java"] = """package com.inventory.ui.controller;

import com.inventory.model.Bundle;
import com.inventory.model.BundleItem;
import com.inventory.model.Product;
import com.inventory.repository.BundleRepository;
import com.inventory.repository.ProductRepository;
import com.inventory.service.InventoryService;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.collections.transformation.SortedList;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import org.springframework.stereotype.Component;
import javafx.application.Platform;
import javafx.util.StringConverter;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Component
public class BundleController {

    @FXML private TextField newBundleSkuField;
    @FXML private TextField newBundleNameField;
    @FXML private TextField newBundlePriceField;
    @FXML private ComboBox<Product> productComboBox;
    @FXML private TextField requiredQtyField;
    @FXML private Button addComponentBtn;
    @FXML private ListView<String> recipeListView;
    @FXML private Button saveBundleBtn;

    @FXML private TableView<Bundle> bundleTable;
    @FXML private TableColumn<Bundle, Long> colBundleId;
    @FXML private TableColumn<Bundle, String> colBundleSku;
    @FXML private TableColumn<Bundle, String> colBundleName;
    @FXML private TableColumn<Bundle, BigDecimal> colBundlePrice;
    @FXML private Button deleteBundleBtn;
    @FXML private TextField searchField;
    
    @FXML private TableView<BundleItem> componentsTable;
    @FXML private TableColumn<BundleItem, String> colCompSku;
    @FXML private TableColumn<BundleItem, String> colCompName;
    @FXML private TableColumn<BundleItem, Integer> colCompQty;

    @FXML private TextField bundleIdField;
    @FXML private Spinner<Integer> dispatchQtySpinner;
    @FXML private Label availabilityLabel;
    @FXML private Button dispatchBtn;
    @FXML private Button restockBtn;

    private final InventoryService inventoryService;
    private final ProductRepository productRepository;
    private final BundleRepository bundleRepository;

    private List<BundleItem> currentRecipe = new ArrayList<>();
    private ObservableList<Bundle> masterData = FXCollections.observableArrayList();

    public BundleController(InventoryService inventoryService, ProductRepository productRepository, BundleRepository bundleRepository) {
        this.inventoryService = inventoryService;
        this.productRepository = productRepository;
        this.bundleRepository = bundleRepository;
    }

    @FXML
    public void initialize() {
        dispatchQtySpinner.setValueFactory(new SpinnerValueFactory.IntegerSpinnerValueFactory(1, 10000, 1));

        dispatchBtn.setOnAction(e -> processBundleMovement(false));
        restockBtn.setOnAction(e -> processBundleMovement(true));
        
        addComponentBtn.setOnAction(e -> addComponentToRecipe());
        saveBundleBtn.setOnAction(e -> saveNewBundle());
        deleteBundleBtn.setOnAction(e -> deleteSelectedBundle());
        
        productComboBox.setConverter(new StringConverter<Product>() {
            @Override
            public String toString(Product product) {
                return product == null ? null : product.getSku() + " - " + product.getName();
            }
            @Override
            public Product fromString(String string) { return null; }
        });
        
        colBundleId.setCellValueFactory(new PropertyValueFactory<>("id"));
        colBundleSku.setCellValueFactory(new PropertyValueFactory<>("bundleSku"));
        colBundleName.setCellValueFactory(new PropertyValueFactory<>("name"));
        colBundlePrice.setCellValueFactory(new PropertyValueFactory<>("bundlePrice"));
        
        colCompSku.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getProduct().getSku()));
        colCompName.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getProduct().getName()));
        colCompQty.setCellValueFactory(new PropertyValueFactory<>("quantityRequired"));

        bundleTable.getSelectionModel().selectedItemProperty().addListener((obs, oldSel, newSel) -> {
            if (newSel != null) {
                bundleIdField.setText(String.valueOf(newSel.getId()));
                loadComponentsForBundle(newSel.getId());
                calculateAvailability();
            }
        });
        
        FilteredList<Bundle> filteredData = new FilteredList<>(masterData, b -> true);
        searchField.textProperty().addListener((observable, oldValue, newValue) -> {
            filteredData.setPredicate(bundle -> {
                if (newValue == null || newValue.isEmpty()) return true;
                String lowerCaseFilter = newValue.toLowerCase();
                if (bundle.getName().toLowerCase().contains(lowerCaseFilter)) return true;
                if (bundle.getBundleSku().toLowerCase().contains(lowerCaseFilter)) return true;
                return false;
            });
        });
        SortedList<Bundle> sortedData = new SortedList<>(filteredData);
        sortedData.comparatorProperty().bind(bundleTable.comparatorProperty());
        bundleTable.setItems(sortedData);
        
        Platform.runLater(() -> {
            loadProducts();
            loadBundles();
        });
    }

    private void loadProducts() {
        productComboBox.setItems(FXCollections.observableArrayList(productRepository.findAll()));
    }

    private void loadBundles() {
        masterData.setAll(bundleRepository.findAll());
    }
    
    private void loadComponentsForBundle(Long bundleId) {
        Task<List<BundleItem>> fetchTask = new Task<>() {
            @Override
            protected List<BundleItem> call() {
                return inventoryService.getBundleComponents(bundleId);
            }
        };
        fetchTask.setOnSucceeded(e -> {
            componentsTable.setItems(FXCollections.observableArrayList(fetchTask.getValue()));
        });
        new Thread(fetchTask).start();
    }

    private void addComponentToRecipe() {
        Product selectedProduct = productComboBox.getValue();
        String qtyText = requiredQtyField.getText();
        
        if (selectedProduct == null || qtyText.isEmpty()) {
            showError("Please select a product and enter a quantity.");
            return;
        }
        
        try {
            int qty = Integer.parseInt(qtyText);
            BundleItem item = new BundleItem();
            item.setProduct(selectedProduct);
            item.setQuantityRequired(qty);
            
            currentRecipe.add(item);
            recipeListView.getItems().add(selectedProduct.getName() + " (Qty: " + qty + ")");
            requiredQtyField.clear();
        } catch (NumberFormatException ex) {
            showError("Quantity must be a valid number.");
        }
    }

    private void saveNewBundle() {
        if (currentRecipe.isEmpty()) {
            showError("A bundle must have at least one component.");
            return;
        }

        try {
            Bundle bundle = new Bundle();
            bundle.setBundleSku(newBundleSkuField.getText());
            bundle.setName(newBundleNameField.getText());
            bundle.setBundlePrice(new BigDecimal(newBundlePriceField.getText()));
            
            for (BundleItem item : currentRecipe) {
                item.setBundle(bundle);
            }
            bundle.setItems(currentRecipe);
            
            Bundle saved = bundleRepository.save(bundle);
            showInfo("Bundle '" + saved.getName() + "' created with ID: " + saved.getId());
            
            newBundleSkuField.clear(); newBundleNameField.clear(); newBundlePriceField.clear();
            recipeListView.getItems().clear(); currentRecipe.clear();
            loadBundles();
        } catch (Exception ex) {
            showError("Could not save bundle: " + ex.getMessage());
        }
    }

    private void deleteSelectedBundle() {
        Bundle selected = bundleTable.getSelectionModel().getSelectedItem();
        if (selected == null) {
            showError("Please select a bundle to delete.");
            return;
        }

        Alert confirm = new Alert(Alert.AlertType.CONFIRMATION, "Are you sure you want to delete this bundle?", ButtonType.YES, ButtonType.NO);
        confirm.showAndWait().ifPresent(res -> {
            if (res == ButtonType.YES) {
                inventoryService.deleteBundle(selected.getId());
                loadBundles();
                componentsTable.getItems().clear();
                bundleIdField.clear();
                availabilityLabel.setText("Select a bundle from the catalog");
            }
        });
    }

    private void calculateAvailability() {
        try {
            Long bundleId = Long.parseLong(bundleIdField.getText());
            Task<Integer> calcTask = new Task<>() {
                @Override
                protected Integer call() { return inventoryService.calculateBundleAvailability(bundleId); }
            };
            
            calcTask.setOnSucceeded(e -> {
                availabilityLabel.setText("Maximum limit: " + calcTask.getValue() + " bundles possible");
                availabilityLabel.setStyle("-fx-text-fill: #181c32; -fx-font-weight: bold;");
            });
            new Thread(calcTask).start();
        } catch (NumberFormatException ignored) {}
    }

    private void processBundleMovement(boolean isRestock) {
        try {
            Long bundleId = Long.parseLong(bundleIdField.getText());
            int qty = dispatchQtySpinner.getValue();
            
            Task<Void> dispatchTask = new Task<>() {
                @Override
                protected Void call() {
                    if (isRestock) {
                        inventoryService.restockBundle(bundleId, qty, "Manual Restock / Disassemble");
                    } else {
                        inventoryService.dispatchBundle(bundleId, qty, "Manual Dispatch / Assemble");
                    }
                    return null;
                }
            };
            
            dispatchTask.setOnSucceeded(e -> {
                showInfo(isRestock ? "Successfully restocked!" : "Successfully dispatched!");
                calculateAvailability(); 
                dispatchQtySpinner.getValueFactory().setValue(1);
            });
            
            dispatchTask.setOnFailed(e -> showError(dispatchTask.getException().getMessage()));
            new Thread(dispatchTask).start();
            
        } catch (NumberFormatException ex) {
            showError("Please select a valid bundle ID.");
        }
    }
    
    private void showError(String content) {
        Platform.runLater(() -> new Alert(Alert.AlertType.ERROR, content).showAndWait());
    }

    private void showInfo(String content) {
        Platform.runLater(() -> new Alert(Alert.AlertType.INFORMATION, content).showAndWait());
    }
}
"""

for filepath, content in files.items():
    with open(os.path.join(base_dir, filepath), "w") as f:
        f.write(content)
