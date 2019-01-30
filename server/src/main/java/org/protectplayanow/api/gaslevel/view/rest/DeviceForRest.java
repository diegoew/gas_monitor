package org.protectplayanow.api.gaslevel.view.rest;

import lombok.Builder;
import lombok.Data;
import lombok.extern.log4j.Log4j;
import lombok.extern.slf4j.Slf4j;
import org.protectplayanow.api.gaslevel.repository.Device;

import java.util.List;
import java.util.stream.Collectors;

@Data
@Builder
@Slf4j
public class DeviceForRest {

    private String deviceId, sensorType;
    private double latitude, longitude;

    public static DeviceForRest make(Device device){
        if(device == null){
            return DeviceForRest.builder().build();
        }

        return DeviceForRest.builder()
                .deviceId(device.getDeviceId())
                .sensorType(device.getSensorType())
                .latitude(device.getLatitude())
                .longitude(device.getLongitude())
                .build();
    }


    public static List<DeviceForRest> make(List<Device> devices){
        log.trace("Devices={}", devices);
        return devices.stream().map(DeviceForRest::make).collect(Collectors.toList());
    }
}
