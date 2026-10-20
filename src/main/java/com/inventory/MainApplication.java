package com.inventory;

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
        
        Scene scene = new Scene(root, 1440, 900);
        scene.getStylesheets().add(getClass().getResource("/css/style.css").toExternalForm());
        
        stage.setTitle("InventoryIQ247 | Inventory workspace");
        stage.setScene(scene);
        stage.setMinWidth(1200);
        stage.setMinHeight(780);
        stage.show();
    }

    @Override
    public void stop() {
        applicationContext.close();
        Platform.exit();
    }
}
