package com.hackathon.back.dto;

import lombok.*;
import lombok.experimental.SuperBuilder;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SuperBuilder
public class LogCoreBankDto extends CommonLogDto {
    private String nivelLog;
    private String tipoTransaccion;
    private String tipoCuenta;
    private String estado;
    private Double valor;
}
