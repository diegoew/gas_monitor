package org.protectplayanow.api.gaslevel;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Builder;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.protectplayanow.api.config.RestApiConsts;

import java.util.*;

/**
 * Created by vladpopescu on 12/12/17.instant, deviceId, gasName, reading, unitOfReading, latitude, longitude
 */
@Data
@Builder
@Slf4j
public class Reading {

    @JsonFormat(pattern = RestApiConsts.dateTimePattern)
    private Date instant;

    private String deviceId, gasName, unitOfReading, sensorType;

    private double latitude, longitude, reading, tempInCelsius, relativeHumidity, input;

    @JsonIgnore
    private double ro;

    private static final double RL_MQ2 = 5;

    public List<Reading> makeReadingsWithCalculation(){

        List<Reading> readings = new ArrayList<>();

        final double input = this.getReading() == 0 ? .0001 : this.getReading();


        log.info("input: {}", input);

        double ro = 0;  //to_do this value needs to be updatd

        double loadResistance = 0;
        Map<String, CalcConsts> calcMap = new HashMap<>();

        switch (this.sensorType) {
            case RestApiConsts.mq2 :
                loadResistance = 5d;
                ro = this.getRo() == 0 ? 6 : this.getRo();
                calcMap.put(RestApiConsts.h2, new CalcConsts(957.82, -2.108));
                calcMap.put(RestApiConsts.lpg, new CalcConsts(569.12, -2.124));
                calcMap.put(RestApiConsts.Methane, new CalcConsts(4295.6, -2.642));
                calcMap.put(RestApiConsts.co, new CalcConsts(28548, -2.968));
                calcMap.put(RestApiConsts.alcohol, new CalcConsts(3480.4, -2.699));
                calcMap.put(RestApiConsts.smoke, new CalcConsts(4013.8, -2.367));
                calcMap.put(RestApiConsts.propane, new CalcConsts(626.13, -2.176));
                break;

            case RestApiConsts.mq9 :
                loadResistance = 18d;
                ro = this.getRo() == 0 ? 50 : this.getRo();
                calcMap.put(RestApiConsts.lpg, new CalcConsts(972.52, -2.133));
                calcMap.put(RestApiConsts.co, new CalcConsts(579.05, -2.247));
                calcMap.put(RestApiConsts.Methane, new CalcConsts(4286.3, -2.624));
                break;

            case RestApiConsts.mq135 :
                loadResistance = 20d;
                ro = this.getRo() == 0 ? 80 : this.getRo();
                calcMap.put(RestApiConsts.co2, new CalcConsts(111.87, -2.893));
                calcMap.put(RestApiConsts.co, new CalcConsts(573.78, -3.924));
                calcMap.put(RestApiConsts.alcohol, new CalcConsts(78.85, -3.206));
                calcMap.put(RestApiConsts.ammonia, new CalcConsts(101.42, -2.482));
                calcMap.put(RestApiConsts.toluene, new CalcConsts(45.116, -3.479));
                calcMap.put(RestApiConsts.acetone, new CalcConsts(34.848, -3.459));
                break;
        }

        log.trace("loadResistance: {}", loadResistance);

        double rs = ((1023/input)-1) * loadResistance;

        log.trace("rs: {}", rs);

        double roFromDefaultOrRecievedValue = ro;

        double rs_over_ro = ((((1023/input)-1)*RL_MQ2)/roFromDefaultOrRecievedValue)
                            /
                            ((.00007*(this.relativeHumidity*100)-.0158)*this.tempInCelsius + (-(.0074*this.relativeHumidity*100) + 1.7761));


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