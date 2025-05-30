package com.hackathon.back;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.io.ClassPathResource;

import com.hackathon.back.dto.LogCoreBankDto;
import com.hackathon.back.dto.LogMidFlowESBDto;
import com.hackathon.back.dto.LogSecureCheckDto;
import com.hackathon.back.mapper.CoreBankLogMapper;
import com.hackathon.back.mapper.MidFlowLogMapper;
import com.hackathon.back.mapper.SecureLogCheckMapper;
import com.hackathon.back.repository.CoreBankLogJpaRepository;
import com.hackathon.back.repository.MidFlowLogJpaRepository;
import com.hackathon.back.repository.SecureCheckLogJpaRepository;
import com.hackathon.back.service.ICsvToJsonService;
import com.hackathon.back.service.ILogSecureService;
import com.hackathon.back.service.LogCoreBankLogToJson;

@SpringBootApplication
public class BackApplication {

    public static void main(String[] args) {
        SpringApplication.run(BackApplication.class, args);
    }

@Bean
CommandLineRunner runner(LogCoreBankLogToJson toJson,
                         ICsvToJsonService service,
                         CoreBankLogJpaRepository repositoryCoreBank,
                         MidFlowLogJpaRepository midFlowLogJpaRepository,
                         MidFlowLogMapper midFlowMapper,
                         CoreBankLogMapper coreBankLogMapper,
                         ILogSecureService logSecureService,
                         SecureCheckLogJpaRepository secureCheckLogJpaRepository,
                         SecureLogCheckMapper secureLogCheckMapper) {
    return args -> {
        String delimiter = ",";

        // Procesar archivo CSV
        try {
            ClassPathResource csvResource = new ClassPathResource("logs_MidFlow_ESB.csv");
            String csvFilePath = csvResource.getFile().getAbsolutePath();
            List<LogMidFlowESBDto> csvDtos = service.convertCsvToJson(csvFilePath, delimiter);
            System.out.println("CSV convertido a JSON exitosamente.");
            midFlowLogJpaRepository.saveAll(csvDtos.stream().map(midFlowMapper::dtoToEntity).toList());
        } catch (Exception e) {
            System.err.println("Error al convertir CSV: " + e.getMessage());
        }

        // Procesar archivo LOG
        try {
            ClassPathResource logResource = new ClassPathResource("logs_CoreBank.log");
            String logFilePath = logResource.getFile().getAbsolutePath();
            List<LogCoreBankDto> logDtos = toJson.convertLogsToJson(logFilePath); // Este método debes implementarlo
            System.out.println("LOG convertido a JSON exitosamente.");
            repositoryCoreBank.saveAll(logDtos.stream().map(coreBankLogMapper::dtoToEntity).toList());
        } catch (Exception e) {
            System.err.println("Error al convertir LOG: " + e.getMessage());
        }
        System.out.println(LocalDateTime.now());
        List<LogSecureCheckDto> dtos = logSecureService.findAllByFile("logs_SecuCheck.json");
        secureCheckLogJpaRepository.saveAll(dtos.stream().map(secureLogCheckMapper::toEntity).toList());

    };
}
}

