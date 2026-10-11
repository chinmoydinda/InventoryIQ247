import os

base_dir = "/Users/chinmoy/IdeaProjects/InventoryIQ/InventoryIQ"

directories = [
    "src/main/java/com/inventory/config",
    "src/main/java/com/inventory/model",
    "src/main/java/com/inventory/exception",
    "src/main/java/com/inventory/repository",
    "src/main/java/com/inventory/service",
    "src/main/java/com/inventory/ui/controller",
    "src/main/resources/fxml",
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

files = {}

files["pom.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.inventory</groupId>
    <artifactId>InventoryIQ</artifactId>
    <version>1.0.0</version>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <spring.boot.version>3.2.4</spring.boot.version>
        <javafx.version>21.0.2</javafx.version>
    </properties>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring.boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- Spring Boot -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        
        <!-- H2 Database -->
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- JavaFX -->
        <dependency>
            <groupId>org.openjfx</groupId>
            <artifactId>javafx-controls</artifactId>
            <version>${javafx.version}</version>
        </dependency>
        <dependency>
            <groupId>org.openjfx</groupId>
            <artifactId>javafx-fxml</artifactId>
            <version>${javafx.version}</version>
        </dependency>

        <!-- AtlantaFX Theme -->
        <dependency>
            <groupId>io.github.mkpaz</groupId>
            <artifactId>atlantafx-base</artifactId>
            <version>2.0.1</version>
        </dependency>
        
        <!-- Lombok -->
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring.boot.version}</version>
            </plugin>
            
            <plugin>
                <groupId>org.openjfx</groupId>
                <artifactId>javafx-maven-plugin</artifactId>
                <version>0.0.8</version>
                <configuration>
                    <mainClass>com.inventory.MainApplication</mainClass>
                </configuration>
            </plugin>
            
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.12.1</version>
                <configuration>
                    <source>21</source>
                    <target>21</target>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>"""

files["src/main/resources/application.properties"] = """spring.datasource.url=jdbc:h2:file:${user.home}/.stockmanager/data/inventory_db;AUTO_SERVER=TRUE;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE
spring.datasource.driverClassName=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.jpa.database-platform=org.hibernate.dialect.H2Dialect
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
"""

files["src/main/java/com/inventory/model/UnitOfMeasure.java"] = """package com.inventory.model;
public enum UnitOfMeasure {
    PIECE, KG, BOX, PACK
}"""

files["src/main/java/com/inventory/model/MovementType.java"] = """package com.inventory.model;
public enum MovementType {
    INWARD, SALE, BUNDLE_SALE, DAMAGE, MANUAL_ADJUSTMENT
}"""

files["src/main/java/com/inventory/model/Product.java"] = """package com.inventory.model;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.time.Instant;

@Entity
@Table(name = "products", indexes = {
    @Index(name = "idx_sku", columnList = "sku", unique = true),
    @Index(name = "idx_barcode", columnList = "barcode")
})
@Getter
@Setter
@NoArgsConstructor
public class Product {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String sku;

    @Column(nullable = false)
    private String name;

    private String description;
    
    private String barcode;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private UnitOfMeasure unitOfMeasure;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal costPrice;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal sellingPrice;

    private Integer minReorderPoint = 0;

    @Column(nullable = false)
    private Integer currentStock = 0;

    @Column(updatable = false)
    private Instant createdAt;

    private Instant updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = Instant.now();
        updatedAt = Instant.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = Instant.now();
    }
}"""

files["src/main/java/com/inventory/model/Bundle.java"] = """package com.inventory.model;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "bundles", indexes = {
    @Index(name = "idx_bundle_sku", columnList = "bundleSku", unique = true)
})
@Getter
@Setter
@NoArgsConstructor
public class Bundle {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String bundleSku;

    @Column(nullable = false)
    private String name;

    private String description;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal bundlePrice;

    @Column(nullable = false)
    private Boolean active = true;

    @OneToMany(mappedBy = "bundle", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<BundleItem> items = new ArrayList<>();
}"""

files["src/main/java/com/inventory/model/BundleItem.java"] = """package com.inventory.model;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "bundle_items")
@Getter
@Setter
@NoArgsConstructor
public class BundleItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "bundle_id", nullable = false)
    private Bundle bundle;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    @Column(nullable = false)
    private Integer quantityRequired;
}"""

files["src/main/java/com/inventory/model/StockMovement.java"] = """package com.inventory.model;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.NoArgsConstructor;
import java.time.Instant;

@Entity
@Table(name = "stock_movements")
@Getter
@Setter
@NoArgsConstructor
public class StockMovement {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long productId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private MovementType movementType;

    @Column(nullable = false)
    private Integer quantityDelta;

    @Column(nullable = false)
    private Integer balanceAfter;

    private String referenceNote;

    @Column(nullable = false, updatable = false)
    private Instant timestamp;

    @PrePersist
    protected void onCreate() {
        timestamp = Instant.now();
    }
}"""

files["src/main/java/com/inventory/exception/InsufficientStockException.java"] = """package com.inventory.exception;
public class InsufficientStockException extends RuntimeException {
    public InsufficientStockException(String message) {
        super(message);
    }
}"""

files["src/main/java/com/inventory/repository/ProductRepository.java"] = """package com.inventory.repository;
import com.inventory.model.Product;
import jakarta.persistence.LockModeType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Lock;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.Optional;

public interface ProductRepository extends JpaRepository<Product, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdForUpdate(@Param("id") Long id);
}"""

files["src/main/java/com/inventory/repository/BundleRepository.java"] = """package com.inventory.repository;
import com.inventory.model.Bundle;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.Optional;

public interface BundleRepository extends JpaRepository<Bundle, Long> {
    @Query("SELECT b FROM Bundle b LEFT JOIN FETCH b.items WHERE b.id = :id")
    Optional<Bundle> findByIdWithItems(@Param("id") Long id);
}"""

files["src/main/java/com/inventory/repository/StockMovementRepository.java"] = """package com.inventory.repository;
import com.inventory.model.StockMovement;
import org.springframework.data.jpa.repository.JpaRepository;

public interface StockMovementRepository extends JpaRepository<StockMovement, Long> {
}"""

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
}"""

files["src/main/java/com/inventory/DesktopInventoryApplication.java"] = """package com.inventory;
import javafx.application.Application;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class DesktopInventoryApplication {
    public static void main(String[] args) {
        Application.launch(MainApplication.class, args);
    }
}"""

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
        Parent root = (Parent) fxmlLoader.load("/fxml/bundle_view.fxml");
        
        stage.setTitle("Desktop Inventory & Stock Management");
        stage.setScene(new Scene(root, 1024, 768));
        stage.show();
    }

    @Override
    public void stop() {
        applicationContext.close();
        Platform.exit();
    }
}"""

files["src/main/java/com/inventory/config/SpringFXMLLoader.java"] = """package com.inventory.config;
import javafx.fxml.FXMLLoader;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;
import java.io.IOException;

@Component
public class SpringFXMLLoader {
    private final ApplicationContext context;

    public SpringFXMLLoader(ApplicationContext context) {
        this.context = context;
    }

    public Object load(String url) throws IOException {
        FXMLLoader loader = new FXMLLoader(getClass().getResource(url));
        loader.setControllerFactory(context::getBean);
        return loader.load();
    }
}"""

files["src/main/java/com/inventory/ui/controller/BundleController.java"] = """package com.inventory.ui.controller;
import com.inventory.service.InventoryService;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.layout.VBox;
import org.springframework.stereotype.Component;
import javafx.application.Platform;

@Component
public class BundleController {
    @FXML private TextField bundleIdField;
    @FXML private TextField dispatchQuantityField;
    @FXML private Label availabilityLabel;
    @FXML private Button calculateBtn;
    @FXML private Button dispatchBtn;
    @FXML private VBox rightPane;

    private final InventoryService inventoryService;

    public BundleController(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
    }

    @FXML
    public void initialize() {
        calculateBtn.setOnAction(e -> calculateAvailability());
        dispatchBtn.setOnAction(e -> dispatchBundle());
    }

    private void calculateAvailability() {
        try {
            Long bundleId = Long.parseLong(bundleIdField.getText());
            
            Task<Integer> calcTask = new Task<>() {
                @Override
                protected Integer call() throws Exception {
                    return inventoryService.calculateBundleAvailability(bundleId);
                }
            };
            
            calcTask.setOnSucceeded(e -> {
                availabilityLabel.setText("Available: " + calcTask.getValue());
                availabilityLabel.setStyle("-fx-text-fill: green; -fx-font-weight: bold;");
            });
            
            calcTask.setOnFailed(e -> {
                showError("Calculation Failed", calcTask.getException().getMessage());
            });
            
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
                protected Void call() throws Exception {
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
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(content);
        alert.showAndWait();
    }

    private void showInfo(String title, String content) {
        Alert alert = new Alert(Alert.AlertType.INFORMATION);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(content);
        alert.showAndWait();
    }
}"""

files["src/main/resources/fxml/bundle_view.fxml"] = """<?xml version="1.0" encoding="UTF-8"?>
<?import javafx.scene.control.*?>
<?import javafx.scene.layout.*?>
<?import javafx.geometry.Insets?>

<SplitPane dividerPositions="0.3" prefHeight="768.0" prefWidth="1024.0" xmlns="http://javafx.com/javafx/21" xmlns:fx="http://javafx.com/fxml/1" fx:controller="com.inventory.ui.controller.BundleController">
   <items>
      <VBox spacing="10" style="-fx-background-color: #f4f5f7;">
         <padding>
            <Insets top="20" right="20" bottom="20" left="20"/>
         </padding>
         <Label text="Bundles (Placeholder)" style="-fx-font-size: 18px; -fx-font-weight: bold;"/>
         <ListView fx:id="bundleListView" VBox.vgrow="ALWAYS"/>
      </VBox>
      
      <VBox fx:id="rightPane" spacing="20" style="-fx-background-color: #ffffff;">
         <padding>
            <Insets top="20" right="30" bottom="20" left="30"/>
         </padding>
         
         <Label text="Bundle Management" style="-fx-font-size: 24px; -fx-font-weight: bold;"/>
         
         <GridPane hgap="10" vgap="15">
             <Label text="Bundle ID:" GridPane.columnIndex="0" GridPane.rowIndex="0"/>
             <TextField fx:id="bundleIdField" promptText="Enter Bundle ID (e.g. 1)" GridPane.columnIndex="1" GridPane.rowIndex="0"/>
             
             <Label text="Dispatch Qty:" GridPane.columnIndex="0" GridPane.rowIndex="1"/>
             <TextField fx:id="dispatchQuantityField" promptText="Enter Qty" GridPane.columnIndex="1" GridPane.rowIndex="1"/>
         </GridPane>
         
         <HBox spacing="15">
             <Button fx:id="calculateBtn" text="Check Availability" styleClass="accent"/>
             <Button fx:id="dispatchBtn" text="Dispatch Bundle" styleClass="success"/>
         </HBox>
         
         <Label fx:id="availabilityLabel" text="Availability: N/A" style="-fx-font-size: 16px;"/>
         
         <Separator/>
         <Label text="Component Breakdown (Placeholder)" style="-fx-font-size: 14px; -fx-font-weight: bold;"/>
         <TableView fx:id="componentsTable" VBox.vgrow="ALWAYS">
             <columns>
                 <TableColumn text="Product SKU" prefWidth="150"/>
                 <TableColumn text="Product Name" prefWidth="250"/>
                 <TableColumn text="Qty Required" prefWidth="100"/>
                 <TableColumn text="Current Stock" prefWidth="100"/>
             </columns>
         </TableView>
      </VBox>
   </items>
</SplitPane>"""

for filepath, content in files.items():
    with open(os.path.join(base_dir, filepath), "w") as f:
        f.write(content)
