package com.hackathon.back.entitys;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

public enum VerificacionesRealizadasEnum {
    FRECUENCIA("frecuencia"),
    TOKEN("token"),
    GEOLOCALIZACION("geolocalización"),
    BLACKLIST("blacklist"),

    OTRO_TIPO("otro_tipo");

    private final String value;

    VerificacionesRealizadasEnum(String value) {
        this.value = value;
    }

    @JsonValue
    public String getValue() {
        return value;
    }

    @JsonCreator
    public static VerificacionesRealizadasEnum fromValue(String value) {
        if (value == null) {
            return null;
        }
        for (VerificacionesRealizadasEnum enumValue : VerificacionesRealizadasEnum.values()) {
            if (enumValue.value.equalsIgnoreCase(value)) {
                return enumValue;
            }
        }
        // Este es el mensaje que estás viendo:
        System.err.println("Valor desconocido para VerificacionesRealizadasEnum: " + value + ". Se usará null.");
        return null;
    }
}
