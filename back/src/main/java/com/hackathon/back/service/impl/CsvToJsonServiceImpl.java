package com.hackathon.back.service.impl;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
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
    public List<LogMidFlowESBDto> convertCsvToJson(String csvFilePath, String delimiter) throws IOException {
        try(FileInputStream file = new FileInputStream(csvFilePath);){
            if (file.available() == 0) {
                throw new IllegalArgumentException("El archivo CSV está vacío.");
            }
            try (Reader reader = new InputStreamReader(file)) {
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


    @Override
    public List<LogMidFlowESBDto> convertLogToJson(String path) throws IOException {
        List<LogMidFlowESBDto> dtos = new ArrayList<>();

        Pattern pattern = Pattern.compile(
                "^(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}) .*? \\[(\\w+)] (\\w+)@(\\d+\\.\\d+\\.\\d+\\.\\d+) .*?transaction: (txn-\\d+), tipo: (\\w+), cuenta: (\\w+), estado: (\\w+), valor: ([\\d.]+)"
        );

        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            String line;
            while ((line = reader.readLine()) != null) {
                Matcher matcher = pattern.matcher(line);
                if (matcher.find()) {
                    LogMidFlowESBDto dto = new LogMidFlowESBDto();
                    DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss");
                    dto.setTimestamp(LocalDateTime.parse(matcher.group(1), formatter));
                    dto.setCanal(matcher.group(2));
                    dto.setUsuario(matcher.group(3));
                    dto.setIp(matcher.group(4));
                    dto.setTransaccionId(matcher.group(5));
                    dto.setTipoTransaccion(matcher.group(6));
                    dto.setCuenta(matcher.group(7));
                    dto.setEstado(matcher.group(8));
                    dto.setValor(Double.parseDouble(matcher.group(9)));

                    dtos.add(dto);
                }
            }
        }

        return dtos;
    }
}
