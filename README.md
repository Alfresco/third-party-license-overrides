# third-party-license-overrides

Centralised overrides for licenses of third party libraries used in Alfresco software.  By sharing a single overrides file then corrections to
license information can benefit all projects.

So far the project only contains a single third party license override file for use with the license-maven-plugin.

The format of this file is:

```
# URL to evidence for license choice
[groupId]--[artifactId]--[version]=[licenseChoice]
```

for example

```
# https://sourceforge.net/projects/acegisecurity/
org.acegisecurity--acegi-security--0.8.2_patched=The Apache Software License, Version 2.0
```

If multiple licenses are available for a third party library then only a single library should be included in this file conforming to the preferences here:
https://alfresco.atlassian.net/wiki/spaces/TECH/pages/248284005/Open+Source+Licenses+-+Approval+Matrix

Note that this project is public to allow it to be easily accessed from local and CI builds.

# Usage

Example configuration for this will look like:

```
  <properties>
    <license-maven-plugin.version>2.0.1.alfresco-1</license-maven-plugin.version>
    ...
  </properties>
...
      <plugins>
        <plugin>
          <groupId>org.codehaus.mojo</groupId>
          <artifactId>license-maven-plugin</artifactId>
          <version>${license-maven-plugin.version}</version>
          <executions>
            <execution>
              <id>third-party-licenses</id>
              <goals>
                <goal>add-third-party</goal>
              </goals>
              <phase>generate-resources</phase>
              <!-- Override of dual licenses is not working due to https://github.com/mojohaus/license-maven-plugin/issues/386 -->
              <!-- Overrides are listed in README instead -->
              <configuration>
                <failOnMissing>true</failOnMissing>
                <excludedScopes>provided,test</excludedScopes>
                <excludedGroups>org.alfresco</excludedGroups>
                <licenseMerges>
                  <licenseMerge>The Apache Software License, Version 2.0|Apache License, Version 2.0|Apache Public License 2.0|Apache 2.0|The Apache License, Version 2.0|Apache License 2.0|Apache Software License - Version 2.0|Apache License Version 2.0</licenseMerge>
                  <licenseMerge>Common Development and Distribution License|CDDL|CDDL+GPL License|CDDL + GPLv2 with classpath exception</licenseMerge>
                  <licenseMerge>Eclipse Distribution License, Version 1.0|Eclipse Distribution License - v 1.0|EDL 1.0</licenseMerge>
                  <licenseMerge>Eclipse Public License, Version 1.0|Eclipse Public License - Version 1.0|Eclipse Public License - v 1.0</licenseMerge>
                  <licenseMerge>Eclipse Public License, Version 2.0|Eclipse Public License - Version 2.0|EPL 2.0</licenseMerge>
                  <licenseMerge>Creative Commons License|CC0|Public Domain, per Creative Commons CC0</licenseMerge>
                  <licenseMerge>The MIT License|MIT License</licenseMerge>
                </licenseMerges>
                <overrideUrl>https://raw.githubusercontent.com/Alfresco/third-party-license-overrides/master/override-THIRD-PARTY.properties</overrideUrl>
              </configuration>
            </execution>
          </executions>
        </plugin>
      </plugins>
```

In particular note the reference to this project in the `overrideUrl` tag.

In order to also use the plugin to enforce the Alfrecso license header has been added to the top of Java files then a second execution and a dependency can be included:

```
...
            <execution>
              <id>check-licenses</id>
              <phase>compile</phase>
              <goals>
                <goal>check-file-header</goal>
              </goals>
              <configuration>
                <addJavaLicenseAfterPackage>false</addJavaLicenseAfterPackage>
                <organizationName>Alfresco Software Limited</organizationName>
                <failOnMissingHeader>true</failOnMissingHeader>
                <failOnNotUptodateHeader>true</failOnNotUptodateHeader>
                <licenseResolver>classpath://alfresco</licenseResolver>
                <licenseName>${licenseName}</licenseName>
                <roots>
                  <root>src</root>
                </roots>
                <includes>
                  <include>**/*.java</include>
                  <include>**/*.jsp</include>
                </includes>
              </configuration>
            </execution>
          </executions>
          <dependencies>
            <dependency>
              <groupId>org.alfresco</groupId>
              <artifactId>alfresco-license-headers</artifactId>
              <version>1.0</version>
            </dependency>
          </dependencies>
...
```

# CSV Generation for Customer Releases

We provide customers with third party license information in CSV format (or sometimes xls). To convert the THIRD-PARTY.txt files
into CSV files then this project includes a Python utility.  This can be used with a command like:

```
./thirdPartyLicenseCSVCreator.py --version 3.0.0 --project ~/projects/alfresco-elasticsearch-connector/
```

More detailed help information can be obtained with:

```
./thirdPartyLicenseCSVCreator.py --help
```
