package com.hackathon.back;

import java.util.List;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.io.ClassPathResource;

import com.hackathon.back.dto.LogMidFlowESBDto;
import com.hackathon.back.mapper.MidFlowLogMapper;
import com.hackathon.back.repository.MidFlowLogJpaRepository;
import com.hackathon.back.service.ICsvToJsonService;

@SpringBootApplication
public class BackApplication {

    public static void main(String[] args) {
        SpringApplication.run(BackApplication.class, args);
    }

@Bean
CommandLineRunner runner(ICsvToJsonService service,
                          MidFlowLogJpaRepository repository,
                          MidFlowLogMapper mapper) {
    return args -> {
        String delimiter = ",";

        // Procesar archivo CSV
        try {
            ClassPathResource csvResource = new ClassPathResource("logs_MidFlow_ESB.csv");
            String csvFilePath = csvResource.getFile().getAbsolutePath();
            List<LogMidFlowESBDto> csvDtos = service.convertCsvToJson(csvFilePath, delimiter);
            System.out.println("CSV convertido a JSON exitosamente.");
            repository.saveAll(csvDtos.stream().map(mapper::dtoToEntity).toList());
        } catch (Exception e) {
            System.err.println("Error al convertir CSV: " + e.getMessage());
        }

        // Procesar archivo LOG
        try {
            ClassPathResource logResource = new ClassPathResource("logs_CoreBank.log");
            String logFilePath = logResource.getFile().getAbsolutePath();
            List<LogMidFlowESBDto> logDtos = service.convertLogToJson(logFilePath); // Este método debes implementarlo
            System.out.println("LOG convertido a JSON exitosamente.");
            repository.saveAll(logDtos.stream().map(mapper::dtoToEntity).toList());
        } catch (Exception e) {
            System.err.println("Error al convertir LOG: " + e.getMessage());
        }
    };

//    @Bean
//    CommandLineRunner runner(ICsvToJsonService service, MidFlowLogJpaRepository repository, MidFlowLogMapper mapper){
//        return args -> {
//            String csvFilePath = "src/main/resources/logs_MidFlow_ESB.csv"; // Ruta del archivo CSV
//            String delimiter = ","; // Delimitador del CSV
//            try {
//                List<LogMidFlowESBDto> dtos = service.convertCsvToJson(csvFilePath, delimiter);
//                System.out.println("CSV convertido a JSON exitosamente.");
//                repository.saveAll(dtos.stream().map(mapper::dtoToEntity).toList());
//            } catch (Exception e) {
//                System.err.println("Error al convertir CSV a JSON: " + e.getMessage());
//            }
//        };
//    }
}
}

