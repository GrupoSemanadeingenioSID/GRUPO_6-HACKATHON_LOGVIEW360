package com.hackathon.back.service;

import java.io.IOException;
import java.util.List;

import com.hackathon.back.dto.LogMidFlowESBDto;

public interface ICsvToJsonService {
    List<LogMidFlowESBDto> convertCsvToJson(String csvFilePath, String delimiter) throws IOException;

    List<LogMidFlowESBDto> convertLogToJson(String logFilePath) throws IOException;

}
