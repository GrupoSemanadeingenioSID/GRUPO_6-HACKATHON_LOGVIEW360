package com.hackathon.back.mapper;

import com.hackathon.back.dto.LogMidFlowESBDto;
import com.hackathon.back.entitys.MidFlowLogEntity;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface MidFlowLogMapper {

    // DTO -> Entity
    LogMidFlowESBDto entityToDto(MidFlowLogEntity midFlowLogEntity);
    // Entity -> DTO
    MidFlowLogEntity dtoToEntity(LogMidFlowESBDto logMidFlowESBDto);
}
