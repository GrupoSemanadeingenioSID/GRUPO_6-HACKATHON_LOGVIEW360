package com.hackathon.back.service.impl;

import com.hackathon.back.dto.LogCoreBankDto;
import com.hackathon.back.service.LogCoreBankLogToJson;
import org.apache.tomcat.jni.FileInfo;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class LogCoreBankLogToJsonImpl implements LogCoreBankLogToJson {


    private static final String LOG_ENTRY_PATTERN =
            "^(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2})\\s+" + // 1: Timestamp
                    "(\\w+)\\s+" +                                     // 2: NivelLog (INFO, ERROR, etc.)
                    "\\[(\\w+)\\]\\s+" +                               // 3: Modulo (mobile, api)
                    "(\\w+)@([\\d\\.]+)\\s+" +                         // 4: UserID, 5: IPAddress
                    "Transacción ejecutada\\s*\\(" +
                    "transaction:\\s*([^,]+),\\s*" +                   // 6: TransactionId
                    "tipo:\\s*([^,]+),\\s*" +                          // 7: TipoTransaccion
                    "cuenta:\\s*([^,]+),\\s*" +                        // 8: TipoCuenta
                    "estado:\\s*([^,]+),\\s*" +                        // 9: Estado
                    "valor:\\s*([\\d\\.]+)\\)$";                       // 10: Valor
    private static final Pattern PATTERN = Pattern.compile(LOG_ENTRY_PATTERN);
    private static final DateTimeFormatter TIMESTAMP_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public LogCoreBankDto parseLine(String logLine) {
        Matcher matcher = PATTERN.matcher(logLine);

        if (matcher.find()) {
            try {
                LocalDateTime timestamp = LocalDateTime.parse(matcher.group(1), TIMESTAMP_FORMATTER);
                String nivelLog = matcher.group(2);
                String modulo = matcher.group(3);
                String userId = matcher.group(4);
                String ipAddress = matcher.group(5);
                String transactionId = matcher.group(6).trim();
                String tipoTransaccion = matcher.group(7).trim();
                String tipoCuenta = matcher.group(8).trim();
                String estado = matcher.group(9).trim();
                Double valor = Double.parseDouble(matcher.group(10));

                return LogCoreBankDto.builder()
                        .timestamp(timestamp)
                        .nivelLog(nivelLog)
                        .modulo(modulo)
                        .userId(userId)
                        .ipAddress(ipAddress)
                        .transactionId(transactionId)
                        .tipoTransaccion(tipoTransaccion)
                        .tipoCuenta(tipoCuenta)
                        .estado(estado)
                        .valor(valor)
                        .build();

            } catch (Exception e) {
                System.err.println("Error al parsear la línea: " + logLine + " - " + e.getMessage());
                return null; // O manejar el error de otra forma
            }
        }
        System.err.println("La línea no coincide con el patrón: " + logLine);
        return null;
    }

    @Override
    public List<LogCoreBankDto> convertLogsToJson(InputStream filePatH) {
        try{
            if (filePatH.available() == 0) {
                throw new IllegalArgumentException("El archivo de logs está vacío.");
            }
            List<String> logLines = new ArrayList<>();
            try (BufferedReader reader = new java.io.BufferedReader(new java.io.InputStreamReader(filePatH))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    logLines.add(line);
                }
                List<LogCoreBankDto> dtoList = new ArrayList<>();
                for (String linea : logLines) {
                    LogCoreBankDto dto = parseLine(linea);
                    if (dto != null) {
                        dtoList.add(dto);
                    }
                }
                return dtoList;
            } catch (IOException e) {
                throw new IOException("Error al leer el archivo de logs: " + e.getMessage(), e);
            }
        }catch (IOException e){
            return Collections.emptyList();
        }
    }
}
