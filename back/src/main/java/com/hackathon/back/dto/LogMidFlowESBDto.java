package com.hackathon.back.dto;

import java.time.LocalDateTime;

import com.opencsv.bean.CsvBindByName;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.SuperBuilder;

@NoArgsConstructor
@Getter
@Setter
@AllArgsConstructor(access = AccessLevel.PROTECTED)
@SuperBuilder
@ToString(callSuper = true)
public class LogMidFlowESBDto extends CommonLogDto {

    // Campos para CSV
    @CsvBindByName(column = "nivel_log", required = true)
    private String nivelLog;

    @CsvBindByName(column = "direction", required = true)
    private String direction;

    @CsvBindByName(column = "operation", required = true)
    private String operation;

    @CsvBindByName(column = "status_code")
    private Long statusCode;

    @CsvBindByName(column = "latency_ms")
    private Long latencyMs;

    // Campos adicionales para LOG (no afectan el parseo del CSV)
    private LocalDateTime timestamp;
    private String canal;
    private String usuario;
    private String ip;
    private String transaccionId;
    private String tipoTransaccion;
    private String cuenta;
    private String estado;
    private Double valor;
}
