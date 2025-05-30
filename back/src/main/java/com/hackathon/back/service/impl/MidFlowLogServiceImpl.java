package com.hackathon.back.service.impl;

import com.hackathon.back.dto.LogMidFlowESBDto;
import com.hackathon.back.entitys.MidFlowLogEntity;
import com.hackathon.back.mapper.MidFlowLogMapper;
import com.hackathon.back.repository.MidFlowLogJpaRepository;
import com.hackathon.back.service.IMidFlowLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class MidFlowLogServiceImpl implements IMidFlowLogService {
    private final MidFlowLogJpaRepository jpaRepository;
    private final MidFlowLogMapper mapper;
    @Override
    public LogMidFlowESBDto save(LogMidFlowESBDto dto) {
        MidFlowLogEntity entity = mapper.dtoToEntity(dto);
        MidFlowLogEntity savedEntity = jpaRepository.save(entity);
        return mapper.entityToDto(savedEntity);
    }

    @Override
    public LogMidFlowESBDto findById(String id) {
        return mapper.entityToDto(jpaRepository.findById(id).orElse(null));
    }

    @Override
    public void deleteById(String id) {
        jpaRepository.deleteById(id);
    }

    @Override
    public void update(LogMidFlowESBDto dto) {
        MidFlowLogEntity entity = mapper.dtoToEntity(dto);
        if (jpaRepository.existsById(entity.getTransactionId())) {
            jpaRepository.save(entity);
        } else {
            throw new IllegalArgumentException("El registro con ID " + entity.getTransactionId() + " no existe.");
        }
    }
}
