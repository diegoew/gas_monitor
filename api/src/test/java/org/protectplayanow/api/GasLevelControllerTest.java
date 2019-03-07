/*
 * Copyright 2016 the original author or authors.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.protectplayanow.api;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import lombok.extern.slf4j.Slf4j;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.protectplayanow.api.config.Constants;
import org.protectplayanow.api.gaslevel.Reading;
import org.protectplayanow.api.gaslevel.view.rest.DeviceForRest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.embedded.LocalServerPort;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import java.util.Random;

@RunWith(SpringRunner.class)
@SpringBootTest(classes = Application.class, webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Slf4j
public class GasLevelControllerTest {

    @LocalServerPort
    private int port;

    String urlBase = "http://localhost:";

    RestTemplate restTemplate = new RestTemplate();

    @Test
    public void testGlobalValue() {
        //GIVEN
        String globalKey = "defaultTemp";
        String globalVal = "21";

        //WHEN
        restTemplate.postForEntity(urlBase + port +
                        "/globalValue?key=" + globalKey + "&value=" + globalVal,
                null,
                String.class);

        //THEN
        ResponseEntity<String> resp = restTemplate.getForEntity(urlBase + port +
                        "/globalValue?key=" + globalKey,
                String.class);

        Assert.assertEquals("returned value must match", globalKey + " = '" + globalVal + "'",
                resp.getBody());


        //GIVEN
        String globalKey1 = "defaultTempUnit";
        String globalVal1 = "Celcius";

        //WHEN
        restTemplate.postForEntity(urlBase + port +
                        "/globalValue?key=" + globalKey1 + "&value=" + globalVal1,
                null,
                String.class);

        //THEN
        resp = restTemplate.getForEntity(urlBase + port +
                        "/globalValue?key=" + globalKey1,
                String.class);


        Assert.assertEquals("returned value must match", globalKey1 + " = '" + globalVal1 + "'",
                resp.getBody());
        
    }
    @Test
    public void testGettingDevices()  {

        ResponseEntity<String> forEntity = restTemplate.getForEntity(urlBase + port + "/devices", String.class);

        log.info("\n\nresp: {}\n", forEntity.getBody());

        ResponseEntity<List<DeviceForRest>> response = restTemplate.exchange(
                urlBase + port + "/devices",
                HttpMethod.GET, null,
                new ParameterizedTypeReference<List<DeviceForRest>>(){});

        List<DeviceForRest> devices = response.getBody();

        log.info("\n\nresp: {}\n", devices);

        Assert.assertTrue("we got back some devices", devices.size() > 0);

    }

    @Test
    public void testGettingDeviceIds()  {
        ResponseEntity<String> forEntity = restTemplate.getForEntity(urlBase + port + "/devices?ids=true", String.class);
        log.info("\n\nresp: {}\n", forEntity.getBody());
        ResponseEntity<List<String>> response = restTemplate.exchange(
                urlBase + port + "/devices?ids=true",
                HttpMethod.GET, null,
                new ParameterizedTypeReference<List<String>>(){});
        List<String> deviceIds = response.getBody();
        log.info("\n\nresp: {}\n", deviceIds);
        Assert.assertTrue("we got back some devices", deviceIds.size() > 0);
    }

    @Test
    public void testSendingNewReading()  {

        String randomDwviceId = "zTest" + new Date().toString().replace(" ", "");
        String sensorType = Constants.mq9;
        double ro = 55;

        log.info("\n\nrandomDwviceId: {}\n", randomDwviceId);

        //Given this reading
        Reading r = Reading.builder()
                .deviceId(randomDwviceId)                 //... from a new device
                .instant(new Date())
                .latitude(Double.parseDouble(Constants.latitudePdr))
                .longitude(Double.parseDouble(Constants.latitudePdr))
                .reading(800)                                           //... with this value
                .resolution(32767)                                      //... and this resolution
                .sensorType(sensorType)
                .ro(ro)
                .tempInCelsius(20)
                .relativeHumidity(.10)
                .build()
                .makeReadingsWithCalculation()
                .stream()
                .filter(rdng -> rdng.getGasName().equals(Constants.Methane) && rdng.getSensorType().equals(Constants.mq9) )
                .findFirst()
                .get();


        ResponseEntity response = restTemplate.exchange(
                urlBase + port + "/readings/calculate?deviceId=" + randomDwviceId +
                        "&instant=now&latitude=33.962492&longitude=-118.437547&sensorType=" + sensorType +
                        "&reading=" + r.getInput() +
                        "&ro=" + ro +
                        "&tempInCelsius=" + r.getTempInCelsius() +
                        "&relativeHumidity=" + r.getRelativeHumidity(),
                HttpMethod.POST, null,
                new ParameterizedTypeReference<String>(){});

        log.info("\n\nresp: {}\n", response);

        Assert.assertTrue("we got back some devices", response.getStatusCodeValue() == 200);


        response = restTemplate.exchange(
                urlBase + port + "/readings?gasName=methane&startDateTime=dayago&endDateTime=now&sensorType=" + sensorType +
                        "&deviceId="+randomDwviceId,
                HttpMethod.GET, null,
                new ParameterizedTypeReference<List<Reading>>(){});

        List<Reading> readings = ((ResponseEntity<List<Reading>> )response).getBody();

        log.info("\n\nresp: {}\n", readings);

        Assert.assertEquals("values should match",
                new BigDecimal(r.getReading()).setScale(2, BigDecimal.ROUND_HALF_UP),
                new BigDecimal(readings.get(0).getReading()).setScale(2, BigDecimal.ROUND_HALF_UP) );


        //test sending reading on new device with a new resolution

        response = restTemplate.exchange(
                urlBase + port + "/readings/calculate?deviceId=" + randomDwviceId +
                        "&instant=now&latitude=33.962492&longitude=-118.437547&sensorType=" + sensorType +
                        "&reading=" + r.getInput() +
                        "&ro=" + ro +
                        "&resolution=" + 12345 +
                        "&tempInCelsius=" + r.getTempInCelsius() +
                        "&relativeHumidity=" + r.getRelativeHumidity(),
                HttpMethod.POST, null,
                new ParameterizedTypeReference<String>(){});

        log.info("\n\nresp: {}\n", response);

        Assert.assertTrue("we got back some devices", response.getStatusCodeValue() == 200);


        response = restTemplate.exchange(
                urlBase + port + "/readings?gasName=methane&startDateTime=dayago&endDateTime=now&sensorType=" + sensorType +
                        "&deviceId="+randomDwviceId,
                HttpMethod.GET, null,
                new ParameterizedTypeReference<List<Reading>>(){});

        readings = ((ResponseEntity<List<Reading>> )response).getBody();

        log.info("\n\nresp: {}\n", readings);

        Assert.assertNotEquals("values should match",
                new BigDecimal(r.getReading()).setScale(2, BigDecimal.ROUND_HALF_UP),
                new BigDecimal(readings.get(0).getReading()).setScale(2, BigDecimal.ROUND_HALF_UP) );

    }

}
