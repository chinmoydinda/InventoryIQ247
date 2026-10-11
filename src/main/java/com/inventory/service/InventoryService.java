package com.inventory.service;

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
    public List<Bundle> getAllBundlesWithComputedAvailability() {
        List<Bundle> bundles = bundleRepository.findAll();
        for (Bundle b : bundles) {
            b.setComputedAvailability(calculateBundleAvailability(b.getId()));
        }
        return bundles;
    }

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
    
    @Transactional(readOnly = true)
    public List<BundleItem> getBundleComponents(Long bundleId) {
        Bundle bundle = bundleRepository.findByIdWithItems(bundleId).orElse(null);
        if (bundle == null) return List.of();
        
        bundle.getItems().forEach(item -> {
            item.getProduct().getSku();
            item.getProduct().getName();
        });
        return bundle.getItems();
    }

    @Transactional
    public void dispatchBundle(Long bundleId, int quantityToDispatch, String referenceNote) {
        if (quantityToDispatch <= 0) {
            throw new IllegalArgumentException("Dispatch quantity must be greater than zero.");
        }

        Bundle bundle = bundleRepository.findByIdWithItems(bundleId)
                .orElseThrow(() -> new IllegalArgumentException("Bundle not found: " + bundleId));

        for (BundleItem item : bundle.getItems()) {
            int totalRequired = item.getQuantityRequired() * quantityToDispatch;
            adjustStockInternal(item.getProduct().getId(), -totalRequired, MovementType.BUNDLE_SALE, 
                    referenceNote != null ? referenceNote : "Bundle dispatch: " + bundle.getName());
        }
    }

    @Transactional
    public void restockBundle(Long bundleId, int quantityToRestock, String referenceNote) {
        if (quantityToRestock <= 0) {
            throw new IllegalArgumentException("Restock quantity must be greater than zero.");
        }

        Bundle bundle = bundleRepository.findByIdWithItems(bundleId)
                .orElseThrow(() -> new IllegalArgumentException("Bundle not found: " + bundleId));

        for (BundleItem item : bundle.getItems()) {
            int totalToAdd = item.getQuantityRequired() * quantityToRestock;
            adjustStockInternal(item.getProduct().getId(), totalToAdd, MovementType.INWARD, 
                    referenceNote != null ? referenceNote : "Bundle return/restock: " + bundle.getName());
        }
    }

    @Transactional
    public void adjustProductStock(Long productId, int quantityDelta, String referenceNote) {
        if (quantityDelta == 0) return;
        MovementType type = quantityDelta > 0 ? MovementType.MANUAL_ADJUSTMENT : MovementType.DAMAGE;
        adjustStockInternal(productId, quantityDelta, type, referenceNote);
    }

    private void adjustStockInternal(Long productId, int quantityDelta, MovementType type, String note) {
        Product product = productRepository.findByIdForUpdate(productId)
                .orElseThrow(() -> new IllegalArgumentException("Product not found: " + productId));

        if (product.getCurrentStock() + quantityDelta < 0) {
            throw new InsufficientStockException(
                    String.format("Insufficient stock for product '%s'. Trying to remove: %d, Available: %d",
                            product.getName(), -quantityDelta, product.getCurrentStock())
            );
        }

        product.setCurrentStock(product.getCurrentStock() + quantityDelta);
        productRepository.save(product);

        StockMovement movement = new StockMovement();
        movement.setProductId(product.getId());
        movement.setMovementType(type);
        movement.setQuantityDelta(quantityDelta);
        movement.setBalanceAfter(product.getCurrentStock());
        movement.setReferenceNote(note);
        stockMovementRepository.save(movement);
    }

    @Transactional
    public void deleteProduct(Long productId) {
        // Find if this product is part of any bundle
        long bundleCount = bundleRepository.findAll().stream()
                .filter(b -> b.getItems().stream().anyMatch(i -> i.getProduct().getId().equals(productId)))
                .count();
        if (bundleCount > 0) {
            throw new IllegalStateException("Cannot delete product because it is used in " + bundleCount + " bundle(s).");
        }
        productRepository.deleteById(productId);
    }

    @Transactional
    public void deleteBundle(Long bundleId) {
        bundleRepository.deleteById(bundleId);
    }
}
