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
org.acegisecurity--acegi-security--0.8.2_patched=Apache-2.0
```

If multiple licenses are available for a third party library then only a single library should be included in this file conforming to the preferences here:
https://alfresco.atlassian.net/wiki/spaces/TECH/pages/248284005/Open+Source+Licenses+-+Approval+Matrix

The libraries should be sorted alphabetically to make it easy to find them. Where possible the [SPDX short identifier](https://spdx.org/licenses/) should be used for the license.

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
              <configuration>
                <failOnMissing>true</failOnMissing>
                <excludedScopes>provided,test</excludedScopes>
                <excludedGroups>org.alfresco</excludedGroups>
                <!-- Each licenseMerge entry should start with the SPDX short identifier and may contain line breaks between entries. -->
                <licenseMerges>
                  <licenseMerge>Apache-2.0|Apache 2.0|The Apache Software License, Version 2.0|Apache License, Version 2.0|
                      Apache License, version 2.0|Apache Public License 2.0|The Apache License, Version 2.0|
                      Apache License 2.0|Apache 2|Apache Software License - Version 2.0|Apache License Version 2.0|Apache v2|
                      Apache License v2|Apache License v2.0|ASF 2.0
                  </licenseMerge>
                  <licenseMerge>BSD-2-Clause|BSD-2
                  </licenseMerge>
                  <licenseMerge>BSD-3-Clause|BSD-3|3-Clause BSD License
                  </licenseMerge>
                  <licenseMerge>CC0-1.0|CC0|Creative Commons License|Public Domain, per Creative Commons CC0
                  </licenseMerge>
                  <licenseMerge>CDDL-1.0|CDDL|Common Development and Distribution License|CDDL+GPL License|
                      CDDL + GPLv2 with classpath exception
                  </licenseMerge>
                  <licenseMerge>CDDL-1.1|Common Development and Distribution License 1.1
                  </licenseMerge>
                  <licenseMerge>CPL-1.0|CPL|Common Public License</licenseMerge>
                  <licenseMerge>EDL-1.0|EDL 1.0|Eclipse Distribution License, Version 1.0|Eclipse Distribution License - v1.0|
                      Eclipse Distribution License - v 1.0
                  </licenseMerge>
                  <licenseMerge>EPL-1.0|EPL 1.0|Eclipse Public License, Version 1.0|Eclipse Public License - Version 1.0 |
                      Eclipse Public License - v 1.0
                  </licenseMerge>
                  <licenseMerge>EPL-2.0|EPL 2.0|Eclipse Public License, Version 2.0|Eclipse Public License - Version 2.0|
                      Eclipse Public License - v 2.0
                  </licenseMerge>
                  <licenseMerge>ICU|Unicode/ICU License
                  </licenseMerge>
                  <licenseMerge>JSON|JSON License|The JSON License</licenseMerge>
                  <licenseMerge>LGPL-2.0-only|GNU Library General Public License v2 only|
                      GNU Library or Lesser General Public License version 2.0 (LGPLv2)
                  </licenseMerge>
                  <licenseMerge>LGPL-2.0-or-later|GNU Library General Public License v2 or later
                  </licenseMerge>
                  <licenseMerge>LGPL-2.1-only|GNU Lesser General Public License v2.1 only
                  </licenseMerge>
                  <licenseMerge>LGPL-2.1-or-later|GNU Lesser General Public License v2.1 or later
                  </licenseMerge>
                  <licenseMerge>LGPL-3.0-only|GNU Lesser General Public License v3.0 only
                  </licenseMerge>
                  <licenseMerge>LGPL-3.0-or-later|GNU Lesser General Public License v3.0 or later|
                      Lesser General Public License v3.0 or later
                  </licenseMerge>
                  <licenseMerge>MIT|The MIT License|MIT License|MIT license|MIT License (MIT)
                  </licenseMerge>
                  <licenseMerge>MPL-1.0|Mozilla Public License 1.0 (MPL 1.1)
                  </licenseMerge>
                  <licenseMerge>MPL-1.1|Mozilla Public License 1.1|Mozilla Public License 1.1 (MPL 1.1)
                  </licenseMerge>
                  <licenseMerge>MPL-2.0|Mozilla Public License 2.0
                  </licenseMerge>
                  <licenseMerge>PostgreSQL|PostgreSQL License
                  </licenseMerge>
                  <licenseMerge>Zlib|zlib License
                  </licenseMerge>
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
