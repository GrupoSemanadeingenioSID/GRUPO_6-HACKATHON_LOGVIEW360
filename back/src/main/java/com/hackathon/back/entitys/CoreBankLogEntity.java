package com.hackathon.back.entitys;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.*;

@Getter
@Setter
@Entity
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "core_bank_log")
public class CoreBankLogEntity {
    @Id
    private String transactionId;
    private LocalDateTime timestamp;
    private String nivelLog;
    private String modulo;
    private String userId;
    private String ipAddress;
    private String tipoTransaccion;
    private String tipoCuenta;
    private String estado;
    private Double valor;
}
