package org.protectplayanow.api.gaslevel.repository;

import org.protectplayanow.api.config.RestApiConsts;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.Collection;
import java.util.Date;
import java.util.stream.Collectors;

/**
 * Created by vladpopescu on 12/17/17.
 */
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

    private static final SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    public static String getDate(Date startDate) {
        return df.format(startDate);
    }
}
