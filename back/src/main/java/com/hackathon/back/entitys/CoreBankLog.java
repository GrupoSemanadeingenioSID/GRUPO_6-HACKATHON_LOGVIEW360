package com.hackathon.back.entitys;

import java.time.LocalDateTime;

import lombok.Data;

@Data
public class CoreBankLog {
    private LocalDateTime timestamp;
    private String nivelLog; // Siempre "INFO"
    private String modulo;
    private String userId;
    private String ipAddress;

    // Detalles de la transacción
    private String transactionId;
    private String tipoTransaccion;
    private String tipoCuenta;
    private String estado;
    private Double valor;
}
