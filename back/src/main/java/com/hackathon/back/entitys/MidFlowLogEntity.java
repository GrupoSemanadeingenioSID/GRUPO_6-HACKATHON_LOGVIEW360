package com.hackathon.back.entitys;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.*;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity
@Table(name = "mid_flow_log")
public class MidFlowLogEntity {
    private LocalDateTime timestamp;
    private String nivelLog;
    @Id
    private String transactionId;
    private String direction;
    private String operation;
    private Long statusCode;
    private Long latencyMs; // Nullable para request
    private String userId;
    private String ipAddress;
    private String modulo;
}
