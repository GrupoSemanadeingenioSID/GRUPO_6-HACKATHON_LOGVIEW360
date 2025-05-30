package com.hackathon.back.repository;

import com.hackathon.back.entitys.MidFlowLogEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MidFlowLogJpaRepository extends JpaRepository<MidFlowLogEntity,String> {
}
