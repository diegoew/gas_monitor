package org.protectplayanow.api.gaslevel.repository;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class Device {

    private String deviceId, sensorType;
    private double latitude, longitude;

}
