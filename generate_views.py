import os

base_dir = "/Users/chinmoy/IdeaProjects/InventoryIQ"

files = {}

files["src/main/java/com/inventory/ui/controller/ProductController.java"] = """package com.inventory.ui.controller;

import com.inventory.model.Product;
import com.inventory.model.UnitOfMeasure;
import com.inventory.repository.ProductRepository;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import org.springframework.stereotype.Component;

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

    private final ProductRepository productRepository;

    public ProductController(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @FXML
    public void initialize() {
        uomComboBox.setItems(FXCollections.observableArrayList(UnitOfMeasure.values()));
        uomComboBox.getSelectionModel().selectFirst();

        colId.setCellValueFactory(new PropertyValueFactory<>("id"));
        colSku.setCellValueFactory(new PropertyValueFactory<>("sku"));
        colName.setCellValueFactory(new PropertyValueFactory<>("name"));
        colUom.setCellValueFactory(new PropertyValueFactory<>("unitOfMeasure"));
        colStock.setCellValueFactory(new PropertyValueFactory<>("currentStock"));

        loadProducts();

        saveButton.setOnAction(e -> saveProduct());
    }

    private void loadProducts() {
        productTable.setItems(FXCollections.observableArrayList(productRepository.findAll()));
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
            
            Alert alert = new Alert(Alert.AlertType.INFORMATION, "Product saved successfully!");
            alert.showAndWait();
            
            loadProducts();
            
            skuField.clear();
            nameField.clear();
            costPriceField.clear();
            sellingPriceField.clear();
            stockField.clear();
        } catch (Exception ex) {
            Alert alert = new Alert(Alert.AlertType.ERROR, "Error saving product: " + ex.getMessage());
            alert.showAndWait();
        }
    }
}
"""

files["src/main/resources/fxml/product_view.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<SplitPane dividerPositions="0.3" prefHeight="768.0" prefWidth="1024.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.ProductController">
   <items>
      <VBox spacing="15" style="-fx-background-color: #ffffff;">
         <padding>
            <Insets top="20" right="20" bottom="20" left="20"/>
         </padding>
         
         <Label text="Create / Edit Product" style="-fx-font-size: 20px; -fx-font-weight: bold;"/>
         
         <GridPane hgap="10" vgap="15">
             <Label text="SKU:" GridPane.columnIndex="0" GridPane.rowIndex="0"/>
             <TextField fx:id="skuField" GridPane.columnIndex="1" GridPane.rowIndex="0"/>
             
             <Label text="Name:" GridPane.columnIndex="0" GridPane.rowIndex="1"/>
             <TextField fx:id="nameField" GridPane.columnIndex="1" GridPane.rowIndex="1"/>
             
             <Label text="UOM:" GridPane.columnIndex="0" GridPane.rowIndex="2"/>
             <ComboBox fx:id="uomComboBox" GridPane.columnIndex="1" GridPane.rowIndex="2" maxWidth="Infinity"/>
             
             <Label text="Cost Price:" GridPane.columnIndex="0" GridPane.rowIndex="3"/>
             <TextField fx:id="costPriceField" GridPane.columnIndex="1" GridPane.rowIndex="3"/>
             
             <Label text="Selling Price:" GridPane.columnIndex="0" GridPane.rowIndex="4"/>
             <TextField fx:id="sellingPriceField" GridPane.columnIndex="1" GridPane.rowIndex="4"/>
             
             <Label text="Initial Stock:" GridPane.columnIndex="0" GridPane.rowIndex="5"/>
             <TextField fx:id="stockField" GridPane.columnIndex="1" GridPane.rowIndex="5"/>
         </GridPane>
         
         <Button fx:id="saveButton" text="Save Product" styleClass="accent" maxWidth="Infinity"/>
      </VBox>
      
      <VBox spacing="10" style="-fx-background-color: #f4f5f7;">
         <padding>
            <Insets top="20" right="20" bottom="20" left="20"/>
         </padding>
         <Label text="Product Inventory" style="-fx-font-size: 18px; -fx-font-weight: bold;"/>
         <TableView fx:id="productTable" VBox.vgrow="ALWAYS">
             <columns>
                 <TableColumn fx:id="colId" text="ID" prefWidth="50"/>
                 <TableColumn fx:id="colSku" text="SKU" prefWidth="120"/>
                 <TableColumn fx:id="colName" text="Name" prefWidth="200"/>
                 <TableColumn fx:id="colUom" text="UOM" prefWidth="80"/>
                 <TableColumn fx:id="colStock" text="Stock" prefWidth="100"/>
             </columns>
         </TableView>
      </VBox>
   </items>
</SplitPane>
"""

files["src/main/java/com/inventory/ui/controller/MainController.java"] = """package com.inventory.ui.controller;

import com.inventory.config.SpringFXMLLoader;
import javafx.fxml.FXML;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class MainController {

    @FXML private Button navProductsBtn;
    @FXML private Button navBundlesBtn;
    @FXML private StackPane contentArea;

    private final SpringFXMLLoader fxmlLoader;
    private Parent productView;
    private Parent bundleView;

    public MainController(SpringFXMLLoader fxmlLoader) {
        this.fxmlLoader = fxmlLoader;
    }

    @FXML
    public void initialize() {
        try {
            productView = (Parent) fxmlLoader.load("/fxml/product_view.fxml");
            bundleView = (Parent) fxmlLoader.load("/fxml/bundle_view.fxml");
            
            contentArea.getChildren().setAll(productView);

            navProductsBtn.setOnAction(e -> contentArea.getChildren().setAll(productView));
            navBundlesBtn.setOnAction(e -> contentArea.getChildren().setAll(bundleView));

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
"""

files["src/main/resources/fxml/main_layout.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<BorderPane prefHeight="768.0" prefWidth="1200.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.MainController">
    
    <left>
        <VBox spacing="15" style="-fx-background-color: #2b2d30;">
            <padding>
                <Insets top="30" right="15" bottom="30" left="15"/>
            </padding>
            <Label text="INVENTORY" style="-fx-text-fill: white; -fx-font-size: 20px; -fx-font-weight: bold;"/>
            <Separator style="-fx-background-color: #555555;"/>
            <Button fx:id="navProductsBtn" text="📦 Products" style="-fx-text-fill: white; -fx-background-color: transparent; -fx-font-size: 16px; -fx-cursor: hand;" maxWidth="Infinity" alignment="BASELINE_LEFT"/>
            <Button fx:id="navBundlesBtn" text="🎁 Bundles" style="-fx-text-fill: white; -fx-background-color: transparent; -fx-font-size: 16px; -fx-cursor: hand;" maxWidth="Infinity" alignment="BASELINE_LEFT"/>
        </VBox>
    </left>

    <center>
        <StackPane fx:id="contentArea"/>
    </center>
</BorderPane>
"""

files["src/main/java/com/inventory/MainApplication.java"] = """package com.inventory;

import com.inventory.config.SpringFXMLLoader;
import javafx.application.Application;
import javafx.application.Platform;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;
import atlantafx.base.theme.PrimerLight;

public class MainApplication extends Application {
    private ConfigurableApplicationContext applicationContext;

    @Override
    public void init() {
        applicationContext = new SpringApplicationBuilder(DesktopInventoryApplication.class).run();
    }

    @Override
    public void start(Stage stage) throws Exception {
        Application.setUserAgentStylesheet(new PrimerLight().getUserAgentStylesheet());

        SpringFXMLLoader fxmlLoader = applicationContext.getBean(SpringFXMLLoader.class);
        Parent root = (Parent) fxmlLoader.load("/fxml/main_layout.fxml");
        
        stage.setTitle("Desktop Inventory & Stock Management");
        stage.setScene(new Scene(root, 1200, 768));
        stage.show();
    }

    @Override
    public void stop() {
        applicationContext.close();
        Platform.exit();
    }
}
"""

for filepath, content in files.items():
    with open(os.path.join(base_dir, filepath), "w") as f:
        f.write(content)
