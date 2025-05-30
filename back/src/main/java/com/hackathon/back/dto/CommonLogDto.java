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
public abstract class CommonLogDto {
    @CsvBindByName(column = "timestamp", required = true)
    @CsvDate("yyyy-MM-dd HH:mm:ss")
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