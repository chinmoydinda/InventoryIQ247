package com.inventory;
import javafx.application.Application;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;

@SpringBootApplication
@EnableAsync
public class DesktopInventoryApplication {
    public static void main(String[] args) {
        Application.launch(MainApplication.class, args);
    }
}
