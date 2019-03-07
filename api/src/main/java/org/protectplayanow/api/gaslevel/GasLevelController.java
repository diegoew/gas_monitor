package org.protectplayanow.api.gaslevel;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import lombok.extern.slf4j.Slf4j;
import org.protectplayanow.api.config.Constants;
import org.protectplayanow.api.gaslevel.view.rest.DeviceForRest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.CustomDateEditor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@RestController
@Api(description = "These endpoints allow you store and retrieve data.")
@Slf4j
public class GasLevelController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();
    public static final ConcurrentHashMap<String, String> globalValueMap = new ConcurrentHashMap<>();
    static {
        globalValueMap.put( Constants.secondsBetweenReadings, Constants.secondsBetweenReadingsDefaultValue);
    }

    @Autowired
    JdbcTemplate jdbcTemplate;

    @Autowired
    GasLevelRepo gasLevelRepo;

    @ApiOperation(value = "This endpoint allows you to set or get a global value. For instance the time interval between readings.")
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/globalValue", method = RequestMethod.GET)
    public ResponseEntity<String> getGlobalValue(

            @ApiParam(value = "enter the value 'key' aka value 'name'")
            @RequestParam(value = "key", defaultValue = Constants.secondsBetweenReadings, required = false)
            @DateTimeFormat(pattern = Constants.dateTimePattern)
                    String key

    ) {

        String previousValue = globalValueMap.get( key );

        log.info("previousValue={}", previousValue);

        previousValue = globalValueMap.get(key);

        HttpHeaders responseHeaders = Constants.makeGlobalHeaders(globalValueMap.get(key));

        return new ResponseEntity<String>(
                key + " = '" + previousValue + "'",
                responseHeaders,
                HttpStatus.OK);

    }


    @ApiOperation(value = "This endpoint allows you to set a global value, for instance the reading frequency.")
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/globalValue", method = RequestMethod.POST)
    public ResponseEntity<String> setGlobalValue(

            @ApiParam(value = "enter the value 'key' aka value 'name'")
            @RequestParam(value = "key", defaultValue = Constants.secondsBetweenReadings, required = false)
            @DateTimeFormat(pattern = Constants.dateTimePattern)
                    String key,

            @ApiParam(value = "enter the new value for the key that you are sending")
            @RequestParam(value = "value", defaultValue = Constants.secondsBetweenReadingsDefaultValue, required = false)
            @DateTimeFormat(pattern = Constants.dateTimePattern)
                    String value

    ) {

        List<Reading> readings = new ArrayList<>();

        log.info("key={}, value={}", key, value);

        String previousValue = globalValueMap.get( key );

        log.info("previousValue={}", previousValue);

        value = globalValueMap.put(key, value);

        return new ResponseEntity<String>(
                "set " + key + " := '" + value + "'. Was '" + previousValue + "'",
                HttpStatus.OK);

    }

    @ApiOperation(value = "This endpoint allows you to get a list of unique deviceIds, sensorType, latidude, longitude.")
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/devices", method = RequestMethod.GET)
    public ResponseEntity<List> getDevices(
            @ApiParam(value = Constants.apiIdsMessage)
            @RequestParam(value = "ids", defaultValue = "false", required = false) boolean shouldIncludeIds
    ) {
        if (shouldIncludeIds) {
            return new ResponseEntity<List>(
                gasLevelRepo.getDeviceIds(),
                HttpStatus.OK);
        } else {
            return new ResponseEntity<List>(
                DeviceForRest.make(gasLevelRepo.getDevices()),
                HttpStatus.OK);
        }
    }

    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/readings", method = RequestMethod.GET)
    public ResponseEntity<List<Reading>> getReadings(

            @ApiParam(value = Constants.apiGasMessage)
            @RequestParam(value = "gasName", defaultValue = Constants.all, required = false)
                    String gasName,

            @ApiParam(value = Constants.apiDateMessage)
            @RequestParam(value = "startDateTime", defaultValue = Constants.dayago, required = false)
            @DateTimeFormat(pattern = Constants.dateTimePattern)
                    Date startDateTime,

            @ApiParam(value = Constants.apiDateMessage)
            @RequestParam(value = "endDateTime", defaultValue = Constants.now, required = false)
            @DateTimeFormat(pattern = Constants.dateTimePattern)
                    Date endDateTime,

            @ApiParam(value = "sensorType")
            @RequestParam(value = "sensorType", defaultValue = Constants.mq9, required = false)
                    String sensorName,

            @ApiParam(value = "deviceId")
            @RequestParam(value = "deviceId", defaultValue = Constants.PleaseSendDeviceIdNextTime, required = false)
                    String deviceId

            ) {

        List<Reading> readings = new ArrayList<>();

        log.info("gasName={}, startDateTime={}, endDateTime={}", gasName, startDateTime, endDateTime);

        HttpHeaders responseHeaders = Constants.makeGlobalHeaders(globalValueMap.get(Constants.secondsBetweenReadings));

        return new ResponseEntity<List<Reading>>(
                gasLevelRepo.getGasReadings(gasName, startDateTime, endDateTime, sensorName, deviceId),
                responseHeaders,
                HttpStatus.OK);

    }

    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 400, message = "You are not sending in the proper request. See 'warning' header for info, Buster!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/readings/calculate", method = RequestMethod.POST)
    public ResponseEntity<Void> setReadingsWriteAfterCalculation(

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

        log.info("deviceId={}, instant={}, latitude={}, longitude={}, sensorTypeMsg={}", deviceId, instant, latitude, longitude, sensorType);

        Reading r = Reading.builder()
                .deviceId(deviceId)
                .instant(instant)
                .latitude(latitude)
                .longitude(longitude)
                .reading(reading)
                .input(reading)
                .sensorType(sensorType)
                .resolution(resolution)
                .ro(ro)
                .tempInCelsius(tempInCelsius)
                .relativeHumidity(relativeHumidity)
                .build();

        gasLevelRepo.saveGasReadings(r.makeReadingsWithCalculation());

        return new ResponseEntity<Void>(Constants.makeGlobalHeaders(
                globalValueMap.get(Constants.secondsBetweenReadings)),
                HttpStatus.OK);

    }

    @InitBinder
    public void dataBinding(WebDataBinder binder) {

        final DateFormat df = new SimpleDateFormat(Constants.dateTimePattern);

        final CustomDateEditor dateEditor = new CustomDateEditor(df, true) {

            @Override
            public void setAsText(String text) throws IllegalArgumentException {

                if (Constants.now.equals(text)) {
                    setValue(new Date());
                } else if (Constants.dayago.equals(text)) {
                    Calendar cal = Calendar.getInstance();
                    cal.setTime(new Date());
                    cal.add(Calendar.DATE, -1);
                    setValue(new Date(cal.getTimeInMillis()));
                } else if (Constants.weekago.equals(text)) {
                    Calendar cal = Calendar.getInstance();
                    cal.setTime(new Date());
                    cal.add(Calendar.DATE, -7);
                    setValue(new Date(cal.getTimeInMillis()));
                } else if (Constants.monthago.equals(text)) {
                    Calendar cal = Calendar.getInstance();
                    cal.setTime(new Date());
                    cal.add(Calendar.DATE, -30);
                    setValue(new Date(cal.getTimeInMillis()));
                } else if (Constants.yearago.equals(text)) {
                    Calendar cal = Calendar.getInstance();
                    cal.setTime(new Date());
                    cal.add(Calendar.DATE, -365);
                    setValue(new Date(cal.getTimeInMillis()));
                }

                else {
                    super.setAsText(text);
                }

            }

        };

        binder.registerCustomEditor(Date.class, dateEditor);

    }

}
