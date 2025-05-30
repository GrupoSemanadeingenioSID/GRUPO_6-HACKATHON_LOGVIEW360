package com.hackathon.back;

import com.hackathon.back.service.ICsvToJsonService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class BackApplication {

    public static void main(String[] args) {
        SpringApplication.run(BackApplication.class, args);
    }


    @Bean
    CommandLineRunner runner(ICsvToJsonService service){
        return args -> {
            String csvFilePath = "/home/alejandro/Documentos/personal/.github/GRUPO_6-HACKATHON_LOGVIEW360/source/logs_MidFlow_ESB.csv"; // Ruta del archivo CSV
            String delimiter = ","; // Delimitador del CSV
            try {
                service.convertCsvToJson(csvFilePath, delimiter).forEach(System.out::println);
                System.out.println("CSV convertido a JSON exitosamente.");
            } catch (Exception e) {
                System.err.println("Error al convertir CSV a JSON: " + e.getMessage());
            }
        };
    }
}
