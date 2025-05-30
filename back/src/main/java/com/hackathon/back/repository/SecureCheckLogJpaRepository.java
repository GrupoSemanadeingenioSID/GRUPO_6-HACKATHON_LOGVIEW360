package com.hackathon.back.repository;

import com.hackathon.back.dto.LogSecureCheckDto;
import com.hackathon.back.entitys.SecureCheckLogEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface SecureCheckLogJpaRepository extends JpaRepository<SecureCheckLogEntity,String> {
}
