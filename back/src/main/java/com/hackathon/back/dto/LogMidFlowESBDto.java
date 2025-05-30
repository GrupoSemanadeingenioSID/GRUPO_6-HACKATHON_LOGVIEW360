package com.hackathon.back.dto;

import com.opencsv.bean.CsvBindByName;
import lombok.*;
import lombok.experimental.SuperBuilder;

@NoArgsConstructor
@Getter
@Setter
@AllArgsConstructor
@SuperBuilder
public class LogMidFlowESBDto extends CommonLogDto {

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
}
