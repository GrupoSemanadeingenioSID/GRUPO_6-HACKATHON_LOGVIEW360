package com.hackathon.back.repository;

import com.hackathon.back.entitys.SecureCheckLogEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface SecureCheckLogJpaRepository extends JpaRepository<SecureCheckLogEntity,String> {
}
