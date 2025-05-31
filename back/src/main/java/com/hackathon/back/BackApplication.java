package com.hackathon.back;


import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.time.LocalDate;
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
        try (InputStream stream = BackApplication.class.getClassLoader().getResourceAsStream("logs_MidFlow_ESB.csv")) {
            List<LogMidFlowESBDto> csvDtos = service.convertCsvToJson(stream, delimiter);
            System.out.println("CSV convertido a JSON exitosamente.");
            midFlowLogJpaRepository.saveAll(csvDtos.stream().map(midFlowMapper::dtoToEntity).toList());
        } catch (Exception e) {
            System.err.println("Error al convertir CSV: " + e.getMessage());
        }

        // Procesar archivo LOG
        try(InputStream stream = BackApplication.class.getClassLoader().getResourceAsStream("logs_CoreBank.log")) {

            List<LogCoreBankDto> logDtos = toJson.convertLogsToJson(stream);
            System.out.println("LOG convertido a JSON exitosamente.");
            repositoryCoreBank.saveAll(logDtos.stream().map(coreBankLogMapper::dtoToEntity).toList());
        } catch (Exception e) {
            System.err.println("Error al convertir LOG: " + e.getMessage());
        }

        try (InputStream stream = BackApplication.class.getClassLoader().getResourceAsStream("logs_SecuCheck.json")) {
            List<LogSecureCheckDto> dtos = logSecureService.findAllByFile(stream);
            secureCheckLogJpaRepository.saveAll(dtos.stream().map(secureLogCheckMapper::toEntity).toList());
        }

    };
}
}

