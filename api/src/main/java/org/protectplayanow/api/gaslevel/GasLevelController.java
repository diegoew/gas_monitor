package org.protectplayanow.api.gaslevel;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

import io.swagger.annotations.*;
import lombok.extern.slf4j.Slf4j;
import org.protectplayanow.api.Greeting;
import org.protectplayanow.api.config.RestApiConsts;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.propertyeditors.CustomDateEditor;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.WebDataBinder;
import org.springframework.web.bind.annotation.*;

@RestController
@Api(description = "These example endpoints don't do anything. But they will respond" +
        " if you call them correctly.")
@Slf4j
public class GasLevelController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();

    @Autowired
    JdbcTemplate jdbcTemplate;

    @Autowired
    GasLevelRepo gasLevelRepo;

    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Well done!"),
            @ApiResponse(code = 500, message = "Server error a.k.a. royal screwup!")})
    @RequestMapping(value = "/readings", method = RequestMethod.GET)
    public List<Reading> readingsRead(

            @ApiParam(value = RestApiConsts.apiGasMessage)
            @RequestParam(value = "gasName", defaultValue = RestApiConsts.all, required = false)
                    String gasName,

            @ApiParam(value = RestApiConsts.apiDateMessage)
            @RequestParam(value = "startDateTime", defaultValue = RestApiConsts.yearago, required = false)
            @DateTimeFormat(pattern = RestApiConsts.dateTimePattern)
                    Date startDateTime,

            @ApiParam(value = RestApiConsts.apiDateMessage)
            @RequestParam(value = "endDateTime", defaultValue = RestApiConsts.now, required = false)
            @DateTimeFormat(pattern = RestApiConsts.dateTimePattern)
                    Date endDateTime

            ) {

        List<Reading> readings = new ArrayList<>();

        log.info("gasName={}, startDateTime={}, endDateTime={}", gasName, startDateTime, endDateTime);

        return gasLevelRepo.getGasReadings(gasName, startDateTime, endDateTime);

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

        return new ResponseEntity<Void>(HttpStatus.OK);

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

    @RequestMapping(value = "/exampleGetValue", method = RequestMethod.GET)
    public Greeting greeting(@RequestParam(value="name", defaultValue="World of Gas Monitoring") String name) {

        jdbcTemplate.query(
                "SELECT * from reading WHERE 1 = ?", new Object[] { 1 },
                (rs, rowNum) -> Reading.builder()
                        .instant(new Date(rs.getTimestamp("instant").getTime()))
                        .deviceId(rs.getString("deviceId"))
                        .gasName(rs.getString("gasName"))
                        .reading(rs.getDouble("reading"))
                        .unitOfReading(rs.getString("unitOfReading"))
                        .latitude(rs.getDouble("latitude"))
                        .longitude(rs.getDouble("longitude"))
                        .build()
        ).forEach(reading -> log.info(reading.toString()));

        return new Greeting(counter.incrementAndGet(),
                            String.format(template, name));

    }

    @RequestMapping(value="/examplePostValue", method = RequestMethod.POST)
    public String add(@RequestBody Reading input) {

        return String.format(template, "buddy");

    }
}
