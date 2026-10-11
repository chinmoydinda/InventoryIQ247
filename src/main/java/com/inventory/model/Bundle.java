package com.inventory.model;
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
    @Transient
    private Integer computedAvailability;

    @OneToMany(mappedBy = "bundle", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<BundleItem> items = new ArrayList<>();
}