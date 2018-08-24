package org.protectplayanow.api.gaslevel.repository;

import lombok.extern.slf4j.Slf4j;
import org.protectplayanow.api.config.RestApiConsts;
import org.protectplayanow.api.gaslevel.GasLevelRepo;
import org.protectplayanow.api.gaslevel.Reading;
import org.protectplayanow.api.gaslevel.ReadingForRestPOST;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BatchPreparedStatementSetter;
import org.springframework.jdbc.core.JdbcTemplate;

import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.util.*;

/**
 * Created by vladpopescu on 12/17/17.
 */
@Slf4j
public class GasLevelAuroraRepo implements GasLevelRepo {

    @Autowired
    JdbcTemplate jdbcTemplate;

    @Override
    public List<Reading> getGasReadings(String gasName, Date startDateTime, Date endDateTime, String sensorType, String deviceId) {

        List<Reading> readings = new ArrayList<>();

        int timeZoneOffset = (startDateTime.getTimezoneOffset()/60);

        log.info("startDate: {}", AuroraDbUtils.getDate(startDateTime));
        log.info("endDateTime: {}", AuroraDbUtils.getDate(endDateTime));

        Calendar cal = GregorianCalendar.getInstance();
        cal.setTimeZone(TimeZone.getTimeZone("UTC"));

        jdbcTemplate.query(
                "SELECT * from reading WHERE " +
                        (gasName.equals(RestApiConsts.all) ? "" : " gasName in " + AuroraDbUtils.getInClauseList(gasName) + " and ") +
                        " deviceId = '" + deviceId + "' and " +
                        " sensorType = '" + sensorType + "' and " +
                        " instant >= '" + AuroraDbUtils.getDate(startDateTime) +
                        " ' and instant <= '" + AuroraDbUtils.getDate(endDateTime) + "'" +
                        " order by instant desc",
                new Object[] { },
                (rs, rowNum) -> {

                    Timestamp tsFromDb = rs.getTimestamp("instant");

                    log.info("from db: {}", tsFromDb);

                    cal.setTime(tsFromDb);

//                    log.info("cal: {}", cal);

                    cal.add(Calendar.HOUR_OF_DAY, -timeZoneOffset);

//                    log.info("cal: {}", cal);

                    Date dToReturn = new Date(cal.getTimeInMillis());

                    log.info("modified: {}", dToReturn);

                    return Reading.builder()
                        .instant(dToReturn)
                        .deviceId(rs.getString("deviceId"))
                        .gasName(rs.getString("gasName"))
                        .reading(rs.getDouble("reading"))
                        .unitOfReading(rs.getString("unitOfReading"))
                        .latitude(rs.getDouble("latitude"))
                        .longitude(rs.getDouble("longitude"))
                        .sensorType(rs.getString("sensorType"))
                        .input(rs.getDouble("input"))
                        .relativeHumidity(rs.getDouble("relHumidity"))
                        .tempInCelsius(rs.getDouble("tempInCelsius"))
                        .ro(rs.getDouble("ro"))
                        .build();}
        ).forEach(reading -> {
            //log.debug(reading.toString());
            readings.add(reading);
        });

        return readings;
    }

    @Override
    public List<Device> getDevices() {

        List<Device> devices = new ArrayList<>();

        jdbcTemplate.query(
                "select distinct deviceId, sensorType, latitude, longitude from reading " +
                        " order by deviceId asc",
                new Object[] { },
                (rs, rowNum) ->
                        Device.builder()
                        .deviceId(rs.getString("deviceId"))
                        .sensorType(rs.getString("sensorType"))
                        .latitude(rs.getDouble("latitude"))
                        .longitude(rs.getDouble("longitude"))
                        .build()
        ).forEach(device -> {
            log.debug(device.toString());
            devices.add(device);
        });

        return devices;
    }

    @Override
    public void saveGasReadings(String deviceId, Date instant, double latitude, double longitude, List<ReadingForRestPOST> readings) {
/*
INSERT INTO reading
(instant, deviceId, gasName, reading, unitOfReading, latitude, longitude)
VALUES
('2016-12-17 14:01:04', 'id1', 'Methane', 0, 'ppm', 0.3, 0.4),
('2016-12-17 14:01:04', 'id1', 'Benzene', 0, 'ppm', 0.3, 0.4);
 */
        String q = " INSERT INTO reading " +
                " (instant, deviceId, gasName, reading, unitOfReading, latitude, longitude) " +
                " VALUES ";
        StringBuffer sb = new StringBuffer(q);

        for(int i = 0; i < readings.size(); i++){

            ReadingForRestPOST r = readings.get(i);

            sb.append("('" + AuroraDbUtils.getDate(instant) +
                    "', '" + deviceId +
                    "', '" + r.getGasName() +
                    "', " + r.getReading() +
                    ", '" + r.getUnitOfReading() +
                    "', " + latitude +
                    ", " + longitude +
                    "),");

        }

        sb.deleteCharAt(sb.length()-1);

        jdbcTemplate.execute(sb.toString());
    }

    @Override
    public void saveGasReadings(List<Reading> readings) {
//INSERT INTO `reading` (`instant`, `deviceId`, `gasName`, `reading`, `unitOfReading`, `latitude`, `longitude`, `sensorType`, `ro`, `relHumidity`, `tempInCelsius`)
//VALUES
//	('2012-12-20 13:14:15', 'PleaseSendDeviceIdNextTime', 'methane', 0.00007825264608338657, 'ppm', 33.962492, -118.437547, 'MQ-2', NULL, NULL, NULL);
        String q = " INSERT INTO reading " +
                " (instant, deviceId, gasName, reading, unitOfReading, latitude, longitude, sensorType, ro, relHumidity, tempInCelsius, input) " +
                " VALUES " +
                " (?,       ?,        ?,       ?,       ?,             ?,        ?,         ?,          ?,  ?,           ?,             ?)";

//        StringBuffer sb = new StringBuffer(q);
//
//        for(int i = 0; i < readings.size(); i++){
//
//            Reading r = readings.get(i);
//
//            sb.append("('" + AuroraDbUtils.getDate(r.getInstant()) +
//                    "', '" + r.getDeviceId() +
//                    "', '" + r.getGasName() +
//                    "', " + r.getReading() +
//                    ", '" + r.getUnitOfReading() +
//                    "', " + r.getLatitude() +
//                    ", " + r.getLongitude() +
//                    ", '" + r.getSensorType() + "'" +
//                    ", " + r.getRo() + "" +
//                    ", " + r.getRelativeHumidity() + "" +
//                    ", " + r.getTempInCelsius() + "" +
//                    "),");
//
//        }
//
//        sb.deleteCharAt(sb.length()-1);
//
//        log.info(sb.toString());
//
//        jdbcTemplate.execute(sb.toString());

        jdbcTemplate.batchUpdate(q,
                new BatchPreparedStatementSetter() {
                    @Override
                    public void setValues(PreparedStatement ps, int i) throws SQLException {

                        ps.setTimestamp(1, new java.sql.Timestamp(readings.get(i).getInstant().getTime()));
                        ps.setString(2, readings.get(i).getDeviceId());
                        ps.setString(3, readings.get(i).getGasName());
                        ps.setDouble(4, readings.get(i).getReading());
                        ps.setString(5, readings.get(i).getUnitOfReading());
                        ps.setDouble(6, readings.get(i).getLatitude());
                        ps.setDouble(7, readings.get(i).getLongitude());
                        ps.setString(8, readings.get(i).getSensorType());
                        ps.setDouble(9, readings.get(i).getRo());
                        ps.setDouble(10, readings.get(i).getRelativeHumidity());
                        ps.setDouble(11, readings.get(i).getTempInCelsius());
                        ps.setDouble(12, readings.get(i).getInput());
                    }
                    @Override
                    public int getBatchSize() {
                        return readings.size();
                    }
                });
    }

}
