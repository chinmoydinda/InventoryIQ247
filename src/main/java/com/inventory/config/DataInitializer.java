package com.inventory.config;

import com.inventory.model.Bundle;
import com.inventory.model.BundleItem;
import com.inventory.model.Product;
import com.inventory.model.UnitOfMeasure;
import com.inventory.repository.BundleRepository;
import com.inventory.repository.ProductRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class DataInitializer implements CommandLineRunner {

    private final ProductRepository productRepository;
    private final BundleRepository bundleRepository;

    public DataInitializer(ProductRepository productRepository, BundleRepository bundleRepository) {
        this.productRepository = productRepository;
        this.bundleRepository = bundleRepository;
    }

    private Product createProd(String sku, String name, String cost, String sell, int stock) {
        Product p = new Product();
        p.setSku(sku);
        p.setName(name);
        p.setUnitOfMeasure(UnitOfMeasure.PIECE);
        p.setCostPrice(new BigDecimal(cost));
        p.setSellingPrice(new BigDecimal(sell));
        p.setCurrentStock(stock);
        return p;
    }

    private BundleItem bItem(Product p, int qty) {
        BundleItem item = new BundleItem();
        item.setProduct(p);
        item.setQuantityRequired(qty);
        return item;
    }

    @Override
    public void run(String... args) throws Exception {
        boolean hasMassData = productRepository.findAll().stream().anyMatch(p -> "CAM-1080".equals(p.getSku()));
        
        if (!hasMassData) {
            Product p1 = createProd("KBD-001", "Mechanical Keyboard RGB", "45.00", "89.99", 150);
            Product p2 = createProd("MSE-002", "Wireless Gaming Mouse", "25.00", "59.99", 200);
            Product p3 = createProd("MON-003", "27-inch 4K Monitor", "180.00", "299.99", 45);
            Product p4 = createProd("CBL-USB", "Braided USB-C Cable", "3.00", "9.99", 500);
            Product p5 = createProd("CBL-HDM", "High-Speed HDMI Cable", "5.00", "14.99", 350);
            Product p6 = createProd("PWR-750", "750W Gold Power Supply", "65.00", "110.00", 60);
            Product p7 = createProd("AUD-001", "7.1 Gaming Headset", "35.00", "79.99", 120);
            Product p8 = createProd("PAD-XL", "Extended Desk Mousepad", "8.00", "24.99", 300);
            Product p9 = createProd("CAM-1080", "1080p Web Camera", "22.00", "49.99", 85);
            Product p10 = createProd("LMP-LED", "LED Ring Desk Lamp", "15.00", "34.99", 110);
            Product p11 = createProd("GPU-4070", "RTX 4070 Graphic Card", "450.00", "599.99", 20);
            Product p12 = createProd("CPU-7800", "Ryzen 7 7800X3D CPU", "300.00", "399.99", 30);
            Product p13 = createProd("RAM-16G", "16GB DDR5 RAM Kit", "45.00", "85.00", 250);
            Product p14 = createProd("SSD-1TB", "1TB NVMe M.2 SSD", "40.00", "75.00", 180);
            Product p15 = createProd("CAS-MID", "Mid-Tower ATX PC Case", "50.00", "89.99", 40);

            productRepository.saveAll(List.of(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15));

            Bundle b1 = new Bundle();
            b1.setBundleSku("BNDL-GAMER-PRO");
            b1.setName("Ultimate Pro Gamer Kit");
            b1.setBundlePrice(new BigDecimal("189.99"));
            List<BundleItem> i1 = List.of(bItem(p1, 1), bItem(p2, 1), bItem(p7, 1), bItem(p8, 1));
            i1.forEach(i -> i.setBundle(b1));
            b1.setItems(i1);

            Bundle b2 = new Bundle();
            b2.setBundleSku("BNDL-STREAM");
            b2.setName("Twitch Streamer Setup");
            b2.setBundlePrice(new BigDecimal("369.99"));
            List<BundleItem> i2 = List.of(bItem(p9, 1), bItem(p3, 1), bItem(p10, 1), bItem(p5, 1));
            i2.forEach(i -> i.setBundle(b2));
            b2.setItems(i2);

            Bundle b3 = new Bundle();
            b3.setBundleSku("BNDL-PCBUILD");
            b3.setName("Enthusiast Custom PC Build");
            b3.setBundlePrice(new BigDecimal("1299.99"));
            List<BundleItem> i3 = List.of(bItem(p12, 1), bItem(p11, 1), bItem(p13, 2), bItem(p14, 1), bItem(p15, 1), bItem(p6, 1));
            i3.forEach(i -> i.setBundle(b3));
            b3.setItems(i3);

            Bundle b4 = new Bundle();
            b4.setBundleSku("BNDL-DUAL-MON");
            b4.setName("Dual Monitor Productivity");
            b4.setBundlePrice(new BigDecimal("599.99"));
            List<BundleItem> i4 = List.of(bItem(p3, 2), bItem(p5, 2), bItem(p10, 1));
            i4.forEach(i -> i.setBundle(b4));
            b4.setItems(i4);

            Bundle b5 = new Bundle();
            b5.setBundleSku("BNDL-REFRESH");
            b5.setName("Peripheral Desk Refresh");
            b5.setBundlePrice(new BigDecimal("139.99"));
            List<BundleItem> i5 = List.of(bItem(p1, 1), bItem(p2, 1), bItem(p4, 1));
            i5.forEach(i -> i.setBundle(b5));
            b5.setItems(i5);

            bundleRepository.saveAll(List.of(b1, b2, b3, b4, b5));
        }
    }
}
