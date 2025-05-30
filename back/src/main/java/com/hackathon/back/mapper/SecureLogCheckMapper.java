package com.hackathon.back.mapper;

import com.hackathon.back.dto.LogSecureCheckDto;
import com.hackathon.back.entitys.SecureCheckLogEntity;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface SecureLogCheckMapper {
    // DTO -> Entity
    LogSecureCheckDto toDto(SecureCheckLogEntity entity);
    // Entity -> DTO
    SecureCheckLogEntity toEntity(LogSecureCheckDto dto);
}
