package org.protectplayanow.api;

import java.util.concurrent.atomic.AtomicLong;

import io.swagger.annotations.Api;
import io.swagger.annotations.ApiParam;
import lombok.extern.log4j.Log4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

@RestController
@Api(description = "These endpoints don't save data, at the moment. But they will respond" +
        " if you call them correctly.")
@Log4j
public class GasLevelController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();


    @Autowired
    JdbcTemplate jdbcTemplate;

    @RequestMapping(value = "/exampleGetValue", method = RequestMethod.GET)
    public Greeting greeting(@RequestParam(value="name", defaultValue="World of Gas Monitoring") String name) {

        log.info("Querying for customer records where first_name = 'Josh':");
/*
INSERT INTO protectplayanow2.reading
(instant, deviceId, gasName, reading, unitOfReading, latitude, longitude)
VALUES('2017-01-01 12:12:12', '', '', 0, '', 0.12, 0);
 */
        jdbcTemplate.query(
                "SELECT * from reading WHERE 1 = ?", new Object[] { 1 },
                (rs, rowNum) -> Reading.builder()
                        .instant(rs.getDate("instant"))
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
