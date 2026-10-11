import os

base_dir = "/Users/chinmoy/IdeaProjects/InventoryIQ"
files = {}

# ---------------------------------------------------------
# 1. Update Main Layout & Controller for New Sidebar Tabs
# ---------------------------------------------------------
files["src/main/resources/fxml/main_layout.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<BorderPane prefHeight="800.0" prefWidth="1280.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.MainController">
    <left>
        <VBox spacing="5" styleClass="sidebar" prefWidth="260">
            <padding>
                <Insets top="30" right="0" bottom="30" left="0"/>
            </padding>
            <HBox alignment="CENTER" style="-fx-padding: 0 0 30 0;">
                 <Label text="⚡ INVENTORY" style="-fx-text-fill: white; -fx-font-size: 22px; -fx-font-weight: 900;"/>
            </HBox>
            <Button fx:id="navDashboardBtn" text="📊  Dashboard" styleClass="sidebar-button" maxWidth="Infinity"/>
            <Button fx:id="navProductsBtn" text="📦  Products Database" styleClass="sidebar-button" maxWidth="Infinity"/>
            <Button fx:id="navBundlesBtn" text="🎁  Bundle Management" styleClass="sidebar-button" maxWidth="Infinity"/>
            <Button fx:id="navAuditBtn" text="📜  Audit Ledger" styleClass="sidebar-button" maxWidth="Infinity"/>
        </VBox>
    </left>
    <center>
        <StackPane fx:id="contentArea" styleClass="background-pane"/>
    </center>
</BorderPane>
"""

files["src/main/java/com/inventory/ui/controller/MainController.java"] = """package com.inventory.ui.controller;

import com.inventory.config.SpringFXMLLoader;
import javafx.fxml.FXML;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import org.springframework.stereotype.Component;

@Component
public class MainController {
    @FXML private Button navDashboardBtn;
    @FXML private Button navProductsBtn;
    @FXML private Button navBundlesBtn;
    @FXML private Button navAuditBtn;
    @FXML private StackPane contentArea;

    private final SpringFXMLLoader fxmlLoader;

    public MainController(SpringFXMLLoader fxmlLoader) {
        this.fxmlLoader = fxmlLoader;
    }

    @FXML
    public void initialize() {
        try {
            Parent dashboardView = (Parent) fxmlLoader.load("/fxml/dashboard_view.fxml");
            Parent productView = (Parent) fxmlLoader.load("/fxml/product_view.fxml");
            Parent bundleView = (Parent) fxmlLoader.load("/fxml/bundle_view.fxml");
            Parent auditView = (Parent) fxmlLoader.load("/fxml/audit_view.fxml");
            
            contentArea.getChildren().setAll(dashboardView);

            navDashboardBtn.setOnAction(e -> contentArea.getChildren().setAll(dashboardView));
            navProductsBtn.setOnAction(e -> contentArea.getChildren().setAll(productView));
            navBundlesBtn.setOnAction(e -> contentArea.getChildren().setAll(bundleView));
            navAuditBtn.setOnAction(e -> contentArea.getChildren().setAll(auditView));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
"""

# ---------------------------------------------------------
# 2. Dashboard View & Controller
# ---------------------------------------------------------
files["src/main/resources/fxml/dashboard_view.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<VBox spacing="20" prefHeight="768.0" prefWidth="1024.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.DashboardController" styleClass="background-pane">
    <padding>
        <Insets top="40" right="40" bottom="40" left="40"/>
    </padding>

    <Label text="Executive Dashboard" styleClass="page-title" style="-fx-font-size: 28px;"/>
    
    <HBox spacing="20">
        <!-- Metric Cards -->
        <VBox styleClass="card" HBox.hgrow="ALWAYS" alignment="CENTER" spacing="10">
            <Label text="Total Products" styleClass="text-muted"/>
            <Label fx:id="totalProductsLabel" text="0" style="-fx-font-size: 36px; -fx-font-weight: bold; -fx-text-fill: #3699ff;"/>
        </VBox>
        <VBox styleClass="card" HBox.hgrow="ALWAYS" alignment="CENTER" spacing="10">
            <Label text="Total Bundles" styleClass="text-muted"/>
            <Label fx:id="totalBundlesLabel" text="0" style="-fx-font-size: 36px; -fx-font-weight: bold; -fx-text-fill: #8950fc;"/>
        </VBox>
        <VBox styleClass="card" HBox.hgrow="ALWAYS" alignment="CENTER" spacing="10">
            <Label text="Total Inventory Value" styleClass="text-muted"/>
            <Label fx:id="totalValueLabel" text="$0.00" style="-fx-font-size: 36px; -fx-font-weight: bold; -fx-text-fill: #1bc5bd;"/>
        </VBox>
    </HBox>
    
    <VBox spacing="15" styleClass="card" VBox.vgrow="ALWAYS">
        <HBox alignment="CENTER_LEFT">
             <Label text="Low Stock Alerts (Requires Restock)" styleClass="section-title" HBox.hgrow="ALWAYS" maxWidth="Infinity"/>
             <Button fx:id="refreshBtn" text="Refresh Data" styleClass="accent"/>
        </HBox>
        <Separator/>
        <TableView fx:id="lowStockTable" VBox.vgrow="ALWAYS">
            <columns>
                <TableColumn fx:id="colSku" text="SKU" prefWidth="150"/>
                <TableColumn fx:id="colName" text="Product Name" prefWidth="300"/>
                <TableColumn fx:id="colStock" text="Current Stock" prefWidth="150"/>
            </columns>
        </TableView>
    </VBox>
</VBox>
"""

files["src/main/java/com/inventory/ui/controller/DashboardController.java"] = """package com.inventory.ui.controller;

import com.inventory.model.Product;
import com.inventory.repository.BundleRepository;
import com.inventory.repository.ProductRepository;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import org.springframework.stereotype.Component;
import javafx.application.Platform;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class DashboardController {
    @FXML private Label totalProductsLabel;
    @FXML private Label totalBundlesLabel;
    @FXML private Label totalValueLabel;
    @FXML private Button refreshBtn;
    
    @FXML private TableView<Product> lowStockTable;
    @FXML private TableColumn<Product, String> colSku;
    @FXML private TableColumn<Product, String> colName;
    @FXML private TableColumn<Product, Integer> colStock;

    private final ProductRepository productRepository;
    private final BundleRepository bundleRepository;

    public DashboardController(ProductRepository productRepository, BundleRepository bundleRepository) {
        this.productRepository = productRepository;
        this.bundleRepository = bundleRepository;
    }

    @FXML
    public void initialize() {
        colSku.setCellValueFactory(new PropertyValueFactory<>("sku"));
        colName.setCellValueFactory(new PropertyValueFactory<>("name"));
        colStock.setCellValueFactory(new PropertyValueFactory<>("currentStock"));

        refreshBtn.setOnAction(e -> loadDashboardData());
        
        Platform.runLater(this::loadDashboardData);
    }

    private void loadDashboardData() {
        List<Product> products = productRepository.findAll();
        
        long totalProducts = products.size();
        long totalBundles = bundleRepository.count();
        
        BigDecimal totalValue = products.stream()
                .map(p -> p.getCostPrice().multiply(BigDecimal.valueOf(p.getCurrentStock())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);

        List<Product> lowStock = products.stream()
                .filter(p -> p.getCurrentStock() < 50)
                .collect(Collectors.toList());

        Platform.runLater(() -> {
            totalProductsLabel.setText(String.valueOf(totalProducts));
            totalBundlesLabel.setText(String.valueOf(totalBundles));
            totalValueLabel.setText(String.format("$%,.2f", totalValue));
            lowStockTable.setItems(FXCollections.observableArrayList(lowStock));
        });
    }
}
"""

# ---------------------------------------------------------
# 3. Audit Ledger View & Controller
# ---------------------------------------------------------
files["src/main/resources/fxml/audit_view.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<VBox spacing="20" prefHeight="768.0" prefWidth="1024.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.AuditController" styleClass="background-pane">
    <padding>
        <Insets top="30" right="40" bottom="40" left="40"/>
    </padding>

    <VBox spacing="15" styleClass="card" VBox.vgrow="ALWAYS">
        <HBox alignment="CENTER_LEFT">
             <Label text="Global Audit Ledger" styleClass="page-title" HBox.hgrow="ALWAYS" maxWidth="Infinity"/>
             <Button fx:id="refreshBtn" text="Refresh Ledger" styleClass="accent"/>
        </HBox>
        <Separator/>
        <TableView fx:id="auditTable" VBox.vgrow="ALWAYS">
            <columns>
                <TableColumn fx:id="colId" text="Record ID" prefWidth="80"/>
                <TableColumn fx:id="colProductId" text="Product ID" prefWidth="80"/>
                <TableColumn fx:id="colType" text="Movement Type" prefWidth="180"/>
                <TableColumn fx:id="colDelta" text="Qty Change" prefWidth="100"/>
                <TableColumn fx:id="colBalance" text="New Balance" prefWidth="100"/>
                <TableColumn fx:id="colNote" text="Reference Note" prefWidth="250"/>
                <TableColumn fx:id="colDate" text="Timestamp" prefWidth="180"/>
            </columns>
        </TableView>
    </VBox>
</VBox>
"""

files["src/main/java/com/inventory/ui/controller/AuditController.java"] = """package com.inventory.ui.controller;

import com.inventory.model.StockMovement;
import com.inventory.repository.StockMovementRepository;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import org.springframework.stereotype.Component;
import org.springframework.data.domain.Sort;
import javafx.application.Platform;

import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Component
public class AuditController {

    @FXML private TableView<StockMovement> auditTable;
    @FXML private TableColumn<StockMovement, Long> colId;
    @FXML private TableColumn<StockMovement, Long> colProductId;
    @FXML private TableColumn<StockMovement, String> colType;
    @FXML private TableColumn<StockMovement, Integer> colDelta;
    @FXML private TableColumn<StockMovement, Integer> colBalance;
    @FXML private TableColumn<StockMovement, String> colNote;
    @FXML private TableColumn<StockMovement, String> colDate;
    @FXML private Button refreshBtn;

    private final StockMovementRepository stockMovementRepository;
    private final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneId.systemDefault());

    public AuditController(StockMovementRepository stockMovementRepository) {
        this.stockMovementRepository = stockMovementRepository;
    }

    @FXML
    public void initialize() {
        colId.setCellValueFactory(new PropertyValueFactory<>("id"));
        colProductId.setCellValueFactory(new PropertyValueFactory<>("productId"));
        colType.setCellValueFactory(cellData -> new SimpleStringProperty(cellData.getValue().getMovementType().name()));
        colDelta.setCellValueFactory(new PropertyValueFactory<>("quantityDelta"));
        colBalance.setCellValueFactory(new PropertyValueFactory<>("balanceAfter"));
        colNote.setCellValueFactory(new PropertyValueFactory<>("referenceNote"));
        colDate.setCellValueFactory(cellData -> new SimpleStringProperty(formatter.format(cellData.getValue().getTimestamp())));

        refreshBtn.setOnAction(e -> loadData());
        
        Platform.runLater(this::loadData);
    }

    private void loadData() {
        List<StockMovement> movements = stockMovementRepository.findAll(Sort.by(Sort.Direction.DESC, "timestamp"));
        auditTable.setItems(FXCollections.observableArrayList(movements));
    }
}
"""

for filepath, content in files.items():
    with open(os.path.join(base_dir, filepath), "w") as f:
        f.write(content)
