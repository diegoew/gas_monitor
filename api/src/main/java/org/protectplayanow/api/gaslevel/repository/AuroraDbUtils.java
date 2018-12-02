package org.protectplayanow.api.gaslevel.repository;

import lombok.extern.slf4j.Slf4j;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Created by vladpopescu on 12/17/17.
 */
@Slf4j
public class AuroraDbUtils {

    public static String getInClauseStringList(Collection<String> strings){
        return "('" + strings.stream().map(String::valueOf).collect(Collectors.joining("','")) + "')";
    }

    public static String getInClauseList(String commaSeparatedStrings){
        return getInClauseStringList( Arrays.stream( commaSeparatedStrings.split(",") ).collect( Collectors.toList() ) );
    }

    public static LocalDateTime makeLocalDateTime(Timestamp ts){
        return LocalDateTime.ofInstant(Instant.ofEpochMilli(ts.getTime()), ZoneId.of("UTC"));
    }


    public static String getDate(Date startDate) {

        //log.info("startdate: {}", startDate);

        ZonedDateTime d = ZonedDateTime.ofInstant(startDate.toInstant(),
                ZoneId.ofOffset("UTC", ZoneOffset.ofHours(startDate.getTimezoneOffset()/60)));

        String fromattedDate = d.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));

        //log.info("fromattedDate: {}", fromattedDate);

        return fromattedDate;
    }

    private static final SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    {df.setTimeZone(TimeZone.getTimeZone("UTC"));}
    public static String makeDateforUTC(Date d){
        return df.format(d);
    }

}
