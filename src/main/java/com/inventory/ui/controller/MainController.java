package com.inventory.ui.controller;

import com.inventory.config.SpringFXMLLoader;
import javafx.fxml.FXML;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.StackPane;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.List;

@Component
public class MainController {
    @FXML private Button navDashboardBtn;
    @FXML private Button navProductsBtn;
    @FXML private Button navBundlesBtn;
    @FXML private Button navAuditBtn;
    @FXML private Label currentPageLabel;
    @FXML private StackPane contentArea;

    private final SpringFXMLLoader fxmlLoader;

    public MainController(SpringFXMLLoader fxmlLoader) {
        this.fxmlLoader = fxmlLoader;
    }

    @FXML
    public void initialize() throws IOException {
        Parent dashboard = (Parent) fxmlLoader.load("/fxml/dashboard_view.fxml");
        Parent products = (Parent) fxmlLoader.load("/fxml/product_view.fxml");
        Parent bundles = (Parent) fxmlLoader.load("/fxml/bundle_view.fxml");
        Parent audit = (Parent) fxmlLoader.load("/fxml/audit_view.fxml");
        navDashboardBtn.setOnAction(e -> navigate(navDashboardBtn, dashboard));
        navProductsBtn.setOnAction(e -> navigate(navProductsBtn, products));
        navBundlesBtn.setOnAction(e -> navigate(navBundlesBtn, bundles));
        navAuditBtn.setOnAction(e -> navigate(navAuditBtn, audit));
        navigate(navDashboardBtn, dashboard);
    }

    private void navigate(Button selected, Parent view) {
        for (Button button : List.of(navDashboardBtn, navProductsBtn, navBundlesBtn, navAuditBtn)) {
            button.getStyleClass().remove("sidebar-button-active");
        }
        selected.getStyleClass().add("sidebar-button-active");
        currentPageLabel.setText(selected.getText());
        contentArea.getChildren().setAll(view);
    }
}
