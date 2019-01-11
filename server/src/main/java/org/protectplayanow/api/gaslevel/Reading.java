package org.protectplayanow.api.gaslevel;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Builder;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.protectplayanow.api.config.Constants;

import java.util.*;

/**
 * Created by vladpopescu on 12/12/17
 */
@Data
@Builder
@Slf4j
public class Reading {

    @JsonFormat(pattern = Constants.dateTimePattern)
    private Date instant;

    private String deviceId, gasName, unitOfReading, sensorType;

    private double latitude, longitude, reading, tempInCelsius, relativeHumidity, input;

    private double ro;

    private double resolution;

    private static final double RL_MQ2 = 5;
    private static final double RL_MQ9 = 18;
    private static final double RL_MQ135 = 20;

    public List<Reading> makeReadingsWithCalculation(){

        List<Reading> readings = new ArrayList<>();

        final double input = this.getReading() == 0 ? .0001 : this.getReading();

        double ro = 0;  //to_do this value needs to be updatd

        double loadResistance = 0;
        Map<String, CalcConsts> calcMap = new HashMap<>();

        switch (this.sensorType) {
            case Constants.mq2 :
                loadResistance = RL_MQ2;
                ro = this.getRo() == 0 ? 6 : this.getRo();
                calcMap.put(Constants.h2, new CalcConsts(957.82, -2.108));
                calcMap.put(Constants.lpg, new CalcConsts(569.12, -2.124));
                calcMap.put(Constants.Methane, new CalcConsts(4295.6, -2.642));
                calcMap.put(Constants.co, new CalcConsts(28548, -2.968));
                calcMap.put(Constants.alcohol, new CalcConsts(3480.4, -2.699));
                calcMap.put(Constants.smoke, new CalcConsts(4013.8, -2.367));
                calcMap.put(Constants.propane, new CalcConsts(626.13, -2.176));
                break;

            case Constants.mq9 :
                loadResistance = RL_MQ9;
                ro = this.getRo() == 0 ? 50 : this.getRo();
                calcMap.put(Constants.lpg, new CalcConsts(972.52, -2.133));
                calcMap.put(Constants.co, new CalcConsts(579.05, -2.247));
                calcMap.put(Constants.Methane, new CalcConsts(4286.3, -2.624));
                break;

            case Constants.mq135 :
                loadResistance = RL_MQ135;
                ro = this.getRo() == 0 ? 80 : this.getRo();
                calcMap.put(Constants.co2, new CalcConsts(111.87, -2.893));
                calcMap.put(Constants.co, new CalcConsts(573.78, -3.924));
                calcMap.put(Constants.alcohol, new CalcConsts(78.85, -3.206));
                calcMap.put(Constants.ammonia, new CalcConsts(101.42, -2.482));
                calcMap.put(Constants.toluene, new CalcConsts(45.116, -3.479));
                calcMap.put(Constants.acetone, new CalcConsts(34.848, -3.459));
                break;
        }

        double roFromDefaultOrRecievedValue = ro;

        double res = (getDeviceId().equals("RaspPi-Vlad-old-script")||getDeviceId().equals("RaspPi-Prototype-1")) ? 1023 : resolution;

        double rs_over_ro = ((((res/input)-1)*loadResistance)/roFromDefaultOrRecievedValue)
                            /
                            ((.00007*(this.relativeHumidity*100)-.0158)*this.tempInCelsius + (-(.0074*this.relativeHumidity*100) + 1.7761));

        log.info("input: {}", input);


        log.trace("roFromDefaultOrRecievedValue: {}", roFromDefaultOrRecievedValue);
        log.trace("rs_over_ro: {}", rs_over_ro);

        calcMap.forEach((key, calc) -> {

            readings.add(

                    Reading.builder()
                    .sensorType(this.sensorType)
                    .deviceId(this.deviceId)
                    .gasName(key)
                    .instant(this.instant)
                    .latitude(this.latitude)
                    .longitude(this.longitude)
                    .relativeHumidity(this.relativeHumidity)
                    .tempInCelsius(this.tempInCelsius)
                    .resolution(res)
                    .ro(roFromDefaultOrRecievedValue)
                    .input(input)
                    .unitOfReading("ppm")
                    .reading(
                            calc.c1 * (Math.pow((rs_over_ro), calc.c2))
                    )
                    .build()

            );

            log.trace("reading: {}, gasName: {} ", readings.get(readings.size()-1).reading, readings.get(readings.size()-1).gasName);
        });

        return readings;
    }

}


class CalcConsts{
    double c1, c2;
    public CalcConsts (double c1, double c2){
        this.c1 = c1;
        this.c2 = c2;
    }
}