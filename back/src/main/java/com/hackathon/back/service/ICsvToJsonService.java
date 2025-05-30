package com.hackathon.back.service;

import com.hackathon.back.dto.LogMidFlowESB;

import java.util.List;

public interface ICsvToJsonService {
    List<LogMidFlowESB> convertCsvToJson(String csvFilePath, String delimiter) throws Exception;

}
