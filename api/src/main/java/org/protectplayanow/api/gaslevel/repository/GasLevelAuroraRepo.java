package org.protectplayanow.api.gaslevel.repository;

import lombok.extern.slf4j.Slf4j;
import org.protectplayanow.api.config.Constants;
import org.protectplayanow.api.gaslevel.GasLevelRepo;
import org.protectplayanow.api.gaslevel.Reading;
import org.protectplayanow.api.gaslevel.ReadingForRestPOST;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.BatchPreparedStatementSetter;
import org.springframework.jdbc.core.JdbcTemplate;

import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Timestamp;
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

        log.info("st: {}", AuroraDbUtils.makeDateforUTC(startDateTime));
        log.info("en: {}", AuroraDbUtils.makeDateforUTC(endDateTime));

        Calendar cal = GregorianCalendar.getInstance();
        cal.setTimeZone(TimeZone.getTimeZone("UTC"));

        jdbcTemplate.query(
                "SELECT * from reading WHERE " +
                        (gasName.equals(Constants.all) ? "" : " gasName in " + AuroraDbUtils.getInClauseList(gasName) + " and ") +
                        " deviceId = '" + deviceId + "' and " +
                        " sensorType = '" + sensorType + "' and " +
                        " instant >= '" + AuroraDbUtils.makeDateforUTC(startDateTime) +
                        " ' and instant <= '" + AuroraDbUtils.getDate(endDateTime) + "'" +
                        " order by instant desc",
                new Object[] { },
                (rs, rowNum) -> {

                    Timestamp tsFromDb = rs.getTimestamp("instant");

                    log.trace("from db: {}", tsFromDb);

                    cal.setTime(tsFromDb);

//                    log.info("cal: {}", cal);

                    cal.add(Calendar.HOUR_OF_DAY, -timeZoneOffset);

//                    log.info("cal: {}", cal);

                    Date dToReturn = new Date(cal.getTimeInMillis());

                    log.trace("modified: {}", dToReturn);

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
                        .resolution(rs.getDouble("resolution"))
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
    public void saveGasReadings(List<Reading> readings) {
        String q = " INSERT INTO reading " +
                " (instant, deviceId, gasName, reading, unitOfReading, latitude, longitude, sensorType, ro, relHumidity, tempInCelsius, input, resolution) " +
                " VALUES " +
                " (?,       ?,        ?,       ?,       ?,             ?,        ?,         ?,          ?,  ?,           ?,             ?,     ?)";


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
                        ps.setDouble(13, readings.get(i).getResolution());
                    }
                    @Override
                    public int getBatchSize() {
                        return readings.size();
                    }
                });
    }

}
