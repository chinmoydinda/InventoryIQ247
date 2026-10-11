package com.inventory.repository;
import com.inventory.model.Bundle;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import java.util.Optional;

public interface BundleRepository extends JpaRepository<Bundle, Long> {
    @Query("SELECT b FROM Bundle b LEFT JOIN FETCH b.items WHERE b.id = :id")
    Optional<Bundle> findByIdWithItems(@Param("id") Long id);
}