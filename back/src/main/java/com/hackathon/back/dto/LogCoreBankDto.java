package com.hackathon.back.dto;

import lombok.*;
import lombok.experimental.SuperBuilder;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SuperBuilder
public class LogCoreBankDto extends CommonLogDto {
    private String info;
    private String status;

    private String transactTypeId;
    private String cuenta;
    private String estado;
    private Long valor;

}
