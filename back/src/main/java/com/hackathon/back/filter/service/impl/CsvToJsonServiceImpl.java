<<<<<<< Updated upstream:back/src/main/java/com/hackathon/back/filter/service/impl/CsvToJsonServiceImpl.java
package com.hackathon.back.filter.service.impl;
=======
package com.hackathon.back.service.impl;

import com.hackathon.back.dto.LogMidFlowESB;
import com.hackathon.back.service.ICsvToJsonService;
import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
>>>>>>> Stashed changes:back/src/main/java/com/hackathon/back/service/impl/CsvToJsonServiceImpl.java

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.List;

import org.springframework.stereotype.Service;

import com.hackathon.back.dto.LogMidFlowESB;
import com.hackathon.back.filter.service.ICsvToJsonService;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class CsvToJsonServiceImpl implements ICsvToJsonService {


    @Override
    public List<LogMidFlowESB> convertCsvToJson(String csvFilePath, String delimiter) throws IOException {
        try(FileInputStream file = new FileInputStream(csvFilePath);){
            if (file.available() == 0) {
                throw new IllegalArgumentException("El archivo CSV está vacío.");
            }
            try (Reader reader = new InputStreamReader(file)) {
                CsvToBean<LogMidFlowESB> csvToBean = new CsvToBeanBuilder<LogMidFlowESB>(reader)
                        .withType(LogMidFlowESB.class)
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
