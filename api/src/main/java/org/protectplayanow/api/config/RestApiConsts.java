package org.protectplayanow.api.config;

import java.util.Arrays;
import java.util.stream.Collectors;

/**
 * Created by vladpopescu on 12/17/17.
 */
public class RestApiConsts {
    public static final String

            dateTimePattern = "yyyy-MM-dd'T'HH:mm:ssXXX",
            dateTimePatternExample = "2012-12-20T13:14:15-00:00",
            now = "now",
            yearago = "yearago",
            monthago = "monthago",
            weekago = "weekago",
            dayago = "dayago",

            all = "all",
            Methane = "methane",
            formaldehyde = "formaldehyde",
            Benzene = "benzene",

            PleaseSendDeviceIdNextTime = "PleaseSendDeviceIdNextTime"
            ;

    public static final String
            dateKeys = "[" + now + "], [" + yearago + "], [" + monthago + "], [" + weekago + "], [" + dayago + "]"
            ;

    public static final String
            apiDateMessage = "pass in strings " + RestApiConsts.dateKeys + ", or date with pattern [" + RestApiConsts.dateTimePatternExample + "]"
            ;

    public static final String
            apiInstantDateMessage = "pass in string [" + RestApiConsts.now + "] or date with pattern [" + RestApiConsts.dateTimePatternExample + "]"
            ;

    public static final String
            gasKeys = "[" + all + "], [" + Methane + "], [" + formaldehyde + "], [" + Benzene + "]"
            ;

    public static final String gasKeysCommaSep = Arrays.asList(Methane, formaldehyde, Benzene)
                                                        .stream()
                                                        .collect(Collectors
                                                        .joining(","));

    public static final String
            apiGasMessage = "pass in strings " + RestApiConsts.gasKeys + ", or other gas names that sensors have reported"
            ;


    public static final double
            latitude = 33.962492,
            longitude = -118.437547
            ;

    public static final String
            latitudePdr = latitude + "",
            longitudePdr = longitude + ""
                    ;



}
