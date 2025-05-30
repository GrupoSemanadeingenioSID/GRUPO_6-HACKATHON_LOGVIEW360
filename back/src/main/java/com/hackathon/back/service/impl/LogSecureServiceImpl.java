package com.hackathon.back.service.impl;

import com.hackathon.back.dto.LogSecureCheckDto;
import com.hackathon.back.entitys.SecureCheckLogEntity;
import com.hackathon.back.mapper.SecureLogCheckMapper;
import com.hackathon.back.repository.SecureCheckLogJpaRepository;
import com.hackathon.back.service.ILogSecureService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class LogSecureServiceImpl implements ILogSecureService {

    private final SecureCheckLogJpaRepository jpaRepository;
    private final SecureLogCheckMapper mapper;
    @Override
    public LogSecureCheckDto save(LogSecureCheckDto dto) {
        SecureCheckLogEntity entity = mapper.toEntity(dto);
        SecureCheckLogEntity savedEntity = jpaRepository.save(entity);
        return mapper.toDto(savedEntity);
    }

    @Override
    public LogSecureCheckDto findById(String id) {
        return mapper.toDto(jpaRepository.findById(id).orElse(null));
    }

    @Override
    public void deleteById(String id) {
        jpaRepository.deleteById(id);
    }

    @Override
    public void update(LogSecureCheckDto dto) {
        if (jpaRepository.existsById(dto.getTransactionId())){
            SecureCheckLogEntity entity = mapper.toEntity(dto);
            jpaRepository.save(entity);
        } else {
            throw new IllegalArgumentException("Entity with id " + dto.getTransactionId() + " does not exist.");
        }
    }
}
