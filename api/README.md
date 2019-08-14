# Spring Boot based Back End Server

This server runs a [Spring Boot][spring-boot] application on a local machine. 

[spring-boot]: http://projects.spring.io/spring-boot/


## Requirements to run locally

You must have [Java 8][java8] installed.

[java8]: http://www.oracle.com/technetwork/java/javase/downloads/

Check that java 8 is installed by typing the following command:

$ javac -version
javac 1.8.0_25

The response must have '1.8.' in it. If not download the java 8 jdk from the link above.

## Configure MySql Database connection

Run a local mysql instance using the schema file in /api/database/schema_create.sql

Modify add local mysql path, username, password in file: /api/src/main/resources/application.properties

## Leverage Gradle to run the application locally 

The server uses the [Gradle][gradle] build system.

[gradle]: https://docs.gradle.org/current/userguide/introduction.html

Go to directory: your/path/ai-suite/AIPipelineBE/ then build and start the application with:

$ ./gradlew bootRun

Look for the second to last line in the console logs for the port. The line will look like this:

2016-11-09 23:55:54.339  INFO 68013 --- [           main] s.b.c.e.t.TomcatEmbeddedServletContainer : Tomcat started on port(s): 8080 (http)

### To Run Tests

$ ./gradlew clean build

If there are errors look at the console output. Gradle will generate and html file with error information.
