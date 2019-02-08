package org.protectplayanow.api.unit;

import lombok.extern.slf4j.Slf4j;
import org.junit.Assert;
import org.junit.Test;
import org.protectplayanow.api.config.Constants;
import org.protectplayanow.api.gaslevel.Reading;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;

/**
 * Created by vladpopescu on 12/1/18.
 */
@Slf4j
public class UnitTest {
/*
         @ApiParam(value = Constants.deviceIdParam)
            @RequestParam(value = "deviceId", defaultValue = Constants.PleaseSendDeviceIdNextTime, required = false)
                    String deviceId,

            @ApiParam(value = Constants.apiInstantDateMessage)
            @RequestParam(value = "instant", defaultValue = Constants.now, required = false)
            @DateTimeFormat(pattern = Constants.dateTimePattern)
                    Date instant,

            @ApiParam(value = Constants.latitudePdr)
            @RequestParam(value = "latitude", defaultValue = Constants.latitudePdr, required = false)
                    double latitude,

            @ApiParam(value = Constants.longitudePdr)
            @RequestParam(value = "longitude", defaultValue = Constants.longitudePdr, required = false)
                    double longitude,

            @ApiParam(value = Constants.sensorTypeMsg)
            @RequestParam(value = "sensorType", defaultValue = Constants.mq2, required = false)
                    String sensorType,

            @ApiParam(value = "this is the voltage reading that we will calculate")
            @RequestParam(value = "reading", required = true)
                    double reading,

            @ApiParam(value = "this value is determined by calibrating the sensor, if you don't know it we'll use defaults")
            @RequestParam(value = "ro", defaultValue = "0", required = false)
                    double ro,

            @ApiParam(value = "this value needs to be sent by the pi, if you don't know it we'll use defaults")
            @RequestParam(value = "tempInCelsius", defaultValue = "20", required = false)
                    double tempInCelsius,

            @ApiParam(value = "this value needs to be sent by the pi, if you don't know it we'll use defaults")
            @RequestParam(value = "relativeHumidity", defaultValue = ".10", required = false)
                    double relativeHumidity,

            @ApiParam(value = "this value needs to be sent by the pi, if you don't " +
                    "know it we'll use the default value 32767")
            @RequestParam(value = "resolution", defaultValue = "32767", required = false)
                    double resolution
    ) {

        log.info("diegosDeviceId={}, instant={}, latitude={}, longitude={}, sensorTypeMsg={}", deviceId, instant, latitude, longitude, sensorType);

        Reading r = Reading.builder()
                .deviceId(deviceId)
                .resolution(resolution)
                .instant(instant)
                .latitude(latitude)
                .longitude(longitude)
                .reading(reading)
                .input(reading)
                .sensorType(sensorType)
                .ro(ro)
                .tempInCelsius(tempInCelsius)
                .relativeHumidity(relativeHumidity)
                .build();
 */

    @Test
    public void testCalculation(){

        //GIVEN a reading ...
        List<Reading> readings = Reading.builder()
                .deviceId(Constants.PleaseSendDeviceIdNextTime+"k")                 //... from a new device
                .instant(new Date())
                .latitude(Double.parseDouble(Constants.latitudePdr))
                .longitude(Double.parseDouble(Constants.latitudePdr))
                .reading(800)                                           //... with this value
                .resolution(32767)                                      //... and this resolution
                .sensorType(Constants.mq9)
                .ro(55)
                .tempInCelsius(20)
                .relativeHumidity(.10)
                .build()
                .makeReadingsWithCalculation();     //WHEN we calculte

        readings.stream().forEach( r -> {
            if(r.getGasName().equals(Constants.Methane) && r.getSensorType().equals(Constants.mq9)){

                log.info("calculated reading: {}", r);

                //THEN we expect this result
                Assert.assertEquals("check calculation",
                        new BigDecimal("12.19").setScale(2,BigDecimal.ROUND_HALF_UP),
                        new BigDecimal(r.getReading()).setScale(2,BigDecimal.ROUND_HALF_UP));
            }
        });

    }
}
