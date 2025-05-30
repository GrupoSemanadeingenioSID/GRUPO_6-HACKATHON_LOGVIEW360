package com.hackathon.back.entitys;

import java.time.LocalDateTime;
import java.util.List;

import lombok.Data;

@Data
public class SecuCheckLog {
    private LocalDateTime timestamp;
    private String transactionId;
    private String userId;
    private String ipAddress;
    private String resultadoValidacion;
    private String motivoFallo;
    private String modulo;
    private List<String> verificacionesRealizadas;
}
