package org.protectplayanow.api.gaslevel;

import lombok.Builder;
import lombok.Data;
import lombok.ToString;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Created by vladpopescu on 12/12/17
 */
@Builder
@ToString
public class ReadingForRestPOST {

    private String gasName, unitOfReading;

    private double reading;

    public String getGasName() {
        return gasName;
    }

    public void setGasName(String gasName) {
        this.gasName = Optional.ofNullable(gasName).orElse("").toLowerCase();
    }

    public String getUnitOfReading() {
        return unitOfReading;
    }

    public void setUnitOfReading(String unitOfReading) {
        this.unitOfReading = unitOfReading;
    }

    public double getReading() {
        return reading;
    }

    public void setReading(double reading) {
        this.reading = reading;
    }
}
