package com.hackathon.back.entitys;

import java.time.LocalDateTime;
import java.util.List;

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
    @ElementCollection
    @CollectionTable(name = "secure_check_log_verificaciones", joinColumns = @JoinColumn(name = "transaction_id"))
    @Column(name = "verificacion_realizada")
    private List<VerificacionesRealizadasEnum> verificacionesRealizadas;
}

