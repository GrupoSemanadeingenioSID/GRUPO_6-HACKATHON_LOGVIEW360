package com.hackathon.back.entitys;

import java.time.LocalDateTime;

import lombok.Data;

@Data
public class MidFlowLog {
    private LocalDateTime timestamp;
    private String nivelLog;
    private String transactionId;
    private String direction;
    private String operation;
    private int statusCode;
    private Long latencyMs; // Nullable para request
    private String userId;
    private String ipAddress;
    private String modulo;
}
