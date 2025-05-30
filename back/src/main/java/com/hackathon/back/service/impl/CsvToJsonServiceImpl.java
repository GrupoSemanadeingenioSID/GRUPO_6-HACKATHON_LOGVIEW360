package com.hackathon.back.service.impl;

import com.hackathon.back.dto.LogMidFlowESB;
import com.hackathon.back.service.ICsvToJsonService;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;

@Service
@RequiredArgsConstructor
public class CsvToJsonServiceImpl implements ICsvToJsonService {




    @Override
    public List<LogMidFlowESB> convertCsvToJson(String csvFilePath, String delimiter) throws Exception {
        List<LogMidFlowESB> logMidFlowESBS = new ArrayList<>();
        try(Reader reader = new InputStreamReader(new FileInputStream(csvFilePath), Charset.defaultCharset());
            CSVReader csvReader = new CSVReaderBuilder(reader).withSkipLines(1).build();){
            return List.of();
        }
    }
}
