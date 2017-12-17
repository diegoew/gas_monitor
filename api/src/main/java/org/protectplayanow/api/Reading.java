package org.protectplayanow.api;

import lombok.Builder;
import lombok.Data;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by vladpopescu on 12/12/17.instant, deviceId, gasName, reading, unitOfReading, latitude, longitude
 */
@Data
@Builder
public class Reading {

    private Date instant;

    private String deviceId, gasName, unitOfReading;

    private double latitude, longitude, reading;

    private Map<String, Double> gasNameAndReading = new HashMap<>();

}
