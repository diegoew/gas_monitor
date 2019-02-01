package org.protectplayanow.api.gaslevel;

import lombok.Builder;
import lombok.ToString;

import java.util.Optional;

/**
 * Created by vladpopescu on 1/5/18.
 */
@Builder
@ToString
public class ReadingBySensorForRest {

    private String sensorType;

    private double reading;

    public String getSensorType() {
        return sensorType;
    }

    public void setSensorType(String sensorType) {
        this.sensorType = Optional.ofNullable(sensorType).orElse("").toUpperCase();
    }

    public double getReading() {
        return reading;
    }

    public void setReading(double reading) {
        this.reading = reading;
    }

}
