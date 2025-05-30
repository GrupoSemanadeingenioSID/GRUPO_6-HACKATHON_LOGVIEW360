package com.hackathon.back.filter.service;

import java.io.IOException;
import java.util.List;

import com.hackathon.back.dto.LogMidFlowESB;

<<<<<<< Updated upstream:back/src/main/java/com/hackathon/back/filter/service/ICsvToJsonService.java
=======
import java.io.IOException;
import java.util.List;

>>>>>>> Stashed changes:back/src/main/java/com/hackathon/back/service/ICsvToJsonService.java
public interface ICsvToJsonService {
    List<LogMidFlowESB> convertCsvToJson(String csvFilePath, String delimiter) throws IOException;
}
