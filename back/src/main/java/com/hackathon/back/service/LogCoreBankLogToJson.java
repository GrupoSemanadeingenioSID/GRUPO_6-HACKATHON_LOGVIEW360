package com.hackathon.back.service;

import com.hackathon.back.dto.LogCoreBankDto;

import java.util.List;

public interface LogCoreBankLogToJson {
    List<LogCoreBankDto> convertLogsToJson(String filePatH);
}
