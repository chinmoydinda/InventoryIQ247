package com.inventory.ui.controller;

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
    @FXML private TableColumn<Bundle, Integer> colBundleQty;
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
        colBundleQty.setCellValueFactory(new PropertyValueFactory<>("computedAvailability"));
        
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
        Task<List<Bundle>> fetchTask = new Task<>() {
            @Override
            protected List<Bundle> call() {
                return inventoryService.getAllBundlesWithComputedAvailability();
            }
        };
        fetchTask.setOnSucceeded(e -> {
            masterData.setAll(fetchTask.getValue());
        });
        new Thread(fetchTask).start();
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
                loadBundles(); // Refresh the table quantities!
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
