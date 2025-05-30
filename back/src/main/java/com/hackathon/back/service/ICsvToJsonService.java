package com.hackathon.back.service;

import com.hackathon.back.dto.LogMidFlowESBDto;

import java.io.IOException;
import java.util.List;

public interface ICsvToJsonService {
    List<LogMidFlowESBDto> convertCsvToJson(String csvFilePath, String delimiter) throws IOException;
}
