package org.alfresco.thirdpartylicense;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/** Validation of the properties file. */
public class ValidateProperties {
    /** Try to load the properties file and crash if unsuccessful. */
    public static void main(String[] args) throws IOException {
        boolean error = false;
        try (InputStream input = new FileInputStream("../override-THIRD-PARTY.properties")) {
            Properties prop = new Properties();
            prop.load(input);
            for (Object keyObject : prop.keySet()) {
                String key = ((String) keyObject);
                if (key.split("--").length != 3) {
                    System.out.println("Problem with key: " + key);
                    error = true;
                }
            }
        }
        if (error) {
            throw new RuntimeException("Failing due to errors.");
        }
    }
}
