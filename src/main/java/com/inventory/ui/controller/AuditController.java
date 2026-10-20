package com.inventory.ui.controller;

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
        auditTable.sceneProperty().addListener((observable, oldScene, newScene) -> {
            if (newScene != null) { loadData(); }
        });
        auditTable.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY_FLEX_LAST_COLUMN);
        auditTable.setPlaceholder(new javafx.scene.control.Label("No stock movements recorded yet."));

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
