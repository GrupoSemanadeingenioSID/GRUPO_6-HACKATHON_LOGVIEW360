package com.hackathon.back.service.impl;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.hackathon.back.dto.LogSecureCheckDto;
import com.hackathon.back.entitys.SecureCheckLogEntity;
import com.hackathon.back.mapper.SecureLogCheckMapper;
import com.hackathon.back.repository.SecureCheckLogJpaRepository;
import com.hackathon.back.service.ILogSecureService;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.ClassPathResource;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class LogSecureServiceImpl implements ILogSecureService {

    private final ObjectMapper jsonMapper;
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

    @Override
    public List<LogSecureCheckDto> findAll(Pageable pageable) {
        return jpaRepository.findAll(pageable).stream().map(mapper::toDto).collect(Collectors.toList());
    }

    @Override
    public List<LogSecureCheckDto> findAllByFile(InputStream filePath) {
        try {
            if (filePath.available() == 0) {
                throw new IllegalArgumentException("El archivo de logs está vacío.");
            }
            List<LogSecureCheckDto> dtos = jsonMapper.readValue(filePath, new TypeReference<List<LogSecureCheckDto>>() {});
            return dtos;
        } catch (Exception e) {
            throw new RuntimeException("Error reading file: " + filePath, e);
        }
    }
}
