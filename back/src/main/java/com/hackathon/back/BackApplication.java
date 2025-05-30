package com.hackathon.back;

import com.hackathon.back.dto.LogMidFlowESBDto;
import com.hackathon.back.entitys.MidFlowLogEntity;
import com.hackathon.back.mapper.MidFlowLogMapper;
import com.hackathon.back.repository.MidFlowLogJpaRepository;
import com.hackathon.back.service.ICsvToJsonService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.List;

@SpringBootApplication
public class BackApplication {

    public static void main(String[] args) {
        SpringApplication.run(BackApplication.class, args);
    }


    @Bean
    CommandLineRunner runner(ICsvToJsonService service, MidFlowLogJpaRepository repository, MidFlowLogMapper mapper){
        return args -> {
            String csvFilePath = "/home/alejandro/Documentos/personal/.github/GRUPO_6-HACKATHON_LOGVIEW360/source/logs_MidFlow_ESB.csv"; // Ruta del archivo CSV
            String delimiter = ","; // Delimitador del CSV
            try {
                List<LogMidFlowESBDto> dtos = service.convertCsvToJson(csvFilePath, delimiter);
                System.out.println("CSV convertido a JSON exitosamente.");
                repository.saveAll(dtos.stream().map(mapper::dtoToEntity).toList());
            } catch (Exception e) {
                System.err.println("Error al convertir CSV a JSON: " + e.getMessage());
            }
        };
    }
}
