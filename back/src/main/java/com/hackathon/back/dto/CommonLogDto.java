package com.hackathon.back.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.opencsv.bean.CsvBindByName;
import com.opencsv.bean.CsvDate;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.time.LocalDateTime;


@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SuperBuilder
@ToString
public abstract class CommonLogDto {
    @CsvBindByName(column = "timestamp", required = true)
    @CsvDate("yyyy-MM-dd HH:mm:ss")
    @JsonProperty("timestamp")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime timestamp;
    @CsvBindByName(column = "transaction_id", required = true)
    @JsonProperty("transaction_id")
    private String transactionId;
    @CsvBindByName(column = "user_id")
    @JsonProperty("user_id")
    private String userId;
    @CsvBindByName(column = "ip_address")
    @JsonProperty("ip_address")
    private String ipAddress;
    @CsvBindByName(column = "modulo")
    @JsonProperty("modulo")
    private String modulo;
}