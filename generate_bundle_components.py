import os

base_dir = "/Users/chinmoy/IdeaProjects/InventoryIQ"
files = {}

# Update InventoryService to provide the components eagerly
files["src/main/java/com/inventory/service/InventoryService.java"] = """package com.inventory.service;
import com.inventory.exception.InsufficientStockException;
import com.inventory.model.*;
import com.inventory.repository.BundleRepository;
import com.inventory.repository.ProductRepository;
import com.inventory.repository.StockMovementRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
@RequiredArgsConstructor
public class InventoryService {

    private final ProductRepository productRepository;
    private final BundleRepository bundleRepository;
    private final StockMovementRepository stockMovementRepository;

    @Transactional(readOnly = true)
    public int calculateBundleAvailability(Long bundleId) {
        Bundle bundle = bundleRepository.findByIdWithItems(bundleId)
                .orElseThrow(() -> new IllegalArgumentException("Bundle not found: " + bundleId));

        if (bundle.getItems().isEmpty()) return 0;

        return bundle.getItems().stream()
                .mapToInt(item -> {
                    Product product = item.getProduct();
                    int required = item.getQuantityRequired();
                    if (required <= 0) return 0;
                    return product.getCurrentStock() / required;
                })
                .min()
                .orElse(0);
    }
    
    @Transactional(readOnly = true)
    public List<BundleItem> getBundleComponents(Long bundleId) {
        Bundle bundle = bundleRepository.findByIdWithItems(bundleId).orElse(null);
        if (bundle == null) return List.of();
        
        // Eagerly initialize the lazily-loaded products inside the transaction
        bundle.getItems().forEach(item -> {
            item.getProduct().getSku();
            item.getProduct().getName();
        });
        return bundle.getItems();
    }

    @Transactional
    public void dispatchBundle(Long bundleId, int quantityToDispatch, String referenceNote) {
        if (quantityToDispatch <= 0) {
            throw new IllegalArgumentException("Dispatch quantity must be greater than zero.");
        }

        Bundle bundle = bundleRepository.findByIdWithItems(bundleId)
                .orElseThrow(() -> new IllegalArgumentException("Bundle not found: " + bundleId));

        for (BundleItem item : bundle.getItems()) {
            int requiredForOneBundle = item.getQuantityRequired();
            int totalRequired = requiredForOneBundle * quantityToDispatch;

            Product product = productRepository.findByIdForUpdate(item.getProduct().getId())
                    .orElseThrow(() -> new IllegalArgumentException("Product not found: " + item.getProduct().getId()));

            if (product.getCurrentStock() < totalRequired) {
                throw new InsufficientStockException(
                        String.format("Insufficient stock for product '%s'. Required: %d, Available: %d",
                                product.getName(), totalRequired, product.getCurrentStock())
                );
            }

            product.setCurrentStock(product.getCurrentStock() - totalRequired);
            productRepository.save(product);

            StockMovement movement = new StockMovement();
            movement.setProductId(product.getId());
            movement.setMovementType(MovementType.BUNDLE_SALE);
            movement.setQuantityDelta(-totalRequired);
            movement.setBalanceAfter(product.getCurrentStock());
            movement.setReferenceNote(referenceNote != null ? referenceNote : "Bundle dispatch: " + bundle.getName());
            stockMovementRepository.save(movement);
        }
    }
}
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

    // Bundle Creation
    @FXML private TextField newBundleSkuField;
    @FXML private TextField newBundleNameField;
    @FXML private TextField newBundlePriceField;
    @FXML private ComboBox<Product> productComboBox;
    @FXML private TextField requiredQtyField;
    @FXML private Button addComponentBtn;
    @FXML private ListView<String> recipeListView;
    @FXML private Button saveBundleBtn;

    // Bundle List
    @FXML private TableView<Bundle> bundleTable;
    @FXML private TableColumn<Bundle, Long> colBundleId;
    @FXML private TableColumn<Bundle, String> colBundleSku;
    @FXML private TableColumn<Bundle, String> colBundleName;
    @FXML private TableColumn<Bundle, BigDecimal> colBundlePrice;
    
    // Components List
    @FXML private TableView<BundleItem> componentsTable;
    @FXML private TableColumn<BundleItem, String> colCompSku;
    @FXML private TableColumn<BundleItem, String> colCompName;
    @FXML private TableColumn<BundleItem, Integer> colCompQty;

    // Dispatch & Availability
    @FXML private TextField bundleIdField;
    @FXML private TextField dispatchQuantityField;
    @FXML private Label availabilityLabel;
    @FXML private Button calculateBtn;
    @FXML private Button dispatchBtn;

    private final InventoryService inventoryService;
    private final ProductRepository productRepository;
    private final BundleRepository bundleRepository;

    private List<BundleItem> currentRecipe = new ArrayList<>();

    public BundleController(InventoryService inventoryService, ProductRepository productRepository, BundleRepository bundleRepository) {
        this.inventoryService = inventoryService;
        this.productRepository = productRepository;
        this.bundleRepository = bundleRepository;
    }

    @FXML
    public void initialize() {
        calculateBtn.setOnAction(e -> calculateAvailability());
        dispatchBtn.setOnAction(e -> dispatchBundle());
        
        addComponentBtn.setOnAction(e -> addComponentToRecipe());
        saveBundleBtn.setOnAction(e -> saveNewBundle());
        
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
            }
        });
        
        Platform.runLater(() -> {
            loadProducts();
            loadBundles();
        });
    }

    private void loadProducts() {
        List<Product> products = productRepository.findAll();
        productComboBox.setItems(FXCollections.observableArrayList(products));
    }

    private void loadBundles() {
        List<Bundle> bundles = bundleRepository.findAll();
        bundleTable.setItems(FXCollections.observableArrayList(bundles));
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
            showError("Input Error", "Please select a product and enter a quantity.");
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
            showError("Input Error", "Quantity must be a valid number.");
        }
    }

    private void saveNewBundle() {
        if (currentRecipe.isEmpty()) {
            showError("Validation Error", "A bundle must have at least one component.");
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
            showInfo("Success", "Bundle '" + saved.getName() + "' created with ID: " + saved.getId());
            
            newBundleSkuField.clear();
            newBundleNameField.clear();
            newBundlePriceField.clear();
            recipeListView.getItems().clear();
            currentRecipe.clear();
            
            loadBundles();
            
        } catch (Exception ex) {
            showError("Error", "Could not save bundle: " + ex.getMessage());
        }
    }

    private void calculateAvailability() {
        try {
            Long bundleId = Long.parseLong(bundleIdField.getText());
            
            Task<Integer> calcTask = new Task<>() {
                @Override
                protected Integer call() {
                    return inventoryService.calculateBundleAvailability(bundleId);
                }
            };
            
            calcTask.setOnSucceeded(e -> {
                availabilityLabel.setText("Available: " + calcTask.getValue());
                availabilityLabel.setStyle("-fx-text-fill: green; -fx-font-weight: bold;");
            });
            
            calcTask.setOnFailed(e -> showError("Calculation Failed", calcTask.getException().getMessage()));
            
            new Thread(calcTask).start();
            
        } catch (NumberFormatException ex) {
            showError("Input Error", "Please enter a valid Bundle ID.");
        }
    }

    private void dispatchBundle() {
        try {
            Long bundleId = Long.parseLong(bundleIdField.getText());
            int qty = Integer.parseInt(dispatchQuantityField.getText());
            dispatchBtn.setDisable(true);
            
            Task<Void> dispatchTask = new Task<>() {
                @Override
                protected Void call() {
                    inventoryService.dispatchBundle(bundleId, qty, "Manual UI Dispatch");
                    return null;
                }
            };
            
            dispatchTask.setOnSucceeded(e -> {
                dispatchBtn.setDisable(false);
                showInfo("Success", "Successfully dispatched " + qty + " bundle(s).");
                calculateAvailability(); 
            });
            
            dispatchTask.setOnFailed(e -> {
                dispatchBtn.setDisable(false);
                showError("Dispatch Failed", dispatchTask.getException().getMessage());
            });
            
            new Thread(dispatchTask).start();
            
        } catch (NumberFormatException ex) {
            showError("Input Error", "Please enter valid numeric values.");
        }
    }
    
    private void showError(String title, String content) {
        Platform.runLater(() -> {
            Alert alert = new Alert(Alert.AlertType.ERROR);
            alert.setTitle(title);
            alert.setHeaderText(null);
            alert.setContentText(content);
            alert.showAndWait();
        });
    }

    private void showInfo(String title, String content) {
        Platform.runLater(() -> {
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle(title);
            alert.setHeaderText(null);
            alert.setContentText(content);
            alert.showAndWait();
        });
    }
}
"""

files["src/main/resources/fxml/bundle_view.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<SplitPane dividerPositions="0.45" prefHeight="768.0" prefWidth="1024.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.BundleController">
   <items>
      <!-- Left Pane: Bundle Creation & Recipe Builder -->
      <VBox spacing="15" style="-fx-background-color: #ffffff;">
         <padding>
            <Insets top="20" right="20" bottom="20" left="20"/>
         </padding>
         
         <Label text="Create New Bundle" style="-fx-font-size: 20px; -fx-font-weight: bold;"/>
         
         <GridPane hgap="10" vgap="15">
             <Label text="Bundle SKU:" GridPane.columnIndex="0" GridPane.rowIndex="0"/>
             <TextField fx:id="newBundleSkuField" GridPane.columnIndex="1" GridPane.rowIndex="0"/>
             
             <Label text="Bundle Name:" GridPane.columnIndex="0" GridPane.rowIndex="1"/>
             <TextField fx:id="newBundleNameField" GridPane.columnIndex="1" GridPane.rowIndex="1"/>
             
             <Label text="Bundle Price:" GridPane.columnIndex="0" GridPane.rowIndex="2"/>
             <TextField fx:id="newBundlePriceField" GridPane.columnIndex="1" GridPane.rowIndex="2"/>
         </GridPane>
         
         <Separator/>
         <Label text="Recipe Builder" style="-fx-font-size: 16px; -fx-font-weight: bold;"/>
         
         <HBox spacing="10">
             <ComboBox fx:id="productComboBox" promptText="Select Product" HBox.hgrow="ALWAYS" maxWidth="Infinity"/>
             <TextField fx:id="requiredQtyField" promptText="Qty" prefWidth="60"/>
             <Button fx:id="addComponentBtn" text="Add" styleClass="accent"/>
         </HBox>
         
         <ListView fx:id="recipeListView" prefHeight="150"/>
         
         <Button fx:id="saveBundleBtn" text="Save Full Bundle" styleClass="success" maxWidth="Infinity"/>
      </VBox>
      
      <!-- Right Pane: Table of Bundles + Components + Dispatching -->
      <VBox fx:id="rightPane" spacing="15" style="-fx-background-color: #f4f5f7;">
         <padding>
            <Insets top="20" right="20" bottom="20" left="20"/>
         </padding>
         
         <Label text="Your Bundles" style="-fx-font-size: 18px; -fx-font-weight: bold;"/>
         <TableView fx:id="bundleTable" prefHeight="180">
             <columns>
                 <TableColumn fx:id="colBundleId" text="ID" prefWidth="50"/>
                 <TableColumn fx:id="colBundleSku" text="SKU" prefWidth="120"/>
                 <TableColumn fx:id="colBundleName" text="Name" prefWidth="180"/>
                 <TableColumn fx:id="colBundlePrice" text="Price" prefWidth="80"/>
             </columns>
         </TableView>
         
         <Label text="Bundle Components" style="-fx-font-size: 16px; -fx-font-weight: bold;"/>
         <TableView fx:id="componentsTable" prefHeight="150">
             <columns>
                 <TableColumn fx:id="colCompSku" text="Product SKU" prefWidth="120"/>
                 <TableColumn fx:id="colCompName" text="Product Name" prefWidth="180"/>
                 <TableColumn fx:id="colCompQty" text="Required Qty" prefWidth="100"/>
             </columns>
         </TableView>
         
         <Separator/>
         <Label text="Dispatch Bundle" style="-fx-font-size: 18px; -fx-font-weight: bold;"/>
         
         <GridPane hgap="10" vgap="10">
             <Label text="Bundle ID:" GridPane.columnIndex="0" GridPane.rowIndex="0"/>
             <TextField fx:id="bundleIdField" promptText="Select from table" GridPane.columnIndex="1" GridPane.rowIndex="0"/>
             
             <Label text="Dispatch Qty:" GridPane.columnIndex="0" GridPane.rowIndex="1"/>
             <TextField fx:id="dispatchQuantityField" promptText="Enter Qty" GridPane.columnIndex="1" GridPane.rowIndex="1"/>
         </GridPane>
         
         <HBox spacing="15" alignment="CENTER_LEFT">
             <Button fx:id="calculateBtn" text="Check Availability" styleClass="accent"/>
             <Button fx:id="dispatchBtn" text="Dispatch Bundle" styleClass="danger"/>
             <Label fx:id="availabilityLabel" text="Availability: N/A" style="-fx-font-size: 16px;"/>
         </HBox>
         
      </VBox>
   </items>
</SplitPane>
"""

for filepath, content in files.items():
    with open(os.path.join(base_dir, filepath), "w") as f:
        f.write(content)
