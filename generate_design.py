import os

base_dir = "/Users/chinmoy/IdeaProjects/InventoryIQ"

css_dir = os.path.join(base_dir, "src/main/resources/css")
os.makedirs(css_dir, exist_ok=True)

files = {}

files["src/main/resources/css/style.css"] = """
.sidebar {
    -fx-background-color: linear-gradient(to bottom, #1e1e2d, #2b2b40);
}
.sidebar-button {
    -fx-text-fill: #a2a3b7;
    -fx-background-color: transparent;
    -fx-font-size: 15px;
    -fx-font-weight: bold;
    -fx-alignment: center-left;
    -fx-padding: 15 20 15 20;
    -fx-cursor: hand;
}
.sidebar-button:hover {
    -fx-background-color: #2b2b3c;
    -fx-text-fill: #ffffff;
}
.sidebar-button-active {
    -fx-background-color: #3699ff;
    -fx-text-fill: #ffffff;
}
.card {
    -fx-background-color: white;
    -fx-background-radius: 8;
    -fx-border-radius: 8;
    -fx-effect: dropshadow(three-pass-box, rgba(0,0,0,0.05), 10, 0, 0, 4);
    -fx-padding: 25;
}
.page-title {
    -fx-font-size: 24px;
    -fx-font-weight: 800;
    -fx-text-fill: #181c32;
}
.section-title {
    -fx-font-size: 16px;
    -fx-font-weight: bold;
    -fx-text-fill: #3f4254;
}
.background-pane {
    -fx-background-color: #f3f6f9;
}
.text-muted {
    -fx-text-fill: #7e8299;
    -fx-font-weight: bold;
}
"""

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
            <HBox alignment="CENTER" padding="0 0 30 0">
                 <Label text="⚡ INVENTORY" style="-fx-text-fill: white; -fx-font-size: 22px; -fx-font-weight: 900;"/>
            </HBox>
            <Button fx:id="navProductsBtn" text="📦  Products Database" styleClass="sidebar-button" maxWidth="Infinity"/>
            <Button fx:id="navBundlesBtn" text="🎁  Bundle Management" styleClass="sidebar-button" maxWidth="Infinity"/>
        </VBox>
    </left>
    <center>
        <StackPane fx:id="contentArea" styleClass="background-pane"/>
    </center>
</BorderPane>
"""

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
        <Region VBox.vgrow="ALWAYS"/>
        <Button fx:id="saveButton" text="Save Product" styleClass="accent" maxWidth="Infinity" prefHeight="45" style="-fx-font-weight: bold; -fx-font-size: 14px;"/>
    </VBox>
    
    <!-- Right Table -->
    <VBox spacing="15" styleClass="card" HBox.hgrow="ALWAYS">
        <Label text="Inventory Overview" styleClass="page-title"/>
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
            <Label text="Bundle Catalog" styleClass="page-title"/>
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
            
            <VBox spacing="15" styleClass="card" prefWidth="300">
                <Label text="Quick Dispatch" styleClass="section-title"/>
                <Separator/>
                <TextField fx:id="bundleIdField" promptText="Selected Bundle ID" editable="false" style="-fx-background-color: #f3f6f9; -fx-text-fill: #7e8299;"/>
                <TextField fx:id="dispatchQuantityField" promptText="Enter Dispatch Qty"/>
                
                <Region VBox.vgrow="ALWAYS"/>
                <Label fx:id="availabilityLabel" text="Select bundle to test" style="-fx-text-fill: #3f4254; -fx-font-weight: bold;"/>
                
                <HBox spacing="10">
                    <Button fx:id="calculateBtn" text="Check" styleClass="accent" HBox.hgrow="ALWAYS" maxWidth="Infinity" prefHeight="35"/>
                    <Button fx:id="dispatchBtn" text="Dispatch" styleClass="danger" HBox.hgrow="ALWAYS" maxWidth="Infinity" prefHeight="35"/>
                </HBox>
            </VBox>
        </HBox>
    </VBox>
</HBox>
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
import atlantafx.base.theme.CupertinoLight;

public class MainApplication extends Application {
    private ConfigurableApplicationContext applicationContext;

    @Override
    public void init() {
        applicationContext = new SpringApplicationBuilder(DesktopInventoryApplication.class).run();
    }

    @Override
    public void start(Stage stage) throws Exception {
        Application.setUserAgentStylesheet(new CupertinoLight().getUserAgentStylesheet());

        SpringFXMLLoader fxmlLoader = applicationContext.getBean(SpringFXMLLoader.class);
        Parent root = (Parent) fxmlLoader.load("/fxml/main_layout.fxml");
        
        Scene scene = new Scene(root, 1300, 800);
        scene.getStylesheets().add(getClass().getResource("/css/style.css").toExternalForm());
        
        stage.setTitle("NextGen Inventory & Stock System");
        stage.setScene(scene);
        stage.setMinWidth(1100);
        stage.setMinHeight(700);
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
