package com.hackathon.back.dto;

import lombok.*;
import lombok.experimental.SuperBuilder;

import java.time.LocalDateTime;


@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SuperBuilder
public abstract class CommonLog {
    private LocalDateTime timestamp;
    private String transactionId;
    private String userId;
    private String ipAddress;
    private String modulo;
}