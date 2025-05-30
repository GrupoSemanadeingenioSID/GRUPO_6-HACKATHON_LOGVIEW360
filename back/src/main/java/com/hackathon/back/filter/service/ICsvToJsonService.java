package com.hackathon.back.filter.service;

import java.util.List;

import com.hackathon.back.dto.LogMidFlowESB;

public interface ICsvToJsonService {
    List<LogMidFlowESB> convertCsvToJson(String csvFilePath, String delimiter) throws Exception;

}
