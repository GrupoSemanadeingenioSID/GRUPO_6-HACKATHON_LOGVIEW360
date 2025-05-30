package com.hackathon.back.dto;

import lombok.*;
import lombok.experimental.SuperBuilder;

@NoArgsConstructor
@Getter
@Setter
@AllArgsConstructor
@SuperBuilder
public class LogMidFlowESB extends CommonLog{
    private String nivelLog;
    private String direction;
    private String operation;
    private Long statusCode;
    private Long latencyMs;
}
