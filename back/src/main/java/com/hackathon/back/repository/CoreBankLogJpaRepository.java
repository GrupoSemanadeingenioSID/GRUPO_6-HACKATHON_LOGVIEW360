package com.hackathon.back.repository;

import com.hackathon.back.entitys.CoreBankLogEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CoreBankLogJpaRepository extends JpaRepository<CoreBankLogEntity,String> {
}
