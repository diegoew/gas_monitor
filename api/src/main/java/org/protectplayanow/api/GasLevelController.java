package org.protectplayanow.api;

import java.util.concurrent.atomic.AtomicLong;

import io.swagger.annotations.Api;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@Api(description = "These endpoints don't save data, at the moment. But they will respond" +
        " if you call them correctly.")
public class GasLevelController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();

    @RequestMapping(value = "/exampleGetValue", method = RequestMethod.GET)
    public Greeting greeting(@RequestParam(value="name", defaultValue="World of Gas Monitoring") String name) {

        return new Greeting(counter.incrementAndGet(),
                            String.format(template, name));

    }

    @RequestMapping(value="/examplePostValue", method = RequestMethod.POST)
    public String add(@RequestBody Reading input) {

        return String.format(template, "buddy");

    }
}
