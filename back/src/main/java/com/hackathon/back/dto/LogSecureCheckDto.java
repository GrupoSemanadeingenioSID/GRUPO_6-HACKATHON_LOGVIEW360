package com.hackathon.back.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.hackathon.back.entitys.VerificacionesRealizadasEnum;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SuperBuilder
public class LogSecureCheckDto extends CommonLogDto {
    @JsonProperty("motivo_fallo")
    private String motivoFallo;
    @JsonProperty("verificaciones_realizadas")
    private List<VerificacionesRealizadasEnum> verificacionesRealizadas;
    @JsonProperty("resultado_validacion")
    private String resultadoValidacion;
}
