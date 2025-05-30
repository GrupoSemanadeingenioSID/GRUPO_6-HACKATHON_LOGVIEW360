package com.hackathon.back.dto;

import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
@SuperBuilder
public class LogSecureCheckDto extends CommonLogDto {
    private String motivoFallo;
    private List<String> verificacionesRealizadas;
}
