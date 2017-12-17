package org.protectplayanow.api.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;

@Configuration
public class DataSourceConfig {

	@Autowired
	private Environment env;

	@Value("${spring.datasource.url}")
	private String url;

	@Value("${spring.datasource.username}")
	private String username;

	@Value("${spring.datasource.password}")
	private String password;

	@Value("${spring.datasource.driver-class-name}")
	private String driverClassName;

	@Value("${spring.datasource.platform}")
	private String platform;

	@Bean
	public JdbcTemplate getJdbcTemplate() {
		
		JdbcTemplate template = new JdbcTemplate();
		template.setDataSource(getDataSource());
		
		return template;
		
	}

	@Bean
	public DriverManagerDataSource getDataSource() {

		DriverManagerDataSource dataSource = new DriverManagerDataSource();

		dataSource.setDriverClassName(driverClassName);

		dataSource.setUrl(url);

		dataSource.setUsername(username);

		dataSource.setPassword(password);

		return dataSource;

	}
	
}