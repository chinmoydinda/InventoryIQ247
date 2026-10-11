package com.inventory.ui.controller;

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
