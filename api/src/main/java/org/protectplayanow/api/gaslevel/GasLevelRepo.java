package org.protectplayanow.api.gaslevel;

import org.protectplayanow.api.gaslevel.repository.Device;

import java.util.Date;
import java.util.List;

/**
 * Created by vladpopescu on 12/17/17.
 */
public interface GasLevelRepo {

    List<Reading> getGasReadings(String gasName, Date startDateTime, Date endDateTime, String sensorType, String deviceId);

    void saveGasReadings(String deviceId, Date instant, double latitude, double longitude, List<ReadingForRestPOST> readings);

    void saveGasReadings(List<Reading> readings);

    List<Device> getDevices();

}
