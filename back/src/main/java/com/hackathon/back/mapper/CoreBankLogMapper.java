package com.hackathon.back.mapper;

import com.hackathon.back.dto.LogCoreBankDto;
import com.hackathon.back.entitys.CoreBankLogEntity;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface CoreBankLogMapper {

    LogCoreBankDto entityToDto(CoreBankLogEntity coreBankLogEntity);
    CoreBankLogEntity dtoToEntity(LogCoreBankDto logCoreBankDto);
}
