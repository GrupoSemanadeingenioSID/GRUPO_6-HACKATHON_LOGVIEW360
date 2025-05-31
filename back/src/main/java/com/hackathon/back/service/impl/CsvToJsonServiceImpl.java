package com.hackathon.back.service.impl;

import java.io.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.springframework.stereotype.Service;

import com.hackathon.back.dto.LogMidFlowESBDto;
import com.hackathon.back.service.ICsvToJsonService;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class CsvToJsonServiceImpl implements ICsvToJsonService {


    @Override
    public List<LogMidFlowESBDto> convertCsvToJson(InputStream csvFilePath, String delimiter) throws IOException {
        try{
            if (csvFilePath.available() == 0) {
                throw new IllegalArgumentException("El archivo CSV está vacío.");
            }
            try (Reader reader = new InputStreamReader(csvFilePath)) {
                CsvToBean<LogMidFlowESBDto> csvToBean = new CsvToBeanBuilder<LogMidFlowESBDto>(reader)
                        .withType(LogMidFlowESBDto.class)
                        .withIgnoreLeadingWhiteSpace(true)
                        .withSeparator(delimiter.toCharArray()[0])
                        .build();

                return csvToBean.parse();
            } catch (IllegalStateException e) {
                throw new IOException("Error al parsear el archivo CSV: " + e.getMessage(), e);
            }
        }catch (Exception e){
        }
        return null;
    }

}
