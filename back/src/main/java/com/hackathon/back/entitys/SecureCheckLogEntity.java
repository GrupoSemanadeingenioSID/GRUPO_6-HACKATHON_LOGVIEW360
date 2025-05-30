package com.hackathon.back.entitys;

import java.time.LocalDateTime;

import jakarta.persistence.*;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
@Table(name = "secure_check_log")
public class SecureCheckLogEntity {
    private LocalDateTime timestamp;
    @Id
    private String transactionId;
    private String userId;
    private String ipAddress;
    private String resultadoValidacion;
    private String motivoFallo;
    private String modulo;
    @Enumerated(EnumType.STRING)
    private VerificacionesRealizadasEnum verificacionesRealizadas;
}

