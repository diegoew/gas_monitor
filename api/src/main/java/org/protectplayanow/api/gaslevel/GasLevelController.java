package org.protectplayanow.api.gaslevel;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.ApiParam;
import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import lombok.extern.slf4j.Slf4j;
import org.protectplayanow.api.config.RestApiConsts;
import org.protectplayanow.api.gaslevel.view.rest.DeviceForRest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.CustomDateEditor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.InitBinder;
import org.springframework.web.bind.annotation.RequestBody;
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
        globalValueMap.put( RestApiConsts.readingFrequency, RestApiConsts.readingFreq70 );
    }

    @Autowired
    JdbcTemplate jdbcTemplate;

    @Autowired
    GasLevelRepo gasLevelRepo;

    @ApiOperation(value = "This endpoint allows you to set or get a global value. For instance the frequency.")
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/globalValue", method = RequestMethod.GET)
    public ResponseEntity<String> setOrGetGlobalValue(

            @ApiParam(value = "use this endpoint to get and set global values")
            @RequestParam(value = "action", defaultValue = RestApiConsts.get, required = true)
                    String action,

            @ApiParam(value = "enter the value 'key' aka value 'name'")
            @RequestParam(value = "key", defaultValue = RestApiConsts.readingFrequency, required = false)
            @DateTimeFormat(pattern = RestApiConsts.dateTimePattern)
                    String key,

            @ApiParam(value = "enter the new value for the key that you are sending")
            @RequestParam(value = "value", defaultValue = RestApiConsts.readingFreq70, required = false)
            @DateTimeFormat(pattern = RestApiConsts.dateTimePattern)
                    String value

    ) {

        List<Reading> readings = new ArrayList<>();

        log.info("action={}, key={}, value={}", action, key, value);

        String previousValue = globalValueMap.get( key );

        log.info("previousValue={}", previousValue);

        if( action.equals( RestApiConsts.get ) ) {
            value = globalValueMap.get( key );
        } else if ( action.equals( RestApiConsts.set ) ) {
            value = globalValueMap.put( key, value );
        }

        value = globalValueMap.get( key );

        HttpHeaders responseHeaders = RestApiConsts.makeGlobalHeaders(globalValueMap.get(RestApiConsts.readingFrequency));

        return new ResponseEntity<String>(
                "thanks for submitting a '" + action +
                        "' request, the value for '" + key +
                        "' is '" + value + "' the previous value was '" + previousValue +
                        "'",
                responseHeaders,
                HttpStatus.OK);

    }


    @ApiOperation(value = "This endpoint allows you to get a list of unique deviceIds, sensorType, latidude, longitude.")
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/devices", method = RequestMethod.GET)
    public ResponseEntity<List<DeviceForRest>> getDevices(){

        HttpHeaders responseHeaders = RestApiConsts.makeGlobalHeaders(globalValueMap.get(RestApiConsts.readingFrequency));

        return new ResponseEntity<List<DeviceForRest>>(
                DeviceForRest.make(gasLevelRepo.getDevices()),
                responseHeaders,
                HttpStatus.OK);

    }

    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/readings", method = RequestMethod.GET)
    public ResponseEntity<List<Reading>> getReadings(

            @ApiParam(value = RestApiConsts.apiGasMessage)
            @RequestParam(value = "gasName", defaultValue = RestApiConsts.all, required = false)
                    String gasName,

            @ApiParam(value = RestApiConsts.apiDateMessage)
            @RequestParam(value = "startDateTime", defaultValue = RestApiConsts.dayago, required = false)
            @DateTimeFormat(pattern = RestApiConsts.dateTimePattern)
                    Date startDateTime,

            @ApiParam(value = RestApiConsts.apiDateMessage)
            @RequestParam(value = "endDateTime", defaultValue = RestApiConsts.now, required = false)
            @DateTimeFormat(pattern = RestApiConsts.dateTimePattern)
                    Date endDateTime,

            @ApiParam(value = "sensorType")
            @RequestParam(value = "sensorType", defaultValue = RestApiConsts.mq9, required = false)
                    String sensorName,

            @ApiParam(value = "deviceId")
            @RequestParam(value = "deviceId", defaultValue = RestApiConsts.deviceId, required = false)
                    String deviceId

            ) {

        List<Reading> readings = new ArrayList<>();

        log.info("gasName={}, startDateTime={}, endDateTime={}", gasName, startDateTime, endDateTime);

        HttpHeaders responseHeaders = RestApiConsts.makeGlobalHeaders(globalValueMap.get(RestApiConsts.readingFrequency));

        return new ResponseEntity<List<Reading>>(
                gasLevelRepo.getGasReadings(gasName, startDateTime, endDateTime, sensorName, deviceId),
                responseHeaders,
                HttpStatus.OK);

    }

    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 400, message = "You are not sending in the proper request. See 'warning' header for info, Buster!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/readings", method = RequestMethod.POST)
    public ResponseEntity<Void> readingsWrite(

            @ApiParam(value = "deviceId")
            @RequestParam(value = "deviceId", defaultValue = RestApiConsts.PleaseSendDeviceIdNextTime, required = false)
                    String deviceId,

            @ApiParam(value = RestApiConsts.apiInstantDateMessage)
            @RequestParam(value = "instant", defaultValue = RestApiConsts.now, required = false)
            @DateTimeFormat(pattern = RestApiConsts.dateTimePattern)
                    Date instant,

            @ApiParam(value = RestApiConsts.latitudePdr)
            @RequestParam(value = "latitude", defaultValue = RestApiConsts.latitudePdr, required = false)
                    double latitude,

            @ApiParam(value = RestApiConsts.longitudePdr)
            @RequestParam(value = "longitude", defaultValue = RestApiConsts.longitudePdr, required = false)
                    double longitude,

            @RequestBody(required = true) List<ReadingForRestPOST> readings

    ) {

        if(readings == null){
            MultiValueMap<String, String> headers = new HttpHeaders();
            headers.set(HttpHeaders.WARNING, "You sent in null for the readings parameter.");
            ResponseEntity re = new ResponseEntity<Void>(headers, HttpStatus.BAD_REQUEST);
            return re;
        } else if(readings.isEmpty()){
            MultiValueMap<String, String> headers = new HttpHeaders();
            headers.set(HttpHeaders.WARNING, "You sent in an empty list for the readings parameter.");
            ResponseEntity re = new ResponseEntity<Void>(headers, HttpStatus.BAD_REQUEST);
            return re;
        }

        log.info("deviceId={}, instant={}, latitude={}, longitude={}", deviceId, instant, latitude, longitude);

        gasLevelRepo.saveGasReadings(deviceId, instant, latitude, longitude, readings);

        return new ResponseEntity<Void>(
                RestApiConsts.makeGlobalHeaders(globalValueMap.get(RestApiConsts.readingFrequency)),
                HttpStatus.OK);

    }
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 400, message = "You are not sending in the proper request. See 'warning' header for info, Buster!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/readings/calculate", method = RequestMethod.POST)
    public ResponseEntity<Void> readingsWriteAfterCalculation(

            @ApiParam(value = "deviceId")
            @RequestParam(value = "deviceId", defaultValue = RestApiConsts.PleaseSendDeviceIdNextTime, required = false)
                    String deviceId,

            @ApiParam(value = RestApiConsts.apiInstantDateMessage)
            @RequestParam(value = "instant", defaultValue = RestApiConsts.now, required = false)
            @DateTimeFormat(pattern = RestApiConsts.dateTimePattern)
                    Date instant,

            @ApiParam(value = RestApiConsts.latitudePdr)
            @RequestParam(value = "latitude", defaultValue = RestApiConsts.latitudePdr, required = false)
                    double latitude,

            @ApiParam(value = RestApiConsts.longitudePdr)
            @RequestParam(value = "longitude", defaultValue = RestApiConsts.longitudePdr, required = false)
                    double longitude,

            @ApiParam(value = RestApiConsts.sensorTypeMsg)
            @RequestParam(value = "sensorType", defaultValue = RestApiConsts.mq2, required = false)
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
                    double relativeHumidity

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
                .ro(ro)
                .tempInCelsius(tempInCelsius)
                .relativeHumidity(relativeHumidity)
                .build();

        gasLevelRepo.saveGasReadings(r.makeReadingsWithCalculation());

        return new ResponseEntity<Void>(RestApiConsts.makeGlobalHeaders(
                globalValueMap.get(RestApiConsts.readingFrequency)),
                HttpStatus.OK);

    }

    @InitBinder
    public void dataBinding(WebDataBinder binder) {

        final DateFormat df = new SimpleDateFormat(RestApiConsts.dateTimePattern);

        final CustomDateEditor dateEditor = new CustomDateEditor(df, true) {

            @Override
            public void setAsText(String text) throws IllegalArgumentException {

                if (RestApiConsts.now.equals(text)) {
                    setValue(new Date());
                } else if (RestApiConsts.dayago.equals(text)) {
                    Calendar cal = Calendar.getInstance();
                    cal.setTime(new Date());
                    cal.add(Calendar.DATE, -1);
                    setValue(new Date(cal.getTimeInMillis()));
                } else if (RestApiConsts.weekago.equals(text)) {
                    Calendar cal = Calendar.getInstance();
                    cal.setTime(new Date());
                    cal.add(Calendar.DATE, -7);
                    setValue(new Date(cal.getTimeInMillis()));
                } else if (RestApiConsts.monthago.equals(text)) {
                    Calendar cal = Calendar.getInstance();
                    cal.setTime(new Date());
                    cal.add(Calendar.DATE, -30);
                    setValue(new Date(cal.getTimeInMillis()));
                } else if (RestApiConsts.yearago.equals(text)) {
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
