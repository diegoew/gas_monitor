package org.protectplayanow.api.gaslevel;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.annotations.ApiModelProperty;
import lombok.Builder;
import lombok.Data;
import org.protectplayanow.api.config.RestApiConsts;

import java.time.LocalDateTime;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * Created by vladpopescu on 12/12/17.instant, deviceId, gasName, reading, unitOfReading, latitude, longitude
 */
@Data
@Builder
public class Reading {

    @JsonFormat(pattern = RestApiConsts.dateTimePattern)
    private Date instant;

    private String deviceId, gasName, unitOfReading;

    private double latitude, longitude, reading;

//    private final Map<String, Double> gasNameAndReading = new HashMap<>();

}
