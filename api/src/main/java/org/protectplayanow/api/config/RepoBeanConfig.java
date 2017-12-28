package org.protectplayanow.api.config;

import org.protectplayanow.api.gaslevel.GasLevelRepo;
import org.protectplayanow.api.gaslevel.repository.GasLevelAuroraRepo;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Created by vladpopescu on 12/17/17.
 */
@Configuration
public class RepoBeanConfig {

    @Bean
    public GasLevelRepo gasLevelRepo() {
        return new GasLevelAuroraRepo();
    }

}
