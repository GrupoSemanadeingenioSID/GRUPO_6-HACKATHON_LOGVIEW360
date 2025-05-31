package com.hackathon.back.service;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

import com.hackathon.back.dto.LogMidFlowESBDto;

public interface ICsvToJsonService {
    List<LogMidFlowESBDto> convertCsvToJson(InputStream csvFilePath, String delimiter) throws IOException;


}
