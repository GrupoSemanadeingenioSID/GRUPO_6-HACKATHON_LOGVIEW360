package com.hackathon.back.service.impl;

import com.hackathon.back.dto.LogCoreBankDto;
import com.hackathon.back.entitys.CoreBankLogEntity;
import com.hackathon.back.mapper.CoreBankLogMapper;
import com.hackathon.back.repository.CoreBankLogJpaRepository;
import com.hackathon.back.service.ICoreBankLogService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class CoreBankServiceImpl implements ICoreBankLogService {

    private final CoreBankLogJpaRepository jpaRepository;
    private final CoreBankLogMapper mapper;

    @Override
    public LogCoreBankDto save(LogCoreBankDto dto) {
        CoreBankLogEntity entity = mapper.dtoToEntity(dto);
        CoreBankLogEntity savedEntity = jpaRepository.save(entity);
        return mapper.entityToDto(savedEntity);
    }

    @Override
    public LogCoreBankDto findById(String id) {
        return mapper.entityToDto(jpaRepository.findById(id).orElse(null));
    }

    @Override
    public void deleteById(String id) {
        jpaRepository.deleteById(id);
    }

    @Override
    public void update(LogCoreBankDto dto) {
        CoreBankLogEntity entity = mapper.dtoToEntity(dto);
        if (jpaRepository.existsById(entity.getTransactionId())) {
            jpaRepository.save(entity);
        } else {
            throw new IllegalArgumentException("El registro con ID " + entity.getTransactionId() + " no existe.");
        }
    }
}
