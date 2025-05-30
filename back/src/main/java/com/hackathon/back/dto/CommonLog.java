package com.hackathon.back.dto;

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
public abstract class CommonLog {
    @CsvBindByName(column = "timestamp", required = true)
    @CsvDate("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
    private LocalDateTime timestamp;
    @CsvBindByName(column = "transaction_id", required = true)
    private String transactionId;
    @CsvBindByName(column = "user_id")
    private String userId;
    @CsvBindByName(column = "ip_address")
    private String ipAddress;
    @CsvBindByName(column = "modulo")
    private String modulo;
}