package com.inventory.ui.controller;

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
